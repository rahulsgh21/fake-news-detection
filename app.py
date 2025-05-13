from flask import Flask,request,render_template
from src.google_search import scrape
from src.get_named_entity import get_important_texts
from src.calc_similiarity import calculate_similarity
from src.logger import logging

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/check_news',methods=['GET','POST'])
def check_news():
    if request.method == 'GET':
        return render_template('home.html')
    
    news = request.form.get('searchInput')
    logging.info(f"Collected news: {news}")

    urls, related_news = scrape(news)
    logging.info(f"Scraped all links. {len(related_news)} links could be scraped.")
    imp_news = get_important_texts(related_news, news)
    result = calculate_similarity(news, imp_news)
    results = []
    for i in range(len(result)):
        results.append([i+1,urls[i],result[i][0],result[i][1]])
    return render_template('home.html', News=news, results=results)


if __name__=="__main__":
    app.run(host="0.0.0.0",port='8000',debug=True)