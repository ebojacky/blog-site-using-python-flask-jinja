import smtplib

from flask import Flask, render_template, url_for, request
import requests

blog_data = ""
MY_EMAIL = "***"
MY_PASSWORD = "***"

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


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", contact_me_text="Contact Me")

    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        message = request.form["message"]

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject:New Message from blog website\n\n"
                    f"{fullname}:{email}:{phone_number}\n"
                    f"{message}"
            )

        return render_template("contact.html", contact_me_text="You have successfully sent your message")


@app.route("/post/<int:index>")
def show_post(index):
    selected_post = ""
    for data in blog_data:
        if data["id"] == index:
            selected_post = data
    return render_template("post.html", post=selected_post)


if __name__ == "__main__":
    app.run(debug=True)
