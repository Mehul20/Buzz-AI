import faiss
from sentence_transformers import SentenceTransformer
from utils import read_file
import numpy as np

def similarity_for_query(user_query):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index("../Processed/faiss_index.index")
    course_ids = np.load("../Processed/course_ids.npy", allow_pickle=True)

    vectorized_query = model.encode(user_query).astype("float32").reshape(1, -1)
    _, indices = index.search(vectorized_query, 2)

    topKIndices = list(indices[0])
    top_results = []
    for index in topKIndices:
        top_results.append(course_ids[index])
    return top_results

def convert_top_results_into_data(top_results):
    data = read_file("../Processing/data_clean.json")
    for curr_result in top_results:
        class_name = data[curr_result]["Name"]
        print(curr_result, class_name)

user_query = "computer archietecture"
top_results = similarity_for_query(user_query)
convert_top_results_into_data(top_results)