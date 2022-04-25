from bs4 import BeautifulSoup
import requests


def get_best_russian_places():
    url = "https://sutochno.ru/info/luchshie-goroda"
    req = requests.get(url)
    src = req.text

    soup = BeautifulSoup(src, "html.parser")
    all_russian_places_tags = soup.find_all(class_="article-col-right")
    all_russian_places_images = soup.find_all(class_="h-full img-path")

    best_russian_places = []
    for k in range(len(all_russian_places_tags)):
        tag = all_russian_places_tags[k]
        header = ""
        ps = []
        while True:
            tag = tag.next_element
            if tag.name:
                if tag.name == "a":
                    if tag.text[0].isdigit():
                        break
                elif tag.name == "h2":
                    header = tag.text
                elif tag.name == "p":
                    ps.append(tag.text)
        li3 = ps[-3][2:]
        li2 = ps[-4][2:]
        li1 = ps[-5][2:]
        sub_header = ps[-6]
        text = ps[0]
        for i in range(1, len(ps) - 6):
            text = text + "\n" + ps[i]

        image = all_russian_places_images[k]
        image_src = "https://sutochno.ru" + image["src"]

        best_russian_places.append([header, text, sub_header, li1, li2, li3, image_src])

    return best_russian_places
