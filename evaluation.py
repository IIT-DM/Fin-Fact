import json

with open("finfact.json", "r") as infile:
    data = json.load(infile)

titles = [entry["title"] for entry in data]
sentences = [item["sentence"] for entry in data for item in entry["data"]]
labels = [entry["label"] for entry in data]

print("Title:", titles)
print("Sentences:", sentences)
print("Labels:", labels)

