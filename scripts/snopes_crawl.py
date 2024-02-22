import requests
from bs4 import BeautifulSoup
import json

# Create a list to store the URLs
urls = []

# Iterate over the pages
for page_num in range(2, 51):
    # Make a request to the website
    r = requests.get(f"https://www.snopes.com/search/stock%20market/?pagenum={page_num}")

    # Parse the HTML content
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find all 'article_wrapper' divs
    article_wrappers = soup.find_all('div', class_='article_wrapper')

    for i, article_wrapper in enumerate(article_wrappers):
        # Find the hidden input element with the article URL
        article_url_input = article_wrapper.find('input', id=f'article_url_{i}')
        
        # Extract the URL from the 'value' attribute of the input element
        article_url = article_url_input['value'] if article_url_input else None

        # Add the URL to the list
        if article_url:
            urls.append(article_url)

# Write the list to a JSON file
with open('urls.json', 'w') as f:
    json.dump(urls, f)
