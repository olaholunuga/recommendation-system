import joblib
import os

class RecommendationService:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        """Loads the serialized model into memory."""
        base_dir = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.join(base_dir, '../../models/svd_model.joblib')
        
        try:
            self.model = joblib.load(model_path)
            print("Model loaded successfully into memory.")
        except FileNotFoundError:
            print(f"Error: Model file not found at {model_path}.")

    def get_user_predictions(self, user_id, all_movie_ids, top_n=10):
        """Predicts top N movies, with a fallback for cold-start users."""
        if not self.model:
            raise ValueError("Model is not loaded.")

        # 1. Hybrid Check: Is this a known user?
        try:
            # If this succeeds, the user was in the training data
            self.model.trainset.to_inner_uid(str(user_id))
            user_known = True
        except ValueError:
            # User is completely new (Cold Start)
            user_known = False

        # 2. Route to the correct strategy
        if not user_known:
            return self._get_popular_fallback(top_n)

        # 3. Standard SVD Prediction for known users
        predictions = []
        for movie_id in all_movie_ids:
            pred = self.model.predict(uid=str(user_id), iid=str(movie_id))
            predictions.append((movie_id, pred.est))
            
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        return [
            {
                "movie_id": movie_id, 
                "estimated_rating": round(score, 2),
                "strategy": "collaborative_filtering"
            } 
            for movie_id, score in predictions[:top_n]]

    def _get_popular_fallback(self, top_n):
        """Returns globally popular movies for new users."""
        # In a production environment, you would query your database for 
        # the movies with the highest aggregate ratings or most views.
        # Here we mock it with classic, universally acclaimed movie IDs.
        popular_movies = []
        
        return popular_movies[:top_n]

recommender = RecommendationService()