import requests
from bs4 import BeautifulSoup
import string
import os

class ArticlesFetcher:

    def __init__(self, article_type, number_of_pages):
        self.article_type = article_type
        self.number_of_pages = number_of_pages

    def get_all_articles(self, url):
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

    def get_article_content(self, url):
        response = requests.get(url)
        if response:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            article_body = soup.find("div", {"class" : "c-article-body"})
            article_content = article_body.text.strip()
            return article_content
        return None

    def file_name_from_title(sele, title):
        title = title.strip()
        for char in string.punctuation:
            if char in title:
                title = title.replace(char, "")
        title = title.replace(" ", "_")
        title += ".txt"
        return title

    def save_articles(self, page_number):
        directory = f"Page_{page_number}"
        if not os.path.exists(directory):
            os.mkdir(directory)
        url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={page_number}"
        articles = self.get_all_articles(url)
        if articles:
            news = [article for article in articles if article["type"] == self.article_type]
            for article in news:
                content = self.get_article_content(article["link"])
                if content:
                    with open(f"{directory}/{self.file_name_from_title(article['title'])}", "wb") as file:
                        file.write(bytes(str(content), "utf-8"))
                else:
                    print("could not find the article")
            print(f"Page number {page_number} Saved!")
        else:
            print("something went wrong")

    def fetch(self):
        for page_number in range(1, self.number_of_pages + 1):
            self.save_articles(page_number)
if __name__ == "__main__":
    try:
        number_of_pages = int(input("> "))
    except ValueError:
        print("Numbers please")
        exit()
    articles_type = input("> ")
    fetcher = ArticlesFetcher(articles_type, number_of_pages)
    fetcher.fetch()
    print("Saved all articles.")
