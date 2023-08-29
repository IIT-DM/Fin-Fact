import json
input_file = './finfact_p2.json'
with open(input_file, "r") as f:
    json_data = json.load(f)

# Remove entries where "label" is "mostly-true"
# json_data = [entry for entry in json_data if entry.get("label") != "false"]
json_data = [entry for entry in json_data if entry.get("label") != "half-true"]


# Define the output file path
output_file = "./finfact_p2_new.json"

# Dump the modified data into the output file
with open(output_file, "w") as f:
    json.dump(json_data, f)

print("Modified JSON data has been saved to", output_file)