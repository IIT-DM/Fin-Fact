import json

# Load the JSON file
with open('./scripts/jsons/b.json', 'r') as f:
    data = json.load(f)

# Initialize a dictionary to store the counts
label_counts = {}

# Iterate over the data
for item in data:
    # Get the label
    label = item['label']
    # If the label is already in the dictionary, increment its count
    if label in label_counts:
        label_counts[label] += 1
    # If the label is not in the dictionary, add it with a count of 1
    else:
        label_counts[label] = 1

# Print the counts
for label, count in label_counts.items():
    print(f'Label: {label}, Count: {count}')
