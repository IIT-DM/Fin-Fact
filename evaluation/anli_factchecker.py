from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json

class FactCheckerApp:
    def __init__(self, hg_model_hub_name='ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli'):
    
        # hg_model_hub_name = "ynie/albert-xxlarge-v2-snli_mnli_fever_anli_R1_R2_R3-nli"
        # hg_model_hub_name = "ynie/bart-large-snli_mnli_fever_anli_R1_R2_R3-nli"
        # hg_model_hub_name = "ynie/electra-large-discriminator-snli_mnli_fever_anli_R1_R2_R3-nli"
        # hg_model_hub_name = "ynie/xlnet-large-cased-snli_mnli_fever_anli_R1_R2_R3-nli"
    
        self.max_length = 512
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
            if "data" in entry:
                self.titles_list.append(entry["title"])
                _evidence = ' '.join([item["sentence"] for item in entry["data"]])
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
                            token_type_ids=token_type_ids,
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

    def calculate_f1_score(self):
        tp = sum([1 for t, p in zip(self.labels_list, self.claim_list) if t == "true" and p == "true"])
        fp = sum([1 for t, p in zip(self.labels_list, self.claim_list) if t == "false" and p == "true"])
        fn = sum([1 for t, p in zip(self.labels_list, self.claim_list) if t == "true" and p == "false"])
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
        return f1_score

if __name__ == "__main__":
    fact_checker_app = FactCheckerApp()
    fact_checker_app.load_data("finfact.json")
    fact_checker_app.preprocess_data()
    fact_checker_app.validate_claims()
    f1_score = fact_checker_app.calculate_f1_score()
    print("F1 score: ", f1_score)
