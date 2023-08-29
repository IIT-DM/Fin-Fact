from bs4 import BeautifulSoup
import pandas as pd
import requests
import json

authors = []
dates = []
statements = []
sources = []
targets = []
href_list =[]

def scrape_website(page_number, source):
    page_num = str(page_number)
    # URL = 'https://www.politifact.com/factchecks/list/?category=cap-and-trade'.format(page_num, source)
    URL = 'https://www.politifact.com/factchecks/list/?category=income&page={}&source={}'.format(page_num, source)
    webpage = requests.get(URL) 
    soup = BeautifulSoup(webpage.text, "html.parser")
    statement_footer =  soup.find_all('footer',attrs={'class':'m-statement__footer'})
    statement_quote = soup.find_all('div', attrs={'class':'m-statement__quote'})
    statement_meta = soup.find_all('div', attrs={'class':'m-statement__meta'})
    target = soup.find_all('div', attrs={'class':'m-statement__meter'})
    
    for i in statement_footer:
        link1 = i.text.strip()
        name_and_date = link1.split()
        first_name = name_and_date[1]
        last_name = name_and_date[2]
        full_name = first_name+' '+last_name
        # month = name_and_date[4]
        # day = name_and_date[5]
        # year = name_and_date[6]
        # date = month+' '+day+' '+year
        # dates.append(date)
        authors.append(full_name)

    for i in statement_quote:
        link2 = i.find_all('a')
        statements.append(link2[0].text.strip())

    for i in statement_meta:
        link3 = i.find_all('a') 
        source_text = link3[0].text.strip()
        sources.append(source_text)

    for i in target:
        fact = i.find('div', attrs={'class':'c-image'}).find('img').get('alt')
        targets.append(fact)

    for i in statement_quote:
        href = i.find('a')['href']
        href = 'https://www.politifact.com' + href
        href_list.append(href)
    
n=70
for i in range(1, n):
    scrape_website(i, source='covid')

data = pd.DataFrame(columns = ['author',  'statement', 'links', 'source', 'date', 'target'])
data['author'] = authors
data['statement'] = statements
data['links'] = href_list
data['source'] = sources
# data['date'] = dates
data['target'] = targets

data_json = {
    "url": data['links'].tolist(),
    "label": data['target'].tolist()
}

with open("./income.json", "w") as outfile:
    json.dump(data_json, outfile)

print(data)
