import faiss
from sentence_transformers import SentenceTransformer
from utils import read_file
import numpy as np

def similarity_for_query(user_query, model = 'all-MiniLM-L6-v2'):
    model = SentenceTransformer(model)
    index = faiss.read_index("../Processed/faiss_index.index")
    course_ids = np.load("../Processed/course_ids.npy", allow_pickle=True)

    vectorized_query = model.encode(user_query).astype("float32").reshape(1, -1)
    _, indices = index.search(vectorized_query, 50)

    topIndices = list(indices[0])
    top_results = []
    for index in topIndices:
        top_results.append(course_ids[index])
    return top_results

def convert_top_results_into_data(top_results, subjects):
    data = read_file("../Processing/data_clean.json")
    baseline, counter = 20, 0
    final_results = []
    for curr_result in top_results:
        class_name = data[curr_result]["Name"]
        curr_subject = curr_result.split(" ")[0]
        if len(subjects) == 0 or curr_subject in subjects:
            if counter > baseline:
                break
            counter = counter + 1
            print(curr_result, class_name)
            final_results.append(curr_result)
    return final_results

def process_query(user_query, subjects, model):
    top_results = similarity_for_query(user_query, model)
    top_results_for_sub = convert_top_results_into_data(top_results, subjects)
    return top_results_for_sub

if __name__ == "__main__":
    user_query = "reinforcement learning"
    subjects = ["CS"]
    model = 'all-MiniLM-L6-v2'
    process_query(user_query, subjects, model)