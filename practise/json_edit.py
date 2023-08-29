# import json
# input_file = "sfact.json"

# with open(input_file, "r") as f:
#     json_data = json.load(f)

# for entry in json_data:
#     entry["label"] = "true"

# output_file = "modified_sfact.json"

# with open(output_file, "w") as f:
#     json.dump(json_data, f)



import json

file1 = "./json/debt_data.json"
file2 = "./json/capital_trade_data.json"
file3 = "./json/state_budget_data.json"
file4 = "./json/financial_regulation_data.json"
file5 = "./json/economy_data.json"
file6 = "./json/taxes_data.json"
file7 = "./json/trade_data.json"

with open(file1, "r") as f1:
    data1 = json.load(f1)
with open(file2, "r") as f2:
    data2 = json.load(f2)
with open(file3, "r") as f3:
    data3 = json.load(f3)
with open(file4, "r") as f4:
    data4 = json.load(f4)
with open(file5, "r") as f5:
    data5 = json.load(f5)
with open(file6, "r") as f6:
    data6 = json.load(f6)
with open(file7, "r") as f7:
    data7 = json.load(f7)

merged_data = data1 + data2 + data3 + data4 + data5 + data6 + data7
output_file = "finfact.json"

with open(output_file, "w") as f:
    json.dump(merged_data, f)

print("Merged JSON data has been saved to", output_file)

