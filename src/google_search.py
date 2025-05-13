import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from dotenv import load_dotenv
load_dotenv()
google_search_api_key = os.environ['GOOGLE_SEARCH_API_KEY']

from src.exception import CustomException
from src.logger import logging

url = "https://google.serper.dev/news"

def search(news):
    payload = json.dumps({"q": news,"gl": "in","num":20})
    headers = {'X-API-KEY': google_search_api_key,'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)

    res = response.json()
    n = res['news']
    links =[]
    for i in range(len(n)):
        links.append(n[i]['link'])

    return links

def scrape(news):
    links = search(news)
    logging.info(f"Loaded all links. {len(links)} links found.")
    other_news = []
    useful_urls = []
    for url in links:
        try:
            page= requests.get(url)
            logging.info(url)
            if (page.status_code != 200):
                logging.info("Page could not be loaded.")
                continue
            soup = BeautifulSoup(page.text, 'lxml')
            logging.info("Successfully loaded page.")
            paragraphs = soup.find_all('p')
            texts=[]
            for i in range(len(paragraphs)):
                para = paragraphs[i].text
                texts.append(para)
            new_text = ' '
            new_text = new_text.join(texts)
            other_news.append(new_text)
            useful_urls.append(url)
        except Exception as e:
            raise CustomException(e, sys)
    return useful_urls, other_news

if __name__=="__main__":
    news = "IIT Kanpur develops artificial rain through cloud seeding technology"
    links = search(news)
    other_news = scrape(links)
    print(links)
