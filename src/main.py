from sentence_transformers import SentenceTransformer
from utils import read_file
import numpy as np
import faiss

def bert_vectorization():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    data = read_file("../Processing/data_clean.json")
    vector_data_obj = {}
    all_vectors = []
    for course_id in data.keys():
        course_description = data[course_id]["Description"]
        curr_vector = list(model.encode(course_description))
        vector_data_obj[tuple(curr_vector)] = course_id
        all_vectors.append(curr_vector)
    all_vectors = np.array(all_vectors).astype("float32")
    return vector_data_obj, all_vectors

def facebook_AI_Search(all_vectors):
    embedding_dimension = all_vectors.shape[1]
    faiss_index = faiss.IndexFlatL2(embedding_dimension)
    faiss_index.add(all_vectors)
    return faiss_index

vector_obj, all_vectors = bert_vectorization()
faiss_index = facebook_AI_Search(all_vectors)
