from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

def create_app():
    app = Flask(__name__)
    
    from app.api.routes import api_bp
    app.register_blueprint(api_bp)
    
    # Standardize all HTTP errors to JSON format
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return jsonify({
            "errors": [{
                "status": e.code,
                "title": e.name,
                "detail": e.description,
            }]
        }), e.code

    @app.route('/health', methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy"}), 200
        
    return app