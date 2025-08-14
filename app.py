from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import re
from bs4 import BeautifulSoup
import requests
import json
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key="sk-61d38daa9e5e412080ea82a235c57c2c", base_url="https://api.deepseek.com")

def scrape_reviews(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    reviews = []
    page = 1
 
    while True:
        if page == 1:
            page_url = url
        else: 
            page_url = f"{url}?page={page}"

        print(f"Collecting reviews from page {page}")
        response = requests.get(page_url, headers=headers)

        if response.status_code != 200:
            print(f"Page {page} request failed, status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        review_container = soup.select(".sr2-review-list-container")

        if not review_container:
            print("No comment found.")
            break

        for review in review_container:
            content_div = review.select_one(".text[itemprop = 'description']")
            if content_div:
                content = content_div.get_text(strip = True)
                content = re.sub(r'\n+', "\n", content)
                content = re.sub(r'\s+', ' ', content)
                reviews.append(content)
            else:
                print("No comments found")
        
        
        next_page = soup.select_one("a.pagination-button.next.js-next")
        if not next_page:
            print("It is the end page")
            break

        page += 1

    print(f"{len(reviews)} reviews collected")
    return reviews


def summarize_reviews_withDS(reviews):
    # combine reviews to a txt file
    review_text = '\n'.join(reviews)

    try: 
        response = client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": "你是一個餐廳評論分析師，透過匯總並分析餐廳的用戶評論，專為用戶在網路平台尋找餐廳時提供參考。"},
                {"role": "user", "content": f"請讀取文件:\n{review_text}，從食物口味，服務態度，價錢合理程度，以及用餐環境等角度，分析評論數據。並在每個方面提取關鍵詞、計算關鍵詞頻率。每一次的輸入均為獨立輸入，不需要聯繫上下文。最後，在此基礎上生成總結。以上所有輸出，必須基於用戶提供的評論數據，不得編造與發揮。"}
            ],
            stream = False
        )

        summary = response.choices[0].message.content.strip()
        return{"Summary": summary}
    
    except Exception as e:
        return {"error": str(e)}


@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        # call crawler
        data = request.get_json()
        url = data.get('url')
        print("Received URL:", url)  

        if not url:
            return jsonify({"error": "No URL"}), 400
        

        # crawler reviews
        reviews = scrape_reviews(url)
        print("Scraped Reviews:", reviews) 

        if not reviews:  # check if review list is empty
            return jsonify({'error': 'No reviews found!'}), 404

        # call deepseek
        result = summarize_reviews_withDS(reviews)
        print("Deepseek Summary:", result) 

        return jsonify(result)
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
        
        # if 'error' in report:
        #     return jsonify({'error': report['error']}), 500
        
        # return Response(json.dumps({'summary': report['Summary']}, ensure_ascii=False), content_type='application/json; charset=utf-8')

        # return jsonify({'summary': report['Summary']}), 200



if __name__ == '__main__':
    # app.run(debug=False, port = 8000)
    app.run(debug=False, host='0.0.0.0', port=8000) 