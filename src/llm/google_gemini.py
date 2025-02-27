from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import time
import json

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini client with the API key from environment variables
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class GenrePreference(BaseModel):
    """
    Pydantic model for genre preferences.
    
    Defines the structure for storing user preferences related to movie genres, stars, directors, years, and ratings.
    """
    liked_genres: list[str]
    disliked_genres: list[str]
    liked_stars: list[str]
    disliked_stars: list[str]
    liked_directors: list[str]
    disliked_directors: list[str]
    liked_years: list[int]
    liked_rating: float

class Gemini:
    """
    A class for interacting with the Google Gemini language model.
    
    Handles API calls, rate limiting, and response formatting.
    """
    def __init__(self, model_info, json_output=False):
        """
        Initializes the Gemini class.
        
        Args:
            model_info (dict): A dictionary containing model name and requests per minute (rpm).
            json_output (bool, optional): Whether to format the output as JSON. Defaults to False.
        """
        self.model_name = model_info['name']
        self.rpm = model_info['rpm']
        self.json_output = json_output
        self.call_timestamps = []

    def generate_response(self, prompt, max_output_tokens=300, temperature=0.7):
        """
        Generates a response from the Gemini language model.
        
        Args:
            prompt (str): The input prompt for the language model.
            max_output_tokens (int, optional): The maximum number of tokens in the output. Defaults to 300.
            temperature (float, optional): The temperature for controlling the randomness of the output. Defaults to 0.7.
        
        Returns:
            str: The generated response from the language model.
        
        Raises:
            Exception: If the API call fails after multiple attempts.
        """
        current_time = time.time()

        # Remove timestamps older than 60 seconds to maintain the rate limit window
        self.call_timestamps = [t for t in self.call_timestamps if current_time - t < 60]

        # Apply rate limiting if the number of calls in the last 60 seconds exceeds the rpm
        if len(self.call_timestamps) >= self.rpm:
            time_to_sleep = 60 - (current_time - self.call_timestamps[0])
            if time_to_sleep > 0:
                print(f"Rate limit reached. Sleeping for {time_to_sleep:.2f} seconds.")
                time.sleep(time_to_sleep)

        # Call the LLM API to generate a response
        print(f"Generating response...")
        counter = 1
        while counter <= 3:
            try:
                if self.json_output:
                    # Generate content with JSON output format
                    response = client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config={
                            'response_mime_type': 'application/json',
                            'response_schema': list[GenrePreference],
                        },
                    )
                else:
                    # Generate content with plain text output format
                    response = client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            max_output_tokens=max_output_tokens,
                            temperature=temperature
                        )
                    )

                print("Generated Summary: " + response.text.strip() + "\n")
                break  # Exit loop if successful
            except Exception as e:
                print(f"Attempt {counter} failed: {e}")
                counter += 1
                time.sleep(5)
        else:
            # This else executes if the loop did not break, i.e. after 3 failed attempts
            # Raise exception and log the error details
            raise Exception("Failed to generate summary after 3 attempts. Please try again later.")
            
        # Update call timestamps
        self.call_timestamps.append(time.time())

        if self.json_output:
            # Load JSON from the response text
            genre_preferences = json.loads(response.text)[0]

            return genre_preferences
        
        return response.text.strip()
