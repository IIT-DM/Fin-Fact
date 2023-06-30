from bs4 import BeautifulSoup
import requests

html = '''
<div class="artembed">
    <a id="see-figure-1-on-politifactcom"></a>
    <div class="infogram-embed" data-id="77c4e508-eabc-4ba1-972e-f7a4babfec2a" data-src="https://e.infogram.com/api/live/flex/77c4e508-eabc-4ba1-972e-f7a4babfec2a/default"></div>
    <script>!function(e,i,n,s){var t="InfogramEmbeds",d=e.getElementsByTagName("script")[0];if(window[t]&&window[t].initialized)window[t].process&&window[t].process();else if(!e.getElementById(n)){var o=e.createElement("script");o.async=1,o.id=n,o.src="https://e.infogram.com/js/dist/embed-loader-min.js",d.parentNode.insertBefore(o,d)}}(document,0,"infogram-async");</script>
</div>
'''

soup = BeautifulSoup(html, 'html.parser')

div_artembed = soup.find('div', class_='artembed')
div_infogram_embed = div_artembed.find('div', class_='infogram-embed')
image_url = div_infogram_embed['data-src']

# Download the image
image_data = requests.get(image_url).content

# Save the image to a file
with open('image.png', 'wb') as file:
    file.write(image_data)
