import google.generativeai as genai
import os, json

genai.configure(api_key=os.environ["API_KEY_GEMINI"])
model = genai.GenerativeModel('gemini-pro')

with open('finfact.json', "r") as infile:
    data = json.load(infile)

responses = []
for item in data:
    try:
        prompt = f'Is it true that {item["claim"]}? True or False or NEI? Use the following format to provide your answer: Prediction: [True or False or NEI(Not Enough Information)].'
        response = model.generate_content(prompt)
        print(response.parts[0].text)
        responses.append({
        "claim": item["claim"],
        "response": response.parts[0].text
        })
        with open("gemini_responses_without_image11.json", "w") as f:
            json.dump(responses, f, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")

