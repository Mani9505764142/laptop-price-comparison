from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def inspect_amazon_html():
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
        print("Opening Amazon homepage first...\n")
        driver.get("https://www.amazon.in")
        time.sleep(random.uniform(3, 5))
        
        print("Now searching for laptop...\n")
        url = "https://www.amazon.in/s?k=laptop"
        driver.get(url)
        time.sleep(random.uniform(5, 8))
        
        page_title = driver.title
        print(f"Page title: {page_title}\n")
        
        if "503" not in page_title and "error" not in page_title.lower():
            print("✓ Page loaded successfully!\n")
            
            driver.execute_script("window.scrollTo(0, 800);")
            time.sleep(2)
            
            # Save full page
            with open('amazon_page.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("✓ Full page saved to: amazon_page.html\n")
            
            # Try different selectors to find products
            print("Looking for product containers...\n")
            
            # Try common Amazon selectors
            selectors = [
                "div[data-component-type='s-search-result']",
                "div.s-result-item",
                "div[data-asin]",
                "div.sg-col-inner"
            ]
            
            for selector in selectors:
                try:
                    products = driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(products) > 0:
                        print(f"✓ Found {len(products)} products using selector: {selector}")
                        
                        # Get first product that has data-asin
                        for product in products[:10]:
                            asin = product.get_attribute('data-asin')
                            if asin and asin != "":
                                print(f"  First product ASIN: {asin}\n")
                                
                                # Save this product's HTML
                                with open('first_amazon_product.html', 'w', encoding='utf-8') as f:
                                    f.write(product.get_attribute('outerHTML'))
                                
                                print("✓ First product HTML saved to: first_amazon_product.html")
                                print("\nOpen this file and look for:")
                                print("1. Product name (search for 'Dell' or 'Lenovo')")
                                print("2. Price (search for '₹' or '55990')")
                                print("3. Note the CSS class names\n")
                                break
                        break
                except Exception as e:
                    continue
        
        time.sleep(3)
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=" * 70)
    print("AMAZON HTML INSPECTOR (Enhanced)")
    print("=" * 70 + "\n")
    inspect_amazon_html()
