import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

class PersonalizedSearchRecommender:
    def __init__(self, num_courses, user_data_dir='../UserData'):
        self.num_courses = num_courses
        self.user_data_dir = user_data_dir
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.read_index("../Processed/faiss_index.index")
        self.course_ids = np.load("../Processed/course_ids.npy", allow_pickle=True)
        self.course_embeddings = self.index.reconstruct_n(0, self.index.ntotal)
        
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)

    def get_user_matrix(self, username):
        user_file = os.path.join(self.user_data_dir, f"{username}.npy")
        if os.path.exists(user_file):
            return np.load(user_file)
        else:
            return np.zeros(self.num_courses)

    def update_user_matrix(self, username, course_id, rating):
        user_matrix = self.get_user_matrix(username)
        normalized_rating = (rating - 1) / 4  # Transform 1-5 to 0-1
        user_matrix[course_id] = normalized_rating
        user_file = os.path.join(self.user_data_dir, f"{username}.npy")
        np.save(user_file, user_matrix)

    def get_personalized_query_vector(self, username, query_vector):
        user_matrix = self.get_user_matrix(username)
        
        weighted_embedding = np.zeros_like(query_vector)
        total_weight = 0
        for course_id, rating in enumerate(user_matrix):
            if rating > 0:
                weighted_embedding += rating * self.course_embeddings[course_id]
                total_weight += rating
        
        if total_weight > 0:
            weighted_embedding /= total_weight
            
            # Combine the original query vector with the personalized vector
            alpha = 0.7  # Weight for the original query. Adjust as needed.
            personalized_query = alpha * query_vector + (1 - alpha) * weighted_embedding
            print("built personalized query vector")
            return personalized_query
        else:
            return query_vector

    def similarity_search(self, user_query, username, top_k=15):
        query_vector = self.model.encode(user_query).astype("float32").reshape(1, -1)
        personalized_query = self.get_personalized_query_vector(username, query_vector)
        
        _, indices = self.index.search(personalized_query, top_k)
        
        topIndices = list(indices[0])
        recommendations = [self.course_ids[index] for index in topIndices]
        
        return recommendations

def get_user_ratings(recommendations):
    ratings = {}
    for item in recommendations:
        while True:
            try:
                rating = int(input(f"Please rate course {item} (1-5, or 0 to skip): "))
                if 0 <= rating <= 5:
                    if rating == 0:
                        break
                    ratings[item] = rating
                    break
                else:
                    print("Please enter a rating between 0 and 5.")
            except ValueError:
                print("Please enter a valid integer rating.")
    return ratings

def main():
    num_courses = len(np.load("../Processed/course_ids.npy", allow_pickle=True))
    recommender = PersonalizedSearchRecommender(num_courses)

    username = input("Please enter your username: ")
    print(f"Welcome, {username}!")

    while True:
        action = input("Enter 'r' for recommendations or 'q' to quit: ")
        if action.lower() == 'q':
            break
        elif action.lower() == 'r':
            user_query = input("Enter your query for course recommendations: ")
            recommendations = recommender.similarity_search(user_query, username)
            print("Here are your recommendations:", recommendations)
            
            ratings = get_user_ratings(recommendations)
            
            for course_id, rating in ratings.items():
                course_index = np.where(recommender.course_ids == course_id)[0][0]
                recommender.update_user_matrix(username, course_index, rating)
            
            print("Thank you for your ratings! Your recommendations will improve next time.")
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()