import json

# Load your data
with open('./share.json', 'r') as f:
    data = json.load(f)

# Filter out instances where "image_data" is null
filtered_data = [item for item in data if item['image_data']]

# Filter out instances where "image_data" is null or "stock market" is not in "justification"
filtered_data = [item for item in filtered_data if 'share' in item['justification']]

# Filter out instances where "image_data" is null, "stock market" is not in "justification", and remove duplicates in "claim"
final_data = []
seen_claims = set()
for item in filtered_data:
    if item['claim'] not in seen_claims:
        final_data.append(item)
        seen_claims.add(item['claim'])

# Save the filtered data
with open('./scripts/filtered_jsons/filtered_share.json', 'w') as f:
    json.dump(final_data, f, indent=4)



# import json

# # Load your data
# with open('./stockmarket.json', 'r') as f:
#     data = json.load(f)

# # Filter out instances where "image_data" is null
# filtered_data = [item for item in data if item['image_data']]

# # Save the filtered data
# with open('filtered_stockmarket.json', 'w') as f:
#     json.dump(filtered_data, f, indent=4)

# import json

# # Load your data
# with open('./filtered_stockmarket.json', 'r') as f:
#     data = json.load(f)

# # Filter out instances where "image_data" is null or "stock market" is not in "justification"
# filtered_data = [item for item in data if item['image_data'] and 'stock market' in item['justification']]

# # Save the filtered data
# with open('filtered_stockmarket.json', 'w') as f:
#     json.dump(filtered_data, f, indent=4)


# import json

# # Load your data
# with open('./filtered_stockmarket.json', 'r') as f:
#     data = json.load(f)

# # Filter out instances where "image_data" is null, "stock market" is not in "justification", and remove duplicates in "claim"
# filtered_data = []
# seen_claims = set()
# for item in data:
#     if item['image_data'] and 'stock market' in item['justification']:
#         if item['claim'] not in seen_claims:
#             filtered_data.append(item)
#             seen_claims.add(item['claim'])

# # Save the filtered data
# with open('filtered_stockmarket.json', 'w') as f:
#     json.dump(filtered_data, f, indent=4)
