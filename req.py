import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
# Make a request to https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/
# Store the result in 'res' variable
res = requests.get(
    'https://codedamn-classrooms.github.io/webscraper-python-codedamn-classroom-website/')
soul = res.text
soul = BeautifulSoup(res, "html.parser")
status = res.status_code

print(soul.get_text())