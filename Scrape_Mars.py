#!/usr/bin/env python
# coding: utf-8
# # Setting UP 

# # Mission to Mars

from splinter import Browser
from bs4 import BeautifulSoup as bs4
import requests
import pymongo
import pandas as pd
import datetime
import time
from pprint import pprint


#define  function for exec path for chromedriver.exe.  
def init_browser():
    executable_path = {'executable_path': 'C:/ChromeSafe/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    


def mars_news(browser):

mars_info_dict = dict()
#Visit the mars NASA News site
url = 'https://mars.nasa.gov/news/'

# This is opening a browser
browser = init_browser()
browser.visit(url)
html = browser.html
nasa_news = bs4(html, 'html.parser')

try:

    top_news = nasa_news.find("div", class_="content_title").get_text()
 #   print(f"The top news item is {top_news}")
    
    
# Now find the "paragraph"  which I call subtitle

    news_blurb = nasa_news.find('div', class_="article_teaser_body").get_text()
 #   print(f"The subtitle is {news_blurb}")
    
except AttibuteError as Atterror: 
    print(Atterror)

mars_info_dict["Top_Headline"] = top_news
mars_info_dict["Top_Headline_Subtitle"] = news_blurb
return mars_info_dict


# ### JPL Mars Space Images - Featured Image
# 
# * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
# 
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
# 
# * Make sure to find the image url to the full size `.jpg` image.
# 
# * Make sure to save a complete url string for this image.
#

def jpl_featured(browser):
url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url2)

# Inspect the "Full image" button 
# class = "button fancybox", id = "full_image"

# Asking splinter to go to the site hit a button with class name full_image
# <button class="full_image">Full Image</button>
full_image = browser.find_by_id('full_image')
full_image.click()

#find the more info button and click that
#Put in a 1 second delay before clicking more info

browser.is_element_present_by_text('more info', wait_time =1)

more_info_button = browser.find_link_by_partial_text('more info')

more_info_button.click()

# Parse the resulting html with soup
html = browser.html

jpl_soup = bs4(html, 'html.parser')

# look at the html. It's not very easy to read,  so inspect the website
#print(jpl_soup.prettify())

# Test out to see if you can get an image
# Select just one image, get the a tag and the img
# get the source (src)


img_url = jpl_soup.select_one('figure.lede a img').get('src')

# Create an absolute url to make sure it always works,  using the base url
#JPL stores their assets internally on their server

img_url = f'https://www.jpl.nasa.gov{img_url}'

# Store the grabbed image into the mars dictionary

mars_info_dict['Image_of_the_Day'] = img_url
return mars_info_dict


# ### Mars Weather
# 
# * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
# 
# ```python
# # Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
def twitter_weather(browser):
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)

html = browser.html
weather_soup = bs4(html, 'html.parser')

# First find a tweet with the data-name `Mars Weather`
# inspect the html on the web page to find the right class

mars_weather_tweet = weather_soup.find('div', 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })
#print(mars_weather_tweet)

# Next search within the tweet for p tag containing the tweet text
mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()

# Store in the Mars dictionary

mars_info_dict["Mars_Weather"] = mars_weather
return mars_info_dict

# ### Mars Facts
# 
# * Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# * Use Pandas to convert the data to a HTML table string.

def mars_facts():
#get the Mars Facts information
mars_facts = pd.read_html('https://space-facts.com/mars/')[0]
print(mars_facts)
mars_facts.columns=['Mars_facts', 'value']
mars_facts.set_index('Mars_facts', inplace=True)
mars_facts

mars_facts_html = mars_facts.to_html(classes = "mars_facts table table-striped")
mars_info_dict["Mars_Facts"] = mars_facts_html

return (mars_info_dict)

# ### Mars Hemispheres
# 
# * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# 
# ```python
# # Example:
# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]
# ```
# 
# Looking for Hemisphere data


def hemisphere(browser)
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

#inspect the website
hemisphere_image_urls = []

# First get a list og all the hemisphers
links = browser.find_by_css('a.product-item h3')
for item in range(len(links)):
    hemisphere = {}
    
    # We have to find the element on each loop to avoid a stale element exception
    browser.find_by_css('a.product-item h3')[item].click()
    
    # Next we find the Sample Image anchor tage and extract the href
    sample_element = browser.find_link_by_text('Sample').first
    hemisphere['img_url'] = sample_element['href']
    
    
    # Get Hemispher title 
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    #Append hemispher object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()


# Store into the dictionary
mars_info_dict["Mars_Hemisphere_Images"] = hemisphere_image_urls
return mars_info_dict


def scrape_hemisphere(html_text):
    hemisphere_soup = bs(html_text, "html.parser")
    try:
        title_element = hemisphere_soup.find('h2', class_="title").get_text()
        sample_element = hemisphere_soup.find('a', text="Sample").get('href')
    except AttributeError:
        title_element = None
        sample_element = None
    hemisphere = {
        'title': title_element,
        'img_url' : sample_element
    }
return hemisphere


def scrape_all():
executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path)

mars_news(browser)
jpl_featured(browser)
twitter_weather(browser)
hemisphere(browser)
mars_facts()

timestamp = dt.datetime.now()

 mars_return_dict =  {
        "Top_Headline": mars_info_dict["Top_Headline"],
        "Top_Headline_Subtitle" :mars_info_dict["Top_Headline_Subtitle"],
        "Featured_Image" : mars_info_dict["Image_of_the_Day"],
        "Weather" : mars_info_dict["Mars_Weather"],
        "Facts" : mars_info_dict["Mars_Facts"],
        "Hemisphere_Images": mars_info_dict["Mars_Hemisphere_Images"],
      #  "Date" : mars_info_dict["Date_time"],
    }
    return mars_return_dict
    
browser.quit()
return def 

if __name__ == "__main__"
    print(scrape_all())
