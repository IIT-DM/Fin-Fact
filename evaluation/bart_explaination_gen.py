from transformers import BartTokenizer, BartForConditionalGeneration
import json 
from nltk.tokenize import word_tokenize
from nltk.util import ngrams


class NLPFactGenerator:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.max_length = 1023
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
        for evidence in self.sentences_list:
            input_ids = self.tokenizer.encode(evidence, return_tensors="pt")
            try:
                generated_ids = self.model.generate(input_ids, max_length=self.max_length, num_return_sequences=1)
                generated_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
                print(generated_text)
                print('*'*50)
                generated_facts.append(generated_text)
            except:
                print('Ev: ', evidence)
                print('Input ID: ', len(input_ids))
                # print('Input ID: ', input_ids)
            
        return generated_facts
    
    def rouge_one(self, generated_facts, sentences_list, n=1):
        if len(sentences_list) <= 0 or len(generated_facts) <= 0:
            raise ValueError("Collections must contain at least 1 sentence.")

        evaluated_ngrams = self._get_word_ngrams(n, sentences_list)
        reference_ngrams = self._get_word_ngrams(n, generated_facts)
        reference_count = len(reference_ngrams)
        evaluated_count = len(evaluated_ngrams)
        overlapping_ngrams = evaluated_ngrams.intersection(reference_ngrams)
        overlapping_count = len(overlapping_ngrams)
        if evaluated_count == 0:
            precision = 0.0
        else:
            precision = overlapping_count / evaluated_count

        if reference_count == 0:
            recall = 0.0
        else:
            recall = overlapping_count / reference_count

        f1_score = 2.0 * ((precision * recall) / (precision + recall + 1e-8))
        return recall

# if __name__ == "__main__":
#     fact_generator = NLPFactGenerator()
#     fact_generator.load_data("finfact.json")
#     fact_generator.preprocess_data()
#     generated_facts = fact_generator.generate_fact()
    
#     # Print generated facts for each title
#     for title, fact in zip(fact_generator.titles_list, generated_facts):
#         print("Title:", title)
#         print("Generated Fact:", fact)
#         print("=" * 50)

if __name__ == "__main__":
    fact_generator = NLPFactGenerator()
    fact_generator.load_data("finfact.json")
    fact_generator.preprocess_data()
    generated_facts = fact_generator.generate_fact()
    rouge_one_score = fact_generator.rouge_one()
    print(rouge_one_score)
    generated_data = []

    for title, sentences_list, fact in zip(fact_generator.titles_list, fact_generator.sentences_list, generated_facts):
        generated_data.append({"title": title, "generated_fact": fact})
    with open("generated_facts.json", "w") as outfile:
        json.dump(generated_data, outfile, indent=4)

    print(rouge_one_score)