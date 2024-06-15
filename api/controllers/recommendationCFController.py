from typing import List
import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pymongo
import os
# Lấy đường dẫn tuyệt đối của thư mục hiện tại
current_directory = os.path.dirname(os.path.abspath(__file__))

# Xác định đường dẫn tương đối của tệp tin "fake_reviews.json"
relative_path = os.path.join(current_directory, '..', 'data', 'fake_reviews.json')

# Kết nối tới MongoDB
client = pymongo.MongoClient('mongodb+srv://moribook:Mori123456@cluster0.xdqbzc5.mongodb.net')

class RecommendationCFController:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb+srv://moribook:Mori123456@cluster0.xdqbzc5.mongodb.net/moridb')
        self.db = self.client['moridb']  # Thay 'your_database_name' bằng tên database của bạn
        self.user_book_matrix = None
        self.user_similarity_df = None
        self.book_similarity_df = None

    def load_fake_data(self):
        with open(relative_path, encoding='utf-8') as f:
            fake_reviews = json.load(f)
        df_fake_reviews = pd.DataFrame(fake_reviews['reviews'])
        df_fake_reviews = df_fake_reviews[['user', 'book_id', 'rating']] 
        return df_fake_reviews

    def load_real_data(self):
        reviews = self.db.reviews.find()
        df_real_reviews = pd.DataFrame(reviews)
        df_real_reviews = df_real_reviews[['user', 'book_id', 'rating']]  # Giữ lại các cột cần thiết
        return df_real_reviews

    def load_data(self):
        # Load dữ liệu giả lập
        df_fake_reviews = self.load_fake_data()

        # Load dữ liệu thực tế từ MongoDB
        df_real_reviews = self.load_real_data()

        # Gộp dữ liệu giả lập và dữ liệu thực tế
        df_reviews = pd.concat([df_fake_reviews, df_real_reviews], ignore_index=True)

        # Tạo ma trận người dùng - sách
        self.user_book_matrix = df_reviews.pivot_table(index='user', columns='book_id', values='rating').fillna(0)
        print("user_book_matrix", self.user_book_matrix)
        self.user_similarity_df = pd.DataFrame(cosine_similarity(self.user_book_matrix), index=self.user_book_matrix.index, columns=self.user_book_matrix.index)
        self.book_similarity_df = pd.DataFrame(cosine_similarity(self.user_book_matrix.T), index=self.user_book_matrix.columns, columns=self.user_book_matrix.columns)
    
    def get_similar_users(self, user_id, n=5):
        similar_users = self.user_similarity_df[user_id].sort_values(ascending=False)[1:n+1]
        return similar_users
    
    def recommend_books_user(self, user_id, n=5):
        similar_users = self.get_similar_users(user_id, n)
        similar_users_ratings = self.user_book_matrix.loc[similar_users.index]
        weights = similar_users.values.reshape(-1, 1)
        weighted_ratings = similar_users_ratings * weights
        book_recommendations = weighted_ratings.sum(axis=0) / weights.sum()
        user_ratings = self.user_book_matrix.loc[user_id]
        book_recommendations = book_recommendations[user_ratings == 0]
        return book_recommendations.sort_values(ascending=False).head(n)
    
    def get_similar_books(self, book_id, n=15):
        similar_books = self.book_similarity_df[book_id].sort_values(ascending=False)[1:n+1]
        return similar_books
    
    def recommend_books_item(self, user_id, n=5):
        user_ratings = self.user_book_matrix.loc[user_id]
        
        # Khởi tạo danh sách để lưu trữ các series tương tự
        similar_books_list = []
        
        # Lặp qua các sách đã được đánh giá bởi người dùng và nhân với hệ số tương tự
        for book_id, rating in user_ratings[user_ratings > 0].items():
            similar_books_list.append(self.book_similarity_df[book_id] * rating)
        
        # Sử dụng pd.concat để kết hợp các series trong danh sách
        if similar_books_list:
            similar_books = pd.concat(similar_books_list)
            similar_books = similar_books.groupby(similar_books.index).sum()
            similar_books = similar_books[~similar_books.index.isin(user_ratings[user_ratings > 0].index)]
            return similar_books.sort_values(ascending=False).head(n)
        else:
            return pd.Series(dtype='float64')  # Trả về một series rỗng nếu không có sách tương tự
    
    def recommend_books_based_on_history(self, user_history: dict, n: int):
        user_read_books = user_history
        print("user history",user_read_books)
        if not user_read_books:
            return []
        
        similar_books_list = []
        for book_id in user_read_books:
            similar_books_list.append(self.book_similarity_df[book_id])
        
        similar_books = pd.concat(similar_books_list)
        similar_books = similar_books.groupby(similar_books.index).sum()
        similar_books = similar_books[~similar_books.index.isin(user_read_books)]

        recommended_books = similar_books.sort_values(ascending=False).head(n).index.tolist()
        return recommended_books


# controller = RecommendationCFController()
# controller.load_data()

# # Gợi ý sách cho người dùng dựa trên người dùng tương tự
# user_id = 'account1'
# recommended_books_user = controller.recommend_books_user(user_id, n=5)
# print("Recommended Books for User:", user_id)
# print(recommended_books_user)

# # Gợi ý sách cho người dùng dựa trên các sách tương tự
# user_id = 'account1'
# recommended_books_item = controller.recommend_books_item(user_id, n=5)
# print("Recommended Books for User based on Item:", user_id)
# print(recommended_books_item)

# # Gợi ý sách cho người dùng dựa trên lịch sử đọc sách
# user_id = 'account00'
# user_history = {'account00': ['664c89478de582782e625255', '65807a589eac8d942b0d7647']}
# recommended_books_history = controller.recommend_books_based_on_history(user_id, user_history, n=5)
# print("Recommended Books for User based on History:", user_id)
# print(recommended_books_history)