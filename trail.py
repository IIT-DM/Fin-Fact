import requests
from bs4 import BeautifulSoup

# page = requests.get(
#     "https://www.factcheck.org/2023/04/scicheck-no-evidence-excess-deaths-linked-to-vaccines-contrary-to-claims-online/")
# soup = BeautifulSoup(page.content, 'html.parser')

page = requests.get('https://www.factcheck.org/2023/04/scicheck-fewer-cases-of-flu-due-to-pandemic-precautions-contrary-to-viral-claim/')
soup = BeautifulSoup(page.content, 'html.parser')

heading_tag = soup.find("h2", string="Full Story")
next_heading_tag = heading_tag.find_next("h2", string="Sources")
paragraph_tags = []
for sibling in heading_tag.find_next_siblings():
    if sibling.name == "h2" and sibling == next_heading_tag:
        break
    elif sibling.name == "p":
        paragraph_tags.append(sibling)
for paragraph_tag in paragraph_tags:
    print(paragraph_tag.text)

for paragraph_tag in paragraph_tags:
    link_tags = paragraph_tag.find_all("a")
    for link_tag in link_tags:
        print(link_tag["href"])

issue_tags = soup.find_all("li", class_="issue")
for issue_tag in issue_tags:
    print(issue_tag.text[6:])


import requests
from bs4 import BeautifulSoup
import json

page = requests.get(
    "https://www.factcheck.org/2023/04/scicheck-no-evidence-excess-deaths-linked-to-vaccines-contrary-to-claims-online/")
soup = BeautifulSoup(page.content, 'html.parser')
page_title = soup.title.text[:-15]
page_author = soup.find('p', class_='byline').text
page_posted = soup.find('p', class_='posted-on').text


page_subheading = soup.find('h2', class_='wp-block-heading')
# print(page_subheading.text)


# for headlines in soup.find_all("h2", class_='wp-block-heading'):
#     print(headlines.text)

# for i in soup.find('div', class_="'entry-content"):


# for i in soup.find_all(class_='wp-block-heading'):
#     j = i.find_all('p')
#     print(j)



# Print text
s = soup.find_all('div', class_='entry-content')
for i in s:
    if str(i).find('</h2>'):
        print(i)
        



# for i in lines

# print(s)
all_lines=[]
# for line in lines:
    # all_lines.append(line.text)
    # print(line.text)
# print(all_lines)

# Print entire text
# print(soup.get_text()) 

# Print all links
# for link in soup.find_all('a'):
    # print(link.get('href'))


# dictionary = {
# 	"title": page_title,
# 	"rollno": 56,
# 	"cgpa": 8.6,
# 	"phonenumber": "9976770500"
# }

# # Serializing json
# json_object = json.dumps(dictionary, indent=4)

# # Writing to sample.json
# with open("sample.json", "w") as outfile:
# 	outfile.write(json_object)
