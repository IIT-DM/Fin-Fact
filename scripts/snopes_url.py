from bs4 import BeautifulSoup
import requests
import json

r = requests.get("https://www.snopes.com/fact-check/biden-fdr-television/")
soup = BeautifulSoup(r.text, 'html.parser')
start_section = soup.find('section', id='fact_check_rating_container')
end_section = soup.find('section', class_='author-container')

evidence = []

if start_section is None:
    print("Could not find a section with the id 'fact_check_rating_container'.")
elif end_section is None:
    print("Could not find a section with the class 'author-container'.")
else:
    start_sibling = start_section.find_next_sibling()
    tags = start_sibling.find_all_next(['p'])
    end_index = tags.index(end_section.find_next('p'))
    tags = tags[:end_index]
    for tag in tags:
        sentence = tag.text
        a_tags = tag.find_all('a')
        hrefs = [a.get('href') for a in a_tags]
        if sentence.strip() and hrefs:
            evidence.append({
                "sentence": sentence,
                "hrefs": hrefs
            })
    # Save to a JSON file
    with open('evidence.json', 'w') as f:
        json.dump({"evidence": evidence}, f, indent=4)

