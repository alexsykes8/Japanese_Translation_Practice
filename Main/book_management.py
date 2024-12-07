import os
import re

import sudachipi
from Main.sudachipi import sentence_breakdown


class BookManagement:
    def __init__(self):
        self.directory_path = "../book_files"
        self.dictionary = {}
        self._add_books()

    def _get_dictionary(self):
        return self.dictionary

    def _save_dic_to_file(self):
        with open('../dictionary_files/book_dictionary.txt', 'w', encoding='utf-8') as file:
            for word in self.dictionary:
                file.write(f"{word}|{self.dictionary[word]}\n")

    def _load_dic_from_file(self):
        with open('../dictionary_files/book_dictionary.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split("|")
                cleaned_part = parts[1].replace("[", "").replace("]", "").replace("'", "")
                sentence_array = cleaned_part.split(", ")
                self.dictionary[parts[0]] = sentence_array

    def _add_book(self, book):
        self._books_added_to_dic(book)
        with open(book, 'r', encoding='utf-8') as file:
            for line in file:
                sentences = re.split(r'(?<=[。！？])|\n', line)                    # Check for matches in each sentence
                for sentence in sentences:
                    sentence = sentence.replace("\u3000", "")
                    sentence_composition = sudachipi.sentence_breakdown()
                    if sentence_composition.get_all_dict_forms():
                        for word in sentence_composition.get_all_dict_forms():
                            if word in self.dictionary:
                                self.dictionary[word].append(sentence)
                            else:
                                self.dictionary[word] = [sentence]

    def _books_added_to_dic(self,book):
        with open('../dictionary_files/books_added.txt', 'a', encoding='utf-8') as file:
            file.write(f"{book}\n")

    def _check_if_book_added(self,book):
        with open('../dictionary_files/books_added.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if book in line:
                    return True
        return False


    ## initialises the dictionary of words to sentences. should be run every time the program loads
    def _add_books(self):
        self._load_dic_from_file()
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.directory_path, filename)
                if not self._check_if_book_added(file_path):
                    self._add_book(file_path)
        self._save_dic_to_file()


    ## Given a word, will return all sentences in the book that contain the word
    def search_dic(self, word):
        return self.dictionary.get(word)

if __name__ == "__main__":
    book_management = BookManagement()
    book_management.add_books()
