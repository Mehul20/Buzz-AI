import json
import pickle
import os

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
    models = [bert_model, RoBERTa_model, multi_qa]
    return models