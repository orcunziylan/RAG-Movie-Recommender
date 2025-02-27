import config
import src.llm.google_gemini as llm

class RecommendationGenerator:
    """
    Generates movie recommendations using the Google Gemini Pro model.

    This class encapsulates the functionality to generate personalized movie recommendations based on user queries.
    It leverages the Gemini Pro model for its advanced natural language processing capabilities to understand user preferences
    and suggest relevant movies from a provided list.
    """
    def __init__(self):
        """
        Initializes the RecommendationGenerator with a specified Gemini model.

        The model name is specified in the config file.
        """
        
        self.model = llm.Gemini(config.RECOMMENDATION_MODEL)  # Initialize the generative model from the google.generativeai library.

    def generate(self, query, movies):
        """
        Generates movie recommendations based on a user query and a list of retrieved movies.

        This is the core method for generating movie recommendations. It takes a user query and a list of movies as input,
        constructs a detailed prompt for the Gemini Pro model, sends the prompt to the model, and returns the generated recommendations.

        Args:
            query (str): The user's movie query or preferences, as a string.
            movies (list): A list of movie dictionaries retrieved from the search engine.

        Returns:
            str: The generated movie recommendations as a text string.
        """


        rag_prompt = f"""
        Act as a movie recommendation engine. Use the following **retrieved list of movies** to suggest films tailored to the user's preferences.

        **Retrieved Movie List (Structured Data):**
        {movies}

        **Task:**
        1. **Analyze the user's query** (e.g., genre, mood, director, actor, or themes).
        2. **Search the retrieved list** for movies that match the criteria. Prioritize close semantic matches (e.g., genre alignment, director/actor overlap, or thematic relevance).
        3. If no exact matches, **adjust criteria** (e.g., suggest similar genres or related directors) and explain the reasoning. This is important for handling cases where the user's query is very specific or when the retrieved movie list is limited.
        4. **Format suggestions** as:
        - A **summary** of the user’s preferences, briefly capturing the essence of the user's query.
        - **3 recommendations**, providing a concise and manageable set of options for the user. 1 with hard constraints and 2 with soft constraints. Each recommendation should include:
          - Share columns of **Year**, **Length**, **PG Rating**, **IMDB Rating**, **Metascore**, **Genre**, **Director**, **Stars**, **Plot Summary**, **Link** for easy identification
          - **Reason**: A brief explanation of why the movie is recommended, explicitly linking it back to the user's query. Examples include 'Matches your interest in [genre]' or 'Features [actor]'.
          - A **note** if you relaxed criteria. This is crucial for transparency and helps the user understand why certain recommendations are made, especially when they are not direct matches to the initial query. Example: 'No comedies found; suggesting lighthearted dramas'.

        **Rules:**
        - Only suggest movies from the retrieved list. This constraint ensures that the recommendations are based on the provided search results and not from a broader database.
        - Avoid spoilers in recommendations to maintain user engagement and enjoyment of the movie-watching experience.
        - Use a friendly, engaging tone to make the recommendations more appealing and user-friendly.

        **Example Output:**
        'Based on your interest in **dark comedies** and **directors like Wes Anderson**, here are my picks:
        1. **The Grand Budapest Hotel** (2014)
          - Reason: Matches your interest in dark comedies and directors like Wes Anderson, featuring a charming and quirky cast that adds depth to the story.

          - Year:
          - Length: 138 minutes

          - PG Rating: PG-13
          - IMDB Rating: 8.9
          - Metascore: 78

          - Genre: Comedy, Drama
          - Director: Wes Anderson
          - Stars: Tom Hanks, Joaquin Phoenix

          - Plot Summary: A young man who becomes a curator of an old hotel in Bruges, Belgium, finds himself drawn into a world of secrets and intrigue.
          - Link: https://www.imdb.com/title/tt2464464/
          
        2. **Movie Title** (year)
          - Reason: Explain why user likes this movie?

          - Year:
          - Length:

          - PG Rating:
          - IMDB Rating:
          - Metascore:

          - Genre:
          - Director:
          - Stars:

          - Plot Summary: 
          - Link: 

        **User Query:** {query}

        """

        # Generate the response using the Gemini model
        return self.model.generate_response(rag_prompt, max_output_tokens=5000)
