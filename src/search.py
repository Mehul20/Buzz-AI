import faiss
from sentence_transformers import SentenceTransformer
from utils import read_file
import numpy as np

def similarity_for_query(user_query):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index("../Processed/faiss_index.index")
    course_ids = np.load("../Processed/course_ids.npy", allow_pickle=True)

    vectorized_query = model.encode(user_query).astype("float32").reshape(1, -1)
    _, indices = index.search(vectorized_query, 15)

    topIndices = list(indices[0])
    top_results = []
    for index in topIndices:
        top_results.append(course_ids[index])
    return top_results

def convert_top_results_into_data(top_results, subject):
    data = read_file("../Processing/data_clean.json")
    for curr_result in top_results:
        class_name = data[curr_result]["Name"]
        curr_subject = curr_result.split(" ")[0]
        #class_description = data[curr_result]["Description"]
        if len(subject) == 0 or curr_subject in subject:
            print(curr_result, class_name)

user_query = "Cryptography"
subject = ["CS"] # This needs can be empty if you want all classes
top_results = similarity_for_query(user_query)
convert_top_results_into_data(top_results, subject)