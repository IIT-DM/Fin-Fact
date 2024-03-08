# from bs4 import BeautifulSoup
# import requests

# url = "https://www.snopes.com/fact-check/ballot-pox/"
# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')
# article = soup.find('article', {'id': 'article-content'})
# img = article.find('img')

# if img is None:
#     print("No image found within the article")
# else:
#     print(img['src'])


# import json

# # Load the JSON files
# with open('snopes_new.json', 'r') as f:
#     data_a = json.load(f)

# with open('merged.json', 'r') as f:
#     data_b = json.load(f)

# # Create a dictionary from a.json for easy lookup
# dict_a = {item['url']: item['issues'] for item in data_a}

# # Iterate over the data in b.json and update the issues
# for item in data_b:
#     if item['url'] in dict_a:
#         item['issues'] = dict_a[item['url']]

# # Save the updated data to b.json
# with open('b.json', 'w') as f:
#     json.dump(data_b, f, indent=4)

# print("Issues in b.json updated based on a.json")

import json

# Load the JSON file
with open('snopes_new.json', 'r') as f:
    data = json.load(f)

# Filter out instances where "label" is an empty string
data = [item for item in data if item['label'] != ""]

# Save the updated data back to the JSON file
with open('a.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Instances where 'label' is an empty string have been removed")


# from bs4 import BeautifulSoup
# import requests
# import json
# from datetime import datetime

# with open('urls.json', 'r') as f:
#     urls = json.load(f)
# all_data = []
# for url in urls:
#     # text_label = ''
#     sci_digest = []
#     justification_text_lt = []
#     evidence_lt = []
#     issues_lt = [""]
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     title_container = soup.find('section', class_='title-container')
#     if title_container is None:
#         print("Could not find a section with the class 'title_container'.")
#     else:
#         h1_text = title_container.find('h1').text
#         h2_text = title_container.find('h2').text
#         bytes_text = h2_text.encode('ascii', 'ignore')
#         h2_text = bytes_text.decode()
#         h2_text = h2_text.replace('\u00a0', ' ')
#         h2_text = h2_text.replace('\u2019', '\'')
#         h2_text = h2_text.replace('\u2014', '')
#         h2_text = h2_text.replace('\u00a0', ' ')
#         sci_digest.append(h2_text)
#         author_name = title_container.find('a', class_='author_link').text.strip()
#         published_date = title_container.find('h3', class_='publish_date').text
#         published_date = published_date.replace('Published ', '')
#         published_date = datetime.strptime(published_date, '%b %d, %Y').strftime('%m/%d/%Y')
    
#     section_label = soup.find('section', id='fact_check_rating_container')
#     article = soup.find('article', {'id': 'article-content'})
#     if article is None:
#         print("No article with id 'article-content' found")
#     else:
#         img = article.find('img')
#         if img is None:
#             print("No image found within the article")
#         else:
#             text_label = img['src']
#     # if section_label:
#     #     div_label = section_label.find('div', class_='rating_title_wrap')
#     #     if div_label:
#     #         text_label = div_label.get_text(strip=True)
#     start_section = soup.find('section', id='fact_check_rating_container')
#     if start_section is None:
#         print("Could not find a section with the id 'fact_check_rating_container'.")
#     else:
#         start_sibling = start_section.find_next_sibling()
#         if start_sibling is None:
#             print("Could not find a sibling section after the 'fact_check_rating_container' section.")
#         else:
#             tags = start_sibling.find_all_next(['p'])
#             end_section = soup.find('section', class_='author-container')
#             if end_section is None:
#                 print("Could not find a section with the class 'author-container'.")
#             else:
#                 end_index = tags.index(end_section.find_next('p'))
#                 tags = tags[:end_index]
#                 p_a_tags = start_sibling.find_all_next(['p', 'a'])
#                 p_a_end_index = p_a_tags.index(end_section.find_next(['p', 'a']))
#                 p_a_tags = p_a_tags[:p_a_end_index]
#                 justification_text = ' '.join(tag.text for tag in p_a_tags)
#                 bytes_text = justification_text.encode('ascii', 'ignore')
#                 justification_text = bytes_text.decode()
#                 justification_text = justification_text.replace('\u00a0', ' ')
#                 justification_text = justification_text.replace('\u2019', '\'')
#                 justification_text = justification_text.replace('\u2014', '')
#                 justification_text = justification_text.replace('\u00a0', ' ')
#                 justification_text_lt.append(justification_text)
#                 p_a_img_tags = start_sibling.find_all_next(['p', 'a', 'img'])
#                 p_a_img_end_index = p_a_img_tags.index(end_section.find_next(['p', 'a', 'img']))
#                 p_a_img_tags = p_a_img_tags[:p_a_img_end_index]
#                 img_data_lt = []
#                 for img in p_a_img_tags:
#                     if img.name == 'img':
#                         src = img['src']
#                         parent = img.find_parent()
#                         caption_tag = parent.find('figcaption') or parent.find('div', class_='caption') or parent.find('span', class_='caption')
#                         caption = caption_tag.text if caption_tag else None
#                         img_data_lt.append({
#                             "image_src": src,
#                             "image_caption": caption
#                         })
#                 for tag in tags:
#                     sentence = tag.text
#                     bytes_text = sentence.encode('ascii', 'ignore')
#                     sentence = bytes_text.decode()
#                     sentence = sentence.replace('\u00a0', ' ')
#                     sentence = sentence.replace('\u2019', '\'')
#                     sentence = sentence.replace('\u2014', '')
#                     sentence = sentence.replace('\u00a0', ' ')
#                     a_tags = tag.find_all('a')
#                     hrefs = [a.get('href') for a in a_tags]
#                     if sentence and hrefs:
#                         evidence_lt.append({"sentence": sentence,
#                             "hrefs": hrefs})
#                         all_data.append({
#                             "url": url,
#                             "claim": h1_text,
#                             "author": author_name,
#                             "posted": published_date,
#                             "sci_digest": sci_digest,
#                             "justification": justification_text,
#                             "issues": issues_lt,
#                             "image_data": img_data_lt,
#                             "evidence": evidence_lt,
#                             "label": text_label
#                         })

# with open('new.json', 'w') as f:
#     json.dump(all_data, f, indent=4)

