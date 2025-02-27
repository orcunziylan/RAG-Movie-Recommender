import config
from src.llm.google_gemini import Gemini

class FeatureExtractor:
    """
    Extracts movie features from a user query using a language model.
    """
    def __init__(self, genres_list=[]):
        """
        Initializes the FeatureExtractor with a Gemini language model and a list of genres.

        Args:
            genres_list (list, optional): A list of movie genres to consider. Defaults to a predefined list.
        """
        self.gemini = Gemini(model_info=config.GENRE_EXTRACTOR_MODEL, json_output=True)
        # Use provided genres list or default to a predefined list
        if len(genres_list):
            self.genres_list = genres_list
        else:
            self.genres_list = [
                "action", "comedy", "drama", "horror", "thriller", "sci-fi",
                "romance", "mystery", "crime", "animation", "adventure", "fantasy"
            ]

    def extract_features(self, query: str) -> dict:
        """
        Extracts movie features (liked/disliked genres, stars, directors, years, rating) from a user query.

        Args:
            query (str): The user's query expressing their movie preferences.

        Returns:
            dict: A dictionary containing the extracted movie features.
        """

        prompt = f"""
        Based on the user query: '{query}', identify the movie features that the user might likes and dislikes.

        Here is an example about how to fill columns;
        liked_genres: list[str] # list of genres the user likes choosen from the genres list
        disliked_genres: list[str] # list of genres the user dislikes choosen from the genres list
        liked_stars: list[str] # list of stars the user likes (optional)
        disliked_stars: list[str] # list of stars the user dislikes (optional)
        liked_directors: list[str] # list of directors the user likes (optional)
        disliked_directors: list[str] # list of directors the user dislikes (optional)
        liked_years: list[int] # list of years the user likes (optional). e.g. user likes 90s, return [1990, 1999] like [start year, end year] if one of them is not defined just write False as placeholder. e.g. user likes years until 2010, return [False, 2010], or user likes years after 2010, return [2010, False].
        liked_rating: float # rating the user gives to the movie (optional) (e.g. user asks +8, write 8.0)

        Here is the genres list to choose from: {str(self.genres_list)}.

        Note: Be flexible and consider all possible genres in the list.
        """

        # Generate response from the Gemini language model
        extracted_genres = self.gemini.generate_response(prompt)

        return extracted_genres

# --- Example Usage ---
if __name__ == "__main__":
    # Example user query
    user_query = "I want to watch an action movie but I dislike horror. Milenium movies are my favorite. imdb rating should be atleast 7.5. I like directors like Christopher Nolan and James Cameron. I dislike directors like Quentin Tarantino and Steven Spielberg. I love Jim Carrey, but not Eddie Murphy. It should be onve of the 90s movies."
    # Create a FeatureExtractor instance
    extractor = FeatureExtractor()
    # Extract features from the user query
    extracted = extractor.extract_features(user_query)
    print("Extracted movie features:")
    # Print the extracted features
    print(extracted)
