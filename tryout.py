import json

def remove_unicode(string):
    return string.encode('ascii', 'ignore').decode('utf-8')

original_string = "COVID-19 \u00a0including the effects \u2014 like site \u2014 are  als As we\u2019ve\u00a0previously explained, the\u00a0Pfizer/BioNTech\u00a0and\u00a0Moderna\u00a0mRNA vaccines. \u2014 show \u201cOur trials,\u201d the 1% of people e"
cleaned_string = remove_unicode(original_string)

data = {
    "str": cleaned_string
}

with open("try.json", "w") as outfile:
    json.dump(data, outfile)
