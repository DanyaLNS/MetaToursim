from collections import namedtuple
from pyexpat.errors import messages

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, redirect, request
from datetime import datetime
from PIL import Image
from api import current_weather
import sqlite3
import matplotlib.pyplot as plt
from parsers import best_places_parser, best_lifehacks_parser, best_russian_places_parser, essential_things_parser, most_common_mistakes_parser


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
    plt.savefig('statistics/diagram1.png')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_from = db.Column(db.String(50), nullable=False)
    city_to = db.Column(db.String(50), nullable=False)
    date_there = db.Column(db.DateTime, default=datetime.utcnow)
    date_back = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Request %r' % self.id


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


# @app.route('/user_request', methods=['GET', 'POST'])
# def user_request():
#     return render_template("user_request.html", messages=messages)


@app.route('/best_russian_places')
def best_russian_places():
    return render_template('best_russian_places.html', russian_places=best_russian_places_parser.get_best_russian_places())


@app.route('/best_lifehacks')
def best_lifehacks():
    return render_template('best_lifehacks.html', lifehacks=best_lifehacks_parser.get_best_lifehacks())


@app.route('/essential_things')
def essential_things():
    return render_template('essential_things.html', essential_things=essential_things_parser.get_essential_things())


@app.route('/most_common_mistakes')
def most_common_mistakes():
    return render_template('most_common_mistakes.html', most_common_mistakes=most_common_mistakes_parser.get_most_common_mistakes())


@app.route('/avia', methods=['GET', 'POST'])
def avia():
    if request.method == "POST":
        city_from = request.form['city_from']
        city_to = request.form['city_to']
        date_there = datetime.strptime(str(request.form['date_there']), "%Y-%m-%d")
        date_back = datetime.strptime(str(request.form['date_back']), "%Y-%m-%d")
        user_req = UserRequest(city_from=city_from, city_to=city_to, date_there=date_there, date_back=date_back)

        try:
            db.session.add(user_req)
            db.session.commit()
            return redirect('/')
        except:
            return "При обработке запроса произошла ошибка"
    else:
        return render_template("user_request.html")


@app.route('/best_places')
def best_places():
    return render_template('best_places.html', places=best_places_parser.get_best_places())


@app.route('/articles')
def articles():
    return render_template('articles.html')


@app.route('/statistics', methods=['GET'])
def statistics():
    reqs = UserRequest.query.order_by(UserRequest.date_there).all()
    create_popularity_of_cities_diagram()
    diagram = Image.open('statistics/diagram1.png')
    return render_template('statistics.html', reqs=reqs, diagram=diagram)


@app.route('/weather', methods=['POST', 'GET'])
def weather():
    weather = {}
    city = ""
    if request.method == "POST":
        city = request.form['city']
        weather = current_weather.get_current_weather(city)
    return render_template('weather.html', weather=weather, place=city)


if __name__ == "__main__":
    app.run(debug=True)
