import requests
from lxml import etree
import sqlite3


class WordSearch:
    def __init__(self, user):
        self.user = user

    def search(self, search_word):

        while (search_word != "q"):
            sentences = self.user.sentence_dictionary.search_dic(search_word)
            if sentences is None:
                print("Word not found")
                break
            scored_sentences = []
            for sentence in sentences:
                JLPT_score = self.user.JLPT_lists.calculate_JLPT_score(sentence)
                temp = []
                temp.append(sentence)
                temp.append(JLPT_score[0])  # JLPT score
                temp.append(JLPT_score[1])  # Extra non-JLPT words
                temp.append(JLPT_score[2])  # Number of words
                scored_sentences.append(temp)

            sorted_sentences = self.sort_sentences(scored_sentences)


            return (self.get_jisho_definition(search_word), sorted_sentences)



    def sort_sentences(self, sentences):
        """
        Sorts the sentences based on the number of words from each JLPT level, relative to the user's level.

        Args:
            sentences: the sentences to sort

        Returns:
            [[sentence,[scores],[words that aren't in a JLPT list], number of words in the sentence]
        """
        match self.user.user_level:
            case "N5":
                sorted_sentences = sorted(sentences, key=lambda x: (x[1][0], x[1][1], x[1][2], x[1][3], x[1][4]), reverse = True)
            case "N4":
                sorted_sentences = sorted(sentences, key=lambda x: (x[1][1], x[1][0], x[1][2], x[1][3], x[1][4]), reverse = True)
            case "N3":
                sorted_sentences = sorted(sentences, key=lambda x: (x[1][2], x[1][1], x[1][0], x[1][3], x[1][4]), reverse = True)
            case "N2":
                sorted_sentences = sorted(sentences, key=lambda x: (x[1][3], x[1][2], x[1][1], x[1][0], x[1][4]), reverse = True)
            case "N1":
                sorted_sentences = sorted(sentences, key=lambda x: (x[1][4], x[1][3], x[1][2], x[1][1], x[1][0]), reverse = True)
        return sorted_sentences

    def get_jisho_definition(self, word):
        url = f"https://jisho.org/api/v1/search/words?keyword={word}"
        response = requests.get(url)
        data = response.json()
        if data["data"]:
            senses = data["data"][0]["senses"]
            # Extract 'english_definitions' from each sense
            definitions = [sense["english_definitions"] for sense in senses]
            # Flatten the list if needed
            flat_definitions = [definition for sublist in definitions for definition in sublist]
            return flat_definitions
        else:
            return ["No definition found."]

    def get_edict_definition(self):
        # Parse the XML file
        tree = etree.parse("../dictionary_files/JMdict_e.xml")  # Replace with your actual file name
        # Example: Search for all entries with a specific word (kanji)
        kanji_to_search = "犬"

        # Use XPath to find all entries that contain a specific kanji
        entries = tree.xpath(f"//entry[k_ele/keb='{kanji_to_search}']")

        # Print the results
        for entry in entries:
            word = entry.xpath("k_ele/keb/text()")[0]
            reading = entry.xpath("r_ele/reb/text()")[0]
            glosses = entry.xpath("sense/gloss/text()")

            print(f"Word: {word}, Reading: {reading}, Meanings: {', '.join(glosses)}")


    def create_db(self):
        # Connect to SQLite (or create the file if it doesn't exist)
        conn = sqlite3.connect('../dictionary_files/edict.db')
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS kanji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kanji TEXT NOT NULL
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reading (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kanji_id INTEGER,
            reading TEXT NOT NULL,
            FOREIGN KEY (kanji_id) REFERENCES kanji(id)
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kanji_id INTEGER,
            pos TEXT,
            gloss TEXT,
            FOREIGN KEY (kanji_id) REFERENCES kanji(id)
        )''')

        return conn, cursor

    def parse_and_insert_xml(self,file_path, cursor):
        # Parse the XML file
        tree = etree.parse(file_path)
        root = tree.getroot()

        for entry in root.findall('entry'):
            # Extract Kanji
            kanji_elem = entry.find('k_ele/keb')
            kanji = kanji_elem.text if kanji_elem is not None else None
            if kanji:
                # Insert kanji into the kanji table
                cursor.execute('INSERT INTO kanji (kanji) VALUES (?)', (kanji,))
                kanji_id = cursor.lastrowid

                # Extract Readings
                for reb_elem in entry.findall('r_ele/reb'):
                    reading = reb_elem.text
                    if reading:
                        # Insert reading into the reading table
                        cursor.execute('INSERT INTO reading (kanji_id, reading) VALUES (?, ?)', (kanji_id, reading))

                # Extract Senses
                for sense_elem in entry.findall('sense'):
                    pos_elem = sense_elem.find('pos')
                    glosses = [gloss.text for gloss in sense_elem.findall('gloss')]
                    pos = pos_elem.text if pos_elem is not None else "Unknown"

                    # Insert senses into the sense table
                    for gloss in glosses:
                        cursor.execute('INSERT INTO sense (kanji_id, pos, gloss) VALUES (?, ?, ?)', (kanji_id, pos, gloss))

