"""
Demo data for deployed version when Selenium/Chrome isn't available
"""

DEMO_LAPTOPS = [
    {
        'Product Name': 'HP Laptop 15s, AMD Ryzen 5 5500U, 15.6-inch (39.6 cm), FHD, 8GB DDR4, 512GB SSD, Thin & Light, Dual Speakers (Win 11, MSO 2021, Silver, 1.69 kg)',
        'Price': '₹42,990',
        'Source': 'Amazon',
        'ASIN': 'B0CX4JGJ8R'
    },
    {
        'Product Name': 'Lenovo IdeaPad Slim 3 Intel Core i3 12th Gen 15.6" (39.62cm) FHD Laptop (8GB/512GB SSD/Windows 11/Office 2021/3 Month Game Pass/Grey/1.6Kg)',
        'Price': '₹35,990',
        'Source': 'Flipkart'
    },
    {
        'Product Name': 'Dell 15 Laptop, Intel Core i3-1215U, 8GB, 512GB SSD, 15.6" (39.62cm) FHD 120Hz, Win 11 + MSO 21, 15 Month McAfee, Spill-Resistant KB, Carbon Black, 1.48kg',
        'Price': '₹39,490',
        'Source': 'Amazon',
        'ASIN': 'B0D3B2JK7M'
    },
    {
        'Product Name': 'ASUS Vivobook 15 Intel Core i3-1215U 12th Gen 15.6" (39.62 cm) FHD Laptop (8GB RAM/512GB SSD/Windows 11/Office 2021/Fingerprint/Silver/1.7 kg)',
        'Price': '₹32,990',
        'Source': 'Flipkart'
    },
    {
        'Product Name': 'Acer Aspire Lite AMD Ryzen 5 5500U Premium Laptop (Windows 11 Home/8 GB RAM/512 GB SSD) AL15-51 with 39.62 cm (15.6") Full HD Display',
        'Price': '₹36,490',
        'Source': 'Amazon',
        'ASIN': 'B0BYQZR3ZW'
    },
    {
        'Product Name': 'HP 14s AMD Ryzen 3 5300U 14-inch(35.6 cm) Laptop (8GB RAM/512GB SSD/AMD Radeon Graphics/FHD/Windows 11/MSO/Natural Silver/1.46 kg)',
        'Price': '₹31,990',
        'Source': 'Flipkart'
    },
    {
        'Product Name': 'Lenovo V15 AMD Ryzen 5 5500U 15.6" (39.62cm) FHD Thin & Light Laptop (8GB RAM/512GB SSD/Windows 11/MS Office 2021/2Yr Warranty/Arctic Grey/1.7Kg)',
        'Price': '₹38,990',
        'Source': 'Amazon',
        'ASIN': 'B0D1YJHB8Y'
    }
]

def get_demo_data(product_name="laptop"):
    """
    Returns demo laptop data for deployment
    
    Args:
        product_name: Search query (not used, returns all demo data)
        
    Returns:
        List of product dictionaries
    """
    return DEMO_LAPTOPS
