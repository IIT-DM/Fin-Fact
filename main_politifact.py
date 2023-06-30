from bs4 import BeautifulSoup
import datetime
import requests
import nltk
import json

class WebScraper:
    def __init__(self, url):
        self.URL = url
        try: 
            self.webpage = requests.get(self.URL)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        if self.webpage:
            try:
                self.soup = BeautifulSoup(self.webpage.text, "html.parser")
            except:
                print("Error: Failed to create BeautifulSoup object.")
    
    def remove_unicode(self, string):
        return string.encode('ascii', 'ignore').decode('utf-8')
    
    def get_page_title(self):
        try:
            div_element = self.soup.find('div', class_='m-statement__quote')
            title = div_element.get_text(strip=True)
            cleaned_title = self.remove_unicode(title)
        except AttributeError:
            return None # Error: Failed to get page title.
        return cleaned_title
    
    def get_page_author(self):
        try:
            author_element = self.soup.find('div', class_='m-author__content').find('a')
            author = author_element.get_text(strip=True)
        except AttributeError:
            return None # Error: Failed to get page author.
        return author
    
    def get_page_posted_date(self):
        date_element = None
        try:
            date_element = self.soup.find('span', class_='m-author__date')
            date = date_element.get_text(strip=True)
            date_obj = datetime.datetime.strptime(date, "%B %d, %Y")
            formatted_date = date_obj.strftime("%m/%d/%Y")
        except (AttributeError, ValueError):
            return None # Error: Failed to get page posted date.
        return formatted_date
    
    def get_sci_check_digest(self):
        try:
            div_element = self.soup.find('div', class_='short-on-time')
            li_tags = div_element.find_all('li') if div_element else []
            sci_digest_list = [li.get_text(strip=True) for li in li_tags]
            final_sci_digest = ", ".join(sci_digest_list)
            cleaned_sci_digest = self.remove_unicode(final_sci_digest)
            tokenised_sci_digest = nltk.sent_tokenize(cleaned_sci_digest)
        except AttributeError:
            return None # Error: Failed to get SciCheck digest.
        return tokenised_sci_digest
    
    def get_paragraph_list(self):
        try:
            paragraph_list = []
            article_element = self.soup.find('article', class_='m-textblock')
            p_elements = article_element.find_all('p')
            text_list = [p.get_text(strip=True) for p in p_elements]
            for text in text_list:
                paragraph_list.append(text)
            final_paragraphs = " ".join(paragraph_list)
            cleaned_paragraphs = final_paragraphs.replace('\u00a0', ' ')
            cleaned_paragraphs = self.remove_unicode(cleaned_paragraphs)
            tokenized_paragraphs = nltk.sent_tokenize(cleaned_paragraphs)
        except AttributeError:
            return None, None # Error: Failed to get paragraphs.
        return paragraph_list, tokenized_paragraphs
    
    def get_sentences_citations(self):
        try:
            p_elements = self.soup.select('article.m-textblock p')
            citation_list = []
            for p in p_elements:
                href = p.find('a')
                if href:
                    href_text = href['href']
                    sentence = p.get_text(strip=True)
                    citation_list.append({"sentence": sentence, "hrefs": href_text})
        except AttributeError:
            return None # Error: Failed to get citation list.
        return citation_list
    
    def get_issue_list(self):
        issue_list = []
        try:
            ul_element = self.soup.find('ul', class_='m-list--horizontal')
            li_elements = ul_element.find_all('li', class_='m-list__item')
            for li in li_elements[:-1]:
                category = li.a['title']
                issue_list.append(category)
        except AttributeError:
            return None # Error: Failed to get issue list.
        return issue_list
    
    def get_image_info(self):
        # img_src, image_caption = None, None
        try:
            div_element = self.soup.find('div', class_='c-image')
            img_element = div_element.find('img')
            img_src = img_element['data-src']
            caption_element = self.soup.find('div', class_='c-image__caption')
            image_caption = caption_element.text.strip()
        except:
            return None, None
        return img_src, image_caption


# # Example usage:
# fact_checker = WebScraper('https://www.politifact.com/factchecks/2023/jun/20/steve-milloy/particulate-matter-is-not-junk-science-decades-of/')
# title = fact_checker.get_page_title()
# author = fact_checker.get_page_author()
# date = fact_checker.get_page_posted_date()
# sci_digest = fact_checker.get_sci_check_digest()
# paragraphs = fact_checker.get_paragraph_list()[1]
# sentences_citations = fact_checker.get_sentences_citations()
# issue_list = fact_checker.get_issue_list()

urls = [
    'https://www.politifact.com/factchecks/2023/jun/20/steve-milloy/particulate-matter-is-not-junk-science-decades-of/'
# 'https://www.factcheck.org/2023/04/scicheck-no-evidence-excess-deaths-linked-to-vaccines-contrary-to-claims-online/',
# 'https://www.factcheck.org/2023/05/scicheck-posts-share-fake-chelsea-clinton-quote-about-global-childhood-vaccination-effort/',
# 'https://www.factcheck.org/2023/05/scicheck-covid-19-vaccine-benefits-outweigh-small-risks-contrary-to-flawed-claim-from-u-k-cardiologist/',
# 'https://www.factcheck.org/2023/04/warming-beyond-1-5-c-harmful-but-not-a-point-of-no-return-as-biden-claims/',
# 'https://www.factcheck.org/2023/04/scicheck-masking-has-minimal-effects-on-respiratory-system-does-not-cause-long-covid/'
]

scraped_data = []
for url in urls:
    scraper = WebScraper(url)
    data = {
        "url": url,
        "title": scraper.get_page_title(),
        "author": scraper.get_page_author(),
        "posted": scraper.get_page_posted_date(),
        "sci_digest": scraper.get_sci_check_digest(),
        "paragraphs": scraper.get_paragraph_list()[1],
        "issues": scraper.get_issue_list(),
        "image_data": [{"image_src": scraper.get_image_info()[0], "image_caption": scraper.get_image_info()[1]}],
        "data": scraper.get_sentences_citations()
    }
    scraped_data.append(data)

with open("scraped_data.json", "w") as outfile:
    json.dump(scraped_data, outfile)

