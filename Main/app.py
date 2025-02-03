from flask import Flask, render_template, redirect, url_for, request, session
from user import User
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Route for the login page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")

        user = User()
        if user.login(username):
            session['username'] = username
            return redirect(url_for('main_menu'))
        else:
            return render_template("login.html", error="Login failed.")
    return render_template("login.html")


@app.route("/main", methods=["GET", "POST"])
def main_menu():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        action = request.form.get("action")

        if action == "search":
            word = "example word"
            return render_template("main_menu.html", word=word)
        elif action == "logout":
            session.pop('username', None)
            return redirect(url_for('login'))

    return render_template("main_menu.html")


if __name__ == "__main__":
    app.run(debug=True)
