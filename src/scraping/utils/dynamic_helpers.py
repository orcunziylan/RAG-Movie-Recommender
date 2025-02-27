from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from typing import List, Dict, Optional
from tqdm import tqdm
import random
import time

def handle_cookies(driver: webdriver.Chrome) -> None:
    """
    Handles the "Cookies" banner by clicking the "Decline" button.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
    """
    print("Handling cookies...")

    COOKIES_REJECT_BUTTON = "//button[@data-testid='reject-button']"

    try:
        cookies_button = driver.find_element(By.XPATH, COOKIES_REJECT_BUTTON)
        cookies_button.click()
        print(" -> Cookies banner declined.")
    except Exception as e:
        print(f"No cookies banner found or already handled: {e}")


def load_all_pages(driver: webdriver.Chrome, timeout=4) -> None:
    """
    Loads all movies on the page by repeatedly clicking the "Show More" button.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
        timeout (int, optional): The maximum time to wait between clicks. Defaults to 4.
    """
    print("Loading all movies...")

    SHOW_MORE_BUTTON = "//button[contains(@class, 'ipc-see-more__button')]"

    while True:
        try:
            print(" -> Button clicked. Loading more movies...")
            show_more_button = driver.find_element(By.XPATH, SHOW_MORE_BUTTON)
            ActionChains(driver).move_to_element(show_more_button).click(show_more_button).perform()
            time.sleep(random.uniform(1, timeout))
        except Exception:
            print(" -> No more 'Show More' button found. All movies loaded.")
            break

def scrape_movies(driver: webdriver.Chrome) -> List[Dict[str, str]]:
    """
    Scrapes movie data from the current page.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary represents a movie
                              and contains its title and link.
    """
    print("Scraping movies...")

    MOVIE_ITEM = "li.ipc-metadata-list-summary-item"
    movie_elements = driver.find_elements(By.CSS_SELECTOR, MOVIE_ITEM)

    TITLE_SELECTOR = ".ipc-title__text"
    LINK_SELECTOR = ".ipc-title-link-wrapper"

    movies = []
    for movie in tqdm(movie_elements):
        try:
            title = movie.find_element(By.CSS_SELECTOR, TITLE_SELECTOR).text.split(". ")[-1]
            link = movie.find_element(By.CSS_SELECTOR, LINK_SELECTOR).get_attribute("href")

            if not link:
                print(f"Could not extract link for movie: {title}. Skipping...")
                continue
    
            movies.append({'title':title, 'link':link})
        except Exception as e:
            print(f"Error scraping movie: {e} - {movie}")

    return movies
