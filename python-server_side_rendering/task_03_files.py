from flask import Flask, render_template, request
import json
import csv
import os

app = Flask(__name__, template_folder="templates")

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

@app.route('/products')
def products():
    source = request.args.get('source')
    id_param = request.args.get('id')

    if source not in ['json', 'csv']:
        return render_template('product_display.html', products=[], error="Wrong source")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "products.json")
    csv_path = os.path.join(base_dir, "products.csv")

    if source == 'json':
        products_data = read_products_json(json_path)
    else:
        products_data = read_products_csv(csv_path)

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
