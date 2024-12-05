from JLPT import JLPT

class JLPT_N2(JLPT):

    def __init__(self):
        super().__init__()
        self.level = "N2"
        self.raw_directory = '../JLPT_lists/raw_N2.txt'
        self.directory = '../JLPT_lists/N2.txt'