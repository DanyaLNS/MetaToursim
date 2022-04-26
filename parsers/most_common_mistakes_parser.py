from bs4 import BeautifulSoup
import requests


def get_most_common_mistakes():
    url = "https://www.arrivo.ru/statii/sovety/10-glavnyh-turisticheskih-oshibok.html?ysclid=l1xr3wyi22"
    req = requests.get(url)
    src = req.text

    soup = BeautifulSoup(src, "html.parser")
    all_most_common_mistakes_tags = soup.find_all("h2")[:10]
    all_most_common_mistakes_images = soup.find_all("img")[76:]
    all_most_common_mistakes_images = all_most_common_mistakes_images[:10]

    most_common_mistakes = []
    for i in range(10):
        tag = all_most_common_mistakes_tags[i]
        header = tag.text
        texts = []
        while True:
            if tag is None:
                break
            else:
                tag = tag.next_element
                if tag.name:
                    if tag.name == "div":
                        break
                    if tag.name == "p":
                        texts.append(tag.text)
                    if tag.name == "li":
                        texts.append("- " + tag.text)

        image_src = all_most_common_mistakes_images[i]["src"]

        most_common_mistakes.append([header, texts, image_src])

    return most_common_mistakes
