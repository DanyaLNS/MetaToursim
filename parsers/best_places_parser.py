import re
from bs4 import BeautifulSoup
import requests


def get_best_places():
    url = "https://lifehacker.ru/special/100places/"
    req = requests.get(url)
    src = req.text

    soup = BeautifulSoup(src, "html.parser")
    all_places_headers = soup.find_all(class_="title-xl")
    all_places_texts = soup.find_all(class_="descr-lg centerText")
    all_places_images = soup.find_all(class_="cover_carrier")[1:101]

    best_places_list = []
    for i in range(100):
        header = all_places_headers[i].next_element.next_element.text
        text = all_places_texts[i].next_element.next_element.text
        image_src = all_places_images[i]["data-content-cover-bg"]

        best_places_list.append([str(i + 1) + ": " + header, text, image_src])

    return best_places_list
