import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

def similarity_for_query(query_string):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index("../Processed/faiss_index.index")
    course_ids = np.load("./Processed/course_ids.npy", allow_pickle=True)

    vectorized_query = model.encode(query_string).astype("float32").reshape(1, -1)
    _, indices = index.search(vectorized_query, 2)
    topKIndices = indices[0].split(" ")
    print(topKIndices)
    print(course_ids[int(topKIndices[0])])

similarity_for_query("computer archietecture")