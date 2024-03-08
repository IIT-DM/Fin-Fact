from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
)
import argparse
import warnings
warnings.filterwarnings("ignore")

from fact_checking import FactChecker
import json
from sklearn.metrics import confusion_matrix, classification_report

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
        max_seq_length = 1024 
        for title, evidence in zip(self.titles_list, self.sentences_list):
            try:
                if len(title) > max_seq_length:
                    title = title[:max_seq_length]
                if len(evidence) > max_seq_length:
                    evidence = evidence[:max_seq_length]
                    print(len(evidence))
                is_claim_true = self.fact_checker.validate(evidence, title)
                print(is_claim_true)
                self.claim_list.append(is_claim_true)
            except IndexError:
                self.claim_list.append(None)

    def calculate_metrics(self):
        conf_matrix = confusion_matrix(self.labels_list, [str(is_claim).lower() for is_claim in self.claim_list])
        cls_report = classification_report(self.labels_list, [str(is_claim).lower() for is_claim in self.claim_list], labels=["true", "false", "neutral"])

        return conf_matrix, cls_report

def parse_args():
    parser = argparse.ArgumentParser(description="Fact Checker Application")
    parser.add_argument("--model_name", default="fractalego/fact-checking", help="Name of the fact-checking model to use")
    parser.add_argument("--data_file", required=True, help="Path to the JSON data file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    fact_checker_app = FactCheckerApp(model_name=args.model_name)
    fact_checker_app.load_data(args.data_file)
    fact_checker_app.preprocess_data()
    fact_checker_app.validate_claims()
    conf_matrix, cls_report = fact_checker_app.calculate_metrics()
    print("Confusion Matrix:\n", conf_matrix)
    print("Report:\n", cls_report)