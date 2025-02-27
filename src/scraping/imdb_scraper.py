from bs4 import BeautifulSoup
from .utils import browser_manager, parser
from .utils.dynamic_helpers import *
import logging
import time
import random

# Initialize logger
logger = logging.getLogger(__name__)

class scrape_imdb_movies:
    """
    A class to scrape movie data from IMDb.
    """
    def __init__(self, url, load_more, headless=True, timeout=2):
        """
        Initializes the scraper with the given parameters.

        Args:
            url (str): The base URL of the IMDb page to scrape.
            load_more (bool): Whether to load all movies on the page by clicking "Show More" button.
            headless (bool, optional): Whether to run the browser in headless mode. Defaults to True.
            timeout (int, optional): The maximum time to wait between actions. Defaults to 2.
        """
        self.base_url = url
        self.load_more = load_more
        self.headless = headless
        self.timeout = timeout if timeout > 1 else 2

    def scrape_dynamic(self,):
        """
        Handles single page scraping with JS-rendered content.

        Uses Selenium to handle JavaScript-rendered content and extract movie links.

        Returns:
            list: A list of dictionaries, where each dictionary represents a movie and contains its title and link.
        """
        with browser_manager.managed_browser(headless=self.headless) as driver:
            driver.get(self.base_url)
            time.sleep(random.uniform(1, self.timeout))
            handle_cookies(driver)

            if self.load_more:
                load_all_pages(driver)

            time.sleep(random.uniform(1, self.timeout))
            return scrape_movies(driver)

    def scrape_static(self, movie_links, advanced):
        """
        Requests with BeautifulSoup parsing logic.

        Uses BeautifulSoup to parse the HTML content of each movie page and extract details.

        Args:
            movie_links (list): A list of dictionaries, where each dictionary represents a movie and contains its title and link.
            advanced (bool): A flag indicating whether to extract advanced movie details.

        Returns:
            list: A list of dictionaries, where each dictionary represents a movie and contains its details.
        """
        movies = []
        for movie in movie_links:
            try:
                movie_details = parser.run(movie['link'], advanced)
                movies.append(movie_details)
            except Exception as e:
                logger.error(f"Error parsing {movie['link']}: {str(e)}")
        return movies

    def run(self, advanced=False):
        """
        Full scraping workflow.

        Orchestrates the full scraping process, including dynamic content loading and static parsing.

        Args:
            advanced (bool, optional): A flag indicating whether to extract advanced movie details. Defaults to False.

        Returns:
            list: A list of dictionaries, where each dictionary represents a movie and contains its details.
        """
        all_movies = []

        movie_info = self.scrape_dynamic()
        all_movies = self.scrape_static(movie_info, advanced)

        return all_movies
