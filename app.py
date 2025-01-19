from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_euro_price():
    url = "https://www.tgju.org/profile/price_eur"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("span", {"data-col": "info.last_trade.PDrCotVal"})
        if price_tag:
            price = price_tag.text.replace(",", "")
            return int(price) // 10
    return None

@app.route('/')
def home():
    price = fetch_euro_price() or 0
    return render_template('index.html', price=price)

@app.route('/get_price')
def get_price():
    price = fetch_euro_price()
    return jsonify({"price": price})

if __name__ == '__main__':
    app.run(debug=True)
