from flask import Flask, render_template, request
import json
import csv
import sqlite3
import os

app = Flask(__name__, template_folder="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "products.json")
CSV_PATH = os.path.join(BASE_DIR, "products.csv")
DB_PATH = os.path.join(BASE_DIR, "products.db")

def read_products_json(filepath):
    """Read and parse JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def read_products_csv(filepath):
    """Read and parse CSV file"""
    products = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row['id'] = int(row.get('id', 0))
                    row['price'] = float(row.get('price', 0))
                except (ValueError, TypeError):
                    row['id'] = 0
                    row['price'] = 0.0
                products.append(row)
    except FileNotFoundError:
        return []
    return products

def init_db(db_path):
    """Initialize SQLite database with Products table and seed data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
    )
    cursor.executemany(
        """
        INSERT OR IGNORE INTO Products (id, name, category, price)
        VALUES (?, ?, ?, ?)
        """,
        [
            (1, 'Laptop', 'Electronics', 799.99),
            (2, 'Coffee Mug', 'Home Goods', 15.99),
        ],
    )
    conn.commit()
    conn.close()

def read_products_sql(db_path):
    """Read and parse data from SQLite database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category, price FROM Products")
        rows = cursor.fetchall()
        conn.close()

        products = []
        for row in rows:
            products.append({
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'price': row[3]
            })
        return products
    except sqlite3.Error:
        return None

@app.route('/products')
def products():
    source = request.args.get('source')
    id_param = request.args.get('id')

    if source not in ['json', 'csv', 'sql']:
        return render_template('product_display.html', products=[], error="Wrong source")

    if source == 'json':
        products_data = read_products_json(JSON_PATH)
    elif source == 'csv':
        products_data = read_products_csv(CSV_PATH)
    else:
        init_db(DB_PATH)
        products_data = read_products_sql(DB_PATH)
        if products_data is None:
            return render_template('product_display.html', products=[], error="Database error")

    error = None

    if id_param is not None:
        try:
            product_id = int(id_param)
        except ValueError:
            return render_template('product_display.html', products=[], error="Product not found")

        products_data = [p for p in products_data if p.get('id') == product_id]
        if not products_data:
            error = "Product not found"

    return render_template('product_display.html', products=products_data, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
