import json
from langdetect import detect
from collections import Counter

def find_unique_elements_with_count(lst):
    element_count = Counter(lst)
    unique_elements = list(element_count.keys())
    counts = list(element_count.values())
    return unique_elements, counts


with open('./finfact_new.json', "r") as infile:
    data = json.load(infile)
titles_list = []
lang_list = []
for entry in data:
    titles_list.append(entry["label"])

for i in titles_list:
    lang = detect(i)
    lang_list.append(lang)

myset = set(lang_list)
print(myset)

unique_elements, counts = find_unique_elements_with_count(lang_list)
print("Unique elements:", unique_elements)
print("Counts:", counts)