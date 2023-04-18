from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://www.politifact.com/factchecks/2023/apr/17/instagram-posts/yall-be-running-with-fake-news-lizzo-did-not-kill/"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
print(soup.get_text())