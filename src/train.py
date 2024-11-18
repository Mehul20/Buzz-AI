from sentence_transformers import SentenceTransformer
from utils import read_file, check_relevant_special_topics
import numpy as np
import faiss

def bert_vectorization(model = 'all-MiniLM-L6-v2'):
    model = SentenceTransformer(model)
    data = read_file("../Processing/data_clean.json")
    course_ids = []
    all_vectors = []
    for course_id in data.keys():
        course_vector = "Name:" + data[course_id]["Name"]  + ". Course Description:" + data[course_id]["Description"]
        sp, code = check_relevant_special_topics(course_id)
        if sp:
            research_area = data[course_id]["Section Information"][code]["Research Area"]
            if len(research_area) > 0:
                course_vector += ". Professor Background: " + research_area
        curr_vector = list(model.encode(course_vector))
        course_ids.append(course_id)
        all_vectors.append(curr_vector)
    all_vectors = np.array(all_vectors).astype("float32")
    np.save("../Processed/course_ids.npy", course_ids)
    return all_vectors

def facebook_AI_Search(all_vectors):
    embedding_dimension = all_vectors.shape[1]
    faiss_index = faiss.IndexFlatL2(embedding_dimension)
    faiss_index.add(all_vectors)
    faiss.write_index(faiss_index, "../Processed/faiss_index.index")

all_vectors = bert_vectorization()
facebook_AI_Search(all_vectors)