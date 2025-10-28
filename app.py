from flask import Flask, render_template, request, jsonify
from flipkart_scraper import scrape_flipkart
from amazon_scraper import scrape_amazon
import pandas as pd
import os

app = Flask(__name__)

# Home page with search form
@app.route('/')
def index():
    return render_template('index.html')

# Loading page - shows immediately when user searches
@app.route('/search', methods=['POST'])
def search():
    product_name = request.form.get('product_name', '').strip()
    
    if not product_name:
        return render_template('index.html', error="Please enter a product name")
    
    # Show loading page immediately
    return render_template('loading.html', product_name=product_name)

# Results page - handles the actual comparison
@app.route('/compare', methods=['POST'])
def compare():
    product_name = request.form.get('product_name', '').strip()
    
    if not product_name:
        return render_template('index.html', error="Please enter a product name")
    
    try:
        # Scrape both platforms
        print(f"Scraping for: {product_name}")
        
        flipkart_products = scrape_flipkart(product_name)
        amazon_products = scrape_amazon(product_name)
        
        all_products = flipkart_products + amazon_products
        
        if not all_products:
            return render_template('results.html', 
                                   product_name=product_name,
                                   products=[],
                                   message="No products found on either platform")
        
        # Clean prices for comparison
        def clean_price(price_str):
            try:
                return int(price_str.replace('₹', '').replace(',', '').strip())
            except:
                return 999999
        
        # Sort by price
        for product in all_products:
            product['price_numeric'] = clean_price(product['Price'])
        
        all_products.sort(key=lambda x: x['price_numeric'])
        
        # Find cheapest
        cheapest = all_products[0]
        
        # Calculate platform stats
        flipkart_count = len(flipkart_products)
        amazon_count = len(amazon_products)
        
        stats = {
            'flipkart_count': flipkart_count,
            'amazon_count': amazon_count,
            'total_count': len(all_products),
            'cheapest_price': cheapest['Price'],
            'cheapest_platform': cheapest['Source']
        }
        
        return render_template('results.html',
                               product_name=product_name,
                               products=all_products,
                               stats=stats,
                               cheapest=cheapest)
    
    except Exception as e:
        return render_template('results.html',
                               product_name=product_name,
                               products=[],
                               message=f"Error: {str(e)}")

if __name__ == '__main__':
    # Create necessary folders
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
   port = int(os.environ.get('PORT', 5000))
  app.run(debug=False, host='0.0.0.0', port=port)
