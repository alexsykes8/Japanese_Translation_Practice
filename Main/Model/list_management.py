from Main.Model.JLPT_N1 import JLPT_N1
from Main.Model.JLPT_N2 import JLPT_N2
from Main.Model.JLPT_N3 import JLPT_N3
from Main.Model.JLPT_N4 import JLPT_N4
from Main.Model.JLPT_N5 import JLPT_N5
from Main.Model.sudachipi import sentence_breakdown


"""
    This word is used to manage the lists of words for each JLPT level. It is used to search for words in the lists and to calculate the JLPT score of a sentence.
"""
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

    def search_lists(self, word):
        """
        This function searches for a word in the JLPT lists.
        :param word: the word to get the level of
        :return: the word and its level. none if it was not in a JLPT list
        """
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
        """
        This function calculates the JLPT score of a sentence.
        The JLPT score is a list of 5 numbers, each representing the number of words
        in the sentence that are from a particular JLPT level.
        :param sentence: the sentence to calculate the JLPT score of
        :return: analysis of the sentence: number of words from each JLPT level [N5, N4, N3, N2, N1],
         list of words that are not in a JLPT list, number of words in the sentence
        """
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

        return JLPT_distribution, non_JLPT_words, len(word_list)
