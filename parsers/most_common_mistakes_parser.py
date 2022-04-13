from bs4 import BeautifulSoup
import requests


def get_most_common_mistakes():
    url = "https://www.arrivo.ru/statii/sovety/10-glavnyh-turisticheskih-oshibok.html?ysclid=l1xr3wyi22"
    req = requests.get(url)
    src = req.text

    soup = BeautifulSoup(src, "html.parser")
    all_most_common_mistakes_headers = soup.find_all("h2")[:10]

    most_common_mistakes = []
    for el in all_most_common_mistakes_headers:
        section = []
        current_sibling = el
        while current_sibling.name != "div":
            section.append(current_sibling)
            current_sibling = current_sibling.nextSibling
        section.append(current_sibling)
        most_common_mistakes.append(section)

    return most_common_mistakes
