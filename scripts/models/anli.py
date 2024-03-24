from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import argparse
import json
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, classification_report, f1_score

class FactCheckerApp:
    def __init__(self, hg_model_hub_name='ynie/electra-large-discriminator-snli_mnli_fever_anli_R1_R2_R3-nli'):
        # hg_model_hub_name = "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
        # hg_model_hub_name = "ynie/albert-xxlarge-v2-snli_mnli_fever_anli_R1_R2_R3-nli"
        # hg_model_hub_name = "ynie/bart-large-snli_mnli_fever_anli_R1_R2_R3-nli"
        # hg_model_hub_name = "ynie/electra-large-discriminator-snli_mnli_fever_anli_R1_R2_R3-nli"
        # hg_model_hub_name = "ynie/xlnet-large-cased-snli_mnli_fever_anli_R1_R2_R3-nli"
    
        self.max_length = 248
        self.tokenizer = AutoTokenizer.from_pretrained(hg_model_hub_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(hg_model_hub_name)
        self.sentences_list = []
        self.titles_list = []
        self.labels_list = []
        self.claim_list = []

    def load_data(self, filename):
        with open(filename, "r") as infile:
            self.data = json.load(infile)

    def preprocess_data(self):
        for entry in self.data:
            if "evidence" in entry:
                self.titles_list.append(entry["claim"])
                _evidence = ' '.join([item["sentence"] for item in entry["evidence"]])
                self.sentences_list.append(_evidence)
                self.labels_list.append(entry["label"])

    def validate_claims(self, threshold=0.5):
        for title, evidence in zip(self.titles_list, self.sentences_list):
            tokenized_input_seq_pair = self.tokenizer.encode_plus(evidence, title,
                                                    max_length=self.max_length,
                                                    return_token_type_ids=True, truncation=True)
            input_ids = torch.Tensor(tokenized_input_seq_pair['input_ids']).long().unsqueeze(0)
            token_type_ids = torch.Tensor(tokenized_input_seq_pair['token_type_ids']).long().unsqueeze(0)
            attention_mask = torch.Tensor(tokenized_input_seq_pair['attention_mask']).long().unsqueeze(0)
            outputs = self.model(input_ids,
                            attention_mask=attention_mask,
                            labels=None)
            predicted_probability = torch.softmax(outputs.logits, dim=1)[0].tolist()
            entailment_prob = predicted_probability[0]
            neutral_prob = predicted_probability[1]
            contradiction_prob = predicted_probability[2]

            if entailment_prob > threshold:
                is_claim_true = "true"
            elif neutral_prob > threshold:
                is_claim_true = "neutral"
            else:
                is_claim_true = "false"

            print(is_claim_true)
            self.claim_list.append(is_claim_true)
    
    def calculate_metrics(self):
        precision = precision_score(self.labels_list, self.claim_list, average='macro')
        accuracy = accuracy_score(self.labels_list, self.claim_list)
        f1_scoree = f1_score(self.labels_list, self.claim_list, average='macro')
        conf_matrix = confusion_matrix(self.labels_list, self.claim_list)
        recall_metric = recall_score(self.labels_list, self.claim_list, pos_label="true", average="macro")
        cls_report = classification_report(self.labels_list, self.claim_list, labels=["true", "false", "neutral"])
        return precision, accuracy, f1_scoree, conf_matrix, recall_metric, cls_report

def parse_args():
    parser = argparse.ArgumentParser(description="Fact Checker Application")
    parser.add_argument("--model_name", default="ynie/bart-large-snli_mnli_fever_anli_R1_R2_R3-nli", help="Name of the pre-trained model to use")
    parser.add_argument("--data_file", required=True, help="Path to the JSON data file")
    parser.add_argument("--threshold", type=float, default=0.5, help="Threshold for claim validation")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    fact_checker_app = FactCheckerApp(hg_model_hub_name=args.model_name)
    fact_checker_app.load_data(args.data_file)
    fact_checker_app.preprocess_data()
    fact_checker_app.validate_claims(threshold=args.threshold)
    precision, accuracy, f1_scoree, conf_matrix, recall_metric, cls_report = fact_checker_app.calculate_metrics()
    print("Precision:", precision)
    print("Accuracy:", accuracy)
    print("F1 score:", f1_scoree)
    print("Recall: ", recall_metric)
    print("Confusion Matrix:\n", conf_matrix)
    print("Report:\n", cls_report)
    
