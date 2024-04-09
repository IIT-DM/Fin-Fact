import google.generativeai as genai
import os, json
import requests
from PIL import Image

genai.configure(api_key=os.environ["API_KEY_GEMINI"])
model = genai.GenerativeModel('gemini-pro-vision')

with open('dataset.json', "r") as infile:
    data = json.load(infile)

responses = []
for item in data:
    try:
        if "image_data" in item and item["image_data"]:
            image_url = item["image_data"][0]["image_src"]
            response_image = requests.get(image_url)
            if response_image.status_code == 200:
                image_data = response_image.content
                save_path = "downloaded_image.jpg"
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                image_data = Image.open(save_path)
                prompt = f'Is it true that {item["claim"]}? True or False? Use the following format to provide your answer: Prediction: [True or False or NEI(Not Enough Information)]. Explanation: [put your evidence and reasoning here]. Confidence Level:[please show the percentage].'
                response = model.generate_content([prompt, image_data])
                os.remove(save_path)
                print(response.text)
                responses.append({
                "claim": item["claim"],
                "response": response.text
                })
                with open("gemini_responses.json", "w") as f:
                    json.dump(responses, f, indent=4)
            else:
                print(f"Failed to retrieve image from URL: {image_url}")
    except Exception as e:
        print(f"An error occurred: {e}")