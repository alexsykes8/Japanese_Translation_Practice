import sqlite3
import os

from Main.Model.book_management import BookManagement
from Main.Model.list_management import list_management
from Main.Model.wordsearch import WordSearch


class User:
    def __init__(self):
        self.user_name = None
        self.user_level = None
        self.known_words = []
        self.JLPT_lists = list_management()
        self.sentence_dictionary = BookManagement()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.user_db_path = os.path.join(self.script_dir, "../../user_files/users.db")


    def _create_user(self, name, level):
        connection = sqlite3.connect(self.user_db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (name,))
        existing_user = cursor.fetchone()
        if existing_user:
            print(f"User '{name}' already exists!")
            connection.close()
            return
        self.user_name = name
        self.user_level = level
        self._add_user_to_db()

    def create_user(self):
        user_name = input("What is your username? ")
        level = input("What is your JLPT level? (N5, N4, N3, N2, N1): ")
        while level not in ["N5", "N4", "N3", "N2", "N1"]:
            level = input("Invalid level. Please enter a valid JLPT level (N5, N4, N3, N2, N1): ")
        self._create_user(user_name, level)

    def login(self, user_name):
        connection = sqlite3.connect(self.user_db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT jlptlevel FROM users WHERE username = ?', (user_name,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("User not found.")
            return None
        else:
            self.user_name = user_name
            self.user_level = rows[0][0]
            self._load_known_words()

        self.JLPT_lists.set_user_level(self.user_level)
        self.JLPT_lists.initialise()



        connection.close()

        return self

    def search_for_word(self, word):
        word_searcher = WordSearch(self)
        print(word)
        return (word_searcher.search(word))


    def _add_user_to_db(self):
        connection = sqlite3.connect(self.user_db_path)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, jlptlevel TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS words (id INTEGER PRIMARY KEY, word TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_words (user_id INTEGER, word_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (word_id) REFERENCES words(id))''')


        cursor.execute('INSERT INTO users (username, jlptlevel) VALUES (?, ?)', (self.user_name, self.user_level))

        connection.commit()
        connection.close()

    def add_known_word(self, word):

        connection = sqlite3.connect(self.user_db_path)
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM words WHERE word = ?', (word,))
        word_row = cursor.fetchone()

        if word_row:
            word_id = word_row[0]
        else:
            cursor.execute('INSERT INTO words (word) VALUES (?)', (word,))
            word_id = cursor.lastrowid

        cursor.execute('SELECT id FROM users WHERE username = ?', (self.user_name,))
        user_row = cursor.fetchone()
        user_id = user_row[0]

        cursor.execute('INSERT INTO user_words (user_id, word_id) VALUES (?, ?)', (user_id, word_id))

        connection.commit()
        connection.close()

    def _load_known_words(self):
        connection = sqlite3.connect(self.user_db_path)
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM users WHERE username = ?', (self.user_name,))
        user_row = cursor.fetchone()
        user_id = user_row[0]

        cursor.execute('''SELECT w.word FROM words w 
                          JOIN user_words uw ON w.id = uw.word_id 
                          WHERE uw.user_id = ?''', (user_id,))
        rows = cursor.fetchall()

        self.known_words = [row[0] for row in rows]

        connection.close()


if __name__ == "__main__":
    connection = sqlite3.connect('../user_files/users.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM users')  # Delete all users
    cursor.execute('DELETE FROM words')  # Delete all words
    cursor.execute('DELETE FROM user_words')  # Delete all user-word relationships

    connection.commit()
    connection.close()
