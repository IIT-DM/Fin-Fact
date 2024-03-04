import torch
from transformers import BertTokenizerFast, EncoderDecoderModel
import json

class NLPFactGenerator:
    def __init__(self, ckpt="mrm8488/bert2bert_shared-german-finetuned-summarization"):
        self.max_length = 1024
        self.tokenizer = BertTokenizerFast.from_pretrained(ckpt)
        self.model = EncoderDecoderModel.from_pretrained(ckpt)
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
        count = 0
        for evidence in self.justification_list:
            if len(evidence) > max_seq_length:
                evidence = evidence[:max_seq_length]
            inputs = self.tokenizer([evidence], padding="max_length", truncation=True, max_length=1024, return_tensors="pt")
            input_ids = inputs.input_ids
            attention_mask = inputs.attention_mask
            try:
                
                output = self.model.generate(input_ids, attention_mask=attention_mask)
                summary = self.tokenizer.decode(output[0], skip_special_tokens=True)
                count+=1
                print(count)
                generated_facts.append(summary)
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
    with open("generated_facts_bert.json", "w") as outfile:
        json.dump(generated_data, outfile, indent=4)



device = 'cuda' if torch.cuda.is_available() else 'cpu'
ckpt = 'mrm8488/bert2bert_shared-german-finetuned-summarization'
tokenizer = BertTokenizerFast.from_pretrained(ckpt)
model = EncoderDecoderModel.from_pretrained(ckpt).to(device)
def generate_summary(text):
   inputs = tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
   input_ids = inputs.input_ids.to(device)
   attention_mask = inputs.attention_mask.to(device)
   output = model.generate(input_ids, attention_mask=attention_mask)
   return tokenizer.decode(output[0], skip_special_tokens=True)
   
text = "Your text here..."

generate_summary(text)
