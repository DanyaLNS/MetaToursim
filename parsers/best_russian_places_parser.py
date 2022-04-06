from bs4 import BeautifulSoup
import requests


def get_best_russian_places():
    url = "https://sutochno.ru/info/luchshie-goroda"
    req = requests.get(url)
    src = req.text

    soup = BeautifulSoup(src, "html.parser")
    all_russian_places_tag = soup.find_all(class_="article-col-right")

    best_russian_places = []
    for el in all_russian_places_tag:
        best_russian_places.append(el)

    return best_russian_places
