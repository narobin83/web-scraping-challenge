from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# NASA Mars News Site Web Scraper
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Get First List Item & Wait Half a Second If Not Immediately Present
    browser.is_element_present_by_css("ul.item_list li.slide")

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")