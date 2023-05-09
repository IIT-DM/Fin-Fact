import json
import requests
from bs4 import BeautifulSoup
import json
import re

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
        except:
            return 0 # Error: Failed to get page title.
        return page_title
    
    def get_page_author(self):
        page_author = None
        try:
            page_author = self.soup.find('p', class_='byline').text[4:]
        except:
            return 0 # Error: Failed to get page author.
        return page_author
    
    def get_page_posted_date(self):
        page_posted = None
        try:
            page_posted = self.soup.find('p', class_='posted-on').text
        except:
            return 0 # Error: Failed to get page posted date.
        return page_posted
    
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
        except:
            return 0 # Error: Failed to get SciCheck digest.
        return cleaned_sci_digest
    
    def get_paragraph_list(self):
        paragraph_list = []
        try:
            heading_tag = self.soup.find("h2", string="Full Story")
            next_heading_tag = heading_tag.find_next("h2", string="Sources")
            for sibling in heading_tag.find_next_siblings():
                if sibling.name == "h2" and sibling == next_heading_tag:
                    break
                elif sibling.name == "p":
                    paragraph_list.append(sibling)
            final_paragraphs = " ".join([p.text for p in paragraph_list])
            myString = final_paragraphs.replace('\u00a0', ' ')
            # myString = re.sub('[\r\n\t\f\v]+', ' ', myString)
            # cleaned_paragraphs = " ".join(final_paragraphs.split())
            cleaned_paragraphs = self.remove_unicode(myString)
        except:
            return 0, 0 # Error: Failed to get paragraphs.
        return paragraph_list, cleaned_paragraphs
    
    def get_citation_list(self, paragraph_list):
        citation_list = []
        try:
            for paragraph_tag in paragraph_list:
                link_tags = paragraph_tag.find_all("a")
                for link_tag in link_tags:
                    citation_list.append(link_tag["href"])
        except:
            return 0 # Error: Failed to get citation list.
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
            return 0 # Error: Failed to get issue list.
        return final_list
    
    def get_image_info(self):
        img_src, image_caption = None, None
        try:
            image_div = self.soup.find("div", class_="wp-block-image")
            img_tag = image_div.find("img")
            img_src = img_tag['src']
            image_caption = self.soup.find("figcaption", class_="wp-element-caption").text
        except:
            return 0, 0 # Error: Failed to get image info.
        return img_src, image_caption

url = 'https://www.factcheck.org/2023/04/scicheck-posts-exaggerate-lab-findings-about-covid-19s-impact-on-immune-system/'
# url = 'https://www.factcheck.org/2023/04/scicheck-no-evidence-excess-deaths-linked-to-vaccines-contrary-to-claims-online/'
scraper = WebScraper(url)
data = {
    "title": scraper.get_page_title(),
    "author": scraper.get_page_author(),
    "posted": scraper.get_page_posted_date(),
    "sci_digest": scraper.get_sci_check_digest(),
    "paragraphs": scraper.get_paragraph_list()[1],
    # "citations": scraper.get_citation_list(scraper.get_paragraph_list()[0]),
    "evidence": [{"e{}".format(i+1): value} for i, value in enumerate(scraper.get_citation_list(scraper.get_paragraph_list()[0]))],
    "issues": scraper.get_issue_list(),
    "image_src": scraper.get_image_info()[0],
    "image_caption": scraper.get_image_info()[1]
}

# Convert the dictionary to JSON and write it to a file
with open("try.json", "w") as outfile:
    json.dump(data, outfile)