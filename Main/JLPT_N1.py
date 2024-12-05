from JLPT import JLPT

class JLPT_N1(JLPT):

    def __init__(self):
        super().__init__()
        self.level = "N1"
        self.raw_directory = '../JLPT_lists/raw_N1.txt'
        self.directory = '../JLPT_lists/N1.txt'