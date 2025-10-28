from flipkart_scraper import scrape_flipkart
from amazon_scraper import scrape_amazon
import pandas as pd
import time

def compare_prices(product_name):
    print("=" * 90)
    print(f"PRODUCT PRICE COMPARISON TOOL - Searching for: {product_name}")
    print("=" * 90 + "\n")
    
    all_products = []
    
    # Scrape Flipkart
    print("📦 Scraping Flipkart...")
    print("-" * 90)
    flipkart_products = scrape_flipkart(product_name)
    all_products.extend(flipkart_products)
    print(f"✓ Found {len(flipkart_products)} products on Flipkart\n")
    time.sleep(2)
    
    # Scrape Amazon
    print("📦 Scraping Amazon...")
    print("-" * 90)
    amazon_products = scrape_amazon(product_name)
    all_products.extend(amazon_products)
    print(f"✓ Found {len(amazon_products)} products on Amazon\n")
    
    if not all_products:
        print("❌ No products found on either platform")
        return
    
    # Save combined results
    df = pd.DataFrame(all_products)
    df.to_csv('data/price_comparison.csv', index=False)
    
    # Clean prices for comparison (remove ₹ and commas)
    def clean_price(price_str):
        try:
            return int(price_str.replace('₹', '').replace(',', '').strip())
        except:
            return 999999
    
    df['Price_Numeric'] = df['Price'].apply(clean_price)
    df_sorted = df.sort_values('Price_Numeric')
    
    # Display results
    print("\n" + "=" * 90)
    print(f"🏆 COMPARISON RESULTS - Total {len(all_products)} products found")
    print("=" * 90 + "\n")
    
    print("💰 TOP 5 CHEAPEST OPTIONS:")
    print("-" * 90)
    for i, row in enumerate(df_sorted.head(5).iterrows(), 1):
        idx, data = row
        print(f"\n{i}. {data['Product Name'][:75]}...")
        print(f"   💵 Price: {data['Price']}")
        print(f"   🏪 Source: {data['Source']}")
    
    print("\n\n📊 PLATFORM SUMMARY:")
    print("-" * 90)
    
    # Calculate averages only if products exist
    if len(flipkart_products) > 0:
        flipkart_avg = df[df['Source'] == 'Flipkart']['Price_Numeric'].mean()
        print(f"Flipkart: {len(flipkart_products)} products, Avg Price: ₹{int(flipkart_avg):,}")
    else:
        print(f"Flipkart: No products found")
    
    if len(amazon_products) > 0:
        amazon_avg = df[df['Source'] == 'Amazon']['Price_Numeric'].mean()
        print(f"Amazon:   {len(amazon_products)} products, Avg Price: ₹{int(amazon_avg):,}")
    else:
        print(f"Amazon:   No products found")
    
    cheapest = df_sorted.iloc[0]
    print(f"\n🎯 BEST DEAL: {cheapest['Source']} - {cheapest['Price']}")
    print(f"   {cheapest['Product Name'][:70]}...")
    
    print("\n✓ Full comparison saved to: data/price_comparison.csv")
    print("=" * 90 + "\n")

if __name__ == "__main__":
    product = input("Enter product name to compare (or press Enter for 'laptop'): ").strip()
    if not product:
        product = "laptop"
    
    compare_prices(product)
