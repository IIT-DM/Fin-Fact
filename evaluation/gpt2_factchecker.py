from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
)
import warnings
warnings.filterwarnings("ignore")

from fact_checking import FactChecker
import json
from sklearn.metrics import confusion_matrix, accuracy_score

class FactCheckerApp:
    def __init__(self, model_name='fractalego/fact-checking'):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.fact_checking_model = GPT2LMHeadModel.from_pretrained(model_name)
        self.fact_checker = FactChecker(self.fact_checking_model, self.tokenizer)
        self.sentences_list = []
        self.titles_list = []
        self.labels_list = []
        self.claim_list = []

    def load_data(self, filename):
        with open(filename, "r") as infile:
            self.data = json.load(infile)

    def preprocess_data(self):
        for entry in self.data:
            if "data" in entry:
                self.titles_list.append(entry["title"])
                _evidence = ' '.join([item["sentence"] for item in entry["data"]])
                self.sentences_list.append(_evidence)
                self.labels_list.append(entry["label"])

    def validate_claims(self):
        for title, evidence in zip(self.titles_list, self.sentences_list):
            try:
                # print(title)
                is_claim_true = self.fact_checker.validate(evidence, title)
                
                # print(type(is_claim_true))
                print(is_claim_true) 
                # if is_claim_true in ["True", "False"]:
                #     self.claim_list.append(is_claim_true)
                # else:
                #     self.claim_list.append(bool('False'))
                self.claim_list.append(is_claim_true)
            except IndexError:
                # print("Skipping validation for evidence:", evidence)
                self.claim_list.append(None)


    
    def calculate_metrics(self):
        fn = sum([1 for t, p in zip(self.labels_list, self.claim_list) if t and not p])
        tp = sum([1 for t, p in zip(self.labels_list, self.claim_list) if t == "true" and p == "true"])
        fp = sum([1 for t, p in zip(self.labels_list, self.claim_list) if t == "false" and p == "true"])
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
        accuracy = accuracy_score(self.labels_list, self.claim_list)
        conf_matrix = confusion_matrix(self.labels_list, self.claim_list)
        # recall_metric = recall_score(self.labels_list, self.claim_list, pos_label="true")
        
        return precision, recall, accuracy, f1_score, conf_matrix

if __name__ == "__main__":
    fact_checker_app = FactCheckerApp()
    fact_checker_app.load_data("finfact.json")
    fact_checker_app.preprocess_data()
    fact_checker_app.validate_claims()
    precision, accuracy, f1_score, conf_matrix = fact_checker_app.calculate_metrics()
    print("Precision:", precision)
    print("Accuracy:", accuracy)
    print("F1 score:", f1_score)
    print("Confusion Matrix:\n", conf_matrix)