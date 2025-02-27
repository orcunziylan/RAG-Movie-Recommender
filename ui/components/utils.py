import streamlit as st
import pandas as pd
import sqlite3

from src.core.generation import RecommendationGenerator
from src.core.retrieval import HybridRetriever
from src.core.reranking import Reranker
from src.core.hyde import Hyde
from src.core.feature_extractor import FeatureExtractor

@st.cache_resource
def load_recommendation_generator():
    """Loads the recommendation generator model."""
    generator = RecommendationGenerator()
    st.success("Recommendation generator model loaded.")
    return generator

@st.cache_resource
def load_feature_extractor():
    """Loads the feature extractor model."""
    conn = sqlite3.connect('data/processed/movies.db')

    # Load data into pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM movies", conn)
    conn.close()

    all_genres = df['genres'].str.split(', ').explode().unique()
    print("All genres:", len(all_genres))

    extractor = FeatureExtractor(all_genres)
    st.success("Genre extraction model loaded.")
    return extractor

@st.cache_resource
def load_movie_retriever():
    """Loads the movie retriever model."""
    try:
        conn = sqlite3.connect('data/processed/movies_summaries.db')
        df_summaries = pd.read_sql_query("SELECT * FROM movies_summaries", conn)
        conn.close()

        conn = sqlite3.connect('data/processed/movies.db')
        df_movies = pd.read_sql_query("SELECT * FROM movies", conn)
        conn.close()

    except FileNotFoundError:
        st.error("Data file not found. Please run data preprocessing script.")
        return None
    retriever = HybridRetriever(
        vector_index_path="data/faiss_index.bin",
        bm25_corpus=df_summaries["generated_summary"].tolist(),
        metadata=df_movies
    )
    st.success("Movie data loaded and search engine initialized.")
    return retriever

@st.cache_resource
def load_movie_reranker():
    """Loads the movie reranker model."""
    reranker = Reranker()
    st.success("Reranking model loaded.")
    return reranker

@st.cache_resource
def load_hyde_generator():
    """Loads the Hyde generator model."""
    hyde = Hyde()
    st.success("Hyde generator loaded.")
    return hyde
