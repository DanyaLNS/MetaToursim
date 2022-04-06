from collections import namedtuple

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, redirect, request
from datetime import datetime
from parsers import best_places_parser
from api import  current_weather

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


@app.route('/user_request', methods=['GET', 'POST'])
def user_request():
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
    return render_template('statistics.html', reqs=reqs)


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
