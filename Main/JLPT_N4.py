from JLPT import JLPT

class JLPT_N4(JLPT):

    def __init__(self):
        super().__init__()
        self.level = "N4"
        self.raw_directory = '../JLPT_lists/raw_N4.txt'
        self.directory = '../JLPT_lists/N4.txt'