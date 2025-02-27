import streamlit as st
from ui.components.utils import load_movie_retriever, load_movie_reranker, load_recommendation_generator, load_hyde_generator, load_feature_extractor
import sqlite3
import pandas as pd

# Set the page configuration to use a wide layout
st.set_page_config(page_title="Movie Recommender App", layout="wide")

# Database connection
conn = sqlite3.connect('data/processed/movies.db')

# Load data into pandas DataFrame
df = pd.read_sql_query("SELECT * FROM movies", conn)
conn.close()

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Movie Recommender App")

    # Query section: remains at the top and centered by default
    query = st.text_input("Enter movie query")

    # Columns section for displaying processing messages and results
    col1, col2 = st.columns([1, 2])

    # Left column: load models and display processing info
    with col1:
        retriever = load_movie_retriever()
        reranker = load_movie_reranker()
        generator = load_recommendation_generator()
        hyde = load_hyde_generator()
        feature_extractor = load_feature_extractor()

        # Check if models are loaded correctly
        if (retriever or reranker or generator or hyde) is None:
            st.write("Search engine not initialized")
            return

    if query:
        # Right column: show results inside expanders (closed by default)
        with col2:

            # Generate genre based on the query
            extracted_features = feature_extractor.extract_features(query=query)
            with st.expander("Generated features", expanded=False):
                st.write(extracted_features)

            # Generate HyDE based on the query
            generated_hyde = hyde.generate(query=query)
            with st.expander("Generated HyDE", expanded=False):
                st.write(generated_hyde)

            # Run the search process if a query is provided
            initial_results = retriever.hybrid_search(query=generated_hyde, 
                                                      top_k=10,
                                                      filters=extracted_features
                                                      )

            with st.expander("Initial Search Results", expanded=False):
                st.write(initial_results)

            # Rerank the initial results
            if initial_results:
                reranked_results = reranker.rerank(
                    query=generated_hyde,
                    candidates=initial_results,
                    combine_score=lambda score, rating: score + 0.1 * rating
                )

            # Expander for search results
            movie_list = []
            with st.expander("Search Movies", expanded=False):
                if initial_results:
                    st.write("Search Results (Reranked):")
                    for movie in reranked_results:
                        st.write(f" -> **{movie['title']}** ({movie['genres']}) - IMDb Rating: {movie['imdb_rating']}")
                        st.write(f"Plot: {movie['plot'][:200]}...")

                        # Find the title in the DataFrame and get its whole row and save it to a list
                        exclude = ['summary', 'synopsis', 'review_title', 'review_rating', 'review_text']
                        movie_row = df[df['title'] == movie['title']].iloc[0].drop(columns=exclude)
                        movie_list.append(movie_row)

                else:
                    st.write("No movies found matching your query.")

            # Expander for movie recommendations (only if search results exist)
            if initial_results:
                with st.expander("Movie Recommendations", expanded=False):
                    response = generator.generate(query=query, movies=movie_list)
                    st.write(response)
            else:
                # Optionally, you can also notify the user outside the expanders
                st.write("No movies found matching your query.")

if __name__ == "__main__":
    main()
