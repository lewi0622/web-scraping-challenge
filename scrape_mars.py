from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from splinter import Browser


def init_browser():
    """initialize chrome browser using chromedriver"""
    executable_path = {"executable_path": "c:/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    # init browser
    browser = init_browser()

    # ************************************************************************
    # nasa mars news site
    url = r'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # wait for page to load
    time.sleep(1)
    
    # soupify
    soup = bs(browser.html, features="lxml")

    # find item list containing all article content
    item_list = soup.find('ul', class_='item_list')

    # access first item
    newest_article = item_list.li

    # get content title and body
    news_title = newest_article.find('div', class_='content_title').text
    news_p = newest_article.find('div', class_='article_teaser_body').text
    # ************************************************************************
    # jpl featured space image
    url = r'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # wait for page to load
    time.sleep(1)

    # click on "full image" button
    browser.find_by_id('full_image').click()

    # get image url
    jpl_img = browser.find_by_css('img[class="fancybox-image"]')['src']
    # ************************************************************************
    # Mars Facts
    url = r'https://space-facts.com/mars/'

    # get tables with pandas
    planet_profile_df = pd.read_html(url)[0]

    # create html table
    planet_profile_html = planet_profile_df.to_html(index=False, header=False)
    # ************************************************************************
    # Mars Hemispheres
    url = r'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # wait for page to load
    time.sleep(1)

    # initialize image dict
    hemisphere_image_urls = [
        {'title': 'Cerberus', 'url': ''},
        {'title': 'Schiaparelli', 'url': ''},
        {'title': 'Syrtis Major', 'url': ''},
        {'title': 'Valles Marineris', 'url': ''}
    ]

    for hemisphere in hemisphere_image_urls:
        # click on link matching hemisphere name
        browser.links.find_by_partial_text(hemisphere['title']).click()
        time.sleep(0.5)
        
        # find image link
        hemisphere['url'] = browser.find_by_css('img[class="wide-image"]')['src']
        browser.back()
        time.sleep(0.5)
    # ************************************************************************
    # close browser session
    browser.quit()

    return {
        'title':news_title, 
        'paragraph': news_p,
        'jpl_img': jpl_img, 
        'mars_fact_table': planet_profile_html, 
        'hemisphere_image_urls': hemisphere_image_urls
    }