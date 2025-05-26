from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'posts.json'


# Load all blog posts from the JSON storage file
def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)


# Save the list of blog posts back to the JSON file
def save_posts(posts):
    with open(DATA_FILE, 'w') as file:
        json.dump(posts, file, indent=4)


# Retrieve a single post by ID
def get_post_by_id(post_id):
    posts = load_posts()
    return next((post for post in posts if post['id'] == post_id), None)


# Home route: display all blog posts
@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


# Route to add a new blog post
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        new_post = {
            "id": max([post["id"] for post in posts], default=0) + 1,
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content"),
            "likes": 0  # initialize likes to 0
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('add.html')


# Route to delete a blog post
@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post["id"] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))


# Route to update an existing blog post
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


# Route to handle "liking" a post
@app.route('/like/<int:post_id>')
def like(post_id):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            post["likes"] = post.get("likes", 0) + 1
            break
    save_posts(posts)
    return redirect(url_for('index'))


# Start the Flask development server
if __name__ == '__main__':
    app.run(debug=True)
