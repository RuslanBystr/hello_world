import requests
import json

def get_currency(ccy):
    content = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5").content
    data = json.loads(content)
    for elem in data:
        if elem["ccy"] == ccy:
            price = elem["buy"]
            price = price.split(".")
            return f"зараз по {price[0]} гривень {price[1][:2]} копійок"
