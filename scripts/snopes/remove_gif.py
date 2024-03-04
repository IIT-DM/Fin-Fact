import json

# Load the file
with open('./scripts/filtered_jsons/filtered_debt.json', 'r') as f:
    data = json.load(f)

# Remove entries where image_src ends with '.gif'
for entry in data:
    entry['image_data'] = [image for image in entry['image_data'] if 'image_src' in image and not image['image_src'].endswith('.gif')]

# Save the file
with open('merged_file.json', 'w') as f:
    json.dump(data, f, indent=4)
