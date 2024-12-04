import os
import pandas as pd
from search import process_query
from utils import get_models

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
    level = ground_truth["level"]

    model_names = [get_models()[-1]]

    for model in model_names:
        overlapping_results = 0
        ground_truth_results = 0
        for i in range(len(query)):
            expected_classes = convert_string_to_list(expected_results[i])
            subj = convert_string_to_list(subjects[i])
            model_result = search_model_results(model, query[i], subj, level[i])
            for result in model_result:
                if result in expected_classes:
                    overlapping_results += 1
            ground_truth_results += len(expected_classes)
        accuracy = overlapping_results / ground_truth_results
        print(f"Accuracy for {model} is {accuracy}")

def search_model_results(model, query, subjects, level):
    top_results, _ = process_query(query, subjects, model, level)
    return top_results

test_model_accuracy()