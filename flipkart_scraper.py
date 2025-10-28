import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_flipkart(product_name):
    """
    Scrapes Flipkart for laptop products using BeautifulSoup
    Works on free hosting (Render, Vercel, etc.)
    """
    
    products = []
    
    # Flipkart search URL
    search_url = f"https://www.flipkart.com/search?q={product_name}+laptop"
    
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
        print(f"Scraping Flipkart for: {product_name}")
        
        # Make request
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Flipkart returned status code: {response.status_code}")
            return []
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find product containers
        # Flipkart uses different class names, trying multiple selectors
        product_containers = soup.find_all('div', {'class': '_1AtVbE'}) or \
                           soup.find_all('div', {'class': '_2kHMtA'}) or \
                           soup.find_all('div', {'class': '_13oc-S'})
        
        print(f"Found {len(product_containers)} products on Flipkart")
        
        for container in product_containers[:15]:  # Limit to 15 products
            try:
                # Extract product name
                name_elem = container.find('div', {'class': '_4rR01T'}) or \
                           container.find('a', {'class': 'IRpwTa'}) or \
                           container.find('a', {'class': 's1Q9rs'})
                
                if not name_elem:
                    continue
                    
                product_name_text = name_elem.get_text(strip=True)
                
                # Filter out non-laptop items
                exclude_keywords = ['printer', 'scanner', 'monitor', 'mouse', 'keyboard', 
                                   'tablet', 'ipad', 'pen drive', 'hard disk', 'bag', 
                                   'backpack', 'cable', 'adapter', 'charger', 'stand']
                
                if any(keyword in product_name_text.lower() for keyword in exclude_keywords):
                    continue
                
                # Must contain laptop-related keywords
                laptop_keywords = ['laptop', 'notebook', 'core i3', 'core i5', 'core i7', 
                                  'ryzen', 'ram', 'ssd', 'windows', 'dos', 'intel', 'amd']
                
                if not any(keyword in product_name_text.lower() for keyword in laptop_keywords):
                    continue
                
                # Extract price
                price_elem = container.find('div', {'class': '_30jeq3'}) or \
                           container.find('div', {'class': '_30jeq3 _1_WHN1'})
                
                if not price_elem:
                    continue
                    
                price = price_elem.get_text(strip=True)
                
                # Clean price
                if not price.startswith('₹'):
                    continue
                    
                # Convert price to number for filtering
                try:
                    price_num = int(price.replace('₹', '').replace(',', '').strip())
                    if price_num < 15000:  # Filter out accessories
                        continue
                except:
                    continue
                
                # Extract product link
                link_elem = container.find('a', href=True)
                product_link = f"https://www.flipkart.com{link_elem['href']}" if link_elem else search_url
                
                # Add to products list
                products.append({
                    'Product Name': product_name_text,
                    'Price': price,
                    'Source': 'Flipkart',
                    'Link': product_link
                })
                
            except Exception as e:
                print(f"Error parsing Flipkart product: {e}")
                continue
        
        print(f"Successfully scraped {len(products)} products from Flipkart")
        return products
        
    except requests.exceptions.Timeout:
        print("Flipkart request timed out")
        return []
    except Exception as e:
        print(f"Error scraping Flipkart: {e}")
        return []


if __name__ == "__main__":
    # Test the scraper
    results = scrape_flipkart("lenovo")
    print(f"\nFound {len(results)} products:")
    for product in results[:3]:
        print(f"\n{product['Product Name']}")
        print(f"Price: {product['Price']}")
        print(f"Link: {product['Link']}")
