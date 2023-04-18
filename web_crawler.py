import requests
from bs4 import BeautifulSoup

page = requests.get(
    "https://www.factcheck.org/2023/04/scicheck-fewer-cases-of-flu-due-to-pandemic-precautions-contrary-to-viral-claim/")
soup = BeautifulSoup(page.content, 'html.parser')
page_title = soup.title.text
print(page_title)
images_list = []
 
# Print images links 
images = soup.select('img')
for image in images:
    src = image.get('src')
    alt = image.get('alt')
    images_list.append({"src": src, "alt": alt})
for image in images_list:
    print(image)

# Print text
s = soup.find('div', class_='entry-content')
lines = s.find_all('p')
for line in lines:
    print(line.text)

# Print entire text
# print(soup.get_text()) 

# Print all links
for link in soup.find_all('a'):
    print(link.get('href'))








