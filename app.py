from flask import Flask, jsonify, render_template
from scraper import get_today_news

app = Flask(__name__)

@app.route("/")
def home():
    news = get_today_news()
    return render_template("index.html", news=news)

@app.route("/latest-news")
def latest_news_api():
    return jsonify(get_today_news())

if __name__ == "__main__":
    app.run(debug=True)
