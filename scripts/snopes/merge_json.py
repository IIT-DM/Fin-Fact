import json

# Load first file
with open('./scripts/filtered_jsons/filtered_income.json', 'r') as f:
    data1 = json.load(f)

# Load second file
with open('./scripts/filtered_jsons/filtered_taxes.json', 'r') as f:
    data2 = json.load(f)

with open('./scripts/filtered_jsons/filtered_stockmarket.json', 'r') as f:
    data3 = json.load(f)

# Merge files
# merged_data = {**data1, **data2, **data3}
merged_data = data1+data2+data3

# Save merged file
with open('merged_file.json', 'w') as f:
    json.dump(merged_data, f, indent=4)
