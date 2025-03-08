import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the homepage with a list of blog posts.

    Reads the blog posts from the JSON file and renders the 'index.html' template,
    passing the list of posts.

    Returns:
        A Flask response object with the rendered homepage.
    """
    with open("blog_posts.json", "r") as fileobj:
        blog_posts = json.load(fileobj)
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add a new blog post to the application.

    For GET requests:
        Renders the 'add.html' template to display the form for adding a new post.
    For POST requests:
        - Reads the current blog posts from the JSON file.
        - Determines the next available ID.
        - Collects form data (author, title, content).
        - Creates a new post and appends it to the list.
        - Writes the updated list back to the JSON file.
        - Redirects the user to the homepage.

    Returns:
        A Flask response object rendering a template or redirecting to the homepage.
    """
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
    """
    Delete a blog post by its ID.

    Reads the blog posts from the JSON file, removes the post with the given post_id,
    writes the updated list back to the JSON file, and redirects the user to the homepage.

    Args:
        post_id (int): The unique identifier of the blog post to be deleted.

    Returns:
        A Flask response object redirecting to the homepage.
    """
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

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update an existing blog post.

    For GET requests:
        Loads the blog post with the specified post_id and renders the 'update.html'
        template pre-populated with the current data.
    For POST requests:
        - Retrieves the updated data from the form.
        - Updates the corresponding blog post.
        - Writes the updated list back to the JSON file.
        - Redirects the user to the homepage.

    Args:
        post_id (int): The unique identifier of the blog post to be updated.

    Returns:
        A Flask response object either rendering the update form or redirecting to the homepage.
    """
    try:
        with open("blog_posts.json", "r") as fileobj:
            blog_posts = json.load(fileobj)
    except json.JSONDecodeError:
        blog_posts = []

    post_to_update = None
    for post in blog_posts:
        if post['id'] == post_id:
            post_to_update = post
            break

    if not post_to_update:
        return "Post not found", 404

    if request.method == 'POST':
        updated_author = request.form['author']
        updated_title = request.form['title']
        updated_content = request.form['content']

        post_to_update['author'] = updated_author
        post_to_update['title'] = updated_title
        post_to_update['content'] = updated_content

        with open("blog_posts.json", "w") as fileobj:
            json.dump(blog_posts, fileobj, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post_to_update)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


