import sqlite3
import matplotlib.pyplot as plt

def create_popularity_of_cities_diagram():
    conn = sqlite3.connect('requests.db')
    cur = conn.cursor()
    cur.execute("SELECT city_to, COUNT(city_to) FROM user_request GROUP BY city_to;")
    # Список кортежей, в которых 1 элемент - название города, а 2 - количество повторений
    query_result = cur.fetchall()
    x = []
    y = []
    for element in query_result:
        x.append(element[0])
        y.append(element[1])

    plt.title('Популярность городов', fontsize=16)
    plt.xlabel('Город', fontsize=12)
    plt.ylabel('Количество запросов', fontsize=12)
    plt.bar(x, y)
    plt.savefig('diagram1.png')
