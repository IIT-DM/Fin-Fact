import nltk
nltk.download('punkt') # download punkt package if you haven't already

paragraph = "This is the first sentence. This is the second sentence. This is the third sentence."

sentences = nltk.sent_tokenize(paragraph)

print(sentences)
