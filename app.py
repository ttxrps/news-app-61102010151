from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json

app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"
OPEN_WEATHER_KEY = '4ce9097983e52afe3b7d001716b92495'

OPEN_COVID_URL ="http://newsapi.org/v2/everything?q=covid-19&from=2020-12-29&sortBy=publishedAt&apiKey=93fef1c121174c29994bce62697f1548"

OPEN_NEWS_URL ="http://newsapi.org/v2/everything?q={0}&from=2020-12-29&sortBy=publishedAt&apiKey={1}"
OPEN_NEWS_KEY = "93fef1c121174c29994bce62697f1548"

@app.route('/')
def home():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    weather = get_weather(city,OPEN_WEATHER_KEY)
    url1 = OPEN_COVID_URL
    data1 = urlopen(url1).read()
    parsed1 = json.loads(data1)
    articles = parsed1['articles']
    desc = []
    news = []
    img = []
    link = []
    for i in range(1,6):
        myarticles = articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['content'])
        img.append(myarticles['urlToImage'])
        link.append(myarticles['url'])
    mylist = zip(news, desc, img, link)
    return render_template('index.html', weather= weather,context = mylist)


def get_weather(city,API_KEY):
    query = quote(city)
    url = OPEN_WEATHER_URL.format(city, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        description = parsed['weather'][0]['description']
        icon = parsed['weather'][0]['icon']+".png"
        temperature = parsed['main']['temp']
        city = parsed['name']
        pressure = parsed['main']['pressure']
        humidity = parsed['main']['humidity']
        wind = parsed['wind']['speed']
        country = parsed['sys']['country']
        weather = {'description': description,
                    'temperature': temperature,
                    'city': city,
                    'country': country,
                    'pressure': pressure,
                    'humidity': humidity,
                    'wind': wind,
                    'icon': icon
                    }
    return weather

@app.route('/news')
def news():
    news = request.args.get('news')
    if not news:
        news = 'covid-19'
    news_list = get_news(news,OPEN_NEWS_KEY)
    return render_template('news.html', context = news_list)

def get_news(news,NEWS_KEY):
    query_news = quote(news)
    url_news = OPEN_NEWS_URL.format(news,NEWS_KEY)
    data_news = urlopen(url_news).read()
    parsed_news = json.loads(data_news)
    articles_news = parsed_news['articles']
    desc = []
    news = []
    link = []
    for i in range(len(articles_news)):
        myarticles_news = articles_news[i]
        news.append(myarticles_news['title'])
        desc.append(myarticles_news['content'])
        link.append(myarticles_news['url'])
    mylist = zip(news,desc,link)
    return mylist


@app.route('/about')
def about():
    return render_template('about.html')
