from sentence_transformers import SentenceTransformer
from utils import read_file

def bert_vectorization():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    data = read_file("../Processing/data_clean.json")
    vector_data = []
    for course_id in data.keys():
        course_description = data[course_id]["Description"]
        curr_vector = list(model.encode(course_description))
        vector_data_model = {
            "Course": course_id,
            "Vector": curr_vector,
        }
        vector_data.append(vector_data_model)
    return vector_data

bert_vectorization()
