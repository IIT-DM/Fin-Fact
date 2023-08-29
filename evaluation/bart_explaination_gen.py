from transformers import BartTokenizer, BartForConditionalGeneration
import json 

class NLPFactGenerator:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.max_length = 320
        self.model = BartForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
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

    def generate_fact(self):
        generated_facts = []  # Store generated facts for all titles
        for title in self.titles_list:
            input_ids = self.tokenizer.encode(title, return_tensors="pt")
            generated_ids = self.model.generate(input_ids, max_length=self.max_length, num_return_sequences=1)
            generated_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            print(generated_text)
            generated_facts.append(generated_text)
        return generated_facts

if __name__ == "__main__":
    fact_generator = NLPFactGenerator()
    fact_generator.load_data("finfact.json")
    fact_generator.preprocess_data()
    generated_facts = fact_generator.generate_fact()
    
    # Print generated facts for each title
    for title, fact in zip(fact_generator.titles_list, generated_facts):
        print("Title:", title)
        print("Generated Fact:", fact)
        print("=" * 50)
