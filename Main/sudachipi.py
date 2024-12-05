from sudachipy import tokenizer
from sudachipy.dictionary import Dictionary

## Given a word, returns the dictionary form of the word

class sentence_breakdown:

    def __init__(self, sentence):
        self.sentence = sentence
        self.tokenizer_obj = Dictionary().create()
        self.mode = tokenizer.Tokenizer.SplitMode.C
        self.tokens = self.tokenizer_obj.tokenize(self.sentence, self.mode)
        self.search_word = None

    def get_all_dict_forms(self):
        # Filter tokens that are NOT particles and NOT punctuation and return their dictionary forms
        dict_forms = [
            token.dictionary_form()
            for token in self.tokens
            if '助詞' not in token.part_of_speech() and '補助記号' not in token.part_of_speech()
        ]
        return dict_forms

    def set_search_word(self, word):
        self.search_word = word

    def get_token(self):
        for token in self.tokens:
            if token.surface() == self.search_word:
                return token
        return "Word not found"

    def get_dict_form(self):
        for token in self.tokens:
            if token.surface() == self.search_word:
                return token.dictionary_form()
        return "Word not found"

if __name__ == "__main__":
    sentence = "私は猫が好きです。"
    breakdown = sentence_breakdown(sentence)
    print(breakdown.get_all_dict_forms())
    breakdown.set_search_word("猫")
    print(breakdown.get_dict_form())
    print(breakdown.get_token())

    token = breakdown.get_token()

    print(f"Word: {token.surface()}")
    print(f"POS: {token.part_of_speech()}")
