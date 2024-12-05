import re

class JLPT:

    def __init__(self):
        self.word_list = {}
        self.raw_directory = ''
        self.directory = ''

    def format(self):
        with open(self.raw_directory, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        processed_lines = [self.process_line(line) for line in lines]
        with open(self.directory, 'w', encoding='utf-8') as file:
            file.write("\n".join(processed_lines))

    def process_line(self,line):
        parts = line.strip().split("\t")
        if len(parts) >= 3:
            word = re.sub(r'\[.*?\]', '', parts[0])
            meaning = parts[1]
            return f"{word}|{meaning}"
        else:
            return line

    def create_dic(self):
        with open(self.directory, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line in lines:
            parts = line.strip().split("|")
            self.word_list[parts[0]] = parts[1]

    def search_dic(self, word):
        return self.word_list.get(word)