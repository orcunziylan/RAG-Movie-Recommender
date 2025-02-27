# Movie Recommender System Using Retrieval-Augmented Generation, RAG

## Overview

This project implements a movie recommendation system that combines several techniques, including web scraping, data preprocessing, vector database creation, and a Streamlit user interface, to provide personalized movie recommendations based on user queries. The system leverages large language models (LLMs) to understand user preferences and generate relevant recommendations.

## Features

-   **Web Scraping**: Scrapes movie data from IMDb using a custom scraper.
-   **Data Preprocessing**: Cleans and prepares the scraped data for further analysis.
-   **Vector Database**: Creates a FAISS vector database to store movie embeddings for efficient similarity search.
-   **Hybrid Retrieval**: Combines semantic search and keyword-based retrieval for improved accuracy.
-   **HyDE (Hypothetical Document Embeddings)**: Generates hypothetical movie synopses based on user queries to improve search relevance.
-   **Feature Extraction**: Extracts movie features (liked/disliked genres, stars, directors, years, rating) from a user query to hard filter the results.
-   **Reranking**: Reranks the search results using a cross-encoder model.
-   **Recommendation Generation**: Generates personalized movie recommendations using LLMs.
-   **User Interface**: Provides a Streamlit UI for users to interact with the system.

## Technologies Used

-   Python 3.11
-   Streamlit
-   Sentence Transformers
-   FAISS
-   Rank BM25
-   Google Gemini API
-   Pandas
-   SQLite
-   Selenium
-   Beautiful Soup

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd movie-recommender-mle
    ```

2.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up the environment variables:**

    -   Obtain an API key for the Google Gemini API.
    -   Set the `GEMINI_API_KEY` environment variable with your API key in ".env".

## Usage

1.  **Scrape and build the database:**

    -   Derive your own link with your preferences from the base link: `https://www.imdb.com/search/title/`

    ```bash
    python -m src.scraping.run_scraper --search basic --load-pages --dry-run --link "<your_own_link>"
    ```

    -   `--search`: \[basic, advanced] / required
        -   `basic`: Includes title, year, IMDb rating, Metascore, PG rating, votes, length, plot, summary, synopsis, directors, stars, genres, review title, review rating, review text, and link.
        -   `advanced`: Also populates summary, synopsis.
    -   `--load-pages`: Optional. Add this if you want to click the "show more" button in the link you created.
    -   `--dry-run`: Optional. Run without saving to the database.
    -   `--link`: Required. Add your own link here.

2.  **Build the vector database (FAISS):**

    ```bash
    python -m src.data_preprocessing.preprocess_data --vd faiss
    ```

    -   `--vd`: vector database options \['faiss', 'qdrant']

3.  **Run the Streamlit UI:**

    ```bash
    streamlit run app.py
    ```

## Project Structure

-   `app.py`: Main application file for the Streamlit UI.
-   `config.py`: Configuration settings for the application.
-   `data/`: Directory containing the processed data and databases.
-   `src/`: Source code directory.
    -   `core/`: Core functionalities of the system.
        -   `feature_extractor.py`: Extracts movie features from user queries.
        -   `generation.py`: Generates movie recommendations using LLMs.
        -   `hyde.py`: Generates hypothetical movie synopses based on user queries.
        -   `reranking.py`: Reranks movie candidates using a cross-encoder model.
        -   `retrieval.py`: Implements hybrid retrieval system combining vector-based semantic search and keyword-based BM25 retrieval.
        -   `summarization.py`: Summarizes movie information using a language model.
    -   `data_preprocessing/`: Data preprocessing scripts.
        -   `preprocess_data.py`: Preprocesses the movie data and builds the vector database.
    -   `database/`: Database management scripts.
        -   `db_manager.py`: Manages the SQLite database.
    -   `llm/`: LLM related scripts.
        -   `google_gemini.py`: Integrates with the Google Gemini API for text generation.
    -   `scraping/`: Web scraping scripts.
        -   `imdb_scraper.py`: Scrapes movie data from IMDb.
        -   `run_scraper.py`: Runs the web scraper.
        -   `utils/`: Utility functions for scraping.
    -   `ui/`: User interface components.
        -   `components/`: UI components.
            -   `utils.py`: Utility functions for the UI.