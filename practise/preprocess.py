# import json

# with open("finfact.json", "r") as infile:
#     data = json.load(infile)

# sentences_list = []
# titles_list = []
# labels_list = []
# for entry in data:
#     if "data" in entry:
#         titles = titles_list.append(entry["title"])
#         # sentences_list.extend([item["sentence"] for item in entry["data"]])
#         sentence_index = ' '.join([item["sentence"] for item in entry["data"]])
#         sentences_list.append(sentence_index)
#         labels = labels_list.append(entry["label"])

# print(len(sentences_list))


def calculate_f1_score(true, predict):
    tp = sum([1 for t, p in zip(true, predict) if t == p and t == True])
    fp = sum([1 for t, p in zip(true, predict) if t != p and p == True])
    fn = sum([1 for t, p in zip(true, predict) if t != p and t == True])
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return f1_score

true_labels = [True, False, True, False, True]
predicted_labels = [True, False, True, False, True]

f1_score = calculate_f1_score(true_labels, predicted_labels)
print("F1 score:", f1_score)