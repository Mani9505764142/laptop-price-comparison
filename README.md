# 👑 Laptop Price Comparison Tool

A royal-themed web application that compares laptop prices across Flipkart and Amazon in real-time using advanced web scraping techniques.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Features

- **Real-time Price Comparison** - Scrapes live data from Flipkart & Amazon
- **Smart Filtering** - Automatically filters out accessories, printers, monitors, and tablets
- **Royal UI Design** - Stunning kingdom-themed interface with VFX animations
- **Direct Purchase Links** - One-click "Buy Now" buttons for both platforms
- **Anti-Bot Detection** - Advanced techniques to bypass scraping restrictions
- **Mobile Responsive** - Works seamlessly on all devices

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Web Scraping**: Selenium WebDriver, ChromeDriver
- **Data Processing**: Pandas
- **Frontend**: HTML5, CSS3 (Royal Kingdom Theme)
- **Automation**: WebDriver Manager

## 📋 Prerequisites

- Python 3.9 or higher
- Google Chrome browser
- Internet connection

## 🚀 Installation

1. **Clone the repository**
git clone https://github.com/Mani9505764142/laptop-price-comparison.git
cd laptop-price-comparison
2. **Create virtual environment**
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # Mac/Linux

3. **Install dependencies**
pip install -r requirements.txt


4. **Run the application**
python app.py

5. **Open in browser**
http://localhost:5000


## 📁 Project Structure

Product Price Comparison Tool/
├── app.py # Flask application
├── flipkart_scraper.py # Flipkart scraper
├── amazon_scraper.py # Amazon scraper
├── requirements.txt # Dependencies
├── .gitignore # Git ignore rules
├── templates/
│ ├── index.html # Homepage
│ ├── loading.html # Loading page
│ └── results.html # Results page
├── static/
│ └── style.css # Royal theme CSS
└── data/
└── *.csv # Scraped data (optional)


## 🎨 Features Deep Dive

### Smart Filtering Algorithm
- Removes printers, scanners, monitors, tablets
- Validates laptop-specific keywords (processor, RAM, SSD)
- Price threshold filtering (₹15,000+)

### Anti-Bot Techniques
- User-agent rotation
- Automation flag removal
- Random delays between requests
- ChromeDriver stealth mode

### Royal Kingdom Theme
- Golden gradient backgrounds
- Glassmorphism effects
- Animated royal guards
- Scrolling announcement banners
- Floating crown animations

## 🔍 How It Works

1. User enters laptop search query (e.g., "dell", "hp", "lenovo")
2. Application scrapes both Flipkart and Amazon simultaneously
3. Filters out non-laptop items using smart algorithms
4. Sorts results by price (lowest to highest)
5. Displays comparison with direct purchase links

## 📊 Scraping Logic

Flipkart: Selenium + Dynamic Content Handling
Amazon: Selenium + ASIN-based Product Links
Filtering: Keyword validation + Price thresholds


## ⚠️ Legal Disclaimer

This tool is for **educational purposes only**. Web scraping should comply with:
- Robots.txt policies
- Terms of Service of websites
- Rate limiting and ethical scraping practices

Always verify prices on official websites before purchasing.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

**Mani Kanta Suthari**
- 🌐 [LinkedIn](https://linkedin.com/in/manikanta-suthari)
- 📧 [Email](mailto:manikanta.suthari2002@gmail.com)
- 💻 [GitHub](https://github.com/manikantasuthari)

## 🙏 Acknowledgments

- Flask framework for web application
- Selenium for web scraping capabilities
- Flipkart & Amazon for product data

---

⭐ **Star this repo if you found it helpful!**
