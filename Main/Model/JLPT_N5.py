from Main.Model.JLPT import JLPT
import os

class JLPT_N5(JLPT):

    def __init__(self):
        super().__init__()
        self.level = "N5"
        self.raw_directory = os.path.join(self.script_dir, '../JLPT_lists/raw_N5.txt')
        self.directory = os.path.join(self.script_dir, '../../JLPT_lists/N5.txt')

