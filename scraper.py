import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

BASE_URL = "https://www.hirunews.lk"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def today_string():
    return datetime.now().strftime("%Y-%m-%d")


def get_latest_article_links(limit=30):
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/news/"):
            full_url = BASE_URL + href
            if full_url not in links:
                links.append(full_url)

        if len(links) >= limit:
            break

    return links


def scrape_full_article(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Title
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else ""

    # Date
    date_text = ""
    time_tag = soup.find("time")
    if time_tag:
        date_text = time_tag.text.strip()

    # Image
    image = ""
    img = soup.find("img")
    if img and img.get("src"):
        image = img["src"]

    # Content
    paragraphs = soup.find_all("p")
    content = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())

    return {
        "title": title,
        "date": date_text,
        "image": image,
        "content": content,
        "link": url
    }


def get_today_news():
    today_news = []
    links = get_latest_article_links()

    today = datetime.now().strftime("%d %B %Y")  # human readable

    for link in links:
        article = scrape_full_article(link)

        # VERY IMPORTANT: match today's date
        if today in article["date"]:
            today_news.append(article)

        time.sleep(1)

    return today_news
