from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def inspect_flipkart_html():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # Go directly to laptop search results
        url = "https://www.flipkart.com/search?q=laptop"
        print(f"Opening: {url}\n")
        driver.get(url)
        time.sleep(5)
        
        print("Page loaded. Saving HTML...\n")
        
        # Scroll to load more content
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(2)
        
        # Save full page source
        with open('flipkart_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        
        print("✓ HTML saved to: flipkart_page.html")
        print("\nNow let's extract just the first product's HTML...\n")
        
        # Try to find the first product and print its HTML
        try:
            # Find first product link
            first_product = driver.find_element(By.XPATH, "//a[contains(@href, '/p/')]")
            
            # Get its parent container
            container = first_product.find_element(By.XPATH, ".//ancestor::div[contains(@class, 'col-12-12')][1]")
            
            # Save first product HTML
            with open('first_product.html', 'w', encoding='utf-8') as f:
                f.write(container.get_attribute('outerHTML'))
            
            print("✓ First product HTML saved to: first_product.html")
            print("\nYou can open these files to see the actual structure!")
            
        except Exception as e:
            print(f"Could not extract first product: {e}")
        
        time.sleep(3)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("FLIPKART HTML INSPECTOR")
    print("=" * 60 + "\n")
    inspect_flipkart_html()
