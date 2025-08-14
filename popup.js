document.addEventListener("DOMContentLoaded", () => {
  const currentUrlElement = document.getElementById("current-url");
  const fetchReportButton = document.getElementById("fetch-report");
  const reportContainer = document.getElementById("report-container");

  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const currentUrl = tabs[0]?.url || "無法獲取當前頁面網址";
    //currentUrlElement.textContent = currentUrl;
    console.log("Current URL:", currentUrl);

    // check if the url belong to Openrice reviews
    const isValidUrl =
      currentUrl.startsWith("https://www.openrice") &&
      currentUrl.endsWith("reviews");

    if (!isValidUrl) {
      // const warningElement = document.getElementById("warning");
      // if (warningElement) {
      reportContainer.innerHTML = "<p>這不是有效的Openrice評論頁面</p>";

      // warningElement.textContent = "當前頁面不是Openrice評論頁面";
      // warningElement.style.color = "red";
    }
  });
  // });

  fetchReportButton.addEventListener("click", async () => {
    reportContainer.innerHTML = "<p>正在加載分析報告，請稍候...</p>";

    // fetch current url
    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      const currentUrl = tabs[0]?.url;

      if (!currentUrl) {
        reportContainer.innerHTML = "<p>無法獲取當前頁面網址</p>";
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/generate_report", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url: currentUrl }),
        });

        console.log("Raw Response:", response);

        const data = await fetchReport(currentUrl);
        console.log("final data in frontend", data);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // const data = await response.json();

        if (data.Summary) {
          const htmlContent = marked.parse(data.Summary);
          console.log("Converted HTML:", htmlContent);
          reportContainer.innerHTML = `<h3>分析報告</h3><div>${htmlContent}</div>`;
          // <p>${data.Summary.replace(
          //   /\n/g,
          //   "<br>"
          // )}</p>`;
        } else if (data.error) {
          reportContainer.innerHTML = `<p>錯誤：${data.error}</p>`;
        } else {
          reportContainer.innerHTML = "<p>未獲取有效的數據。</p>";
        }
      } catch (error) {
        reportContainer.innerHTML = `<p>加載失敗：請確保處於正確的Openrice評論頁面</p>`;
      }
    });
  });
});

async function fetchReport(currentUrl) {
  try {
    const response = await fetch("http://127.0.0.1:8000/generate_report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: currentUrl }),
    });

    console.log("Raw Response:", response);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Parsed Response:", data);

    return data;
  } catch (error) {
    console.error("Fetch Error:", error);
    throw error;
  }
}
