import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    with open("blog_posts.json", "r") as fileobj:
        blog_posts = json.load(fileobj)
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Load the current blog posts from the JSON file
        try:
            with open("blog_posts.json", "r") as fileobj:
                blog_posts = json.load(fileobj)
        except json.JSONDecodeError:
            blog_posts = []

        # Determine the next available ID
        if blog_posts:
            next_id = max(post['id'] for post in blog_posts) + 1
        else:
            next_id = 1

        # Collect form data
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Create a new post dictionary with the calculated ID
        new_post = {
            'id': next_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Append the new post to the list of blog posts
        blog_posts.append(new_post)

        # Write the updated list back to the JSON file
        with open("blog_posts.json", "w") as fileobj:
            json.dump(blog_posts, fileobj, indent=4)

        # Redirect back to the homepage to show the new post
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    try:
        with open("blog_posts.json", "r") as fileobj:
            blog_posts = json.load(fileobj)
    except json.JSONDecodeError:
        blog_posts = []

    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            print(f"removed the blog with the ID: {post['id']}")
            break

    # Write the updated list back to the JSON file
    with open("blog_posts.json", "w") as fileobj:
        json.dump(blog_posts, fileobj, indent=4)

    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


