from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from flask_cors import CORS
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
CORS(app)

# ✅ MongoDB
app.config["MONGO_URI"] = "mongodb://mongodb:27017/ecommerce"
mongo = PyMongo(app)

# ✅ Custom metric
REQUEST_COUNT = Counter('app_requests_total', 'Total requests')

# ---------------- ROUTES ---------------- #

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/api/products', methods=['GET'])
def get_products():
    REQUEST_COUNT.inc()
    products = list(mongo.db.products.find({}, {'_id': 0}))
    return jsonify(products)

@app.route('/api/search', methods=['GET'])
def search_products():
    try:
        query = request.args.get('q', '')
        min_price = float(request.args.get('min_price', 0))
        max_price = float(request.args.get('max_price', 999999))
        brand = request.args.get('brand', '')
        min_rating = float(request.args.get('min_rating', 0))
        category = request.args.get('category', '')

        # Sanitize query — remove special characters
        import re
        query = re.sub(r"[^\w\s]", "", query)
        brand = re.sub(r"[^\w\s]", "", brand)
        category = re.sub(r"[^\w\s]", "", category)

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

    except Exception as e:
        return jsonify({'error': 'Invalid request', 'message': str(e)}), 400

@app.route('/api/compare', methods=['GET'])
def compare_products():
    REQUEST_COUNT.inc()
    ids = request.args.getlist('id')
    products = list(mongo.db.products.find({'product_id': {'$in': ids}}, {'_id': 0}))
    return jsonify(products)

@app.route('/health', methods=['GET'])
def health():
    REQUEST_COUNT.inc()
    return jsonify({'status': 'healthy'})

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)