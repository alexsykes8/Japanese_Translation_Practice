from JLPT import JLPT

class JLPT_N5(JLPT):

    def __init__(self):
        super().__init__()
        self.level = "N5"
        self.raw_directory = '../JLPT_lists/raw_N5.txt'
        self.directory = '../JLPT_lists/N5.txt'

