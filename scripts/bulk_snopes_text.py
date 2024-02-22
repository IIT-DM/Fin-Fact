from bs4 import BeautifulSoup
import requests
import json

# Load the URLs from the JSON file
with open('urls.json', 'r') as f:
    urls = json.load(f)

# Iterate over the URLs
for url in urls:
    # Make a request to the website
    r = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(r.text, 'html.parser')

    start_section = soup.find('section', id='fact_check_rating_container')

    # Find the section with the class 'author-container'
    end_section = soup.find('section', class_='author-container')

    if start_section is None:
        print("Could not find a section with the id 'fact_check_rating_container'.")
    elif end_section is None:
        print("Could not find a section with the class 'author-container'.")
    else:

        start_sibling = start_section.find_next_sibling()
        # Find all 'p' and 'a' tags after the 'fact_check_rating_container' section and before the 'author-container' section
        tags = start_sibling.find_all_next(['p', 'a'])
        end_index = tags.index(end_section.find_next(['p', 'a']))
        tags = tags[:end_index]

        # Extract the text from each tag and join them into a single string
        text = ' '.join(tag.text for tag in tags)

        print(text)
