import json
from sklearn.feature_extraction.text import TfidfVectorizer

with open('sfact.json', 'r') as file:
    dataset = json.load(file)

citations_list = [item['data'] for item in dataset]
href_count = 0

for item in citations_list:
    if item is not None:
        for citation in item:
            if citation is not None and 'hrefs' in citation:
                href_count += len(citation['hrefs'])

print(f"Total number of href occurrences: {href_count}")

citations = [item['data'][0]['sentence'] for item in dataset if item['data']]
preprocessed_citations = [citation.lower() for citation in citations]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(preprocessed_citations)
citation_scores = tfidf_matrix.toarray().sum(axis=1)
ranked_citations = sorted(zip(citations, citation_scores), key=lambda x: x[1], reverse=True)

for citation, score in ranked_citations:
    print(f"Citation: {citation}")
    print(f"Relevance Score: {score}")
    print("---")

ranked_dataset = [{'citation': citation, 'relevance_score': score} for citation, score in ranked_citations]
ranked_json = json.dumps(ranked_dataset, indent=4)
print(len(ranked_json))
    
