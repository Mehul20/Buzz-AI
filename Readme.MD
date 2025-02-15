# Buzz-AI

## Codebase

Enhancing Georgia Tech Course Discovery Using Transformer-Based Semantic Search

- `DataSource` has all the data that we have worked with.

- `processing` has all the scripts for pre-processing and scraping data.

- `src` has all the code required for training and searching.

- `Syllabus` will have all the Syllabus PDFs

- `User` and `UserData` have code and dynamic files for Adpative Recommendations/Collaborative Filtering.

## Setup

```
pip install faiss-cpu sentence-transformers numpy pandas pdfplumber
```

## Search Queries

- -q: User Query - String (Mandatory)

- -l: Level - "grad", "undergrad" (Optional)

- -c: Courses - "MGT", "CS", "CSE" (Optional)

You can run:

```
cd src 
python3 search.py -q "Poker Theory" -c "CS,CSE" -l "grad"
```

You can change the flags as needed and required.

## Adaptive Recommendations

```
cd User 
python3 main.py
```

## Contributors
- Mehul Rastogi
- Akshat Karwa
- Pranay Begwani
- Vidushi Maheshwari
