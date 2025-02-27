import sqlite3
from typing import List, Dict, Optional, Any

class MovieDatabase:
    """Handles database operations for movies."""

    def __init__(self, db_filename: str = 'data/processed/movies.db'):
        """
        Initializes the MovieDatabase class.

        Args:
            db_filename (str): The name of the SQLite database file.
        """
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()
        self._create_movie_table()

    def _create_movie_table(self) -> None:
        """Creates the movies table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                year INTEGER,
                imdb_rating REAL,
                metascore REAL,
                pg_rating TEXT,
                votes TEXT,
                length TEXT,
                plot TEXT,
                summary TEXT,
                synopsis TEXT,
                directors TEXT,
                stars TEXT,
                genres TEXT,
                review_title TEXT,
                review_rating INTEGER,
                review_text TEXT,
                link TEXT
            )
        ''')
        self.conn.commit()

    def insert_movie_data(self, movie_data: Dict[str, Optional[str]]) -> None:
        """
        Inserts movie data into the database.

        Args:
            movie_data (Dict[str, Optional[str]]): A dictionary containing movie data.
        """
        try:
            # Check if a movie with the same title already exists
            self.cursor.execute('''SELECT COUNT(*) FROM movies WHERE title = ?''', (movie_data['title'],))
            result = self.cursor.fetchone()

            if result[0] == 0:  # No record with this title
                # Insert the movie data into the database
                self.cursor.execute('''
                    INSERT INTO movies (title, year, imdb_rating, metascore, pg_rating, votes, length, plot, summary, synopsis, directors, stars, genres, review_title, review_rating, review_text, link)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    movie_data['title'],
                    movie_data['year'],
                    movie_data['imdb_rating'],
                    movie_data['metascore'],
                    movie_data['pg_rating'],
                    movie_data['votes'],
                    movie_data['length'],
                    movie_data['plot'],
                    movie_data['summary'],
                    movie_data['synopsis'],
                    movie_data['directors'],
                    movie_data['stars'],
                    movie_data['genres'],
                    movie_data['review_title'],
                    movie_data['review_rating'],
                    movie_data['review_text'],
                    movie_data['link']
                ))
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting movie data: {e}")

    def delete_movie_by_title(self, title: str) -> None:
        """
        Deletes a movie from the database based on its title.

        Args:
            title (str): The title of the movie to delete.
        """
        try:
            self.cursor.execute("DELETE FROM movies WHERE title = ?", (title,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print(f"No movie found with title: {title}")
            else:
                print(f"Movie with title '{title}' deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting movie: {e}")

    def read_movie_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Reads a movie from the database based on its title.

        Args:
            title (str): The title of the movie to read.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the movie data, or None if no movie is found.
        """
        try:
            query = "SELECT * FROM movies WHERE title LIKE ?"
            self.cursor.execute(query, (f"%{title}%",))

            rows = self.cursor.fetchall()

            if rows:
                movies = []
                for row in rows:
                    movie = {
                        "id": row[0],
                        "title": row[1],
                        "year": row[2],
                        "imdb_rating": row[3],
                        "metascore": row[4],
                        "pg_rating": row[5],
                        "votes": row[6],
                        "length": row[7],
                        "plot": row[8],
                        "summary": row[9],
                        "synopsis": row[10],
                        "directors": row[11],
                        "stars": row[12],
                        "genres": row[13],
                        "review_title": row[14],
                        "review_rating": row[15],
                        "review_text": row[16],
                        "link": row[17]
                    }
                    movies.append(movie)
                return movies
            
            else:
                # print(f"No movie found with title: {title}")
                return None
        except sqlite3.Error as e:
            print(f"Error reading movie: {e}")
            return None

    def read_all_movies(self) -> List[Dict[str, Any]]:
        """
        Reads all movies from the database.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing movie data.
        """
        try:
            self.cursor.execute("SELECT * FROM movies")
            rows = self.cursor.fetchall()
            movies = []
            for row in rows:
                movies.append({
                    "id": row[0],
                    "title": row[1],
                    "year": row[2],
                    "imdb_rating": row[3],
                    "metascore": row[4],
                    "pg_rating": row[5],
                    "votes": row[6],
                    "length": row[7],
                    "plot": row[8],
                    "summary": row[9],
                    "synopsis": row[10],
                    "directors": row[11],
                    "stars": row[12],
                    "genres": row[13],
                    "review_title": row[14],
                    "review_rating": row[15],
                    "review_text": row[16],
                    "link": row[17]
                })
            return movies
        except sqlite3.Error as e:
            print(f"Error reading all movies: {e}")
            return []

    def read_movies_with_columns(self, columns: List[str]) -> List[Dict[str, Any]]:
        """
        Reads movies from the database, returning only the specified columns.

        Args:
            columns (List[str]): A list of column names to retrieve.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing movie data with the specified columns.
        """
        try:
            if not columns:
                return []
            
            query = f"SELECT {', '.join(columns)} FROM movies"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            movies = []
            for row in rows:
                movie = {}
                for i, col in enumerate(columns):
                    movie[col] = row[i]
                movies.append(movie)
            return movies
        except sqlite3.Error as e:
            print(f"Error reading movies with columns: {e}")
            return []

    def close(self) -> None:
        """Closes the database connection."""
        self.conn.close()
