from bs4 import BeautifulSoup
import pandas as pd
import requests
import json

targets = []
href_list = []

def scrape_website(page_number, source):
    page_num = str(page_number)
    URL = 'https://www.politifact.com/factchecks/list/?category=economy'.format(page_num, source)
    webpage = requests.get(URL) 
    soup = BeautifulSoup(webpage.text, "html.parser")
    statement_quote = soup.find_all('div', attrs={'class':'m-statement__quote'})
    target = soup.find_all('div', attrs={'class':'m-statement__meter'})
    
    for i in range(len(target)):
        fact = target[i].find('div', attrs={'class':'c-image'}).find('img').get('alt')
        href = statement_quote[i].find('a')['href']
        href = 'https://www.politifact.com' + href
        
        if fact in ['true', 'mostly-true', 'false', 'pants-fire']:
            targets.append(fact)
            href_list.append(href)

n = 150
for i in range(1, n):
    scrape_website(i, source='covid')

data = pd.DataFrame(columns=['links', 'target'])
data['links'] = href_list
data['target'] = targets

data_json = {
    "url": data['links'].tolist()
}

with open("politifact_data.json", "w") as outfile:
    json.dump(data_json, outfile)

print(data)