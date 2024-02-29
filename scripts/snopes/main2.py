from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

with open('urls.json', 'r') as f:
    urls = json.load(f)

all_data = []

for url in urls:
    sci_digest = []
    justification_text_lt = []
    evidence_lt = []
    issues_lt = ["stock market"]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title_container = soup.find('section', class_='title-container')
    if title_container is None:
        print("Could not find a section with the class 'title_container'.")
    else:
        h1_text = title_container.find('h1').text
        h2_text = title_container.find('h2').text
        sci_digest.append(h2_text)
        author_name = title_container.find('a', class_='author_link').text.strip()
        published_date = title_container.find('h3', class_='publish_date').text
        published_date = published_date.replace('Published ', '')
        published_date = datetime.strptime(published_date, '%b %d, %Y').strftime('%m/%d/%Y')

    start_section = soup.find('section', id='fact_check_rating_container')
    end_section = soup.find('section', class_='author-container')
    if start_section is None:
        print("Could not find a section with the id 'fact_check_rating_container'.")
    elif end_section is None:
        print("Could not find a section with the class 'author-container'.")
    else:
        start_sibling = start_section.find_next_sibling()
        tags = start_sibling.find_all_next(['p'])
        end_index = tags.index(end_section.find_next('p'))
        tags = tags[:end_index]
        p_a_tags = start_sibling.find_all_next(['p', 'a'])
        p_a_end_index = p_a_tags.index(end_section.find_next(['p', 'a']))
        p_a_tags = p_a_tags[:p_a_end_index]
        justification_text = ' '.join(tag.text for tag in p_a_tags)
        justification_text_lt.append(justification_text)
        p_a_img_tags = start_sibling.find_all_next(['p', 'a', 'img'])
        p_a_img_end_index = p_a_img_tags.index(end_section.find_next(['p', 'a', 'img']))
        p_a_img_tags = p_a_img_tags[:p_a_img_end_index]
        img_data_lt = []
        for img in p_a_img_tags:
            if img.name == 'img':
                src = img['src']
                parent = img.find_parent()
                caption_tag = parent.find('figcaption') or parent.find('div', class_='caption') or parent.find('span', class_='caption')
                caption = caption_tag.text if caption_tag else None
                img_data_lt.append({
                    "src": src,
                    "caption": caption
                })
        # print(f'Image data: {img_data_lt}')
        for tag in tags:
            sentence = tag.text
            a_tags = tag.find_all('a')
            hrefs = [a.get('href') for a in a_tags]
            if sentence and hrefs:
                evidence_lt.append({"sentence": sentence,
                    "hrefs": hrefs})
                all_data.append({
                    "url": url,
                    "claim": h1_text,
                    "author": author_name,
                    "posted": published_date,
                    "sci_digest": sci_digest,
                    "justification": justification_text,
                    "issues": issues_lt,
                    "image_data": img_data_lt,
                    "evidence": evidence_lt
                    
                })
        # sci_digest.clear()
        # justification_text_lt.clear()
        # evidence_lt.clear()
        # img_data_lt.clear()

# Save to a JSON file
with open('all_data.json', 'w') as f:
    json.dump(all_data, f, indent=4)
