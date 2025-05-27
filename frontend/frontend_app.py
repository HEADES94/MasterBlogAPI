# frontend/frontend_app.py

from flask import Flask, render_template

# Initialize frontend Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/add')
def add():
    """Render the add post page."""
    return render_template('add.html')

@app.route('/update')
def update():
    """Render the update post page."""
    return render_template('update.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
