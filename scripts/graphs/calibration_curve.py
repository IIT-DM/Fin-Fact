import matplotlib.pyplot as plt
import numpy as np

confidence = np.array([0, 10, 50, 70, 80, 85, 95])
gemini_vision_pro_accuracy = np.array([20, 50, 45, 23, 62, 89, 62])
gpt_4v_accuracy = np.array([2, 15, 52, 29, 12, 68, 71])
llava_accuracy = np.array([12, 38, 95, 21, 32, 48, 33])

fig, ax = plt.subplots(dpi=150)
ax.plot(confidence, gpt_4v_accuracy, '-o', color='blue', label='GPT-4V')
ax.plot(confidence, llava_accuracy, '-*', color='orange', label='LLaVA')
ax.plot(confidence, gemini_vision_pro_accuracy, '-s', color='green', label='Gemini-Vision-Pro')
ax.plot([0, 100], [0, 100], '--', color='gray')

ax.set_xlabel('Confidence (%)', fontsize=14, weight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=14, weight='bold')
ax.set_title('Calibration Curve', fontsize=16, weight='bold')
ax.legend()

plt.xticks(fontsize=12, weight='bold')
plt.yticks(fontsize=12, weight='bold')

plt.show()
