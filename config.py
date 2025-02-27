# Model used for generating embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Model used for reranking search results
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Model used for generating summaries / Only Google AI models are supported

SUMMARY_MODEL = {"name": "gemini-2.0-flash-lite-preview-02-05",
                 "rpm": 30 # Requests per minute
                 }

# Model used for generating hypothetical documents (HyDE) / Only Google AI models are supported
HYDE_MODEL = {"name": "gemini-2.0-flash",
              "rpm": 20  # Requests per minute
              }

# Model used for generating recommendations / Only Google AI models are supported
RECOMMENDATION_MODEL = {"name": "gemini-2.0-flash",
                        "rpm": 20  # Requests per minute
                        }

# Model used for extracting genres / Only Google AI models are supported
GENRE_EXTRACTOR_MODEL = {"name": "gemini-2.0-flash",
                         "rpm": 20  # Requests per minute
                         }

# Path to the Chrome WebDriver executable
CHROME_DRIVER_PATH = "PATH/TO/chromedriver.exe"  # Replace with your actual path

# List of user agents to rotate through during scraping
USER_AGENTS_LIST = [] # Populate this list if you want to use a rotating list of user agents.
