import re
from bs4 import BeautifulSoup
import requests

def get_best_places():
    url = "https://lifehacker.ru/special/100places/"
    req = requests.get(url)
    src = req.text

    soup = BeautifulSoup(src, "html.parser")
    all_places_hrefs = soup.find_all(class_="t202")

    best_places_list = []
    for item in all_places_hrefs:
        text = re.sub(r'\s{4,}', ' ', item.text)
        text = re.sub(r'\d{1,3}', '', text, 1)
        text = text.strip()
        best_places_list.append(text)

    return best_places_list

