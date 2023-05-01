import requests
from bs4 import BeautifulSoup

# page = requests.get("https://www.factcheck.org/2023/04/scicheck-no-evidence-excess-deaths-linked-to-vaccines-contrary-to-claims-online/")
# soup = BeautifulSoup(page.content, 'html.parser')

page = requests.get('https://www.factcheck.org/2023/04/scicheck-posts-exaggerate-lab-findings-about-covid-19s-impact-on-immune-system/')
soup = BeautifulSoup(page.content, 'html.parser')

page_title = soup.title.text[:-15]
page_author = soup.find('p', class_='byline').text
page_posted = soup.find('p', class_='posted-on').text

sci_digest = soup.find("h2", string="SciCheck Digest")
heading_tag = soup.find("h2", string="Full Story")
next_heading_tag = heading_tag.find_next("h2", string="Sources")
issues_tag = soup.find_all("li", class_="issue")

sci_digest_list = []
p_tags = sci_digest.find_next_siblings("p")
for p in p_tags:
    sci_digest_list.append(p.text)
for p_text in sci_digest_list:
    print(p_text)

paragraph_list = []
for sibling in heading_tag.find_next_siblings():
    if sibling.name == "h2" and sibling == next_heading_tag:
        break
    elif sibling.name == "p":
        paragraph_list.append(sibling)
for paragraph_tag in paragraph_list:
    print(paragraph_tag.text)

citation_list = []
for paragraph_tag in paragraph_list:
    link_tags = paragraph_tag.find_all("a")
    for link_tag in link_tags:
        citation_list.append(link_tag["href"])
for citations in citation_list:
    print(citations)

issue_list = []
for issues in issues_tag:
    issue_list.append(issues.text[6:])
for iss in issue_list:
    print(iss)

image_div = soup.find("div", class_="wp-block-image")
image_caption = soup.find("figcaption", class_="wp-element-caption").text

img_tag = image_div.find("img")
img_src = img_tag['src']
print(img_src)
print(image_caption)

