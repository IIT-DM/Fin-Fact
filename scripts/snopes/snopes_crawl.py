import requests
from bs4 import BeautifulSoup
import json

urls = []
for page_num in range(2, 51):
    r = requests.get(f"https://www.snopes.com/search/taxes/?pagenum={page_num}")
    soup = BeautifulSoup(r.text, 'html.parser')
    article_wrappers = soup.find_all('div', class_='article_wrapper')
    for i, article_wrapper in enumerate(article_wrappers):
        article_url_input = article_wrapper.find('input', id=f'article_url_{i}')
        article_url = article_url_input['value'] if article_url_input else None
        if article_url:
            urls.append(article_url)
with open('taxes_urls.json', 'w') as f:
    json.dump(urls, f)
