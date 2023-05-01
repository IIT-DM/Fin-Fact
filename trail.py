import requests
from bs4 import BeautifulSoup

# page = requests.get(
#     "https://www.factcheck.org/2023/04/scicheck-no-evidence-excess-deaths-linked-to-vaccines-contrary-to-claims-online/")
# soup = BeautifulSoup(page.content, 'html.parser')

page = requests.get('https://www.factcheck.org/2023/04/scicheck-fewer-cases-of-flu-due-to-pandemic-precautions-contrary-to-viral-claim/')
soup = BeautifulSoup(page.content, 'html.parser')

# heading_tag = soup.find("h2", class_="wp-block-heading")
# separator_tag = soup.find("hr", class_="wp-block-separator")
# next_tag = heading_tag.find_next_sibling()
# paragraph_tag = None
# while next_tag is not None:
#     if next_tag.name == "p" and next_tag.find(separator_tag.name, separator_tag.attrs) is not None:
#         paragraph_tag = next_tag
#         break
#     next_tag = next_tag.find_next_sibling()
# if paragraph_tag is not None:
#     print(paragraph_tag.text)
# else:
#     print("Paragraph tag not found.")


# Find the heading tag
# heading_tag = soup.find("h2", text="Full Story")
# next_tag = heading_tag.find_next_sibling()
# paragraph_tag = next_tag.find_next_sibling("p")
# print(paragraph_tag.text)

# heading_tag = soup.find("h2", text="Full Story")
# for p_tag in heading_tag.find_all_next("p"):
#     print(p_tag.text)

# heading_tags = soup.find_all("h2", text="Full Story")
# for heading_tag in heading_tags:
#     paragraph_tag = heading_tag.find_next_sibling("p")
#     print(paragraph_tag.text)

# heading_tag = soup.find("h2", text="Full Story")
# paragraph_tags = heading_tag.find_next_siblings("p", until=lambda tag: tag == "h2")
# for paragraph_tag in paragraph_tags:
#     print(paragraph_tag.text)

# h2_tags = soup.find_all("h2")
# for i in range(len(h2_tags)-1):
#     if h2_tags[i].text == "Full Story":
#         heading_tag = h2_tags[i]
#         next_heading_tag = h2_tags[i+1]
#         paragraph_tags = heading_tag.find_next_siblings("p", until=lambda tag: tag == next_heading_tag)
#         for paragraph_tag in paragraph_tags:
#             print(paragraph_tag.text)


# # Find the first h2 tag with the text "Full Story"
# heading_tag = soup.find("h2", string="Full Story")
# print(heading_tag)
# # Find the next h2 tag with the text "Sources"
# next_heading_tag = heading_tag.find_next("h2", string="Sources")
# print(next_heading_tag)
# # Find all the p tags between the two h2 tags
# paragraph_tags = heading_tag.find_next_siblings("p", until=lambda tag: tag == next_heading_tag)
# print(paragraph_tags)
# # Loop through all the paragraph tags and extract the text content
# for paragraph_tag in paragraph_tags:
#     print(paragraph_tag.text)

heading_tag = soup.find("h2", string="Full Story")
next_heading_tag = heading_tag.find_next("h2", string="Sources")
paragraph_tags = []
for sibling in heading_tag.find_next_siblings():
    if sibling.name == "h2" and sibling == next_heading_tag:
        break
    elif sibling.name == "p":
        paragraph_tags.append(sibling)
# for paragraph_tag in paragraph_tags:
    # print(paragraph_tag.text)

for paragraph_tag in paragraph_tags:
    link_tags = paragraph_tag.find_all("a")
    for link_tag in link_tags:
        print(link_tag["href"])

issue_tags = soup.find_all("li", class_="issue")
for issue_tag in issue_tags:
    print(issue_tag.text[6:])
