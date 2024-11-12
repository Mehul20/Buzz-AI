import json
import pickle

def read_file(filePath):
    with open(filePath, "r") as file:
        data = json.load(file)
    return data

# Unused - Might need them in the future
def save_pickle_dictionary(dictionary, filePath):
    with open(filePath, "wb") as file:
        pickle.dump(dictionary, file)

def read_pickle_dictionary(filePath):
    with open(filePath, "rb") as file:
        dictionary_found = pickle.load(file)
    return dictionary_found