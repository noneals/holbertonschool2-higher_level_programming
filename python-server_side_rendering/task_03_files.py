from flask import Flask, render_template, request
import json
import csv

app = Flask(__name__)

def read_json(filepath):
    """Read and parse JSON file"""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def read_csv(filepath):
    """Read and parse CSV file"""
    try:
        products = []
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert id to int and price to float
                row['id'] = int(row['id'])
                row['price'] = float(row['price'])
                products.append(row)
        return products
    except FileNotFoundError:
        return None
    except (ValueError, KeyError):
        return None

@app.route('/products')
def products():
    source = request.args.get('source')
    product_id = request.args.get('id', type=int)
    
    # Validate source parameter
    if source not in ['json', 'csv']:
        return render_template('product_display.html', error="Wrong source")
    
    # Read data from the appropriate source
    if source == 'json':
        products_data = read_json('products.json')
    else:  # csv
        products_data = read_csv('products.csv')
    
    # Handle file reading errors
    if products_data is None:
        return render_template('product_display.html', error="Error reading file")
    
    # Filter by ID if provided
    if product_id is not None:
        products_data = [p for p in products_data if p['id'] == product_id]
        if not products_data:
            return render_template('product_display.html', error="Product not found")
    
    return render_template('product_display.html', products=products_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
