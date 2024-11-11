import json

def read_file(filePath):
    with open(filePath, 'r') as f:
        data = json.load(f)
    return data