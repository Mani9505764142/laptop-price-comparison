import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_amazon(product_name):
    """
    Scrapes Amazon for laptop products using BeautifulSoup
    Works on free hosting (Render, Vercel, etc.)
    """
    
    products = []
    
    # Amazon search URL
    search_url = f"https://www.amazon.in/s?k={product_name}+laptop"
    
    # Headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        print(f"Scraping Amazon for: {product_name}")
        
        # Make request
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Amazon returned status code: {response.status_code}")
            return []
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find product containers
        product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        print(f"Found {len(product_containers)} products on Amazon")
        
        for container in product_containers[:15]:  # Limit to 15 products
            try:
                # Extract product name
                name_elem = container.find('h2', {'class': 'a-size-mini'}) or \
                           container.find('span', {'class': 'a-size-medium'}) or \
                           container.find('span', {'class': 'a-size-base-plus'})
                
                if not name_elem:
                    continue
                    
                product_name_text = name_elem.get_text(strip=True)
                
                # Filter out non-laptop items
                exclude_keywords = ['tablet', 'monitor', 'mouse', 'keyboard', 'bag', 
                                   'backpack', 'cable', 'adapter', 'charger', 'stand',
                                   'cover', 'case', 'screen guard', 'pen drive']
                
                if any(keyword in product_name_text.lower() for keyword in exclude_keywords):
                    continue
                
                # Must contain laptop-related keywords
                laptop_keywords = ['laptop', 'notebook', 'core i3', 'core i5', 'core i7', 
                                  'ryzen', 'ram', 'ssd', 'windows', 'intel', 'amd', 'gb']
                
                if not any(keyword in product_name_text.lower() for keyword in laptop_keywords):
                    continue
                
                # Extract price
                price_elem = container.find('span', {'class': 'a-price-whole'})
                
                if not price_elem:
                    continue
                    
                price = price_elem.get_text(strip=True)
                
                # Format price
                price = f"₹{price.replace(',', '')}"
                
                # Convert price to number for filtering
                try:
                    price_num = int(price.replace('₹', '').replace(',', '').strip())
                    if price_num < 15000:  # Filter out accessories
                        continue
                except:
                    continue
                
                # Extract ASIN and create product link
                asin = container.get('data-asin', '')
                if asin:
                    product_link = f"https://www.amazon.in/dp/{asin}"
                else:
                    product_link = search_url
                
                # Add to products list
                products.append({
                    'Product Name': product_name_text,
                    'Price': price,
                    'Source': 'Amazon',
                    'ASIN': asin,
                    'Link': product_link
                })
                
            except Exception as e:
                print(f"Error parsing Amazon product: {e}")
                continue
        
        print(f"Successfully scraped {len(products)} products from Amazon")
        return products
        
    except requests.exceptions.Timeout:
        print("Amazon request timed out")
        return []
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
        return []


if __name__ == "__main__":
    # Test the scraper
    results = scrape_amazon("hp")
    print(f"\nFound {len(results)} products:")
    for product in results[:3]:
        print(f"\n{product['Product Name']}")
        print(f"Price: {product['Price']}")
        print(f"Link: {product['Link']}")
