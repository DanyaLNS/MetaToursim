from bs4 import BeautifulSoup
import requests


def get_best_lifehacks():
    url = "https://travelask.ru/blog/posts/35-28-blestyaschih-layfhakov-dlya-sbora-v-puteshestvie?"
    req = requests.get(url)
    src = req.text

    soup = BeautifulSoup(src, "html.parser")
    all_lifehacks_tags = soup.find_all("h4")
    all_lifehacks_images = soup.find_all("img")
    all_lifehacks_images = all_lifehacks_images[2:31]

    best_lifehacks = []
    for el in list(zip(all_lifehacks_tags, all_lifehacks_images)):
        pair = [el[0].text, el[1]["src"]]
        best_lifehacks.append(pair)

    return best_lifehacks
