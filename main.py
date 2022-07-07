from flask import Flask, render_template, url_for
import requests

blog_data = ""


def get_blog_data():
    url = "https://api.npoint.io/2d1cdf51d281cab506ab"
    global blog_data
    blog_data = requests.get(url=url).json()


app = Flask(__name__)


@app.route("/")
def home():
    get_blog_data()
    return render_template("index.html", posts=blog_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    selected_post = ""
    for data in blog_data:
        if data["id"] == index:
            selected_post = data
    return render_template("post.html", post=selected_post)


if __name__ == "__main__":
    app.run(debug=True)
