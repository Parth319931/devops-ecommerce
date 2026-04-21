from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://mongodb:27017/ecommerce"
mongo = PyMongo(app)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(mongo.db.products.find({}, {'_id': 0}))
    return jsonify(products)

@app.route('/api/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', 999999))
    brand = request.args.get('brand', '')
    min_rating = float(request.args.get('min_rating', 0))
    category = request.args.get('category', '')

    filter_query = {
        'price': {'$gte': min_price, '$lte': max_price},
        'rating': {'$gte': min_rating}
    }

    if query:
        filter_query['$or'] = [
            {'name': {'$regex': query, '$options': 'i'}},
            {'description': {'$regex': query, '$options': 'i'}}
        ]
    if brand:
        filter_query['brand'] = {'$regex': brand, '$options': 'i'}
    if category:
        filter_query['category'] = {'$regex': category, '$options': 'i'}

    products = list(mongo.db.products.find(filter_query, {'_id': 0}))
    return jsonify(products)

@app.route('/api/compare', methods=['GET'])
def compare_products():
    ids = request.args.getlist('id')
    products = list(mongo.db.products.find({'product_id': {'$in': ids}}, {'_id': 0}))
    return jsonify(products)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)