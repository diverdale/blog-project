from src import app
from src.models import Post
from flask import render_template


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
