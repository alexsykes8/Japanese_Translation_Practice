import os
import re

from Main.Model import sudachipi


class BookManagement:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.directory_path = os.path.join(self.script_dir, '../../book_files')
        self.book_dictionary_path = os.path.join(self.script_dir, '../../dictionary_files/book_dictionary.txt')
        self.dictionary = {}
        self._add_books()

    def _get_dictionary(self):
        return self.dictionary

    def _save_dic_to_file(self):
        with open(self.book_dictionary_path, 'w', encoding='utf-8') as file:
            for word in self.dictionary:
                file.write(f"{word}|{self.dictionary[word]}\n")

    def _load_dic_from_file(self):
        with open(self.book_dictionary_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split("|")
                cleaned_part = parts[1].replace("[", "").replace("]", "").replace("'", "")
                sentence_array = cleaned_part.split(", ")
                self.dictionary[parts[0]] = sentence_array

    def _add_book(self, book):
        """
        Adds a book to the dictionary. Looks at each sentence in the book and
        adds it to the dictionary in the entries of the words that are in the sentence
        :param book: book to be added
        """
        # notes that the book is added so that it is skipped in future
        self._books_added_to_dic(book)
        file_path = os.path.join(self.directory_path, book)
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                sentences = re.split(r'(?<=[。！？])|\n', line)                    # Check for matches in each sentence
                for sentence in sentences:
                    sentence = sentence.replace("\u3000", "")
                    # uses sudachipi to break down the sentence into its component words
                    sentence_composition = sudachipi.sentence_breakdown()
                    sentence_composition.set_sentence(sentence)
                    if sentence_composition.get_all_dict_forms():
                        for word in sentence_composition.get_all_dict_forms():
                            if word in self.dictionary:
                                self.dictionary[word].append(sentence)
                            else:
                                self.dictionary[word] = [sentence]

    def _books_added_to_dic(self,book):
        """
        Once a book is added to the dictionary, make a note of it
        :param book: book that was added
        """
        file_path = os.path.join(self.script_dir, '../../dictionary_files/books_added.txt')
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{book}\n")

    def _check_if_book_added(self,book):
        """
        checks if a book has already been added to the dictionary
        :param book: the book to check for
        :return: true if already in dict, false if not
        """
        file_path = os.path.join(self.script_dir, '../../dictionary_files/books_added.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if book in line:
                    return True
        return False


    def _add_books(self):
        """
        initialises the dictionary of words to sentences to be used for searching. should be run every time the program loads
        """
        # loads the existing dictionary
        self._load_dic_from_file()
        # checks if any new books have been added
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".txt"):
                if not self._check_if_book_added(filename):
                    # if there is a new book, add its sentences to the dictionary
                    self._add_book(filename)
        # save the new dictionary
        self._save_dic_to_file()


    def search_dic(self, word):
        """
        Given a word, will return all sentences in the book that contain the word
        :param word: word to look for
        :return: a list of sentences which contain the word
        """
        return self.dictionary.get(word)

if __name__ == "__main__":
    book_management = BookManagement()
    book_management._add_books()
