import faiss
from utils import read_pickle_dictionary

index = faiss.read_index("../Processed/faiss_index.index")
vector_dictionary = read_pickle_dictionary("../Processed/vector_map.pkl")