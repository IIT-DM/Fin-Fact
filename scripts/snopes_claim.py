from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json

# url = 'https://www.snopes.com/fact-check/biden-fdr-television/'
# r = requests.get(url)

with open('urls.json', 'r') as f:
    urls = json.load(f)

# Iterate over the URLs
for url in urls:
    # Make a request to the website
    r = requests.get(url)
# Parse the HTML content
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find the 'title-container' section
    title_container = soup.find('section', class_='title-container')

    if title_container is None:
        print("Could not find a section with the class 'title_container'.")
    else:
        # Find the h1 and h2 tags and extract their text
        h1_text = title_container.find('h1').text
        h2_text = title_container.find('h2').text

        # Find the author name and extract it
        author_name = title_container.find('a', class_='author_link').text.strip()

        # Find the published date, extract it, and convert it to mm/dd/yyyy format
        published_date = title_container.find('h3', class_='publish_date').text
        published_date = published_date.replace('Published ', '')
        published_date = datetime.strptime(published_date, '%b %d, %Y').strftime('%m/%d/%Y')

        print(f'claim: {h1_text}')
        print(f'sci_digest: {h2_text}')
        print(f'author: {author_name}')
        print(f'posted: {published_date}')

