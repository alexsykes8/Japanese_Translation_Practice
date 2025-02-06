from flask import Flask, render_template, redirect, url_for, request, session
from Main.Model.user import User

app = Flask(__name__)
app.secret_key = 'tiger'

user = User()
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")

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
            return redirect(url_for('search_page'))
        elif action == "logout":
            session.pop('username', None)
            return redirect(url_for('login'))

    return render_template("main_menu.html")

def read_sentences_from_file(filename="sentences.txt"):
    with open(filename, 'r', encoding='utf-8') as file:
        sentences = [line.strip() for line in file.readlines()]  # Remove the newline and store in a 1D list
    return sentences


def write_sentences_to_file(sentences, filename="sentences.txt"):
    with open(filename, 'w', encoding='utf-8') as file:
        for sentence in sentences:
            file.write(sentence[0] + '\n')


@app.route("/search", methods=["GET", "POST"])
def search_page():
    if 'index' not in session:
        session['index'] = 0

    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        action = request.form.get("action")  # Check for button actions
        word = request.form.get("word")

        if action == "next_sentence":
            sentences = read_sentences_from_file()
            session['index'] = (session['index'] + 1) % len(sentences)
            sentence = sentences[session['index']]
            return render_template("search_results.html", sentences=sentence)

        elif action == "return":
            return redirect(url_for('main_menu'))

        elif word:
            result = user.search_for_word(word)
            definition = result[0]
            sentences = result[1]
            write_sentences_to_file(sentences)
            return render_template("search_results.html", definition = definition, sentences=sentences[0][0])

        else:
            return render_template("search_page.html", error="Please enter a word.")

    return render_template("search_page.html")

if __name__ == "__main__":
    app.run(debug=True)