#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        bakeries.append(bakery_dict)

    response = make_response(jsonify(bakeries), 200)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = BakedGood.query.filter_by(id=id).first()

    baker_dict = bakery.to_dict()
    response = make_response(jsonify(baker_dict), 200)

    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_list = []

    for baked_good in BakedGood.query.order_by(-BakedGood.price).all():
        baked_good_dict = baked_good.to_dict()
        baked_list.append(baked_good_dict)

    response = make_response(jsonify(baked_list), 200)

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expencive = BakedGood.query.order_by(+BakedGood.price).first()
    most_expencive_dict = most_expencive.to_dict()

    response = make_response(jsonify(most_expencive_dict), 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
