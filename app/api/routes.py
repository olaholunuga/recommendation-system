from flask import Blueprint, request, jsonify, abort
from app.services.model_service import recommender

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/recommend/user/<int:user_id>', methods=["GET"])
def recommend_for_user(user_id):
    # 1. Input Validation
    limit = request.args.get('limit', default=5, type=int)
    if limit <= 0:
        # This will now trigger our custom JSON error handler
        abort(400, description="The 'limit' parameter must be a positive integer.")
    
    all_movie_ids = list(range(1, 1000))
    
    try:
        # 2. Get Predictions
        raw_recommendations = recommender.get_user_predictions(user_id, all_movie_ids, limit)
        
        # 3. JSON:API Formatting
        formatted_data = []
        for rec in raw_recommendations:
            formatted_data.append({
                "type": "movie",
                "id": str(rec['movie_id']),
                "attributes": {
                    "estimated_rating": rec['estimated_rating'],
                    "recommendation_strategy": rec['strategy']
                }
            })
            
        response = {
            "meta": {
                "user_id": user_id,
                "count": len(formatted_data)
            },
            "data": formatted_data,
            "links": {
                "self": request.url
            }
        }
        return jsonify(response), 200
        
    except Exception as e:
        # Catch unexpected ML/Server errors
        abort(500, description="An internal error occurred while generating recommendations.")