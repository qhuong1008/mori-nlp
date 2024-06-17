from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from concurrent.futures import ThreadPoolExecutor

# Load model sentence-transformers
model = SentenceTransformer('all-MiniLM-L6-v2')


class RecommendationCBController:
    # Hàm để lấy embeddings
    def get_embeddings(self, texts):
        return model.encode(texts)

    # Hàm để tính toán độ tương đồng cosine
    def compute_similarity(self, vec1, vec2):
        return cosine_similarity([vec1], [vec2])[0][0]

    def process_book(self, book, all_books):
        book_texts = [book["name"], book["author"], book["intro"], " ".join(book["tags"])]
        book_embedding = self.get_embeddings(book_texts)

        recommendations = []

        for other_book in all_books:
            if book['_id'] == other_book['_id']:
                continue

            other_book_texts = [other_book["name"], other_book["author"], other_book["intro"], " ".join(other_book["tags"])]
            other_book_embedding = self.get_embeddings(other_book_texts)

            name_similarity = self.compute_similarity(book_embedding[0], other_book_embedding[0])
            author_similarity = self.compute_similarity(book_embedding[1], other_book_embedding[1])
            intro_similarity = self.compute_similarity(book_embedding[2], other_book_embedding[2])
            tags_similarity = self.compute_similarity(book_embedding[3], other_book_embedding[3])

            name_weight = 0.2
            author_weight = 0.1
            intro_weight = 0.35
            tags_weight = 0.35

            total_similarity = (name_similarity * name_weight) + (author_similarity * author_weight) + \
                                (intro_similarity * intro_weight) + (tags_similarity * tags_weight)

            recommendations.append({
                "book_id": other_book["_id"],
                "similarity": total_similarity
            })

        recommendations.sort(key=lambda x: x["similarity"], reverse=True)
        result = [rec["book_id"] for rec in recommendations][:10]

        return {
            "book_id": book["_id"],
            "recommendations": result
        }

    def generate_recommendations(self, all_books: dict):
        recommendations_per_book = []

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(self.process_book, book, all_books) for book in all_books]

            for future in futures:
                result = future.result()
                recommendations_per_book.append(result)

        return recommendations_per_book
