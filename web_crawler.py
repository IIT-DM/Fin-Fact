import requests
from bs4 import BeautifulSoup
import json

page = requests.get(
    "https://www.factcheck.org/2023/04/scicheck-fewer-cases-of-flu-due-to-pandemic-precautions-contrary-to-viral-claim/")
soup = BeautifulSoup(page.content, 'html.parser')
page_title = soup.title.text[:-15]
page_author = soup.find('p', class_='byline').text
page_posted = soup.find('p', class_='posted-on').text


page_subheading = soup.find('p', class_='wp-block-heading')
print(page_subheading)


# for headlines in soup.find_all("h2"):
#     print(headlines.contents[0])

# for i in soup.find_all(class_='wp-block-heading'):
#     j = i.find_all('p')
#     print(j)



# Print text
# s = soup.find('div', class_='entry-content')
# lines = s.find_all('p')
# print(lines)
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







