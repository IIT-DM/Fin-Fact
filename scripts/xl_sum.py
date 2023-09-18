# import re
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))

# article_text = """Videos that say approved vaccines are dangerous and cause autism, cancer or infertility are among those that will be taken down, the company said.  The policy includes the termination of accounts of anti-vaccine influencers.  Tech giants have been criticised for not doing more to counter false health information on their sites.  In July, US President Joe Biden said social media platforms were largely responsible for people's scepticism in getting vaccinated by spreading misinformation, and appealed for them to address the issue.  YouTube, which is owned by Google, said 130,000 videos were removed from its platform since last year, when it implemented a ban on content spreading misinformation about Covid vaccines.  In a blog post, the company said it had seen false claims about Covid jabs "spill over into misinformation about vaccines in general". The new policy covers long-approved vaccines, such as those against measles or hepatitis B.  "We're expanding our medical misinformation policies on YouTube with new guidelines on currently administered vaccines that are approved and confirmed to be safe and effective by local health authorities and the WHO," the post said, referring to the World Health Organization."""

# model_name = "csebuetnlp/mT5_multilingual_XLSum"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# input_ids = tokenizer(
#     [WHITESPACE_HANDLER(article_text)],
#     return_tensors="pt",
#     padding="max_length",
#     truncation=True,
#     max_length=1024
# )["input_ids"]

# output_ids = model.generate(
#     input_ids=input_ids,
#     max_length=128,
#     no_repeat_ngram_size=2,
#     num_beams=4
# )[0]

# summary = tokenizer.decode(
#     output_ids,
#     skip_special_tokens=True,
#     clean_up_tokenization_spaces=False
# )

# print(summary)

# from transformers import BigBirdPegasusForConditionalGeneration, AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained("google/bigbird-pegasus-large-arxiv")

# # by default encoder-attention is `block_sparse` with num_random_blocks=3, block_size=64
# model = BigBirdPegasusForConditionalGeneration.from_pretrained("google/bigbird-pegasus-large-arxiv")

# # decoder attention type can't be changed & will be "original_full"
# # you can change `attention_type` (encoder only) to full attention like this:
# model = BigBirdPegasusForConditionalGeneration.from_pretrained("google/bigbird-pegasus-large-arxiv", attention_type="original_full")

# # you can change `block_size` & `num_random_blocks` like this:
# model = BigBirdPegasusForConditionalGeneration.from_pretrained("google/bigbird-pegasus-large-arxiv", block_size=16, num_random_blocks=2)

# text = "Replace me by any text you'd like."
# inputs = tokenizer(text, return_tensors='pt')
# prediction = model.generate(**inputs)
# prediction = tokenizer.batch_decode(prediction)

from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration

# Let's load the model and the tokenizer 
model_name = "human-centered-summarization/financial-summarization-pegasus"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name) # If you want to use the Tensorflow model 
                                                                    # just replace with TFPegasusForConditionalGeneration


# Some text to summarize here
text_to_summarize = "National Commercial Bank (NCB), Saudi Arabia’s largest lender by assets, agreed to buy rival Samba Financial Group for $15 billion in the biggest banking takeover this year.NCB will pay 28.45 riyals ($7.58) for each Samba share, according to a statement on Sunday, valuing it at about 55.7 billion riyals. NCB will offer 0.739 new shares for each Samba share, at the lower end of the 0.736-0.787 ratio the banks set when they signed an initial framework agreement in June.The offer is a 3.5% premium to Samba’s Oct. 8 closing price of 27.50 riyals and about 24% higher than the level the shares traded at before the talks were made public. Bloomberg News first reported the merger discussions.The new bank will have total assets of more than $220 billion, creating the Gulf region’s third-largest lender. The entity’s $46 billion market capitalization nearly matches that of Qatar National Bank QPSC, which is still the Middle East’s biggest lender with about $268 billion of assets."

# Tokenize our text
# If you want to run the code in Tensorflow, please remember to return the particular tensors as simply as using return_tensors = 'tf'
input_ids = tokenizer(text_to_summarize, return_tensors="pt").input_ids

# Generate the output (Here, we use beam search but you can also use any other strategy you like)
output = model.generate(
    input_ids, 
    max_length=32, 
    num_beams=5, 
    early_stopping=True
)

# Finally, we can print the generated summary
print(tokenizer.decode(output[0], skip_special_tokens=True))
# Generated Output: Saudi bank to pay a 3.5% premium to Samba share price. Gulf region’s third-largest lender will have total assets of $220 billion
