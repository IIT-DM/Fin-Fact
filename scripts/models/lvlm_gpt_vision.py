from openai import OpenAI
import json
import time 
import os 

client = OpenAI(api_key=os.environ["API_KEY_OPENAI"])

with open('dataset.json', "r") as infile:
    data = json.load(infile)

responses = []
for item in data:
    try:
        if "image_data" in item and item["image_data"]:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f'Is it true that {item["claim"]}? True or False? Use the following format to provide your answer: Prediction: [True or False or NEI(Not Enough Information)]. Explanation: [put your evidence and reasoning here]. Confidence Level:[please show the percentage].'
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": item["image_data"][0]["image_src"]
                            },
                        }
                    ],
                }
            ]
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
                max_tokens=500,
            )

            print(response.choices[0].message.content)
            responses.append({
                "claim": item["claim"],
                "response": response.choices[0].message.content
            })
            with open("responses2.json", "w") as f:
                json.dump(responses, f)

            time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")

print("Responses saved in responses.json")
