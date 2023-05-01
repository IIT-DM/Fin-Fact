import requests
from bs4 import BeautifulSoup

class WebScraper:
    
    def __init__(self, url):
        self.url = url
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
    
    def get_page_title(self):
        page_title = self.soup.title.text[:-15]
        return page_title
    
    def get_page_author(self):
        page_author = self.soup.find('p', class_='byline').text
        return page_author
    
    def get_page_posted_date(self):
        page_posted = self.soup.find('p', class_='posted-on').text
        return page_posted
    
    def get_sci_check_digest(self):
        sci_digest = self.soup.find("h2", string="SciCheck Digest")
        sci_digest_list = []
        p_tags = sci_digest.find_next_siblings("p")
        for p in p_tags:
            sci_digest_list.append(p.text)
        return sci_digest_list
    
    def get_paragraph_list(self):
        heading_tag = self.soup.find("h2", string="Full Story")
        next_heading_tag = heading_tag.find_next("h2", string="Sources")
        paragraph_list = []
        for sibling in heading_tag.find_next_siblings():
            if sibling.name == "h2" and sibling == next_heading_tag:
                break
            elif sibling.name == "p":
                paragraph_list.append(sibling)
        return paragraph_list
    
    def get_citation_list(self, paragraph_list):
        citation_list = []
        for paragraph_tag in paragraph_list:
            link_tags = paragraph_tag.find_all("a")
            for link_tag in link_tags:
                citation_list.append(link_tag["href"])
        return citation_list
    
    def get_issue_list(self):
        issues_tag = self.soup.find_all("li", class_="issue")
        issue_list = []
        for issues in issues_tag:
            issue_list.append(issues.text[6:])
        return issue_list
    
    def get_image_info(self):
        image_div = self.soup.find("div", class_="wp-block-image")
        image_caption = self.soup.find("figcaption", class_="wp-element-caption").text
        img_tag = image_div.find("img")
        img_src = img_tag['src']
        return img_src, image_caption

url = 'https://www.factcheck.org/2023/04/scicheck-posts-exaggerate-lab-findings-about-covid-19s-impact-on-immune-system/'
scraper = WebScraper(url)
print(scraper.get_page_title())
print(scraper.get_page_author())
print(scraper.get_page_posted_date())
print(scraper.get_sci_check_digest())
paragraph_list = scraper.get_paragraph_list()
for paragraph_tag in paragraph_list:
    print(paragraph_tag.text)
citation_list = scraper.get_citation_list(paragraph_list)
for citation in citation_list:
    print(citation)
print(scraper.get_issue_list())
print(scraper.get_image_info())

