from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
import config

class HybridRetriever:
    """
    Hybrid retrieval system combining vector-based semantic search and keyword-based BM25 retrieval.

    This class implements a hybrid approach to movie retrieval, leveraging the strengths of both semantic similarity search using FAISS
    and keyword-based relevance ranking using BM25. It is designed to enhance search accuracy and recall by considering both semantic meaning
    and keyword matches in user queries.
    """
    def __init__(self, vector_index_path, bm25_corpus, metadata):
        """
        Initializes the HybridRetriever with necessary components for hybrid search.

        Args:
            vector_index_path (str): Path to the FAISS vector index file.
            bm25_corpus (list): Corpus of movie descriptions used for BM25 keyword-based retrieval.
            metadata (DataFrame): Movie metadata containing movie information such as genres and IMDb ratings.
        """
        self.vector_index = faiss.read_index(vector_index_path)
        self.bm25_corpus = bm25_corpus
        self.bm25 = BM25Okapi(bm25_corpus)
        self.metadata = metadata
        self.embeddings_generator = SentenceTransformer(config.EMBEDDING_MODEL)

    def semantic_search(self, query, top_k=10):
        """
        Performs semantic similarity search using a pre-trained SentenceTransformer model and a FAISS index.

        This method encodes the query into a vector embedding and uses FAISS to find the top_k most similar movie embeddings in the index.

        Args:
            query (str): The user's search query as a text string.
            top_k (int, optional): The number of top similar movies to retrieve. Defaults to 10.

        Returns:
            np.ndarray: Indices of the top_k most semantically similar movies in the FAISS index.
        """
        query_embedding = self.embeddings_generator.encode(query)
        _, I = self.vector_index.search(np.array([query_embedding]).astype("float32"), top_k*5)
        return I[0]

    def keyword_search_bm25(self, query, top_k=10):
        """
        Performs keyword-based retrieval using the BM25Okapi algorithm.

        This method tokenizes the query and uses the BM25 model to score each movie in the corpus based on keyword relevance.

        Args:
            query (str): The user's search query as a text string.
            top_k (int, optional): The number of top keyword-relevant movies to retrieve. Defaults to 10.

        Returns:
            np.ndarray: Indices of the top_k most keyword-relevant movies according to BM25.
        """
        
        tokenized_query = query.split(" ")
        bm25_scores = self.bm25.get_scores(tokenized_query)
        top_n_idx = np.argsort(bm25_scores)[::-1][:top_k*5]
        return top_n_idx

    def hybrid_search(self, query, top_k=10, filters=None):
        """
        Executes a hybrid search combining semantic and keyword-based retrieval, with optional filtering.

        This method integrates the results from both semantic_search and keyword_search_bm25 to provide a more comprehensive set of relevant movies.

        Args:
            query (str): The user's search query as a text string.
            top_k (int, optional): The number of top movies to return after hybrid search and filtering. Defaults to 10.
            filters (dict, optional): Dictionary containing liked and disliked genres. Defaults to None.

        Returns:
            list: A list of movie metadata dictionaries for the top_k movies that are relevant to the query,
                  considering both semantic and keyword relevance, and filtered by genre if specified.
        """
        
        semantic_results_idx = self.semantic_search(query, top_k=top_k)
        keyword_results_idx = self.keyword_search_bm25(query, top_k=top_k)

        hybrid_results_idx = np.unique(np.concatenate((semantic_results_idx, keyword_results_idx)))

        filtered_results = []
        if filters:
            positive_genres = set(filters['liked_genres'])
            negative_genres = set(filters['disliked_genres'])
            liked_stars = set(filters['liked_stars'])
            disliked_stars = set(filters['disliked_stars'])
            liked_directors = set(filters['liked_directors'])
            disliked_directors = set(filters['disliked_directors'])
            liked_years = set(filters['liked_years'])
            liked_rating = filters['liked_rating']

            for idx in semantic_results_idx:
                movie_metadata = self.metadata.iloc[idx]
                movie_genres = set(movie_metadata["genres"].split(", "))  # Convert to set for faster lookup
                movie_stars = set(movie_metadata["stars"].split(", "))  # Convert to set for faster lookup
                movie_directors = set(movie_metadata["directors"].split(", "))  # Convert to set for faster lookup
                movie_year = int(movie_metadata["year"])
                movie_rating = float(movie_metadata["imdb_rating"])

                if positive_genres and not any(p_genre in m_genre for p_genre in positive_genres for m_genre in movie_genres):
                    print("Positive Genre Not Found in", movie_metadata["title"])
                    print("Genres:", movie_genres)
                    continue

                if negative_genres and any(n_genre in m_genre for n_genre in negative_genres for m_genre in movie_genres):
                    print("Negative Genre Found in", movie_metadata["title"])
                    print("Genres:", movie_genres)
                    continue
                
                # if liked_stars and not any(l_star in m_star for l_star in liked_stars for m_star in movie_stars):
                #     print("Liked Star Not Found in", movie_metadata["title"])
                #     print("Stars:", movie_stars)
                #     continue

                # if disliked_stars and any(d_star in m_star for d_star in disliked_stars for m_star in movie_stars):
                #     print("Disliked Star Found in", movie_metadata["title"])
                #     print("Stars:", movie_stars)
                #     continue
            
                # if liked_directors and not any(l_director in m_director for l_director in liked_directors for m_director in movie_directors):
                #     print("Liked Director Not Found in", movie_metadata["title"])
                #     print("Directors:", movie_directors)
                #     continue

                # if disliked_directors and any(d_director in m_director for d_director in disliked_directors for m_director in movie_directors):
                #     print("Disliked Director Found in", movie_metadata["title"])
                #     print("Directors:", movie_directors)
                #     continue

                # if liked_years[0]:
                #     if liked_years[0] > movie_year:
                #         print(f"Year {movie_year} is not in the liked years list.")
                #         continue
                # if liked_years[1]:
                #     if movie_year > liked_years[1]:
                #         print(f"Year {movie_year} is not in the liked years list.")
                #         continue

                # if liked_rating and movie_rating < liked_rating:
                #     print(f"Movie Rating is less than the liked rating. It is {movie_year}.")
                #     continue

                filtered_results.append(movie_metadata)
        else:
            filtered_results = [self.metadata.iloc[idx] for idx in hybrid_results_idx]

        return filtered_results[:top_k]
