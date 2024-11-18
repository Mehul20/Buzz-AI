import os
import pandas as pd
from search import process_query
from train import bert_vectorization, facebook_AI_Search


def read_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist")
    testing_data = pd.read_csv(file_path)
    return testing_data

def convert_string_to_list(string):
    if type(string) == float:
        return []
    return string.split(",")

def test_model_accuracy():
    ground_truth = read_csv("../DataSource/ground_truth_testing.csv")
    subjects = ground_truth["subject"]
    query = ground_truth["query"]
    expected_results = ground_truth["ground_truth"]

    model_names = ["all-MiniLM-L6-v2"]

    for model in model_names:
        #vectorize_models(model)
        overlapping_results = 0
        ground_truth_results = 0
        for i in range(len(query)):
            expected_classes = convert_string_to_list(expected_results[i])
            subj = convert_string_to_list(subjects[i])
            model_result = search_model_results(model, query[i], subj)
            for result in model_result:
                if result in expected_classes:
                    overlapping_results += 1
            ground_truth_results += len(expected_classes)
        accuracy = overlapping_results / ground_truth_results
        print(f"Accuracy for {model} is {accuracy}")

def vectorize_models(model_name):
    all_vectors = bert_vectorization(model_name)
    facebook_AI_Search(all_vectors)

def search_model_results(model, query, subjects):
    top_results = process_query(query, subjects, model)
    return top_results

test_model_accuracy()