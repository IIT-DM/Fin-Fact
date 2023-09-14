from transformers import BartTokenizer, BartForConditionalGeneration
import json

class NLPFactGenerator:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.max_length = 1024
        self.model = BartForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.sentences_list = []
        self.justification_list = []
        self.titles_list = []
        self.labels_list = []
        self.claim_list = []
    
    def load_data(self, filename):
        with open(filename, "r") as infile:
            self.data = json.load(infile)

    def preprocess_data(self):
        max_seq_length = 1024
        for entry in self.data:
            if "data" in entry:
                self.titles_list.append(entry["title"])
                justification = ' '.join(entry["paragraphs"])
                for evidence in self.sentences_list:
                    if len(evidence) > max_seq_length:
                        evidence = evidence[:max_seq_length]
                _evidence = ' '.join([item["sentence"] for item in entry["data"]])
                self.justification_list.append(justification)
                self.sentences_list.append(_evidence)
                self.labels_list.append(entry["label"])

    def generate_fact(self):
        max_seq_length = 1024
        generated_facts = []
        for evidence in self.justification_list:
            if len(evidence) > max_seq_length:
                evidence = evidence[:max_seq_length]
            input_ids = self.tokenizer.encode(evidence, return_tensors="pt")
            try:
                generated_ids = self.model.generate(input_ids, max_length=self.max_length, num_return_sequences=1)
                generated_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
                print('Done')
                print('*'*50)
                generated_facts.append(generated_text)
            except:
                print('Input ID: ', len(input_ids))
        return generated_facts


if __name__ == "__main__":
    fact_generator = NLPFactGenerator()
    fact_generator.load_data("finfact_old.json")
    fact_generator.preprocess_data()
    generated_facts = fact_generator.generate_fact()
    generated_data = []

    for title, evi, fact in zip(fact_generator.titles_list, fact_generator.sentences_list, generated_facts):
        generated_data.append({"title": title, "evidence":evi, "generated_fact": fact})
    with open("generated_facts.json", "w") as outfile:
        json.dump(generated_data, outfile, indent=4)


    # def load_data(self, filename, num_instances=3):
    #     with open(filename, "r") as infile:
    #         self.data = json.load(infile)[:num_instances]