from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
db.products.drop()

products = [
    {"product_id": "1", "name": "Sony WH-1000XM5 Headphones", "brand": "Sony", "category": "Electronics", "price": 24990, "rating": 4.7, "description": "Wireless noise-cancelling headphones"},
    {"product_id": "2", "name": "Boat Rockerz 450 Headphones", "brand": "Boat", "category": "Electronics", "price": 1499, "rating": 4.2, "description": "Wireless on-ear headphones"},
    {"product_id": "3", "name": "JBL Tune 510BT", "brand": "JBL", "category": "Electronics", "price": 2999, "rating": 4.3, "description": "Wireless on-ear headphones with pure bass sound"},
    {"product_id": "4", "name": "Samsung Galaxy Buds2", "brand": "Samsung", "category": "Electronics", "price": 5999, "rating": 4.5, "description": "True wireless earbuds with ANC"},
    {"product_id": "5", "name": "Apple AirPods Pro", "brand": "Apple", "category": "Electronics", "price": 19900, "rating": 4.8, "description": "Active noise cancellation earbuds"},
    {"product_id": "6", "name": "Levi's 511 Slim Jeans", "brand": "Levis", "category": "Clothing", "price": 2999, "rating": 4.4, "description": "Classic slim fit jeans"},
    {"product_id": "7", "name": "Nike Air Max 270", "brand": "Nike", "category": "Clothing", "price": 8999, "rating": 4.6, "description": "Lifestyle shoes with Air unit"},
    {"product_id": "8", "name": "Adidas Ultraboost 22", "brand": "Adidas", "category": "Clothing", "price": 12999, "rating": 4.5, "description": "Running shoes with Boost midsole"},
    {"product_id": "9", "name": "H&M Basic T-Shirt", "brand": "HM", "category": "Clothing", "price": 499, "rating": 4.0, "description": "Cotton round-neck t-shirt"},
    {"product_id": "10", "name": "Zara Slim Chinos", "brand": "Zara", "category": "Clothing", "price": 2499, "rating": 4.1, "description": "Slim fit chino trousers"},
    {"product_id": "11", "name": "Atomic Habits", "brand": "Penguin", "category": "Books", "price": 499, "rating": 4.9, "description": "By James Clear — habits and productivity"},
    {"product_id": "12", "name": "The Psychology of Money", "brand": "Jaico", "category": "Books", "price": 399, "rating": 4.8, "description": "By Morgan Housel — personal finance"},
    {"product_id": "13", "name": "Deep Work", "brand": "Piatkus", "category": "Books", "price": 449, "rating": 4.7, "description": "By Cal Newport — focused success"},
    {"product_id": "14", "name": "Rich Dad Poor Dad", "brand": "Manjul", "category": "Books", "price": 299, "rating": 4.6, "description": "By Robert Kiyosaki — financial literacy"},
    {"product_id": "15", "name": "Think and Grow Rich", "brand": "Fingerprint", "category": "Books", "price": 199, "rating": 4.5, "description": "By Napoleon Hill — success mindset"},
    {"product_id": "16", "name": "Philips Air Fryer HD9200", "brand": "Philips", "category": "Appliances", "price": 7999, "rating": 4.4, "description": "2L compact air fryer"},
    {"product_id": "17", "name": "Prestige Induction Cooktop", "brand": "Prestige", "category": "Appliances", "price": 2299, "rating": 4.2, "description": "2000W induction cooktop"},
    {"product_id": "18", "name": "Bajaj Mixer Grinder", "brand": "Bajaj", "category": "Appliances", "price": 1799, "rating": 4.1, "description": "500W 3-jar mixer grinder"},
    {"product_id": "19", "name": "Usha Tower Fan", "brand": "Usha", "category": "Appliances", "price": 3499, "rating": 4.0, "description": "55W tower fan with remote"},
    {"product_id": "20", "name": "Havells Iron", "brand": "Havells", "category": "Appliances", "price": 999, "rating": 4.3, "description": "1000W dry iron"},
    {"product_id": "21", "name": "Wildcraft Backpack 30L", "brand": "Wildcraft", "category": "Sports", "price": 1499, "rating": 4.3, "description": "Durable trekking backpack"},
    {"product_id": "22", "name": "Decathlon Yoga Mat", "brand": "Decathlon", "category": "Sports", "price": 699, "rating": 4.5, "description": "6mm anti-slip yoga mat"},
    {"product_id": "23", "name": "Cosco Basketball", "brand": "Cosco", "category": "Sports", "price": 899, "rating": 4.2, "description": "Official size 7 basketball"},
    {"product_id": "24", "name": "Nivia Football", "brand": "Nivia", "category": "Sports", "price": 599, "rating": 4.1, "description": "Size 5 football"},
    {"product_id": "25", "name": "Aurion Running Shoes", "brand": "Aurion", "category": "Sports", "price": 1299, "rating": 4.0, "description": "Lightweight mesh running shoes"},
    {"product_id": "26", "name": "Mi Smart Band 7", "brand": "Xiaomi", "category": "Electronics", "price": 2499, "rating": 4.3, "description": "Fitness band with AMOLED display"},
    {"product_id": "27", "name": "Fire-Boltt Phoenix Pro", "brand": "FireBoltt", "category": "Electronics", "price": 1999, "rating": 4.1, "description": "Smartwatch with calling feature"},
    {"product_id": "28", "name": "Realme Watch 3", "brand": "Realme", "category": "Electronics", "price": 2999, "rating": 4.2, "description": "1.8 inch HD display smartwatch"},
    {"product_id": "29", "name": "TP-Link WiFi Router Archer", "brand": "TPLink", "category": "Electronics", "price": 2499, "rating": 4.4, "description": "AC1200 dual-band WiFi router"},
    {"product_id": "30", "name": "Portronics Power Bank 20000mAh", "brand": "Portronics", "category": "Electronics", "price": 1499, "rating": 4.2, "description": "20000mAh fast charging power bank"},
    {"product_id": "31", "name": "Dell Inspiron 15 Laptop", "brand": "Dell", "category": "Electronics", "price": 54990, "rating": 4.5, "description": "Intel i5 12th gen, 8GB RAM, 512GB SSD"},
    {"product_id": "32", "name": "HP Pavilion x360", "brand": "HP", "category": "Electronics", "price": 62990, "rating": 4.4, "description": "2-in-1 convertible laptop Intel i5"},
    {"product_id": "33", "name": "Logitech MX Master 3 Mouse", "brand": "Logitech", "category": "Electronics", "price": 7999, "rating": 4.8, "description": "Advanced wireless mouse for productivity"},
    {"product_id": "34", "name": "Keychron K2 Keyboard", "brand": "Keychron", "category": "Electronics", "price": 6999, "rating": 4.7, "description": "75% wireless mechanical keyboard"},
    {"product_id": "35", "name": "LG 24 inch Monitor", "brand": "LG", "category": "Electronics", "price": 13999, "rating": 4.5, "description": "Full HD IPS monitor with AMD FreeSync"},
    {"product_id": "36", "name": "Puma Track Pants", "brand": "Puma", "category": "Clothing", "price": 1299, "rating": 4.2, "description": "Polyester dry cell track pants"},
    {"product_id": "37", "name": "Reebok Classic Sneakers", "brand": "Reebok", "category": "Clothing", "price": 3999, "rating": 4.3, "description": "Classic leather sneakers"},
    {"product_id": "38", "name": "Van Heusen Formal Shirt", "brand": "VanHeusen", "category": "Clothing", "price": 1299, "rating": 4.4, "description": "Slim fit cotton formal shirt"},
    {"product_id": "39", "name": "Peter England Trousers", "brand": "PeterEngland", "category": "Clothing", "price": 1999, "rating": 4.3, "description": "Formal slim fit trousers"},
    {"product_id": "40", "name": "Fastrack Sunglasses", "brand": "Fastrack", "category": "Clothing", "price": 899, "rating": 4.0, "description": "UV400 protection sunglasses"},
    {"product_id": "41", "name": "The Alchemist", "brand": "HarperCollins", "category": "Books", "price": 299, "rating": 4.8, "description": "By Paulo Coelho — journey of self-discovery"},
    {"product_id": "42", "name": "Zero to One", "brand": "Virgin Books", "category": "Books", "price": 549, "rating": 4.7, "description": "By Peter Thiel — startup secrets"},
    {"product_id": "43", "name": "1984", "brand": "Penguin", "category": "Books", "price": 249, "rating": 4.6, "description": "By George Orwell — dystopian classic"},
    {"product_id": "44", "name": "Clean Code", "brand": "Pearson", "category": "Books", "price": 2199, "rating": 4.7, "description": "By Robert Martin — software craftsmanship"},
    {"product_id": "45", "name": "The Lean Startup", "brand": "Crown Business", "category": "Books", "price": 699, "rating": 4.6, "description": "By Eric Ries — startup methodology"},
    {"product_id": "46", "name": "Borosil Glass Water Bottle", "brand": "Borosil", "category": "Appliances", "price": 449, "rating": 4.4, "description": "500ml borosilicate glass bottle"},
    {"product_id": "47", "name": "Pigeon Pressure Cooker 3L", "brand": "Pigeon", "category": "Appliances", "price": 999, "rating": 4.3, "description": "Aluminium pressure cooker"},
    {"product_id": "48", "name": "Godrej Microwave 20L", "brand": "Godrej", "category": "Appliances", "price": 6499, "rating": 4.2, "description": "Solo microwave oven 20 litres"},
    {"product_id": "49", "name": "Orient Ceiling Fan 48 inch", "brand": "Orient", "category": "Appliances", "price": 2199, "rating": 4.3, "description": "Energy efficient BLDC ceiling fan"},
    {"product_id": "50", "name": "Eureka Forbes Vacuum Cleaner", "brand": "EurekaForbes", "category": "Appliances", "price": 3999, "rating": 4.1, "description": "1000W dry vacuum cleaner"},
]

db.products.insert_many(products)
print(f"Inserted {len(products)} products successfully!")