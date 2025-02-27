from sentence_transformers import CrossEncoder
import config

class Reranker:
    """
    Reranks movie candidates using a cross-encoder model to improve search result relevance.
    """
    def __init__(self, model_name=config.RERANKER_MODEL):
        """
        Initialize the Reranker with a pre-trained cross-encoder model.

        Args:
            model_name (str, optional): Name of the cross-encoder model for reranking.
                                         Defaults to a model fine-tuned for semantic similarity specified in config.py.
        """
        self.model = CrossEncoder(model_name)

    def rerank(self, query, candidates, combine_score=None):
        """
        Rerank movie candidates based on query relevance using a cross-encoder.

        This method takes a user query and a list of movie candidates, and uses a cross-encoder model
        to re-rank the candidates based on their relevance to the query.

        Args:
            query (str): User's search query.
            candidates (list): List of movie candidate dictionaries.
            combine_score (function, optional): Function to combine cross-encoder score with other metrics. Defaults to None.

        Returns:
            list: Reranked list of movie candidates.
        """
        if not candidates:
            return []
        
        pairs = []
        # Create pairs of query and candidate text for cross-encoder input
        for candidate in candidates:

            text = f"""
            directors: {str(candidate['directors'])}
            stars: {str(candidate['stars'])}
            genres: {str(candidate['genres'])}
            plot: {str(candidate['plot'])}
            """

            pairs.append((query, text))
        
        # Get cross-encoder scores for each pair
        cross_encoder_scores = self.model.predict(pairs)

        # Combine scores if a combine function is provided
        if combine_score:
            combined_scores = [combine_score(score, candidate["imdb_rating"]) 
                               for score, candidate in zip(cross_encoder_scores, candidates)]
        else:
            combined_scores = cross_encoder_scores

        # Sort candidates by combined scores in descending order
        reranked_candidates = sorted(zip(candidates, combined_scores), key=lambda x: x[1], reverse=True)
        return [candidate for candidate, score in reranked_candidates]
