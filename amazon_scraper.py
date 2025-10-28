from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import pandas as pd

def scrape_amazon(product_name):
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": user_agent,
        "platform": "Win32"
    })
    
    try:
        time.sleep(random.uniform(1, 2))
        
        driver.get("https://www.amazon.in")
        time.sleep(random.uniform(2, 3))
        
        search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
        driver.get(search_url)
        time.sleep(random.uniform(4, 6))
        
        print("Page loaded, extracting data...\n")
        
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(1)
        
        products = []
        product_containers = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
        
        print(f"Found {len(product_containers)} product containers\n")
        
        for idx, container in enumerate(product_containers[:15], 1):
            try:
                time.sleep(random.uniform(0.1, 0.3))
                
                asin = container.get_attribute('data-asin')
                if not asin:
                    continue
                
                # Try to find product name
                name = None
                name_selectors = [
                    "h2 span.a-text-normal",
                    "h2 a span",
                    "h2 span",
                    "span.a-size-medium.a-color-base.a-text-normal",
                    "span.a-size-base-plus"
                ]
                
                for selector in name_selectors:
                    try:
                        name_elem = container.find_element(By.CSS_SELECTOR, selector)
                        name = name_elem.text.strip()
                        if name:
                            break
                    except:
                        continue
                
                # Try to find price
                price = None
                price_selectors = [
                    "span.a-price-whole",
                    "span.a-price span",
                    "span.a-offscreen",
                    "span.a-color-price"
                ]
                
                for selector in price_selectors:
                    try:
                        price_elem = container.find_element(By.CSS_SELECTOR, selector)
                        price_text = price_elem.text or price_elem.get_attribute('textContent')
                        if price_text and ('₹' in price_text or price_text.replace(',', '').isdigit()):
                            price = price_text.strip()
                            if not price.startswith('₹'):
                                price = '₹' + price
                            break
                    except:
                        continue
                
                # ============ NEW FILTER LOGIC ============
                if name and price:
                    # Skip tablets, accessories, and non-laptop items
                    skip_keywords = [
                        'Tab|',  # Tablets (Tab| to avoid matching in descriptions)
    'Tablet',
    'iPad',
    'Keyboard',
    'Mouse',
    'Bag',
    'Case',
    'Charger',
    'Adapter',
    'Cable',
    'Stand',
    'Screen Protector',
    'Sleeve',
    'Monitor',
    'Display Only'  # Changed from just "Display"
                    ]
                    
                    # Check if product name contains skip keywords
                    name_lower = name.lower()
                    if any(keyword.lower() in name_lower for keyword in skip_keywords):
                        print(f"  ✗ Skipped: {name[:50]} (Not a laptop)")
                        continue
                    
                    # Skip if price is too low (likely accessory)
                    try:
                        price_num = int(price.replace('₹', '').replace(',', '').strip())
                        if price_num < 15000:  # Skip items under ₹15,000
                            print(f"  ✗ Skipped: {name[:50]} (Price too low: {price})")
                            continue
                    except:
                        pass
                    
                    products.append({
                        'Product Name': name,
                        'Price': price,
                        'Source': 'Amazon',
                        'ASIN': asin
                    })
                    print(f"  ✓ {len(products)}. {name[:60]}...")
                    print(f"     {price}\n")
                    
                    if len(products) >= 5:
                        break
                    
            except Exception as e:
                continue
        
        return products
        
    except Exception as e:
        print(f"Fatal Error: {e}")
        return []
        
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    print("=" * 80)
    print("AMAZON PRODUCT SCRAPER (WITH LAPTOP FILTER)")
    print("=" * 80 + "\n")
    
    results = scrape_amazon("lenovo")
    
    if results:
        print("\n" + "=" * 80)
        print(f"✓ SUCCESS! Scraped {len(results)} products")
        print("=" * 80 + "\n")
        
        for i, product in enumerate(results, 1):
            print(f"{i}. {product['Product Name'][:60]}...")
            print(f"   {product['Price']}\n")
    else:
        print("\n❌ No products found")
