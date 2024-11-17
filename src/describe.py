from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import search

def get_T5():
    model = T5ForConditionalGeneration.from_pretrained('google/t5-v1_1-base')
    tokenizer = T5Tokenizer.from_pretrained('google/t5-v1_1-base')
    return model, tokenizer

def get_T5_description(user_query):
    model, tokenizer = get_T5()
    tokenizer.pad_token = tokenizer.eos_token
    inputs = tokenizer(user_query, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(inputs['input_ids'], attention_mask=inputs['attention_mask'], pad_token_id=tokenizer.pad_token_id, max_length=150)
    detailed_description = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return detailed_description

def get_BART():
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
    return model, tokenizer

def get_BART_description(user_query):
    model, tokenizer = get_BART()
    inputs = tokenizer(user_query, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=150, num_beams=5, temperature=0.7)
    detailed_description = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return detailed_description

def get_GPT():
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    return model, tokenizer

def get_GPT_description(user_query):
    model, tokenizer = get_GPT()
    inputs = tokenizer(user_query, return_tensors="pt", padding=True, truncation=True)
    attention_mask = inputs['attention_mask']
    pad_token_id = tokenizer.eos_token_id
    outputs = model.generate(inputs['input_ids'], attention_mask=attention_mask, pad_token_id=pad_token_id, max_length=150)
    detailed_description = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return detailed_description

if __name__ == "__main__":
    user_query = "Mutex Locks"
    subject = ["CS"] # This needs can be empty if you want all classes
    top_results, class_descriptions = search.run(query=user_query, sub=subject)
    for course in class_descriptions:
        query = f"Describe the course {class_descriptions[course][0]} with description {class_descriptions[course][1]}"
        print(f"{query}\n\n")
        break
    T5_description = get_T5_description(query)
    # BART_description = get_BART_description(query)
    # GPT_description = get_GPT_description(query)
    print(T5_description)
