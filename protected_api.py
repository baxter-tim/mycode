"""Classroom bearer authentication and authorization example."""
import hmac
import os
from functools import wraps

from flask import Flask, g, jsonify, request


def create_app(reader_token, admin_token):
    if not reader_token or not admin_token or reader_token == admin_token:
        raise ValueError("Two different nonempty tokens are required")

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 1024
    notes = []

    def protected(*roles):
        def decorate(view):
            @wraps(view)
            def wrapped(*args, **kwargs):
                scheme, _, token = request.headers.get(
                    "Authorization", ""
                ).partition(" ")
                role = None
                if scheme.lower() == "bearer" and token:
                    supplied = token.encode("utf-8")
                    if hmac.compare_digest(supplied, admin_token.encode()):
                        role = "admin"
                    elif hmac.compare_digest(supplied, reader_token.encode()):
                        role = "reader"
                if role is None:
                    response = jsonify(error="authentication required")
                    response.status_code = 401
                    response.headers["WWW-Authenticate"] = "Bearer"
                    return response
                if role not in roles:
                    return jsonify(error="permission denied"), 403
                g.role = role
                return view(*args, **kwargs)
            return wrapped
        return decorate

    @app.after_request
    def response_headers(response):
        response.headers["Cache-Control"] = "no-store"
       # response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.get("/notes")
    @protected("reader", "admin")
    def list_notes():
        return jsonify(notes=notes, role=g.role)

    @app.post("/notes")
    @protected("admin")
    def add_note():
        if not request.is_json:
            return jsonify(error="application/json required"), 415
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="JSON object required"), 400
        title = data.get("title")
        if not isinstance(title, str) or not 1 <= len(title.strip()) <= 80:
            return jsonify(error="title must contain 1 to 80 characters"), 400
        note = {"id": len(notes) + 1, "title": title.strip()}
        notes.append(note)
        return jsonify(note), 201

    return app


if __name__ == "__main__":
    app = create_app(
        os.environ.get("LAB_READER_TOKEN"),
        os.environ.get("LAB_ADMIN_TOKEN"),
    )
    app.run(host="127.0.0.1", port=5001, debug=False)
