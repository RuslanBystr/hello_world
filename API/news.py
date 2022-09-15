import requests

NEWS_TOKEN = "467efc68363d43b58b14f0bd04c56baf"

url = 'https://newsapi.org/v2/everything?'

news_parameters = {
    'q': 'business',# query phrase
    'pageSize': 10,# max
    'apiKey': NEWS_TOKEN,# API
    'language': 'uk'
}
def news():
    response = requests.get(url, params = news_parameters)
    response_json = response.json()

    for elem in response_json['articles']:
        return elem['title']



