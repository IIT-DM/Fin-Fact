# # import json
# # import re
# # import matplotlib.pyplot as plt

# # def extract_confidence_scores(json_file):
# #     with open(json_file, 'r') as file:
# #         data = json.load(file)
# #     confidence_scores = []
# #     for item in data:
# #         response = item.get('response', '')
# #         match = re.search(r'(\d+)%', response)  # Search for a pattern like '90%'
# #         if match:
# #             confidence_score = int(match.group(1))  # Extract the numeric value
# #             confidence_scores.append(confidence_score)
    
# #     print(f"Total number of confidence scores extracted: {len(confidence_scores)}")  # Print total count of confidence scores
# #     return confidence_scores

# # def plot_confidence_distribution(confidence_scores):
# #     plt.figure(figsize=(8, 6))
# #     plt.hist(confidence_scores, bins=10, edgecolor='black')
# #     plt.title('Confidence Score Distribution')
# #     plt.xlabel('Confidence Score (%)')
# #     plt.ylabel('Frequency')
# #     plt.grid(True)

# #     # Count occurrences of each confidence score
# #     counts, bins, _ = plt.hist(confidence_scores, bins=10, edgecolor='black')

# #     # Display counts for specific confidence score percentages
# #     confidence_score_counts = {}
# #     for score in confidence_scores:
# #         if score in confidence_score_counts:
# #             confidence_score_counts[score] += 1
# #         else:
# #             confidence_score_counts[score] = 1

# #     # Print counts for specific confidence score percentages
# #     print("Counts of specific confidence score percentages:")
# #     for score in sorted(confidence_score_counts.keys()):
# #         print(f"{score}%: {confidence_score_counts[score]}")

# #     # Annotate each bin with the count
# #     for i in range(len(counts)):
# #         if counts[i] > 0:
# #             plt.text(bins[i], counts[i], str(int(counts[i])), ha='center', va='bottom')

# #     plt.show()

# # # Specify your JSON file path
# # json_file_path = 'filtered_jsons/responses/gemini_responses.json'

# # # Extract confidence scores
# # confidence_scores = extract_confidence_scores(json_file_path)

# # # Plot the confidence score distribution
# # plot_confidence_distribution(confidence_scores)


import matplotlib.pyplot as plt
import numpy as np

# Replace these with your actual data
gemini_pro_vision = {
    0: 38, 1: 2, 2: 3, 3: 4, 4: 5, 5: 7, 6: 6, 7: 1, 8: 2, 9: 10, 10: 3, 12: 2, 13: 1, 14: 1, 15: 2, 16: 1, 20: 2, 27: 2, 29: 1, 31: 1, 33: 1, 34: 1, 35: 1, 40: 1, 46: 1, 50: 20, 54: 1, 58: 1, 60: 9, 70: 144, 71: 1, 75: 1, 80: 120, 85: 1, 90: 339, 92: 1, 95: 341, 98: 2, 99: 148, 100: 347
}

gpt_4_vision = {
    0: 4, 2: 4, 3: 2, 5: 2, 6: 2, 8: 2, 10: 1, 14: 2, 21: 1, 35: 1, 50: 10, 52: 1, 60: 6, 65: 1, 66: 1, 69: 1, 70: 22, 75: 25, 80: 39, 85: 45, 90: 310, 95: 392, 98: 4, 99: 21, 100: 50
}

llava = {
    0: 4, 2: 4, 3: 2, 5: 2, 6: 2, 8: 2, 10: 1, 14: 2, 21: 1, 35: 1, 50: 10, 52: 1, 60: 6, 65: 1, 66: 1, 69: 1, 70: 22, 75: 25, 80: 39, 85: 45, 90: 310, 95: 392, 98: 4, 100: 21
}

bins = np.arange(0, 100, 5)

gemini_pro_vision_binned = np.histogram(list(gemini_pro_vision.keys()), bins, weights=list(gemini_pro_vision.values()))[0]
gpt_4_vision_binned = np.histogram(list(gpt_4_vision.keys()), bins, weights=list(gpt_4_vision.values()))[0]
llava_binned = np.histogram(list(llava.keys()), bins, weights=list(llava.values()))[0]
fig, ax = plt.subplots(dpi=150)  
ax.bar(bins[:-1], gemini_pro_vision_binned, width=4, color='b', alpha=0.5, label='Gemini Pro Vision')
ax.bar(bins[:-1], gpt_4_vision_binned, width=4, color='r', alpha=0.5, label='GPT-4 Vision', bottom=gemini_pro_vision_binned)
ax.bar(bins[:-1], llava_binned, width=4, color='g', alpha=0.5, label='LLaVA', bottom=gemini_pro_vision_binned+gpt_4_vision_binned)
ax.set_xlabel('Confidence Scores', fontsize=14, fontweight='bold')
ax.set_ylabel('Counts', fontsize=14, fontweight='bold')
ax.set_title('Confidence Score Percentages of LVLMs', fontsize=16, fontweight='bold')
ax.tick_params(axis='both', which='major', labelsize=12)
ax.legend(fontsize=12)
plt.xticks(fontsize=12, weight='bold')
plt.yticks(fontsize=12, weight='bold')
plt.show()