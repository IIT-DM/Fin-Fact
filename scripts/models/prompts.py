closed_book_system = """Evaluate the veracity of the claim using your existing knowledge base.
Use the following format to provide your answer:
Prediction: [TRUE or FALSE or NEI (NOT ENOUGH INFORMATION))]
Confidence Level: [please show the percentage]
"""

open_book_system = """Given a claim and evidence  (which can be text or image), determine whether the claim is TRUE or FALSE or NEI (NOT ENOUGH INFORMATION)) by the evidence. 
            
Use the following format to provide your answer:
Prediction: [TRUE or FALSE or NEI (NOT ENOUGH INFORMATION))]
Explanation: [put your evidence and step-by-step reasoning here]
Confidence Level: [please show the percentage]

The confidence level indicates the degree of certainty you have about your answer and is represented as a percentage. 
For instance, if your confidence level is 80%, it means you are 80% certain that your answer is correct and there is a 20% chance that it may be incorrect."""

chain_of_thought = """Given a claim, classify the claim based on your parametric knowledge.

Chain of Thought:
Before providing your prediction, explain your reasoning step-by-step based on the knowledge you have about the claim. Break down any historical, factual, or contextual information that leads to your final classification.

Use the following format to provide your answer:
- Chain of Thought: [Step-by-step reasoning here]
- Prediction: [TRUE or FALSE or NEI (NOT ENOUGH INFORMATION))]
- Confidence Level: [show the percentage]

The confidence level indicates the degree of certainty you have about your answer and is represented as a percentage. For instance, if your confidence level is 80%, it means you are 80% certain that your answer is correct and there is a 20% chance that it may be incorrect.
"""

symbolic = """Given a claim and evidence  (which can be text, table, or an image), determine whether the claim is SUPPORT or REFUTE by the evidence.
    enerate Reasoning Steps by writing a Python-like program that outlines the step-by-step reasoning needed to verify the claim.
    ou can call three functions in the program : 1. Question () to answer a question ; 2. Verify () to verify a simple claim ; 3. Predict () to predict the veracity label.
    xecute the generated reasoning steps to determine the overall relationship between the claim and the evidence and return your judgement.
    Please only return the label and nothing else. Just respond with the label without the program. Do not respond with the Python-like Program."""


self_help = """Given a claim and evidence  (which can be text, table, or an image), determine whether the claim is SUPPORT or REFUTE by the evidence.
    Instruction: 1. Decompose the Claim: Break down the claim into a series of follow-up questions that will help assess the relationship between the claim and the evidence.
    2. Answer the Follow-Up Questions: Evaluate the evidence to answer each follow-up question.
    3. Aggregate and Conclude: Use the answers to the follow-up questions to determine the overall relationship between the claim and the evidence.
    Please only return the label and nothing else."""
