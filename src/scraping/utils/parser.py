import os
import re
import time
import random
import requests

from bs4 import BeautifulSoup

import config

def fetch_page_content(url, file_path):
    """
    Fetches the content of a web page, either from a local file or by downloading it.

    Args:
        url (str): The URL of the web page to fetch.
        file_path (str): The path to the local file where the content should be saved or loaded from.

    Returns:
        bytes: The content of the web page as bytes, or None if the content could not be fetched.
    """
    # Rotate User-Agent header
    headers = {
        "User-Agent": random.choice(config.USER_AGENTS_LIST),
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    # Ensure the directory exists
    os.makedirs('data/raw/html_content', exist_ok=True)

    # Fetch or load the HTML file
    if not os.path.exists(file_path):
        try:
            time.sleep(random.uniform(1, 2))  # Randomized delay between 1 and 3 seconds
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Will raise HTTPError for bad responses
            with open(file_path, 'wb') as f:
                f.write(response.content)
            data = response.content
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data: {e}")
            return None
    else:
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
        except IOError as e:
            print(f"Failed to read local file: {e}")
            return None
        
    return data

def fetch_movie_advanced(movie_id):
    """
    Fetches advanced movie details, including plot summaries and synopsis.

    Args:
        movie_id (str): The IMDb ID of the movie.

    Returns:
        tuple: A tuple containing the plot summaries and synopsis, or (None, None) if the data could not be fetched.
    """
    file_path = f'data/raw/html_content/{movie_id}_story.json'
    url = f"https://www.imdb.com/title/{movie_id}/plotsummary/"
    data = fetch_page_content(url, file_path)

    if not data:
        return None, None

    # Parse the HTML content
    try:
        soup = BeautifulSoup(data, 'html.parser')
    except Exception as e:
        print(f"Failed to parse HTML content: {e}")
        raise Exception("Failed to parse HTML content: {e}\nURL: {url}")

    sections = soup.find_all("section", {"class": "ipc-page-section ipc-page-section--base"})

    summaries = []
    synopsis = "N/A"

    for i, section in enumerate(sections):
        if i == 0:
            try: 
                summary_items = section.find_all('div', class_='ipc-metadata-list-item__content-container')
                for item in summary_items:
                    summary_div = item.find('div', class_='ipc-html-content-inner-div')
                    if summary_div:
                        summary = summary_div.get_text(strip=True)
                        summaries.append(summary)

                if summaries:
                    summaries = " ".join(summaries)
                else:
                    summaries = "N/A"
                    
            except:
                print(f"Failed to find summary items in section {i}.")
        if i == 1:
            synopsis_div = section.find('div', class_='ipc-html-content-inner-div')
            if synopsis_div:
                synopsis = synopsis_div.get_text(strip=True)

    return summaries, synopsis

def fetch_movie(movie_id, advanced=False):
    """
    Fetches movie details from IMDb.

    Args:
        movie_id (str): The IMDb ID of the movie.
        advanced (bool, optional): Whether to fetch advanced details like reviews and synopsis. Defaults to False.

    Returns:
        dict: A dictionary containing movie details, or None if the data could not be fetched.
    """
    file_path = f'data/raw/html_content/{movie_id}.json'
    url = f"https://www.imdb.com/title/{movie_id}/"
    data = fetch_page_content(url, file_path)

    if not data:
        return None

    try:
        soup = BeautifulSoup(data, 'html.parser')
    except Exception as e:
        print(f"Failed to parse HTML content: {e}")
        return None

    details = {
        "title": "N/A",
        "year": 0,
        "imdb_rating": 0,
        "metascore": 0,
        "pg_rating": "N/A",
        "votes": "N/A",
        "length": "N/A",
        "plot": "N/A",
        "summary": "N/A",
        "synopsis": "N/A",
        "directors": "N/A",
        "stars": "N/A",
        "genres": "N/A",
        "review_title": "N/A",
        "review_rating": 0,
        "review_text": "N/A",
        "link": "N/A"
    }

    # Save url
    details["link"] = url

    # Extract title
    title_element = soup.find('span', {'data-testid': 'hero__primary-text'})
    details['title'] = title_element.text.strip() if title_element else 'N/A'

    # Extract genres
    genre_element = soup.find("div", {"class": "ipc-chip-list--baseAlt ipc-chip-list ipc-chip-list--nowrap sc-42125d72-4 iPHzA-d"})
    details['genres'] = ", ".join([span.text for span in genre_element.select('div.ipc-chip-list__scroller a span.ipc-chip__text')] if genre_element else [])

    # Extract IMDb Rating
    rating_element = soup.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating__score'})
    details['imdb_rating'] = rating_element.find('span').text.strip() if rating_element else 0

    # Extract user votes
    votes_element = soup.find_all("div", {"class": "sc-d541859f-3 dwhNqC"})
    details['votes'] = votes_element[0].text if votes_element else 'N/A'

    # Extract Metascore
    metascore_element = soup.find("span", {"class": "sc-b0901df4-0 bXIOoL metacritic-score-box"})
    details['metascore'] = metascore_element.text.strip() if metascore_element else 0

    # Extract year, PG rating, and length
    ul_element = soup.find('ul', class_='ipc-inline-list ipc-inline-list--show-dividers sc-ec65ba05-2 joVhBE baseAlt')
    li_elements = ul_element.find_all('li') if ul_element else []
    details['year'] = li_elements[0].get_text(strip=True) if len(li_elements) > 0 else 0
    details['pg_rating'] = li_elements[1].get_text(strip=True) if len(li_elements) > 1 else 'N/A'
    details['length'] = li_elements[2].get_text(strip=True) if len(li_elements) > 2 else 'N/A'

    # Extract plot
    plot_element = soup.find('span', {'data-testid': 'plot-xl'})
    details['plot'] = plot_element.text.strip() if plot_element.text.strip() else 'N/A'

    # Extract stars and directors
    credits = soup.select('li[data-testid="title-pc-principal-credit"]')
    for credit in credits:
        if 'Stars' in credit.text:
            details['stars'] = ", ".join([a.text.strip() for a in credit.find_all('a') if a.text.strip()][1:])
        if 'Director' in credit.text:
            details['directors'] = ", ".join([a.text.strip() for a in credit.find_all('a')])

    # Extract advanced information if needed
    if advanced:

        # Extract featured review
        try:
            review_section = soup.find("section", {"data-testid": "UserReviews"})
            if review_section:
                review_cards = review_section.find_all('article', {'class': 'sc-f4aa788c-0'})
                for card in review_cards:
                    title_tag = card.find('h3', {'class': 'ipc-title__text'})
                    review_title = title_tag.text.strip() if title_tag else "No title"
                    rating_tag = card.find('span', {'class': 'ipc-rating-star--rating'})
                    review_rating = rating_tag.text.strip() if rating_tag else "No rating"
                    text_tag = card.find('div', {'class': 'ipc-html-content-inner-div'})
                    review_text = text_tag.text.strip() if text_tag else "No text"
                    details['review_title'] = review_title
                    details['review_rating'] = review_rating
                    details['review_text'] = review_text
                    break
        except Exception as e:
            print(f"Failed to extract reviews: {e} \nFailed url: {url}")
            
        # Extract summary and synopsis
        details["summary"], details["synopsis"] = fetch_movie_advanced(movie_id)

    return details

def run(movie_url, advanced):
    """
    Runs the movie data extraction process.

    Args:
        movie_url (str): The URL of the movie on IMDb.
        advanced (bool): A flag indicating whether to extract advanced movie details.

    Returns:
        dict: A dictionary containing the extracted movie details.
    """
    # match movie code using regex
    match = re.search(r"tt\d{7,8}", movie_url)

    if match:
        movie_code = match.group()
    else:
        print(f"No movie code found: {movie_url}")

    return fetch_movie(movie_code, advanced)
