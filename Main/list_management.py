from Main.JLPT_N1 import JLPT_N1
from Main.JLPT_N2 import JLPT_N2
from Main.JLPT_N3 import JLPT_N3
from Main.JLPT_N4 import JLPT_N4
from Main.JLPT_N5 import JLPT_N5
from Main.sudachipi import sentence_breakdown


# Given a word, will check the JLPT lists that the user knows
# Will eventually be used to find the JLPT composition of sentences

class list_management:
    def __init__(self):
        self.N5 = None
        self.N4 = None
        self.N3 = None
        self.N2 = None
        self.N1 = None
        self.user_level = None
        self.sentence_breakdown = sentence_breakdown()
        self.score_distribution = None

    def set_user_level(self, level):
        self.user_level = level
        if self.user_level == "N5":
            self.score_distribution = [5,-1,-2,-3,-4]
        elif self.user_level == "N4":
            self.score_distribution = [4,5,-1,-2,-3]
        elif self.user_level == "N3":
            self.score_distribution = [3,4,5,-1,-2]
        elif self.user_level == "N2":
            self.score_distribution = [2,3,4,5,-1]
        elif self.user_level == "N1":
            self.score_distribution = [1,2,3,4,5]

    def initialise(self):

        self.N5 = JLPT_N5()
        self.N5.create_dic()

        self.N4 = JLPT_N4()
        self.N4.create_dic()

        self.N3 = JLPT_N3()
        self.N3.create_dic()

        self.N2 = JLPT_N2()
        self.N2.create_dic()

        self.N1 = JLPT_N1()
        self.N1.create_dic()

        return

    def get_JLPT_level(self):
        result = self.N5.search_dic(self.search_word)

        if result != None:
            return "N5"

        result = self.N4.search_dic(self.search_word)

        if result != None:
            return "N4"

        result = self.N3.search_dic(self.search_word)

        if result != None:
            return "N3"

        result = self.N2.search_dic(self.search_word)

        if result != None:
            return "N2"

        result = self.N1.search_dic(self.search_word)

        if result != None:
            return "N1"

        return None




    def search_lists(self, word):
        result = self.N5.search_dic(word)

        if result != None:
            return result, "N5"

        result = self.N4.search_dic(word)

        if result != None:
            return result, "N4"

        result = self.N3.search_dic(word)

        if result != None:
            return result,  "N3"

        result = self.N2.search_dic(word)

        if result != None:
            return result, "N2"

        result = self.N1.search_dic(word)

        if result != None:
            return result,  "N1"

        return None

    def calculate_JLPT_score(self, sentence):
        JLPT_distribution = [0,0,0,0,0]
        non_JLPT_words = []
        self.sentence_breakdown.set_sentence(sentence)
        word_list = self.sentence_breakdown.get_all_dict_forms()
        for word in word_list:
            result = self.search_lists(word)
            if result == None:
                non_JLPT_words.append(word)
            elif result[1] == "N5":
                JLPT_distribution[0] += 1
            elif result[1] == "N4":
                JLPT_distribution[1] += 1
            elif result[1] == "N3":
                JLPT_distribution[2] += 1
            elif result[1] == "N2":
                JLPT_distribution[3] += 1
            elif result[1] == "N1":
                JLPT_distribution[4] += 1
        for i in range(5):
            JLPT_distribution[i] = JLPT_distribution[i] / len(word_list)

        ##TODO make a new class to handle all this. You also need to get a dictionary for all the words the user won't know due to their JLPT level
        return JLPT_distribution, non_JLPT_words, len(word_list)
