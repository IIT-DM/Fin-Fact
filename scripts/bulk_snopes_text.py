from bs4 import BeautifulSoup
import requests
import json

# with open('urls.json', 'r') as f:
#     urls = json.load(f)
# for url in urls:
url = "https://www.snopes.com/fact-check/meghan-markle-shocking-announcement/"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
start_section = soup.find('section', id='fact_check_rating_container')
end_section = soup.find('section', class_='author-container')

if start_section is None:
    print("Could not find a section with the id 'fact_check_rating_container'.")
elif end_section is None:
    print("Could not find a section with the class 'author-container'.")
else:
    start_sibling = start_section.find_next_sibling()
    p_a_tags = start_sibling.find_all_next(['p', 'a'])
    p_a_end_index = p_a_tags.index(end_section.find_next(['p', 'a']))
    p_a_tags = p_a_tags[:p_a_end_index]
    justification_text = ' '.join(tag.text for tag in p_a_tags)

    print(justification_text)
