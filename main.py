import requests
from bs4 import BeautifulSoup
import json

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
    
    def get_page_title(self):
        page_title = None
        try:
            page_title = self.soup.title.text[:-15]
        except:
            print("Error: Failed to get page title.")
        return page_title
    
    def get_page_author(self):
        page_author = None
        try:
            page_author = self.soup.find('p', class_='byline').text[4:]
        except:
            print("Error: Failed to get page author.")
        return page_author
    
    def get_page_posted_date(self):
        page_posted = None
        try:
            page_posted = self.soup.find('p', class_='posted-on').text
        except:
            print("Error: Failed to get page posted date.")
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
        except:
            print("Error: Failed to get SciCheck digest.")
        return final_sci_digest
    
    def get_paragraph_list(self):
        paragraph_list = []
        try:
            heading_tag = self.soup.find("h2", string="Full Story")
            next_heading_tag = heading_tag.find_next("h2", string="Sources")
            for sibling in heading_tag.find_next_siblings():
                if sibling.name == "h2" and sibling == next_heading_tag:
                    break
                elif sibling.name == "p":
                    paragraph_list.append(sibling.text)
            final_paragraph = ", ".join(paragraph_list)
        except:
            print("Error: Failed to get paragraphs.")
        return paragraph_list, final_paragraph
    
    def get_citation_list(self, paragraph_list):
        citation_list = []
        try:
            for paragraph_tag in paragraph_list:
                link_tags = paragraph_tag.find_all("a")
                for link_tag in link_tags:
                    citation_list.append(link_tag["href"])
        except:
            print("Error: Failed to get citation list.")
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
            print("Error: Failed to get issue list.")
        return final_list
    
    def get_image_info(self):
        img_src, image_caption = None, None
        try:
            image_div = self.soup.find("div", class_="wp-block-image")
            img_tag = image_div.find("img")
            img_src = img_tag['src']
            image_caption = self.soup.find("figcaption", class_="wp-element-caption").text
        except:
            print("Error: Failed to get image info.")
        return img_src, image_caption


url = 'https://www.factcheck.org/2023/04/scicheck-posts-exaggerate-lab-findings-about-covid-19s-impact-on-immune-system/'
scraper = WebScraper(url)
# print(scraper.get_page_title())
# print(scraper.get_page_author())
# print(scraper.get_page_posted_date())
# print(scraper.get_sci_check_digest())
paragraph_list = scraper.get_paragraph_list()[0]
print(paragraph_list)
for paragraph_tag in paragraph_list:
    print(paragraph_tag)
citation_list = scraper.get_citation_list(paragraph_list)
print(citation_list)
# for citation in citation_list:
#     print(citation)
# print(scraper.get_issue_list())
# print(scraper.get_image_info()[1])

# data = {
#     "title": scraper.get_page_title(),
#     "author": scraper.get_page_author(),
#     "posted": scraper.get_page_posted_date(),
#     "sci_digest": scraper.get_sci_check_digest(),
#     "paragraphs": scraper.get_paragraph_list()[1],
#     "citations": citation_list,
#     "issues": scraper.get_issue_list(),
#     "image_src": scraper.get_image_info()[0],
#     "image_caption": scraper.get_image_info()[1]
# }

# with open("scraped_data.json", "w") as outfile:
#     json.dump(data, outfile)