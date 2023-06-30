import requests
from bs4 import BeautifulSoup
import json
import nltk

def remove_unicode(string):
    return string.encode('ascii', 'ignore').decode('utf-8')

page = requests.get('https://www.factcheck.org/2015/02/paul-repeats-baseless-vaccine-claims/')
soup = BeautifulSoup(page.content, 'html.parser')

paragraph_list = []
p_tags = soup.find_all('p')
for p_tag in p_tags:
    span_tags = p_tag.find_all('span')
    paragraph_list.extend([tag.get_text(strip=True) for tag in span_tags])

final_paragraphs = " ".join(paragraph_list)
cleaned_paragraphs = final_paragraphs.replace('\u00a0', ' ')
cleaned_paragraphs = remove_unicode(cleaned_paragraphs)
tokenized_paragraphs = nltk.sent_tokenize(cleaned_paragraphs)
print(tokenized_paragraphs)

# soup = BeautifulSoup('./html/web3.html', 'html.parser')
p_tags = soup.find_all('p')

paragraphs = [tag.get_text(strip=True) for tag in p_tags]
print(paragraphs)

'''
def merge_json_files(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    merged_data = data1 + data2  # Merge the lists
    with open(output_file, 'w') as outfile:
        json.dump(merged_data, outfile)
file1 = './json/scraped_data.json'
file2 = './json/remaining.json'
output_file = 'sfact.json'
merge_json_files(file1, file2, output_file)


# def get_paragraph_list(soup):
#     paragraph_list = []
#     try:
#         p_tags = soup.find_all('p', attrs={'dir': 'ltr'})
#         if not p_tags:
#             p_tags = soup.find_all('p')

#         for p_tag in p_tags:
#             span_tags = p_tag.find_all('span')
#             if not span_tags:
#                 paragraph_list.append(p_tag.get_text(strip=True))
#             else:
#                 paragraph_list.extend([tag.get_text(strip=True) for tag in span_tags])

#         final_paragraphs = " ".join(paragraph_list)
#         cleaned_paragraphs = final_paragraphs.replace('\u00a0', ' ')
#         cleaned_paragraphs = remove_unicode(cleaned_paragraphs)
#         tokenized_paragraphs = nltk.sent_tokenize(cleaned_paragraphs)

#         if not tokenized_paragraphs:
#             raise Exception("No tokenized paragraphs available.")

#     except Exception as e:
#         print("Error:", str(e))
#         print("No paragraph-list")
#         return None, None  # Error: Failed to get paragraphs.

#     return paragraph_list, tokenized_paragraphs

# paragraph_list, tokenized_paragraphs = get_paragraph_list(soup)
# print(tokenized_paragraphs)

base_url = "https://www.factcheck.org/scicheck/page/"
num_pages = 51  
href_list = []
for page_num in range(1, num_pages + 1):
    url = f"{base_url}{page_num}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article_elements = soup.find_all("article")

    for article_element in article_elements:
        a_tag = article_element.find("a")
        if a_tag:
            href = a_tag["href"]
            href_list.append(href)

print(href_list)
with open("all_links.json", "w") as file:
    json.dump(href_list, file)

page = requests.get('https://www.factcheck.org/scicheck/')
soup = BeautifulSoup(page.content, 'html.parser')

article_elements = soup.find_all("article")

href_list = []

for article_element in article_elements:
    a_tag = article_element.find("a")
    if a_tag:
        href = a_tag["href"]
        href_list.append(href)

print(href_list)

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
# for p_text in sci_digest_list:
#     print(p_text,"\n")

paragraph_list = []
for sibling in heading_tag.find_next_siblings():
    if sibling.name == "h2" and sibling == next_heading_tag:
        break
    elif sibling.name == "p":
        paragraph_list.append(sibling)
# for paragraph_tag in paragraph_list:
#     print(paragraph_tag.text)

sentences_with_citations=[]
citation_list = []
for paragraph_tag in paragraph_list:
    link_tags = paragraph_tag.find_all("a")
    for link_tag in link_tags:
        citation_list.append(link_tag["href"])
        if link_tag.has_attr("href") and link_tag["href"].startswith("http"):
            link_text = link_tag.get_text().strip()
            escaped_text = re.escape(link_text)
        for sentence in re.findall(f"[^.]*?{escaped_text}[^.]*\.", soup.get_text()):
            sentences_with_citations.append(sentence)

# for citations in citation_list:
#     print(citations)

print(len(sentences_with_citations))
print(len(citation_list))
issue_list = []
for issues in issues_tag:
    issue_list.append(issues.text[6:])
# for iss in issue_list:
#     print(iss)

image_div = soup.find("div", class_="wp-block-image")
image_caption = soup.find("figcaption", class_="wp-element-caption").text

img_tag = image_div.find("img")
img_src = img_tag['src']
print(img_src)
print(image_caption)

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
'''


'''
from bs4 import BeautifulSoup
import datetime
import requests
import nltk

URL = 'https://www.politifact.com/factchecks/2023/jun/20/steve-milloy/particulate-matter-is-not-junk-science-decades-of/'
webpage = requests.get(URL)
soup = BeautifulSoup(webpage.text, "html.parser")

def remove_unicode(string):
    return string.encode('ascii', 'ignore').decode('utf-8')

def get_page_title():
    div_element = soup.find('div', class_='m-statement__quote')
    title = div_element.get_text(strip=True)
    return title

def get_page_author():
    author_element = soup.find('div', class_='m-author__content').find('a')
    author = author_element.get_text(strip=True)
    return author

def get_page_posted_date():
    date_element = soup.find('span', class_='m-author__date')
    date = date_element.get_text(strip=True)
    date_obj = datetime.datetime.strptime(date, "%B %d, %Y")
    formatted_date = date_obj.strftime("%m/%d/%Y")
    return formatted_date

def get_sci_check_digest():
    div_element = soup.find('div', class_='short-on-time')
    li_tags = div_element.find_all('li') if div_element else []
    sci_digest_list = [li.get_text(strip=True) for li in li_tags]
    final_sci_digest = ", ".join(sci_digest_list)
    cleaned_sci_digest = remove_unicode(final_sci_digest)
    tokenised_sci_digest = nltk.sent_tokenize(cleaned_sci_digest)
    return tokenised_sci_digest

def get_paragraph_list():
    paragraph_list = []
    article_element = soup.find('article', class_='m-textblock')
    p_elements = article_element.find_all('p')
    text_list = [p.get_text(strip=True) for p in p_elements]
    for text in text_list:
        paragraph_list.append(text)
    final_paragraphs = " ".join(paragraph_list)
    cleaned_paragraphs = final_paragraphs.replace('\u00a0', ' ')
    tokenized_paragraphs = nltk.sent_tokenize(cleaned_paragraphs)
    return tokenized_paragraphs

def get_sentences_citations():
    p_elements = soup.select('article.m-textblock p')
    data = []
    for p in p_elements:
        href = p.find('a')
        if href:
            href_text = href['href']
            sentence = p.get_text(strip=True)
            data.append({"sentence": sentence, "hrefs": href_text})
    return data

def get_issue_list():
    issue_list = []
    ul_element = soup.find('ul', class_='m-list--horizontal')
    li_elements = ul_element.find_all('li', class_='m-list__item')
    for li in li_elements[:-1]:
        category = li.a['title']
        issue_list.append(category)
    return issue_list

# urls = [
#     'https://www.factcheck.org/2023/04/scicheck-posts-exaggerate-lab-findings-about-covid-19s-impact-on-immune-system/',
# 'https://www.factcheck.org/2023/04/scicheck-no-evidence-excess-deaths-linked-to-vaccines-contrary-to-claims-online/',
# 'https://www.factcheck.org/2023/05/scicheck-posts-share-fake-chelsea-clinton-quote-about-global-childhood-vaccination-effort/',
# 'https://www.factcheck.org/2023/05/scicheck-covid-19-vaccine-benefits-outweigh-small-risks-contrary-to-flawed-claim-from-u-k-cardiologist/',
# 'https://www.factcheck.org/2023/04/warming-beyond-1-5-c-harmful-but-not-a-point-of-no-return-as-biden-claims/',
# 'https://www.factcheck.org/2023/04/scicheck-masking-has-minimal-effects-on-respiratory-system-does-not-cause-long-covid/'
# ]

# scraped_data = []
# for url in urls:
#     scraper = WebScraper(url)
#     data = {
#         "url": url,
#         "title": scraper.get_page_title(),
#         "author": scraper.get_page_author(),
#         "posted": scraper.get_page_posted_date(),
#         "sci_digest": scraper.get_sci_check_digest(),
#         "paragraphs": scraper.get_paragraph_list()[1],
#         "issues": scraper.get_issue_list(),
#         "image_data": [{"image_src": scraper.get_image_info()[0], "image_caption": scraper.get_image_info()[1]}],
#         "data": scraper.get_sentences_citations()
#     }
#     scraped_data.append(data)

# with open("scraped_data.json", "w") as outfile:
#     json.dump(scraped_data, outfile)
'''