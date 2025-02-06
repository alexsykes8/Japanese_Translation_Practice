import re
import os

class JLPT:

    """
    This class is the parent class for all JLPT levels. It represents all of the JLPT words associated with that level
    """

    def __init__(self):
        self.word_list = {}
        self.raw_directory = ''
        self.directory = ''
        self.script_dir = os.path.dirname(os.path.abspath(__file__))


    ## this should only be called if you want to reformat the raw txt files
    def format(self):
        with open(self.raw_directory, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        processed_lines = [self.process_line(line) for line in lines]
        with open(self.directory, 'w', encoding='utf-8') as file:
            file.write("\n".join(processed_lines))


    def process_line(self,line):
        """
        :param line: takes a line from the raw txt file
        :return: returns the word and meaning in the format "word|meaning"
        """
        parts = line.strip().split("\t")
        if len(parts) >= 3:
            word = re.sub(r'\[.*?\]', '', parts[0])
            meaning = parts[1]
            return f"{word}|{meaning}"
        else:
            return line


    def create_dic(self):
        """
        This function creates a dictionary of words and their meanings from a formatted dictionary text file
        :return: returns the dictionary of words to meanings
        """
        with open(self.directory, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line in lines:
            parts = line.strip().split("|")
            self.word_list[parts[0]] = parts[1]

    def search_dic(self, word):
        """
        This function searches the dictionary for a word
        :param word: word to be searched for
        :return: word's meaning
        """
        return self.word_list.get(word)