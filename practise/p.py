from bs4 import BeautifulSoup
import datetime
import requests
import nltk

URL = 'https://www.politifact.com/factchecks/2022/jul/29/facebook-posts/theres-no-evidence-pfizer-covid-19-vaccine-connect/'
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

# def get_image_info():
#     img_src, image_caption = None, None
#     try:
#         article_element = soup.find('article', class_='m-textblock')
#         p_elements = article_element.find_all('p')
#         image_captions = []
#         for p in p_elements:
#             img_tag = p.find('img')
#             if img_tag:
#                 img_src = img_tag['src']
#                 em_tag = p.find('em')
#                 if em_tag:
#                     image_caption = em_tag.get_text(strip=True)
#                 else:
#                     image_caption = None
#                 image_captions.append({"href": img_src, "caption": image_caption})
#     except:
#         return None, None
#     return image_captions



def get_image_info():
    try:
        article_element = soup.find('article', class_='m-textblock')
        p_elements = article_element.find_all('p')
        em_elements = article_element.find_all('em')
        img_count = 0
        image_captions = []
        for p in p_elements:
            img_tag = p.find('img')
            if img_tag:
                img_src = img_tag['src']
                if img_src:
                    img_count += 1
                    if img_count <= len(em_elements):
                        image_caption = em_elements[img_count - 1].get_text(strip=True)
                        image_captions.append({"image_src": img_src, "image_caption": image_caption})
    except:
        return None
    return image_captions

print(get_image_info())

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