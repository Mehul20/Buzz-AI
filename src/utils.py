import json
import pickle
import os
from sentence_transformers import SentenceTransformer, models
import pdfplumber

def read_file(filePath):
    with open(filePath, "r") as file:
        data = json.load(file)
    return data

def check_relevant_special_topics(course):
    init_split = course.split(" ")
    subject = init_split[0]
    split2 = init_split[1].split("-")
    number = split2[0]
    compatible_courses = {"CS", "CSE", "CM", "CX"}
    if subject in compatible_courses and (number == "4803" or number == "8803"):
        return True, split2[1]
    return False, None

# Unused - Might need them in the future
def save_pickle_dictionary(dictionary, filePath):
    with open(filePath, "wb") as file:
        pickle.dump(dictionary, file)

def read_pickle_dictionary(filePath):
    with open(filePath, "rb") as file:
        dictionary_found = pickle.load(file)
    return dictionary_found

def get_path(model):
    base_dir = "../Processed"
    save_path = os.path.join(base_dir, model)
    os.makedirs(save_path, exist_ok=True)
    return save_path

def get_models():
    RoBERTa_model = 'all-distilroberta-v1'
    bert_model = 'all-MiniLM-L6-v2'
    multi_qa = 'multi-qa-mpnet-base-dot-v1'
    bert_base = "bert-base-uncased"
    models = [bert_model, RoBERTa_model, multi_qa, bert_base]
    return models

def construct_custom_model(model_name):
    model_transformer = models.Transformer(model_name)
    model_pool_layer = models.Pooling(model_transformer.get_word_embedding_dimension(), pooling_mode_mean_tokens = True)
    custom_model_construct = SentenceTransformer(modules = [model_transformer, model_pool_layer])
    return custom_model_construct

def read_text_from_pdf(path):
    all_text = ""
    with pdfplumber.open(path) as curr_pdf:
        for curr_page in curr_pdf.pages:
            all_text = all_text + curr_page.extract_text()
    return all_text