from JLPT import JLPT

class JLPT_N3(JLPT):

    def __init__(self):
        super().__init__()
        self.level = "N3"
        self.raw_directory = '../JLPT_lists/raw_N3.txt'
        self.directory = '../JLPT_lists/N3.txt'