import faiss
from sentence_transformers import SentenceTransformer
from utils import read_file, get_path, get_models
import numpy as np
from train import run_train

def similarity_for_query(user_query, model_name):
    path = get_path(model_name)
    model = SentenceTransformer(model_name)
    index = faiss.read_index(f"{path}/faiss_index.index")
    course_ids = np.load(f"{path}/course_ids.npy", allow_pickle=True)

    vectorized_query = model.encode(user_query).astype("float32").reshape(1, -1)
    _, indices = index.search(vectorized_query, 100)

    topIndices = list(indices[0])
    top_results = []
    for index in topIndices:
        top_results.append(course_ids[index])
    return top_results

def check_level_eligible(level, course):
    first_digit = int(course.split(" ")[1][0])
    if level == "grad":
        return first_digit > 5
    elif level == "undergrad":
        return first_digit < 5
    return True

def convert_top_results_into_data(top_results, subjects, level):
    data = read_file("../Processing/data_clean.json")
    baseline, counter = 20, 0
    final_results = []
    descriptions = []
    for curr_result in top_results:
        class_name = data[curr_result]["Name"]
        description = data[curr_result]["Description"]
        curr_subject = curr_result.split(" ")[0]
        level_eligible = check_level_eligible(level, curr_result)
        if (len(subjects) == 0 or curr_subject in subjects) and level_eligible:
            if counter > baseline:
                break
            counter = counter + 1
            # print(curr_result, class_name)
            # print(description)
            final_results.append(curr_result)
            descriptions.append(description)
    return final_results, descriptions

def process_query(user_query, subjects, model, level):
    top_results = similarity_for_query(user_query, model)
    top_results_for_sub, descriptions = convert_top_results_into_data(top_results, subjects, level)
    return top_results_for_sub, descriptions

def run_search(query, subject, model_name, level):
    top_results_for_sub, descriptions = process_query(query, subject, model_name, level)
    return top_results_for_sub, descriptions

if __name__ == "__main__":
    models = get_models()
    model_name = models[1]
    train = False
    if train:
        run_train(model=model_name)
    user_query = "reinforcement learning"
    subject = ["CS"]
    level = "undergrad" # Takes in "grad", "undergrad", or None
    top_results_for_sub, descriptions = run_search(user_query, subject, model_name, level)
    print(top_results_for_sub)
    print(descriptions)
