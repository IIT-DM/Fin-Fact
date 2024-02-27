from bs4 import BeautifulSoup
import requests
import json

with open('urls.json', 'r') as f:
    urls = json.load(f)
for url in urls:
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
        p_a_img_tags = start_sibling.find_all_next(['p', 'a', 'img'])
        p_a_img_end_index = p_a_img_tags.index(end_section.find_next(['p', 'a', 'img']))
        p_a_img_tags = p_a_img_tags[:p_a_img_end_index]
        justification_text = ' '.join(tag.text for tag in p_a_img_tags if tag.name != 'img')
        img_data = []
        for img in p_a_img_tags:
            if img.name == 'img':
                src = img['src']
                parent = img.find_parent()
                caption_tag = parent.find('figcaption') or parent.find('div', class_='caption') or parent.find('span', class_='caption')
                caption = caption_tag.text if caption_tag else None
                img_data.append({
                    "src": src,
                    "caption": caption
                })
        print(f'Image data: {img_data}')
