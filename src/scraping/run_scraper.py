"""
Scrapes movie data from IMDb/Metacritic and saves to SQLite DB.
Usage: python -m src.scraping.run_scraper --source imdb --max-pages 5
"""

import argparse
from src.database.db_manager import MovieDatabase
from src.scraping.imdb_scraper import scrape_imdb_movies

def main():
    """
    Main function to run the scraper and save data to the database.
    """
    # CLI arguments (showcasing production-grade design)
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", choices=["basic", "advanced"], required=True)
    parser.add_argument("--load-pages", action="store_true", 
                       help="Load pages to scrape all")
    parser.add_argument("--dry-run", action="store_true",
                       help="Test scraping without saving to DB")
    parser.add_argument("--link", type=str, default="https://www.imdb.com/search/title/?title=The%20Godfather&title_type=feature&runtime=120",
                       help="Link to scrape from")

    args = parser.parse_args()

    movies = []

    scrape = scrape_imdb_movies(args.link, args.load_pages)

    # Scrape based on search
    if args.search == "basic":
        movies = scrape.run()
    elif args.search == "advanced":
        movies = scrape.run(advanced=True)
    
    # Save to DB unless dry-run
    if not args.dry_run:
        # Initialize database
        db = MovieDatabase()
        for movie_data in movies:
            db.insert_movie_data(movie_data)
        db.close()
        print(f"Added {len(movies)} movies to database")
    else:
        print("[Dry run] Sample movie:", movies[0])

if __name__ == "__main__":
    main()
