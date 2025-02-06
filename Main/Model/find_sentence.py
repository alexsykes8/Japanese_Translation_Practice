import os
import re

class SearchFiles:

    def __init__(self, search_term):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.directory_path = self.user_db_path = os.path.join(self.script_dir, "../book_files")
        self.search_term = search_term
        self.pattern = re.compile(re.escape(search_term), re.UNICODE)

    def return_sentence(self):
        matches = []
        # Iterate through files in the directory
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.directory_path, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    # Split content into sentences
                    sentences = re.split(r'(?<=[。！？])|\n', content)                    # Check for matches in each sentence
                    for sentence in sentences:
                        if self.pattern.search(sentence):
                            matches.append(f"Found in {filename}: {sentence.strip()}")
        return matches

    def score_sentence(self):
        pass

if __name__ == "__main__":
    searcher = SearchFiles("我輩")
    for result in searcher.return_sentence():
        print(result)
