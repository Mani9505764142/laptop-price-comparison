from flask import Flask, render_template, request
from flipkart_scraper import scrape_flipkart
from amazon_scraper import scrape_amazon
from demo_data import get_demo_data
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
        # Check if running in production (Render) or locally
        is_production = os.environ.get('RENDER') is not None
        
        print(f"Scraping for: {product_name}")
        print(f"Environment: {'Production (Demo Mode)' if is_production else 'Local (Live Scraping)'}")
        
        if is_production:
            # Use demo data on Render (Chrome/Selenium not available)
            all_products = get_demo_data(product_name)
            message = "📌 Demo Mode: Showing sample laptop data. Web scraping requires Chrome/ChromeDriver which isn't available on free hosting. For live scraping, run locally - see GitHub README for installation."
        else:
            # Use real scraping locally
            flipkart_products = []
            amazon_products = []
            
            try:
                flipkart_products = scrape_flipkart(product_name) or []
            except Exception as e:
                print(f"Flipkart scraping error: {e}")
            
            try:
                amazon_products = scrape_amazon(product_name) or []
            except Exception as e:
                print(f"Amazon scraping error: {e}")
            
            all_products = flipkart_products + amazon_products
            message = None
        
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
        flipkart_count = len([p for p in all_products if p['Source'] == 'Flipkart'])
        amazon_count = len([p for p in all_products if p['Source'] == 'Amazon'])
        
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
                               cheapest=cheapest,
                               message=message)
    
    except Exception as e:
        print(f"Error in compare route: {str(e)}")
        return render_template('results.html',
                               product_name=product_name,
                               products=[],
                               message=f"Error: {str(e)}")

if __name__ == '__main__':
    # Create necessary folders
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Get port from environment variable (for deployment) or use 5000 for local
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
