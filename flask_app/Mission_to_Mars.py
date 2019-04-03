#!/usr/bin/env python
# coding: utf-8

# # Setting UP 

# # Mission to Mars
# 
# In this assignment, you will build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following outlines what you need to do.
# 
# Step 1 - Scraping
# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# 
# Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.
# 
# 
# NASA Mars News
# 
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
# 
# # Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 

# In[ ]:





# In[7]:


# Import BeautifulSoup
from bs4 import BeautifulSoup as bs
from splinter import Browser


# In[ ]:





# In[2]:


# Set the executable path and initialize the chrome browser 
# ----------------------MAC-----------------------------------------
#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#browser = Browser('chrome', **executable_path)

# ======================Windows=====================================
executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path)


# # Visit the NASA MARS NEWS SITES
# 
# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# 
# Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.
# 
# 
# ## NASA Mars News
# https://mars.nasa.gov/news/
# 
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
# 
# ## Example:
# 
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."

# In[3]:


# Visit the mars nasa new site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[5]:


html = browser.html
news_soup = bs(html, 'html.parser')

# look at the html. It's not very easy to read,  so inspect the website
print(news_soup.prettify())

# slide element contains everything in the 
# <ul class = 'item_list'>
#    <li class = "slide">

# grabbing all the slides in item_list only
#    ...
#</ul>    

slide_element = news_soup.select_one('ul.item_list li.slide')

slide_element.find("div", class_='content_title')


# In[ ]:





# In[ ]:


# you can find class side
# Checking the website,  the first News item is in a li class call slide

results = news_soup.find('li', class_='slide')

print(results.prettify())

# The top headline is "NASA's Mars Helicopter Completes Flight Teests"
# The first paragraph or sub-title is "The first helicopter to fly on Mars had its first flight on Earth

# to extract the text we need to go down in the hierarchy
# Look at the very bottom of the printout

# The headline is in <div class="content_title">
# The sub title is in <div class = "article_teaser_body"


# In[ ]:





# In[ ]:


top_news = news_soup.find("div", class_="content_title").get_text()
top_news


# In[ ]:





# In[ ]:


sub_title = news_soup.find('div', class_="article_teaser_body").get_text()
sub_title


# # JPL MARS SPACE IMAGES FEATURED IMAGE
# 
# Visit the url for JPL Featured Space Image here. https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
# 
# 
# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# 
# 
# Make sure to find the image url to the full size .jpg image.
# 
# 
# Make sure to save a complete url string for this image.
# 
# # Example:
# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
# 

# In[ ]:


# Visit URL
from bs4 import BeautifulSoup
import requests
executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path)
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#browser.visit(url)


# In[ ]:


response = requests.get(url)
print(response)


# In[ ]:


#html = browser.html
jpl_soup = BeautifulSoup(response.text, 'html.parser')

# look at the html. It's not very easy to read,  so inspect the website
print(jpl_soup.prettify())



# In[ ]:


# it's hard to find from above.  Inspect the "Full image" button 
# class = "button fancybox", id = "full_image"

#image_ofthday = jpl_soup.find("h1", class_ ="media_feature_title").get_text()


# In[ ]:


# Asking splinter to go to the site hit a button with class name full_image
#<button class = "full_image">Full Image</button>

# Current full image is called Ghostly Boomerang

full_image_button = browser.find_by_id('full_image')
full_image_button.click()


# In[ ]:


# Find the more info button and click that

browser.is_element_present_by_text('more info', wait_time=1)
# 1 second delay

more_info_button = browser.find_link_by_partial_text('more info')
more_info_button.click()


# In[ ]:


# Parse the results html with soup
html = browser.html
jpl_soup = bs(html, 'html.parser')


# In[ ]:


# src is the sources
# don't forget to ask what does figure.lede a img mean
# get 

img_url = jpl_soup.select_one('figure.lede a img').get('src')
img_url


# In[ ]:


# Use the base url to create an absolute url to make sure it always works
# JPL stores their assets internally on their server

img_url = f'https://www.jpl.nasa.gov{img_url}'
img_url


# # MARS WEATHER
# 
# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
# 
# # Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
# 

# In[8]:


executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path)
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[9]:


html = browser.html
weather_soup = bs(html, 'html.parser')


# In[10]:


# First find a tweet with the data-name `Mars Weather`
# You have to inspect the html on the web page
mars_weather_tweet = weather_soup.find('div', 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })
print(mars_weather_tweet)


# In[11]:


# Next search within the tweet for p tag containing the tweet text
mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()
mars_weather


# In[12]:


# Go to  astrogeology website 

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[13]:


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
    
    
    # Get Hemisphere title 
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    #Append hemispher object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()
    


# In[14]:


hemisphere_image_urls


# In[ ]:





# In[ ]:





# # Mars Facts
# 
# Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# 
# Use Pandas to convert the data to a HTML table string.
# 
# http://space-facts.com/mars/

# In[15]:


import pandas as pd
df = pd.read_html('https://space-facts.com/mars/')[0]
print(df)
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[ ]:





# In[16]:


df.to_html()


# In[17]:


browser.quit()


# # Mars Hemispheres
# 
# 
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# 
# 
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# 
# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# 
# 
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# 
# # Example:
# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]
# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Step 2 - MongoDB and Flask Application
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
# 
# 
# Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
# 
# 
# Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.
# 
# Store the return value in Mongo as a Python dictionary.
# 
# 
# 
# Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.
# 
# 
# Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.

# In[ ]:





# In[ ]:





# In[ ]:




