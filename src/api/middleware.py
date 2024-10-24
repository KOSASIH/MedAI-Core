# api/middleware.py

from flask import request, jsonify
from functools import wraps

def token_required(f):
    """Decorator to enforce token-based authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != "Bearer your_secure_token":
            return jsonify({"message": "Token is missing or invalid!"}), 403
        return f(*args, **kwargs)
    return decorated

# Example usage of the middleware in routes.py
# @app.route('/api/v1/protected_route', methods=['GET'])
# @token_required
# def protected_route():
#     return jsonify({"message": "This is a protected route."}), 200
