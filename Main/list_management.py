from Main.JLPT_N1 import JLPT_N1
from Main.JLPT_N2 import JLPT_N2
from Main.JLPT_N3 import JLPT_N3
from Main.JLPT_N4 import JLPT_N4
from Main.JLPT_N5 import JLPT_N5

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
        self.search_word = None

    def set_user_level(self, level):
        self.user_level = level

    def initialise(self):

        self.N5 = JLPT_N5()
        self.N5.format()
        self.N5.create_dic()

        if self.user_level == "N5":
            return

        self.N4 = JLPT_N4()
        self.N4.format()
        self.N4.create_dic()

        if self.user_level == "N4":
            return

        self.N3 = JLPT_N3()
        self.N3.format()
        self.N3.create_dic()

        if self.user_level == "N3":
            return

        self.N2 = JLPT_N2()
        self.N2.format()
        self.N2.create_dic()

        if self.user_level == "N2":
            return

        self.N1 = JLPT_N1()
        self.N1.format()
        self.N1.create_dic()

        if self.user_level == "N1":
            return

        print("Could not initialise JLPT lists.")
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


    def set_search_word(self, word):
        self.search_word = word


    def search_lists(self):
        result = self.N5.search_dic(self.search_word)

        if self.user_level == "N5" or result != None:
            return result

        result = self.N4.search_dic(self.search_word)

        if self.user_level == "N4" or result != None:
            return result

        result = self.N3.search_dic(self.search_word)

        if self.user_level == "N3" or result != None:
            return result

        result = self.N2.search_dic(self.search_word)

        if self.user_level == "N2" or result != None:
            return result

        result = self.N1.search_dic(self.search_word)

        if self.user_level == "N1" or result != None:
            return result

        return None