import requests
import json
from bs4 import BeautifulSoup

page = requests.get('https://www.factcheck.org/2023/04/scicheck-posts-exaggerate-lab-findings-about-covid-19s-impact-on-immune-system/')
soup = BeautifulSoup(page.content, 'html.parser')

fullstory_tag = soup.find("h2", string="Full Story")
source_tag = fullstory_tag.find_next("h2", string="Sources")

data = []
current_tag = fullstory_tag
while True:
    current_tag = current_tag.find_next()
    if current_tag == source_tag:
        break
    if current_tag.name == "p" and current_tag.find("a", href=True):
        p_text = current_tag.get_text().strip()
        hrefs = [a["href"] for a in current_tag.find_all("a", href=True)]
        data.append({"p_text": p_text, "hrefs": hrefs})

with open("output.json", "w") as f:
    json.dump(data, f)

'''
import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.factcheck.org/2023/04/scicheck-posts-exaggerate-lab-findings-about-covid-19s-impact-on-immune-system/')
soup = BeautifulSoup(page.content, 'html.parser')

fullstory_tag = soup.find("h2", string="Full Story")
source_tag = fullstory_tag.find_next("h2", string="Sources")

current_tag = fullstory_tag
while True:
    current_tag = current_tag.find_next()
    if current_tag == source_tag:
        break
    if current_tag.name == "a":
        print(current_tag.text)
        # print()
    # elif current_tag.name == "p":
    #     sentences = current_tag.text.split(". ")
    #     for sentence in sentences:
    #         if "http" in sentence:
    #             print(sentence.strip())
    #             print(current_tag.find("a").get("href"))
    #             print()
    #         else:
    #             print(sentence.strip())
    #             print()


current_tag = fullstory_tag
while True:
    current_tag = current_tag.find_next()
    if current_tag == source_tag:
        break
    if current_tag.name == "p":
        print(current_tag.text)

import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.factcheck.org/2023/04/scicheck-posts-exaggerate-lab-findings-about-covid-19s-impact-on-immune-system/')
soup = BeautifulSoup(page.content, 'html.parser')

fullstory_tag = soup.find("h2", string="Full Story")
source_tag = fullstory_tag.find_next("h2", string="Sources")
sentence_list = []
current_tag = fullstory_tag
while True:
    current_tag = current_tag.find_next()
    if current_tag == source_tag:
        break
    if current_tag.name == "p" and current_tag.find("a", href=True):
        print(current_tag.text)

import requests
import json
from bs4 import BeautifulSoup

page = requests.get('https://www.factcheck.org/2023/04/scicheck-posts-exaggerate-lab-findings-about-covid-19s-impact-on-immune-system/')
soup = BeautifulSoup(page.content, 'html.parser')

fullstory_tag = soup.find("h2", string="Full Story")
source_tag = fullstory_tag.find_next("h2", string="Sources")

data = []
current_tag = fullstory_tag
while True:
    current_tag = current_tag.find_next()
    if current_tag == source_tag:
        break
    if current_tag.name == "p" and current_tag.find("a", href=True):
        p_text = current_tag.get_text().strip()
        href = current_tag.find("a", href=True)["href"]
        data.append({"p_text": p_text, "href": href})

with open("output.json", "w") as f:
    json.dump(data, f)
'''