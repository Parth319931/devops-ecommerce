import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    with patch('flask_pymongo.PyMongo.init_app'):
        from app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

def test_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'healthy'

def test_search_returns_200(client):
    with patch('app.mongo') as mock_mongo:
        mock_mongo.db.products.find.return_value = []
        res = client.get('/api/search?q=headphones')
        assert res.status_code == 200

def test_search_with_empty_query(client):
    with patch('app.mongo') as mock_mongo:
        mock_mongo.db.products.find.return_value = []
        res = client.get('/api/search')
        assert res.status_code == 200

def test_products_endpoint(client):
    with patch('app.mongo') as mock_mongo:
        mock_mongo.db.products.find.return_value = []
        res = client.get('/api/products')
        assert res.status_code == 200

def test_compare_endpoint(client):
    with patch('app.mongo') as mock_mongo:
        mock_mongo.db.products.find.return_value = []
        res = client.get('/api/compare?id=1&id=2')
        assert res.status_code == 200

def test_search_returns_list(client):
    with patch('app.mongo') as mock_mongo:
        mock_mock_product = {'product_id': '1', 'name': 'Test', 'price': 100, 'rating': 4.0, 'brand': 'X', 'category': 'Electronics', 'description': 'desc'}
        mock_mongo.db.products.find.return_value = [mock_mock_product]
        res = client.get('/api/search?q=test')
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

def test_search_price_filter(client):
    with patch('app.mongo') as mock_mongo:
        mock_mongo.db.products.find.return_value = []
        res = client.get('/api/search?min_price=100&max_price=5000')
        assert res.status_code == 200

def test_search_brand_filter(client):
    with patch('app.mongo') as mock_mongo:
        mock_mongo.db.products.find.return_value = []
        res = client.get('/api/search?brand=Sony')
        assert res.status_code == 200

def test_search_category_filter(client):
    with patch('app.mongo') as mock_mongo:
        mock_mongo.db.products.find.return_value = []
        res = client.get('/api/search?category=Electronics')
        assert res.status_code == 200

def test_search_rating_filter(client):
    with patch('app.mongo') as mock_mongo:
        mock_mongo.db.products.find.return_value = []
        res = client.get('/api/search?min_rating=4.0')
        assert res.status_code == 200