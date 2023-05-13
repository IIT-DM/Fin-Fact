#Import the dependencies
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
import time

#Create lists to store the scraped data
authors = []
dates = []
statements = []
sources = []
targets = []

#Create a function to scrape the site
def scrape_website(page_number, source):
    page_num = str(page_number) #Convert the page number to a string

    '''source: a certain speaker only'''
    # URL = 'https://www.politifact.com/factchecks/list/?page={}&speaker={}'.format(page_num, source)

    URL = 'https://www.politifact.com/factchecks/list/?category=science'.format(page_num, source)

    '''source: all'''
    # URL = 'https://www.politifact.com/factchecks/list/?page='+page_num #append the page number to complete the URL

    # URL = 'https://www.politifact.com/factchecks/2023/apr/20/facebook-posts/video-of-former-cia-director-is-not-proof-that-gov/'

    webpage = requests.get(URL)  #Make a request to the website
    #time.sleep(3)
    soup = BeautifulSoup(webpage.text, "html.parser") #Parse the text from the website
    #Get the tags and it's class
    statement_footer =  soup.find_all('footer',attrs={'class':'m-statement__footer'})  #Get the tag and it's class
    statement_quote = soup.find_all('div', attrs={'class':'m-statement__quote'}) #Get the tag and it's class
    statement_meta = soup.find_all('div', attrs={'class':'m-statement__meta'})#Get the tag and it's class
    target = soup.find_all('div', attrs={'class':'m-statement__meter'}) #Get the tag and it's class
    #loop through the footer class m-statement__footer to get the date and author
    for i in statement_footer:
        link1 = i.text.strip()
        name_and_date = link1.split()
        first_name = name_and_date[1]
        last_name = name_and_date[2]
        full_name = first_name+' '+last_name
        month = name_and_date[4]
        day = name_and_date[5]
        year = name_and_date[6]
        date = month+' '+day+' '+year
        dates.append(date)
        authors.append(full_name)
    #Loop through the div m-statement__quote to get the link
    for i in statement_quote:
        link2 = i.find_all('a')
        statements.append(link2[0].text.strip())
    #Loop through the div m-statement__meta to get the source
    for i in statement_meta:
        link3 = i.find_all('a') #Source
        source_text = link3[0].text.strip()
        sources.append(source_text)
    #Loop through the target or the div m-statement__meter to get the facts about the statement (True or False)
    for i in target:
        fact = i.find('div', attrs={'class':'c-image'}).find('img').get('alt')
        targets.append(fact)

n=2
for i in range(1, n):
    scrape_website(i, source='covid')

data = pd.DataFrame(columns = ['author',  'statement', 'source', 'date', 'target'])
data['author'] = authors
data['statement'] = statements
data['source'] = sources
data['date'] = dates
data['target'] = targets
#Show the data set
print(data)
# data.iloc[:5].to_csv('politifact-joe-biden-sample.csv', index=False, sep=',')

