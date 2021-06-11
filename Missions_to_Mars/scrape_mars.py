import pymongo
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    collection.drop()
 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)    
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    news_title = news_soup.find("div",class_="content_title").text
    news_p = news_soup.find("div", class_="article_teaser_body").text

    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    full_image_button =  browser.links.find_by_partial_text('FULL IMAGE')
    full_image_button.click()
    img_url = image_soup.find(class_="headerimage fade-in").get("src")      
    featured_img_url = f"https://spaceimages-mars.com/{img_url}"  

    mars_facts_df = pd.read_html("https://galaxyfacts-mars.com/")
    mars_facts_df.reset_index(inplace=True)
    mars_facts_df.columns=["ID", "Properties", "Mars", "Earth"]
    mars_facts_df

    umhurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mhurl)  
    mhtml = browser.html 
    mh_soup = BeautifulSoup(mhtml,"html.parser") 
    results = mh_soup.find_all("div",class_='item')
    hemisphere_image_urls = []
    for result in results:
            product_dict = {}
            titles = result.find('h3').text
            end_link = result.find("a")["href"]
            image_link = "https://astrogeology.usgs.gov/" + end_link    
            browser.visit(image_link)
            html = browser.html
            soup= BeautifulSoup(html, "html.parser")
            downloads = soup.find("div", class_="downloads")
            image_url = downloads.find("a")["href"]
            product_dict['title']= titles
            product_dict['image_url']= image_url
            hemisphere_image_urls.append(product_dict)

    browser.quit()

    mars_data ={
		'news_title' : news_title,
		'summary': news_p,
        'featured_image': feature_url,
		'fact_table': mars_fact_html,
		'hemisphere_image_urls': hemisphere_image_urls,
        'news_url': news_url,
        'jpl_url': url,
        'fact_url': murl,
        'hemisphere_url': mhurl,
        }
    collection.insert(mars_data)