#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup as bs4
import requests
import pymongo
import pandas as pd
import datetime
import time
from pprint import pprint


executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path)

mars_info_dict = dict()

def nasa_inf(nasa_news)
#Visit the mars NASA News site
url = 'https://mars.nasa.gov/news/'

# This is opening a browser
browser.visit(url)

html = browser.html

nasa_news = bs4(html, 'html.parser')

print(nasa_news.prettify())


# Inspect the html online with the inspector or look at the html print(news_soup)
# The NASA Mars websites ul and li
# <ul class="item_list">
#     <li class="slide">
#     ....
# </ul>

#Alternative approach:   slide_element = news.select_one('ul.item_list li.slide')
#slide_element.find("div", class_="content_title")
# Alternative approach
#news_title = slide_element.find('div', class_="content_title").get_text()
#news_title 


# In[13]:


# Approach I'm using - Inspecting the NASA website, thte title name is content_title, and the sub-title is "article_teaser_body"
# to extract the text we need to go down in the hierarchy
# Look at the very bottom of the printout

# The headline is in <div class="content_title">
# The sub title is in <div class = "article_teaser_body"

results = nasa_news.find('li', class_='slide')

print(results.prettify())

# The top headline and paragraph will change frequently with updates


# In[15]:


# Scrape the top news headline and news blurb 
try:

    top_news = nasa_news.find("div", class_="content_title").get_text()
    print(f"The top news item is {top_news}")
    
    
# Now find the "paragraph"  which I call subtitle

    news_blurb = nasa_news.find('div', class_="article_teaser_body").get_text()
    print(f"The subtitle is {news_blurb}")
    
except AttibuteError as Atterror: 
    print(Atterror)


# In[48]:


# Store the headline and blurb

mars_info_dict["Top_Headline"] = top_news
mars_info_dict["Top_Headline_Subtitle"] = news_blurb
mars_info_dict


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
# 
# 

# In[17]:


# Windows
executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

## Mars space images 
#* Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
#* Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a 
#* variable called `featured_image_url`. Make sure to find the image url to the full size `.jpg` image.
#* Make sure to save a complete url string for this image.
url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url2)

# Inspect the "Full image" button 
# class = "button fancybox", id = "full_image"

# Asking splinter to go to the site hit a button with class name full_image
# <button class="full_image">Full Image</button>
full_image = browser.find_by_id('full_image')
full_image.click()


# In[18]:



#find the more info button and click that
#Put in a 1 second delay before clicking more info

browser.is_element_present_by_text('more info', wait_time =1)

more_info_button = browser.find_link_by_partial_text('more info')

more_info_button.click()


# In[19]:


# Parse the resulting html with soup
html = browser.html

jpl_soup = bs4(html, 'html.parser')

# look at the html. It's not very easy to read,  so inspect the website
print(jpl_soup.prettify())


# In[20]:


# Test out to see if you can get an image
# Select just one image, get the a tag and the img
# get the source (src)


img_url = jpl_soup.select_one('figure.lede a img').get('src')
img_url


# In[22]:


# Create an absolute url to make sure it always works,  using the base url
#JPL stores their assets internally on their server

img_url = f'https://www.jpl.nasa.gov{img_url}'
img_url


# In[31]:


# Store the grabbed image into the mars dictionary

mars_info_dict['Image_of_the_Day'] = img_url
pprint(mars_info_dict)


# In[ ]:





# In[ ]:





# ### Mars Weather
# 
# * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
# 
# ```python
# # Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
# ```

# In[25]:


executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path)
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[26]:


# opening a new browser, the chrome driver is used 

html = browser.html
weather_soup = bs4(html, 'html.parser')


# In[27]:


# First find a tweet with the data-name `Mars Weather`
# inspect the html on the web page to find the right class

mars_weather_tweet = weather_soup.find('div', 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })
print(mars_weather_tweet)


# In[28]:


# Next search within the tweet for p tag containing the tweet text
mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()
mars_weather


# In[32]:


# Store in the Mars dictionary

mars_info_dict["Mars_Weather"] = mars_weather
pprint(mars_info_dict)


# In[ ]:



    
    
    
    


# In[ ]:





# ### Mars Facts
# 
# * Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# * Use Pandas to convert the data to a HTML table string.

# In[35]:


#get the Mars Facts information
mars_facts = pd.read_html('https://space-facts.com/mars/')[0]
print(mars_facts)
mars_facts.columns=['Mars_facts', 'value']
mars_facts.set_index('Mars_facts', inplace=True)
mars_facts


# In[36]:


#df.to_html()
mars_facts_html = mars_facts.to_html(classes = "mars_facts table table-striped")
mars_info_dict["Mars_Facts"] = mars_facts_html


# In[37]:


pprint(mars_info_dict)


# In[ ]:





# 
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
# - - -
# 
# 

# In[41]:


# Looking for Hemisphere data

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[43]:


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
    
    
    


# In[44]:


hemisphere_image_urls


# In[49]:


# Store into the dictionary
mars_info_dict["Mars_Hemisphere_Images"] = hemisphere_image_urls
pprint(mars_info_dict)


# In[ ]:





# In[50]:


browser.quit()


# In[ ]:





# ## Step 2 - MongoDB and Flask Application
# 
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
# 
# * Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
# 
# * Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
# 
#   * Store the return value in Mongo as a Python dictionary.
# 
# * Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
# 
# * Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.
# 
# ![final_app_part1.png](Images/final_app_part1.png)
# ![final_app_part2.png](Images/final_app_part2.png)
# 
# - - -
# 
# ## Hints
# 
# * Use Splinter to navigate the sites when needed and BeautifulSoup to help find and parse out the necessary data.
# 
# * Use Pymongo for CRUD applications for your database. For this homework, you can simply overwrite the existing document each time the `/scrape` url is visited and new data is obtained.
# 
# * Use Bootstrap to structure your HTML template.
# 
# ## Copyright
# 
# Trilogy Education Services © 2017. All Rights Reserved.

# ## Next Steps
# 
# 1. Save the Jupyter notebook as a .py file (File, Download As .py)
# 2. Copy the .py file from the "Downloads folder" into the "Flask App folder"
# 3. Make sure you have 4 parts of the scraping,  clean up the code
# 4. Cells are now all in one file
# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




