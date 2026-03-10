import json
from unittest.mock import patch

def test_health_check(client):
    """Ensure the API is running."""
    response = client.get('/health')
    assert response.status_code == 200
    assert json.loads(response.data) == {"status": "healthy"}

def test_invalid_limit_parameter(client):
    """Ensure negative limits return a 400 Bad Request."""
    response = client.get('/api/v1/recommend/user/42?limit=-5')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "errors" in data
    # Properly access the first dictionary in the 'errors' list
    assert data["errors"][0]["status"] == 400

@patch('app.api.routes.recommender.get_user_predictions')
def test_recommend_for_user_success(mock_predict, client):
    """Test a successful recommendation request using mock data."""
    
    # 1. Define what the fake ML model should return
    mock_predict.return_value = [
        {"movie_id": 101, "estimated_rating": 4.5, "strategy": "collaborative_filtering"},
        {"movie_id": 204, "estimated_rating": 4.2, "strategy": "collaborative_filtering"}
    ]
    
    # 2. Make a simulated GET request to the endpoint
    response = client.get('/api/v1/recommend/user/42?limit=2')
    
    # 3. Assert the HTTP status code is correct
    assert response.status_code == 200
    
    # 4. Parse the JSON and assert the JSON:API structure is correct
    data = json.loads(response.data)
    assert data["meta"]["count"] == 2
    assert data["meta"]["user_id"] == 42
    assert len(data["data"]) == 2
    
    # 5. Verify the data formatting by grabbing the first item in the list
    first_movie = data["data"][0]
    assert first_movie["type"] == "movie"
    assert first_movie["id"] == "101"
    assert first_movie["attributes"]["estimated_rating"] == 4.5
    
    # 6. Verify that our mocked function was actually called
    mock_predict.assert_called_once()