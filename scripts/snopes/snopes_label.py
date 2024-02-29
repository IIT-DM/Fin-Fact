from bs4 import BeautifulSoup
import requests
import json

with open('urls.json', 'r') as f:
    urls = json.load(f)

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    section_label = soup.find('section', id='fact_check_rating_container')
    if section_label:
        div_label = section_label.find('div', class_='rating_title_wrap')
        if div_label:
            text_label = div_label.get_text(strip=True)
            print(text_label)
