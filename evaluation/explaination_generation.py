from transformers import BertForSequenceClassification, BertTokenizer
from transformers import pipeline

model = BertForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

claim = "The company's revenue increased by 20% last quarter."
inputs = tokenizer(claim, return_tensors="pt", padding=True, truncation=True)

explanation_generator = pipeline("explainable_nlp", model=model)
explanation = explanation_generator(claim, **inputs)

# Print explanation
print("Claim:", claim)
print("Explanation:", explanation[0]["word_attributions"])

