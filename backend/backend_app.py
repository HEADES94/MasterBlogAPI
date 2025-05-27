# backend/backend_app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

POSTS_FILE = "posts.json"

def load_posts():
    """Load blog posts from JSON file."""
    if not os.path.exists(POSTS_FILE):
        return []
    with open(POSTS_FILE, "r") as file:
        return json.load(file)

def save_posts(posts):
    """Save blog posts to JSON file."""
    with open(POSTS_FILE, "w") as file:
        json.dump(posts, file, indent=4)

@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    """Handle listing and creating blog posts."""
    posts = load_posts()

    if request.method == 'GET':
        return jsonify(posts)

    if request.method == 'POST':
        data = request.get_json()
        required = ['title', 'content', 'author', 'category', 'date']
        if not all(k in data and data[k] for k in required):
            return jsonify({"error": "Missing required fields"}), 400

        new_id = max((p['id'] for p in posts), default=0) + 1
        new_post = {
            "id": new_id,
            "title": data["title"],
            "content": data["content"],
            "author": data["author"],
            "category": data["category"],
            "date": data["date"],
            "likes": 0
        }
        posts.append(new_post)
        save_posts(posts)
        return jsonify(new_post), 201

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Delete a blog post by ID."""
    posts = load_posts()
    post = next((p for p in posts if p['id'] == id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    posts = [p for p in posts if p['id'] != id]
    save_posts(posts)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200

@app.route('/api/posts/<int:id>/like', methods=['POST'])
def like_post(id):
    """Increment like count for a blog post."""
    posts = load_posts()
    post = next((p for p in posts if p['id'] == id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    post['likes'] += 1
    save_posts(posts)
    return jsonify(post), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)
