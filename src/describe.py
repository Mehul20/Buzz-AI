from transformers import pipeline
from search import run_search
from utils import get_models
import torch

def get_llama():
    model_id = "meta-llama/Llama-3.2-1B"
    pipe = pipeline(
        "text-generation", 
        model=model_id, 
        torch_dtype=torch.bfloat16, 
        device_map="auto"
    )
    if pipe.model.config.pad_token_id is None:
        pipe.model.config.pad_token_id = pipe.model.config.eos_token_id
    return pipe

def generate(user_query):
    pipe = get_llama()
    return pipe(user_query, max_new_tokens=150)

if __name__ == "__main__":
    user_query = "reinforcement learning"
    subject = ["CS"]
    level = "undergrad"
    models = get_models()
    # ['all-MiniLM-L6-v2', 'all-distilroberta-v1']
    model_name = models[1]
    top_results, class_descriptions = run_search(query=user_query, subject=subject, model_name=model_name, level=level)
    llama_outputs = []
    for i in range(len(class_descriptions)):
        query = f"Describe: {top_results[i]}: {class_descriptions[i]}"
        llama_output = generate(query)[0]['generated_text']
        llama_outputs.append(llama_output)

    for i in range(len(class_descriptions)):
        print(f"\n{top_results[i]}:\n")
        print(f"{llama_outputs[i]}")