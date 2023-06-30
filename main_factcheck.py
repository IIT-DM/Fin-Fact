import json
import requests
from bs4 import BeautifulSoup
import json
import nltk
from datetime import datetime

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.page = None
        self.soup = None
        try:
            self.page = requests.get(self.url)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        if self.page:
            try:
                self.soup = BeautifulSoup(self.page.content, 'html.parser')
            except:
                print("Error: Failed to create BeautifulSoup object.")

    def remove_unicode(self, string):
        return string.encode('ascii', 'ignore').decode('utf-8')

    def get_page_title(self):
        page_title = None
        try:
            page_title = self.soup.title.text[:-15]
            cleaned_page_title = self.remove_unicode(page_title)
        except:
            return None # Error: Failed to get page title.
        return cleaned_page_title
    
    def get_page_author(self):
        page_author = None
        try:
            page_author = self.soup.find('p', class_='byline').text[4:]
        except:
            return None # Error: Failed to get page author.
        return page_author
    
    def get_page_posted_date(self):
        page_posted = None
        try:
            page_posted = self.soup.find('p', class_='posted-on').text[10:]
            date_object = datetime.strptime(page_posted, "%B %d, %Y")
            formatted_date = date_object.strftime("%m/%d/%Y")
        except:
            return None # Error: Failed to get page posted date.
        return formatted_date
    
    def get_sci_check_digest(self):
        sci_digest_list = []
        try:
            sci_digest = self.soup.find("h2", string="SciCheck Digest")
            if sci_digest:
                p_tags = sci_digest.find_next_siblings("p")
                for p in p_tags:
                    sci_digest_list.append(p.text)
            final_sci_digest = ", ".join(sci_digest_list)
            cleaned_sci_digest = self.remove_unicode(final_sci_digest)
            tokenised_sci_digest = nltk.sent_tokenize(cleaned_sci_digest)
        except:
            return None # Error: Failed to get SciCheck digest.
        return tokenised_sci_digest
    
    def get_paragraph_list(self):
        paragraph_list = []
        try:
            heading_tag = self.soup.find("h2", string="Full Story")
            if not heading_tag:
                heading_tag = self.soup.find("h2")
            next_heading_tag = heading_tag.find_next("h2", string="Sources")
            if not next_heading_tag:
                next_heading_tag = self.soup.find("h2")

            for sibling in heading_tag.find_next_siblings():
                if sibling.name == "h2" and sibling == next_heading_tag:
                    break
                elif sibling.name == "p":
                    paragraph_list.append(sibling)
            final_paragraphs = " ".join([p.text for p in paragraph_list])
            cleaned_paragraphs = final_paragraphs.replace('\u00a0', ' ')
            cleaned_paragraphs = self.remove_unicode(cleaned_paragraphs)
            tokenized_paragraphs = nltk.sent_tokenize(cleaned_paragraphs)
        except Exception as e:
            return None, None  # Error: Failed to get paragraphs.
        return paragraph_list, tokenized_paragraphs
    
    def get_paragraph_list_span(self):
        paragraph_list = []
        try:
            p_tags = self.soup.find_all('p', attrs={'dir': 'ltr'})
            if not p_tags:
                p_tags = self.soup.find_all('p')
            for p_tag in p_tags:
                span_tags = p_tag.find_all('span')
                if not span_tags:
                    paragraph_list.append(p_tag.get_text(strip=True))
                else:
                    paragraph_list.extend([tag.get_text(strip=True) for tag in span_tags])
            final_paragraphs = " ".join(paragraph_list)
            cleaned_paragraphs = final_paragraphs.replace('\u00a0', ' ')
            cleaned_paragraphs = self.remove_unicode(cleaned_paragraphs)
            tokenized_paragraphs = nltk.sent_tokenize(cleaned_paragraphs)
            if not tokenized_paragraphs:
                raise Exception("No tokenized paragraphs available.")
        except Exception as e:
            return None, None  # Error: Failed to get paragraphs.
        return paragraph_list, tokenized_paragraphs
    
    def get_citation_list(self, paragraph_list):
        citation_list = []
        try:
            for paragraph_tag in paragraph_list:
                link_tags = paragraph_tag.find_all("a")
                for link_tag in link_tags:
                    citation_list.append(link_tag["href"])
        except:
            return None # Error: Failed to get citation list.
        return citation_list
    
    def get_issue_list(self):
        issue_list = []
        try:
            issues_tag = self.soup.find_all("li", class_="issue")
            for issues in issues_tag:
                issue_list.append(issues.text[6:])
                new_string = ''.join(issue_list).replace('\n\n', ',')
                final_list = [word.strip() for word in new_string.split(',') if word.strip()]
        except:
            return None # Error: Failed to get issue list.
        return final_list
    
    def get_image_info(self):
        img_src, image_caption = None, None
        try:
            div_elements = self.soup.find_all("div", class_="wp-block-image")
            for div_element in div_elements:
                img_tag = div_element.find("img", loading="lazy")
                if img_tag:
                    img_src = img_tag["src"]
                    figcaption_element = div_element.find("figcaption", class_="wp-element-caption")
                    image_caption = figcaption_element.get_text(strip=True)
        except:
            return None, None
        return img_src, image_caption
    
    def get_sentences_citations(self):
        data = []
        try:
            fullstory_tag = self.soup.find("h2", string="Full Story")
            if not fullstory_tag:
                fullstory_tag = self.soup.find("h2")
            current_tag = fullstory_tag
            while True:
                current_tag = current_tag.find_next()
                if not current_tag or current_tag.name == "h2":
                    break
                if current_tag.name == "p" and current_tag.find("a", href=True):
                    p_text = current_tag.get_text().strip()
                    cleaned_paragraphs = self.remove_unicode(p_text)
                    hrefs = [a["href"] for a in current_tag.find_all("a", href=True)]
                    data.append({"sentence": cleaned_paragraphs, "hrefs": hrefs})
        except Exception as e:
            return None
        return data

    def get_sentences_citations_span(self):
        data = []
        try:
            p_tags = self.soup.find_all('p', attrs={'dir': 'ltr'})
            if not p_tags:
                p_tags = self.soup.find_all('p')

            for p_tag in p_tags:
                if p_tag.find('a', href=True):
                    p_text = p_tag.get_text().strip()
                    cleaned_paragraphs = self.remove_unicode(p_text)
                    hrefs = [a['href'] for a in p_tag.find_all('a', href=True)]
                    data.append({"sentence": cleaned_paragraphs, "hrefs": hrefs})
        except Exception as e:
            print(self.url, "No Sentence citations")
            return None
        return data

urls = [
    'https://www.factcheck.org/2023/04/scicheck-posts-exaggerate-lab-findings-about-covid-19s-impact-on-immune-system/',
'https://www.factcheck.org/2023/04/scicheck-no-evidence-excess-deaths-linked-to-vaccines-contrary-to-claims-online/',
'https://www.factcheck.org/2023/05/scicheck-posts-share-fake-chelsea-clinton-quote-about-global-childhood-vaccination-effort/',
'https://www.factcheck.org/2023/05/scicheck-covid-19-vaccine-benefits-outweigh-small-risks-contrary-to-flawed-claim-from-u-k-cardiologist/',
'https://www.factcheck.org/2023/04/warming-beyond-1-5-c-harmful-but-not-a-point-of-no-return-as-biden-claims/',
'https://www.factcheck.org/2023/04/scicheck-masking-has-minimal-effects-on-respiratory-system-does-not-cause-long-covid/'
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
