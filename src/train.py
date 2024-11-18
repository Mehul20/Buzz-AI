from sentence_transformers import SentenceTransformer
from utils import read_file, check_relevant_special_topics, get_path, get_model_name
import numpy as np
import faiss

def vectorization(model_name):
    model = SentenceTransformer(model_name)
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
    print(f"The {model_name} model has been successfully trained on {i} courses!")
    all_vectors = np.array(all_vectors).astype("float32")
    path = get_path(model=model_name)
    np.save(f"{path}/course_ids.npy", course_ids)
    return all_vectors

def facebook_AI_Search(all_vectors, model_name):
    embedding_dimension = all_vectors.shape[1]
    faiss_index = faiss.IndexFlatL2(embedding_dimension)
    faiss_index.add(all_vectors)
    path = get_path(model=model_name)
    faiss.write_index(faiss_index, f"{path}/faiss_index.index")

def run_train(model):
    all_vectors = vectorization(model_name=model)
    facebook_AI_Search(all_vectors, model_name=model)

if __name__ == "__main__":
    model_name = get_model_name()
    run_train(model=model_name)