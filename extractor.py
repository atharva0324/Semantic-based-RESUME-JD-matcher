from transformers import AutoModelForTokenClassification,AutoTokenizer
from transformers import pipeline
import os

model_path=os.path.join(os.path.dirname(__file__),"skill-extractor-model")

model=AutoModelForTokenClassification.from_pretrained(model_path)
tokenizer=AutoTokenizer.from_pretrained(model_path)

ner_pipeline=pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy='simple'
)

def extract_skills(text: str) -> dict:
    results = ner_pipeline(text)
    
    skills = set()
    knowledge = set()
    
    for entity in results:
        word = entity['word'].strip().lower()
        
        # Clean brackets and special characters
        word = word.replace('(', '').replace(')', '').replace('[', '').replace(']', '').strip()
        
        if word.startswith('##'):
            continue
        if len(word) <= 2:
            continue
        if not any(c.isalpha() for c in word):
            continue
            
        label = entity['entity_group']
        
        if label == 'SKILL':
            skills.add(word)
        elif label == 'KNOWLEDGE':
            knowledge.add(word)
    
    return {
        "skills": list(skills),
        "knowledge": list(knowledge)
    }