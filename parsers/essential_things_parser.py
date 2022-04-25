from bs4 import BeautifulSoup
import requests


def get_essential_things():
    url = "https://travelq.ru/chto-vzyat-v-poezdku-spisok-neobhodimyih-veshhey-i-sboryi/?ysclid=l1xo3ferid"
    req = requests.get(url)
    src = req.text

    soup = BeautifulSoup(src, "html.parser")
    all_essential_things_headers = soup.find_all("h3")[:6]
    all_essential_things_images = [element.nextSibling.nextSibling for element in all_essential_things_headers][:6]
    all_essential_things_text = [element.nextSibling.nextSibling for element in all_essential_things_images][:6]
    all_essential_things_list = [element.nextSibling.nextSibling for element in all_essential_things_text][:6]

    essential_things = []
    for el in list(zip(all_essential_things_headers, all_essential_things_images, all_essential_things_text, all_essential_things_list)):
        tag = el[3]
        lis = []
        while tag.next_element:
            tag = tag.next_element
            if tag.name:
                if tag.name == "a":
                    continue
                if tag.name != "li":
                    break
                lis.append(tag.text)

        essential_things.append([el[0].text, el[1].next["data-src-img"], el[2].text, lis])

    return essential_things
