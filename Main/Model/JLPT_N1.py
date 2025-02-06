from Main.Model.JLPT import JLPT
import os

class JLPT_N1(JLPT):

    def __init__(self):
        super().__init__()
        self.level = "N1"
        self.raw_directory = os.path.join(self.script_dir, '../../JLPT_lists/raw_N1.txt')
        self.directory = os.path.join(self.script_dir, '../../JLPT_lists/N1.txt')