from bs4 import BeautifulSoup
import requests

# Make a request to the website
r = requests.get("https://www.snopes.com/fact-check/biden-fdr-television/")

# Parse the HTML content
soup = BeautifulSoup(r.text, 'html.parser')

# Find the section with the id 'fact_check_rating_container'
start_section = soup.find('section', id='fact_check_rating_container')

# Find the section with the class 'author-container'
end_section = soup.find('section', class_='author-container')

if start_section is None:
    print("Could not find a section with the id 'fact_check_rating_container'.")
elif end_section is None:
    print("Could not find a section with the class 'author-container'.")
else:
    # Find the next sibling of the 'fact_check_rating_container' section
    start_sibling = start_section.find_next_sibling()

    # Find all 'p' and 'a' tags after the sibling and before the 'author-container' section
    tags = start_sibling.find_all_next(['p', 'a'])
    end_index = tags.index(end_section.find_next(['p', 'a']))
    tags = tags[:end_index]

    # Create a list to store the sentences and hrefs
    sentences_and_hrefs = []

    # Iterate over the 'a' tags
    for tag in tags:
        if tag.name == 'a':
            # Extract the text and href from the 'a' tag
            sentence = tag.text
            href = tag.get('href')

            # Add the sentence and href to the list
            sentences_and_hrefs.append({
                "sentence": sentence,
                "hrefs": href
            })

    print(sentences_and_hrefs)
