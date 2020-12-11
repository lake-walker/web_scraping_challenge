# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():

    browser = init_browser()
    # URL of page to be scraped 
    url = 'https://mars.nasa.gov/news/8805/moxie-could-help-future-rockets-launch-off-mars/'

    # Retrive page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with html
    soup = bs(response.text, 'html.parser')

    # Retrieve the parent divs for all articles
    article_title = soup.find('h1', class_='article_title').text
    content = soup.find('div', class_='wysiwyg_content').text

    
    # Assign url and have the browser open it
    nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_url)

    # Dig into the main image and then further down into the appropriate href
    featured = mars_soup.find('div', class_='carousel_container')
    featured_image = featured.find('footer')
    featured_url = featured_image.find('a')['data-fancybox-href']
    featured_url = 'https://www.jpl.nasa.gov/' + featured_url
    # print(featured_url)

    browser.quit()

    # Create all new variable for all the new url
    mars_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(mars_url)
    mars_df = mars_facts[0]
    # mars_df

    browser = init_browser()

    # Create new url
    pics_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Visit the new url
    browser.visit(pics_url)

    # Use splinter to find all the urls for the images
    # Create new html and soup for the new url
    pics_html = browser.html
    pics_soup = bs(pics_html, 'html.parser')

    base_url = 'https://astrogeology.usgs.gov'

    pictures = pics_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for picture in pictures:
        hemi_dict = {}
        # Scrape for title
        title = picture.find('h3').text
        # print('------------')
        # print(title)
        hemi_dict['title'] = title
        
        
        href = picture.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)
        
        
        hemi_html = browser.html
        
        hemi_soup = bs(hemi_html, 'html.parser')
        
        img_url = hemi_soup.find('div', class_='downloads').find('a')['href']
        hemi_dict['img_url'] = img_url
        
        hemisphere_image_urls.append(hemi_dict)
    
    browser.quit()







    mars_dict = {}

    mars_dict["Article Title"] = article_title
    mars_dict["content"] = content
    mars_dict["featured url"] = featured_url
    mars_dict["mars df"] = mars_df
    mars_dict["hemisphere image urls"] = hemisphere_image_urls

    return mars_dict