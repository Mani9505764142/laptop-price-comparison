from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import pandas as pd

def scrape_flipkart(product_name):
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    ]
    chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        time.sleep(random.uniform(1, 3))
        
        search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}"
        print(f"Opening: {search_url}\n")
        driver.get(search_url)
        
        time.sleep(random.uniform(3, 6))
        
        print("Page loaded, extracting data...\n")
        
        scroll_height = random.randint(800, 1200)
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        time.sleep(random.uniform(1, 2))
        
        products = []
        
        # Find product containers
        product_containers = driver.find_elements(By.CSS_SELECTOR, "div.cPHDOP.col-12-12")
        
        print(f"Found {len(product_containers)} product containers\n")
        
        for idx, container in enumerate(product_containers[:20], 1):
            try:
                time.sleep(random.uniform(0.1, 0.3))
                
                # Get ALL text from container first
                container_text = container.text
                
                # Skip if container is too small (likely an ad or empty)
                if len(container_text) < 20:
                    continue
                
                # Method 1: Try standard product name selector
                name = None
                try:
                    name_elem = container.find_element(By.CSS_SELECTOR, "div.KzDlHZ")
                    name = name_elem.text.strip()
                except:
                    pass
                
                # Method 2: If no name found, try to extract from all text
                if not name or len(name) < 10:
                    lines = [line.strip() for line in container_text.split('\n')]
                    for line in lines:
                        if (len(line) > 15 and 
                            not line.startswith('₹') and 
                            not line.startswith('Add to') and
                            not line.replace(',', '').isdigit() and
                            'Sponsored' not in line and
                            'Rating' not in line):
                            name = line
                            break
                
                # Get price
                price = None
                try:
                    price_elem = container.find_element(By.CSS_SELECTOR, "div.Nx9bqj")
                    price = price_elem.text.strip()
                except:
                    import re
                    price_match = re.search(r'₹[\d,]+', container_text)
                    if price_match:
                        price = price_match.group(0)
                
                # ============ COMPREHENSIVE FILTER LOGIC ============
                if name and price and len(name) > 10:
                    # Skip obvious non-laptop items (printers, monitors, accessories)
                    skip_keywords = [
                        'Laptop Accessories', 
                        'PROCESSOR GENERATION', 
                        'Add to', 
                        'Filter', 
                        'Sort By', 
                        'BRAND', 
                        'RAM Size',
                        'Keyboard',
                        'Mouse',
                        'Bag',
                        'Case',
                        'Charger',
                        'Adapter',
                        'Cable',
                        'Printer',
                        'Scanner',
                        'Ink Tank',
                        'Multi-function',
                        'All In One 5',
                        'DeskJet',
                        'LaserJet',
                        'OfficeJet',
                        'Smart Tank',
                        '27 inch)',        # Monitors
                        '24 inch)',        # Monitors
                        '22 inch)',        # Monitors
                        '32 inch)',        # Monitors
                        '21 inch)',        # Monitors
                        'LED Backlit IPS', # Monitor description
                        'IPS Panel with',  # Monitor description
                        'Monitor',
                        'Display Only',
                        'cm (27 inch)',    # Monitor size format
                        'cm (24 inch)',
                        'cm (22 inch)',
                        'Full HD LED Backlit'  # Common monitor phrase
                    ]
                    
                    # Check if any skip keyword is in the product name
                    if any(keyword.lower() in name.lower() for keyword in skip_keywords):
                        print(f"  ✗ Skipped: {name[:60]} (Printer/Monitor/Accessory)")
                        continue
                    
                    # Positive check: Must contain strong laptop-related terms
                    has_laptop_indicator = any(word in name.lower() for word in [
                        'laptop', 'notebook', 'vivobook', 'ideapad', 'thinkpad', 
                        'inspiron', 'vostro', 'latitude', 'pavilion', 'envy', 'omen', 
                        'predator', 'aspire', 'swift', 'zenbook', 'chromebook', 
                        'macbook', 'elitebook', 'probook', 'spectre', 'zbook',
                        'core i3', 'core i5', 'core i7', 'core i9',
                        'ryzen 3', 'ryzen 5', 'ryzen 7', 'ryzen 9',
                        'intel celeron', 'intel pentium', 'intel core',
                        'windows 11', 'windows 10', 'dos', 'ubuntu', 'chrome os',
                        '8gb ram', '16gb ram', '4gb ram', '12gb ram', '32gb ram',
                        '512gb ssd', '256gb ssd', '1tb ssd', '128gb ssd',
                        'ddr4', 'ddr5', 'lpddr4', 'lpddr5',
                        'thin & light', 'thin and light', 'ultrabook', 'gaming laptop',
                        '13th gen', '12th gen', '11th gen', '10th gen',
                        'amd athlon', 'celeron dual core'
                    ])
                    
                    if not has_laptop_indicator:
                        print(f"  ✗ Skipped: {name[:60]} (No laptop indicators)")
                        continue
                    
                    # Skip if price is too low (accessories, parts)
                    try:
                        price_num = int(price.replace('₹', '').replace(',', '').strip())
                        if price_num < 15000:  # Minimum laptop price threshold
                            print(f"  ✗ Skipped: {name[:60]} (Price too low: {price})")
                            continue
                    except:
                        pass
                    
                    # If it passed all filters, add it
                    products.append({
                        'Product Name': name,
                        'Price': price,
                        'Source': 'Flipkart'
                    })
                    print(f"✓ {len(products)}. {name[:70]}...")
                    print(f"   {price}\n")
                    
                    if len(products) >= 5:
                        break
                        
            except Exception as e:
                continue
        
        return products
        
    except Exception as e:
        print(f"Error: {e}")
        return []
        
    finally:
        time.sleep(random.uniform(2, 4))
        driver.quit()

if __name__ == "__main__":
    print("=" * 80)
    print("FLIPKART PRODUCT SCRAPER (FINAL VERSION - LAPTOP ONLY)")
    print("=" * 80 + "\n")
    
    results = scrape_flipkart("hp")
    
    if results:
        print("\n" + "=" * 80)
        print(f"✓ SUCCESS! Scraped {len(results)} laptops")
        print("=" * 80 + "\n")
        
        df = pd.DataFrame(results)
        df.to_csv('data/flipkart_products.csv', index=False)
        print(f"✓ Data saved to data/flipkart_products.csv\n")
        
        print("FINAL RESULTS:")
        print("-" * 80)
        for i, product in enumerate(results, 1):
            print(f"\n{i}. {product['Product Name']}")
            print(f"   Price: {product['Price']}")
            print(f"   Source: {product['Source']}")
    else:
        print("\n❌ FAILED - No laptops extracted")
        print("This could mean Flipkart changed their HTML or is blocking the scraper\n")
