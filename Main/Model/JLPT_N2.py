from Main.Model.JLPT import JLPT
import os

class JLPT_N2(JLPT):

    def __init__(self):
        super().__init__()
        self.level = "N2"
        self.raw_directory = os.path.join(self.script_dir, '../JLPT_lists/raw_N2.txt')
        self.directory = os.path.join(self.script_dir, '../../JLPT_lists/N2.txt')