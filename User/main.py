import os
import numpy as np
import sys
sys.path.append('../')

# from src.utils import read_file
from src.search import similarity_for_query

class UserRecommender:
    def __init__(self, num_courses, user_data_dir='../User/user_profiles'):
        self.num_courses = num_courses
        self.user_data_dir = user_data_dir
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
        user_matrix[course_id] = rating
        user_file = os.path.join(self.user_data_dir, f"{username}.npy")
        np.save(user_file, user_matrix)

def user_login():
    username = input("Please enter your username: ")
    print(f"Welcome to BuzzAI, {username}!")
    return username

def convert_top_results_into_data(top_results, subject):
    data = read_file("../Processing/data_clean.json")
    for curr_result in top_results:
        class_name = data[curr_result]["Name"]
        curr_subject = curr_result.split(" ")[0]
        print(curr_subject)

def get_user_ratings(recommendations):
    ratings = {}
    for item in recommendations:
        while True:
            try:
                rating = int(input(f"Please rate item {item} (1-5): "))
                if 1 <= rating <= 5:
                    ratings[item] = rating
                    break
                else:
                    print("Please enter a rating between 1 and 5.")
            except ValueError:
                print("Please enter a valid integer rating.")
    return ratings



if __name__ == "__main__":
    num_courses = len(np.load("../Processed/course_ids.npy", allow_pickle=True))
    user_recommender = UserRecommender(num_courses)
    username = user_login()
    user_matrix = user_recommender.get_user_matrix(username)

    while True:
        action = input("Enter 'r' for recommendations or 'q' to quit: ")
        if action.lower() == 'q':
            break
        elif action.lower() == 'r':
            user_query = input("Enter your query for course recommendations: ")
            recommendations, recommend_idx = similarity_for_query(user_query)
            print("Here are your recommendations:", recommendations)
            
            ratings = get_user_ratings(recommendations)
            
            for (course_id, rating), course_idx in zip(ratings.items(), recommend_idx):
                user_recommender.update_user_matrix(username, course_idx, rating)
            
            print("Thank you for your ratings! Your recommendations will improve next time.")
        else:
            print("Invalid input. Please try again.")
