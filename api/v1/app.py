#!/usr/bin/python3
"""Flask App"""
import models
from flask import Flask, jsonify
import os
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

@app.route('/api/v1/nop', strict_slashes=False)
def error_404():
    """Handles 404 error """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the current db session"""
    models.storage.close()


if __name__ == "__main__":
    host = os.getenv('EMS_API_HOST', '0.0.0.0')
    port = int(os.getenv('EMS_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)

