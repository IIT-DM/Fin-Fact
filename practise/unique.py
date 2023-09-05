# import json

# with open("finfact.json", "r") as infile:
#     scraped_data = json.load(infile)

# title_counts = {}
# for item in scraped_data:
#     title = item['title']
#     if title in title_counts:
#         title_counts[title] += 1
#     else:
#         title_counts[title] = 1

# for title, count in title_counts.items():
#     print(f"'{title}' appears {count} times")

# import json

# with open("finfact.json", "r") as infile:
#     scraped_data = json.load(infile)

# unique_data = []
# titles_seen = set()

# for item in scraped_data:
#     title = item['url']
#     if title not in titles_seen:
#         unique_data.append(item)
#         titles_seen.add(title)

# with open("finfact_new.json", "w") as outfile:
#     json.dump(unique_data, outfile, indent=4)

# print("Duplicates removed and unique data saved to 'unique_finfact.json'")



import json
with open("finfact_new.json", "r") as infile:
    scraped_data = json.load(infile)
label_counts = {}
for item in scraped_data:
    label = item['label']
    label_counts[label] = label_counts.get(label, 0) + 1
for label, count in label_counts.items():
    print(f"Label: {label}, Count: {count}")
