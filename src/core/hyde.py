import config
import src.llm.google_gemini as llm

class Hyde:
    """
    Generates hypothetical movie synopses based on user queries.

    This class uses a language model to create engaging movie synopses that capture the essence
    of a film based on user-provided details.
    """
    def __init__(self):
        """
        Initializes the Hyde class with a Gemini model for document generation.
        """
        self.model = llm.Gemini(config.HYDE_MODEL)

    def generate(self, query):
        """
        Generates a hypothetical movie synopsis for a given query using the generation model.

        The synopsis is crafted to reflect the themes, genres, and specific elements mentioned in the user's query.

        Args:
            query (str): The search query describing the desired movie characteristics.

        Returns:
            str: A hypothetical movie synopsis generated based on the query.
        """

        # prompt = f"""
        # You are a creative film critic and an imaginative storyteller. Your task is to generate a vivid and engaging movie synopsis that captures the essence of a film based solely on the details provided by the user. The synopsis should dynamically incorporate the genres, themes, and specific elements mentioned in the user’s query.

        # User Query: "{query}"

        # Instructions:
        # 1. Analyze the user query and extract key themes, genres, and descriptors.
        # 2. Write a concise yet detailed synopsis that highlights the plot, tone, and unique characteristics of a movie matching the query.
        # 3. The synopsis should reflect the dynamic nature of the query—if the query mentions action and romance, for example, the synopsis should blend those elements organically.
        # 4. Ensure the narrative is original, creative, and specific, providing enough detail to form a strong  conceptual embedding of the recommended movie.
        # 5. Never generate titles or names unless user query explicitly mentions them.
        # 6. Generated text should be unstructured paragraphs, with no headings or subheadings.
        # 7. Use daily language.

        # Generate the movie synopsis accordingly.
        # """

        prompt = f"""
        Based on the user's description, generate a short but detailed synopsis of a movie that matches what they might be thinking of. Focus on the main plot, setting, and key themes without mentioning a specific title or name. Keep it natural, like something you'd read in a movie summary."


        Example Output:
        "A bounty hunter and his captured outlaw get trapped in a remote cabin during a brutal snowstorm. As more strangers arrive, tensions rise, secrets come out, and the night turns into a deadly game of deception and survival."

        User Input: {query}
        Output:
        """

        # Generate the response using the Gemini model with a temperature of 1 for creativity
        return self.model.generate_response(prompt, temperature=1)
