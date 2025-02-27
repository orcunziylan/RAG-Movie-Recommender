# Movie Recommender System Using Retrieval-Augmented Generation, RAG

## Overview

This project implements a movie recommendation system that combines several techniques, including web scraping, data preprocessing, vector database creation, and a Streamlit user interface, to provide personalized movie recommendations based on user queries. The system leverages large language models (LLMs) to understand user preferences and generate relevant recommendations.

## Features

-   **Web Scraping:** Scrapes movie data from IMDb using a custom scraper.
-   **Data Preprocessing:** Cleans and prepares the scraped data for further analysis.
-   **Vector Database:** Creates a FAISS vector database to store movie embeddings for efficient similarity search.
-   **Hybrid Retrieval:** Combines semantic search and keyword-based retrieval for improved accuracy.
-   **HyDE (Hypothetical Document Embeddings):** Generates hypothetical movie synopses based on user queries to improve search relevance.
-   **Feature Extraction:** Extracts movie features (liked/disliked genres, stars, directors, years, rating) from a user query to hard filter the results.
-   **Reranking:** Reranks the search results using a cross-encoder model.
-   **Recommendation Generation:** Generates personalized movie recommendations using LLMs.
-   **User Interface:** Provides a Streamlit UI for users to interact with the system.
-   **Docker:** Containerization of the application for easy deployment.

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
-   Docker

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/orcunziylan/RAG-Movie-Recommender
    cd RAG-Movie-Recommender
    ```


2. **Create a Virtual Environment:**

    Create and activate a virtual environment to isolate project dependencies:

    - On macOS/Linux:
      ```bash
      python -m venv venv
      source venv/bin/activate
      ```

    - On Windows:
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```

3. **Install the dependencies (Development Environment):**

    ```bash
    pip install -r requirements.txt
    ```

    > **Note:**  
    > - The `requirements.txt` file installs the full set of dependencies required for development, including libraries for web scraping (e.g., Selenium, Beautiful Soup) and additional tools.
    > - For production deployments, a slimmer set of runtime dependencies is defined in `requirements_app.txt`.

3.  **Set up the environment variables:**

    -   Obtain an API key for the Google Gemini API.
    -   Set the `GEMINI_API_KEY` environment variable with your API key in ".env".
    -   Configurate 'config.py' to define paths and parameters.

## Usage 

1.  **Scrape and build the database:**

    -   Derive your own link with your preferences from the base link: `https://www.imdb.com/search/title/`

    ```bash
    python -m src.scraping.run_scraper --search basic --load-pages --link "<your_own_link>"
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

## Dockerization / Optional Deployment

For production deployments, you can containerize the application using Docker. To reduce the final image size, the Docker build uses the `requirements_app.txt` file—which installs only the essential runtime dependencies (excluding development libraries).

The `Dockerfile`, `docker-compose.yml`, and `.dockerignore` files are provided for your convenience.

### To Build and Run the Docker Container:

- **Using Docker CLI:**

    ```bash
    docker build -t movie-recommender .
    docker run -p 8501:8501 movie-recommender
    ```

- **Using Docker Compose:**

    ```bash
    docker-compose up
    ```

Once the container is running, access the app at [http://localhost:8501](http://localhost:8501).

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
