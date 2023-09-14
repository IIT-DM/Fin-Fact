from transformers import BartTokenizer, BartForConditionalGeneration
import json, itertools 
from nltk.translate.bleu_score import SmoothingFunction, corpus_bleu
from nltk.tokenize import word_tokenize
from nltk.util import ngrams


class NLPFactGenerator:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.max_length = 1024
        self.model = BartForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.gen_fact_list = []
        self.evidence_list = []

    def _split_into_words(self, sentences):
        return list(itertools.chain(*[_.split(" ") for _ in sentences]))
    
    def _get_word_ngrams(self, n, sentences):
        assert len(sentences) > 0
        assert n > 0
        words = self._split_into_words(sentences)
        return self._get_ngrams(n, words)

    def _get_ngrams(self, n, text):
        ngram_set = set()
        text_length = len(text)
        max_index_ngram_start = text_length - n
        for i in range(max_index_ngram_start + 1):
            ngram_set.add(tuple(text[i:i + n]))
        return ngram_set
    
    def load_data(self, filename):
        with open(filename, "r") as infile:
            self.data = json.load(infile)
    
    def get_title_evidence_generated_facts(self):
        titles = []
        evidences = []
        generated_facts = []

        for entry in self.data:
            titles.append(entry["title"])
            evidences.append(entry["evidence"])
            generated_facts.append(entry["generated_fact"])

        return evidences, generated_facts

    def bleu(self):
        evidence_list, gen_fact_list = self.get_title_evidence_generated_facts()
        ref_bleu = []
        gen_bleu = []
        for l in evidence_list:
            gen_bleu.append(l.split())
        for i,l in enumerate(gen_fact_list):
            ref_bleu.append([l.split()])
        cc = SmoothingFunction()
        score_bleu = corpus_bleu(ref_bleu, gen_bleu, weights=(0, 1, 0, 0), smoothing_function=cc.method4)
        return score_bleu
    

    def rouge_one(self,n=1):
        evidence_list, gen_fact_list = self.get_title_evidence_generated_facts()
        evaluated_ngrams = self._get_word_ngrams(n, evidence_list)
        reference_ngrams = self._get_word_ngrams(n, gen_fact_list)
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


if __name__ == "__main__":
    fact_generator = NLPFactGenerator()
    fact_generator.load_data("generated_facts.json")
    rouge_one_score = fact_generator.rouge_one()
    blue_score = fact_generator.bleu()
    print(rouge_one_score)
    print(blue_score)

