# CommentSense
Prerequisites
Before you start, ensure you have:
	•	Google Chrome browser installed.
	•	Python 3.7+ installed on your system.
	•	Necessary Python dependencies (Flask, BeautifulSoup, requests, openai).

Installation Steps

1. Download this project.
2. Install Dependencies.
3. Start the backend service (python app.py)
4. Load the Chrome Extension:
	•	Open Chrome and navigate to: chrome://extensions/.
	•	Enable Developer Mode (toggle in the upper-right corner).
	•	Click Load unpacked and select the project folder.

Usage Instructions

	•	Open the Chrome browser and navigate to a restaurant’s review page on OpenRice.
	•	Click the OpenRice Review Analyzer icon in the browser toolbar.
	•	In the pop-up, click the Analyze Reviews button.
	•	The extension will scrape the reviews, analyze them, and display a structured report in the pop-up.


File Structure
	•	popup.html: HTML file for the Chrome extension’s user interface.
	•	popup.js: JavaScript file handling front-end logic and backend communication.
	•	styles.css: CSS file for styling the extension interface.
	•	app.py: Flask-based backend server for web scraping and NLP processing.
	•	manifest.json: Configuration file for the Chrome extension.

