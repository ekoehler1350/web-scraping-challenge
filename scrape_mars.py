#!/usr/bin/env python
# coding: utf-8

#import dependencies 
import pandas as pd
from bs4 import BeautifulSoup as bs
import pymongo
from splinter import Browser
import requests
from selenium import webdriver
import time
from sys import platform
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data_scrape = {}
    
    #scrape for Nasa News
    url="https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    
    html=browser.html
    soup=bs(html, 'html.parser')

    #collect the latest News Title and Paragraph Text
    news_title= soup.find('div', class_='content_title').get_text()
    news_ptext= soup.find('div', class_='article_teaser_body').get_text()
    time.sleep(2)
    mars_data_scrape['data1']=news_title
    mars_data_scrape['data2']=news_ptext


# In[43]:


#Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called
#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#browser = Browser('chrome', **executable_path, headless=False)
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')
    
    html=browser.html
    jpl_soup=bs(html,"html.parser")


# In[44]:


    #image=soup.find('img', class_="thumb")["src"]
    featured_image_url= jpl_soup('img').get('src')
    mars_data_scrape['image']=featured_image_url


# In[45]:


#Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    facts_url='https://space-facts.com/mars/'
    facts_table=pd.read_html(facts_url)
    facts_df=facts_table[0]
    facts_df.columns=['measurement', 'value']
    facts_df=facts_df.set_index('measurement', drop=True)
    mars_data_scrape['table']=facts_df.to_html()


# In[46]:


#Convert to html table string
#facts_html=facts_df.to_html()
#print(facts_html)


# In[57]:


#Obtain high resolution images for each of Mar's hemisheres.
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #browser = Browser('chrome', **executable_path, headless=False)
    base_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(base_url)
    html=browser.html
    hem_soup=bs(html,"html.parser")


# In[58]:


#titles=soup.find_all('h3')
#for title in titles:
 #   browser.links.find_by_partial_text("Hemisphere")
    
#print(titles)


# In[60]:


    hem_image_urls=[]
    hem_dictionary={'title': [],'img_url': []}
    titles=hem_soup.find_all('h3')
    for i in titles:
        long_title=i.get_text()
        title=long_title.strip('Enhanced')
        browser.click_link_by_partial_text(long_title)
        base_url=browser.find_link_by_partial_href('download')['href']
        hem_dictionary={'title': title,'img_url': base_url}
        hem_image_urls.append(hem_dictionary)
        browser.back()
        
    mars_data_scrape['hemispheres']=hem_image_urls
    
    return mars_data_scrape
    #print(hem_image_urls)


# In[ ]:




