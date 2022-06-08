import requests
from bs4 import BeautifulSoup
import string
def get_all_articles(url):
    articles = []
    response = requests.get(url)
    if response:
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        article_elelents = soup.find_all("article")
        for article in article_elelents:
            anchor_tag = article.find("a")
            title = anchor_tag.text
            link = "https://www.nature.com" + anchor_tag.get("href")
            type = article.find("span", {"class" : "c-meta__type"}).text
            articles.append({"title" : title, "type" : type, "link": link})  
        return articles  
    return None

def get_article_content(url):
    response = requests.get(url)
    if response:
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        article_body = soup.find("div", {"class" : "c-article-body u-clearfix"})
        return article_body
    return None

def title_cleaning(title):
    title = title.strip()
    for char in string.punctuation:
        if char in title:
            title = title.replace(char, "")
    title = title.replace(" ", "_")
    title += ".txt"
    return title
if __name__ == "__main__":
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
    articles = get_all_articles(url)
    if articles:
        news = [article for article in articles if article["type"] == "News"]
        for article in news:
            content = get_article_content(article["link"])
            if content:
                with open(title_cleaning(article["title"]), "wb") as file:
                    file.write(bytes(str(content), "utf-8"))
            else:
                print("could not find the article")
    else:
        print("something went wrong")