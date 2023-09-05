from bs4 import BeautifulSoup
import pandas as pd
import requests
import json

class FactCheckerScraper:
    def __init__(self):
        self.authors = []
        self.statements = []
        self.sources = []
        self.targets = []
        self.href_list = []

    def scrape_website(self, page_number, source):
        page_num = str(page_number)
        URL = 'https://www.politifact.com/factchecks/list/?category=income&page={}&source={}'.format(page_num, source)
        webpage = requests.get(URL) 
        soup = BeautifulSoup(webpage.text, "html.parser")
        statement_footer =  soup.find_all('footer', attrs={'class':'m-statement__footer'})
        statement_quote = soup.find_all('div', attrs={'class':'m-statement__quote'})
        statement_meta = soup.find_all('div', attrs={'class':'m-statement__meta'})
        target = soup.find_all('div', attrs={'class':'m-statement__meter'})
        
        for i in statement_footer:
            link1 = i.text.strip()
            name_and_date = link1.split()
            first_name = name_and_date[1]
            last_name = name_and_date[2]
            full_name = first_name+' '+last_name
            self.authors.append(full_name)

        for i in statement_quote:
            link2 = i.find_all('a')
            self.statements.append(link2[0].text.strip())

        for i in statement_meta:
            link3 = i.find_all('a') 
            source_text = link3[0].text.strip()
            self.sources.append(source_text)

        for i in target:
            fact = i.find('div', attrs={'class':'c-image'}).find('img').get('alt')
            self.targets.append(fact)

        for i in statement_quote:
            href = i.find('a')['href']
            href = 'https://www.politifact.com' + href
            self.href_list.append(href)

    def scrape_multiple_pages(self, num_pages, source):
        for i in range(1, num_pages):
            self.scrape_website(i, source)

    def create_dataframe(self):
        data = pd.DataFrame(columns=['author', 'statement', 'links', 'source', 'date', 'target'])
        data['author'] = self.authors
        data['statement'] = self.statements
        data['links'] = self.href_list
        data['source'] = self.sources
        data['target'] = self.targets
        return data

    def save_to_json(self, filename):
        data_json = {
            "url": self.href_list,
            "label": self.targets
        }

        with open(filename, "w") as outfile:
            json.dump(data_json, outfile)

if __name__ == "__main__":
    scraper = FactCheckerScraper()
    scraper.scrape_multiple_pages(70, source='covid')
    data = scraper.create_dataframe()
    scraper.save_to_json("./income.json")
