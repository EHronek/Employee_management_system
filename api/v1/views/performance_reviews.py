#!/usr/bin/python3
from flask import jsonify, request
from models import storage
from models.performance_review import PerformanceReview
from api.v1.views import app_views


@app_views.route("/performance_reviews", methods=["GET"], strict_slashes=False)
def get_performance_reviews():
    '''Retrieves all performance reviews'''
    reviews = storage.all(PerformanceReview).values()

    if not reviews:
        return jsonify({"error": "not found"}), 404
    return jsonify([review.to_dict() for review in reviews]), 200


@app_views.route("/performance_reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_performance_review(review_id):
    """Retrieve a specific performance review"""
    review = storage.get(PerformanceReview, review_id)
    if not review:
        return jsonify({"error": "review not found"}), 404
    
    return jsonify(review.to_dict()), 200


@app_views.route("/performance_reviews", methods=["POST"])
def create_performance_review():
    """create a new performance review"""
    data = request.get_json(silent=True)

    if not data or "employee_id" not in data or "score" not in data:
        return jsonify({"error": "missing required fields"}), 400
    
    review = PerformanceReview(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/performance_reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_performance_review(review_id):
    """Update an existing performance review"""
    review = storage.get(PerformanceReview, review_id)
    if not review:
        return jsonify({"error": "review not found"}), 404
    
    data = request.get_json(silent=True)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            if hasattr(review, key):
                setattr(review, key, value)
            else:
                return jsonify({"error": "key is not an defined attribute"}), 400
    
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route("/performance_reviews", methods=["DELETE"], strict_slashes=False)
def delete_performance_review(review_id):
    """Deletes a performance review"""
    review = storage.get(PerformanceReview, review_id)
    if not review:
        return jsonify({"error": "review not found"}), 404
    
    storage.delete(review)
    storage.save()
    return jsonify({"message": "Performance review deleted"}), 200
