
# coding: utf-8

# In[1]:


import pandas as pd, seaborn as sns
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import time
import smtplib

# %matplotlib inline


# In[4]:


data = pd.read_csv('./data/coinTelegraph_feb13.csv')
data.iloc[50]


# In[93]:


options = webdriver.ChromeOptions()
options.add_argument('headless')

path_to_chromedriver = './../chromedriver' # change path as needed
driver = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=options)


# In[95]:


data = pd.read_csv('./data/coinTelegraph_feb13.csv')
data.rename(columns= {'Unnamed: 0':'article_id'}, inplace =True)


# In[96]:



## -- pick up where we left or set our index reader fresh at -1
try: 
    tail = get_ipython().getoutput('tail -1 data/tags.csv')
    last = int(tail[0].split(',')[0])
    type(last)
    
except: 
    last = -1 
    

## -- if from scratch - prepare files and write headers 
headers = {
    'articles': ['article_id','shares','text','views'],
    'links': ['article_id','link'],
    'tags': ['article_id','tag']
}

if(last==-1):

    for h in headers:
        headers[h]
        fd = open('data/'+h+'.csv','w')
        fd.write(','.join(headers[h]))
        fd.write('\n')
        fd.close()


# In[100]:


articles = []
tags = []
links = []

for i, d in data.iterrows():
    
    if(i <= last): continue
    
    print(i)
    
    article_id = d['article_id']
    url = d['url']
    
    result  = driver.get(url)
    html = driver.page_source;
    soup = BeautifulSoup(html, "lxml")

    article = {}

    try:
        # - main stuff
        article['article_id'] = article_id
        article['text'] = soup.find('div', {'class': 'post-full-text'}).text.strip()
        article['views'] = soup.find('div', {'class': 'total-views'}).find('span', {'class': 'total-qty'}).text.strip()
        article['shares'] = soup.find('div', {'class': 'total-shares'}).find('span', {'class': 'total-qty'}).text.strip()

        # - tags 
        tg = soup.find('div',{'class':'tags'})

        for tag in tg.findAll('li'):
            tags.append((article_id, tag.text.strip()))

        # - links 
        body = soup.find('div', {'class': 'post-full-text'})

        for a in body.findAll('a'):
            #print(a.attrs['href'])
            links.append((article_id, a.attrs['href']))

        articles.append(article)

        print('-')
        
    except: print('--404')
    
    if(i!=0 and i%10==0):
        print("dump..")
        
        ### hmmm.... think abut how i can try this down; var names are tricky & articles already has headers 
        tags_df     =  pd.DataFrame(tags, columns = ['article_id','tag'])
        links_df    =  pd.DataFrame(links, columns = ['article_id','link'])
        articles_df =  pd.DataFrame(articles)
        
        articles_df.to_csv('data/articles.csv', mode = 'a',  header = None, index = None)
        links_df.to_csv('data/links.csv', mode = 'a',  header = None, index = None)
        tags_df.to_csv('data/tags.csv', mode = 'a',  header = None, index = None)
        
        articles = []
        tags = []
        links = []        
        

