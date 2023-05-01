import requests
from bs4 import BeautifulSoup
import json

page = requests.get(
    "https://www.factcheck.org/2023/04/scicheck-no-evidence-excess-deaths-linked-to-vaccines-contrary-to-claims-online/")
soup = BeautifulSoup(page.content, 'html.parser')
page_title = soup.title.text[:-15]
page_author = soup.find('p', class_='byline').text
page_posted = soup.find('p', class_='posted-on').text

fullstory_tag = soup.find("h2", string="Full Story")
sources_tag = fullstory_tag.find_next("h2", string="Sources")
issues_tag = soup.find_all("li", class_="issue")

paragraph_list = []
citation_list = []
issue_list = []

for sibling in fullstory_tag.find_next_siblings():
    if sibling.name == "h2" and sibling == sources_tag:
        break
    elif sibling.name == "p":
        paragraph_list.append(sibling)
for p_text in paragraph_list:
    print(p_text.text)

for paragraph_tag in paragraph_list:
    link_tags = paragraph_tag.find_all("a")
    for links in link_tags:
        citation_list.append(links["href"])
for citations in citation_list:
    print(citations)

for issues in issues_tag:
    issue_list.append(issues.text[6:])
for iss in issue_list:
    print(iss)



