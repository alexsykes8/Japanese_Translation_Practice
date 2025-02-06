from Main.Model.JLPT import JLPT
import os

class JLPT_N4(JLPT):

    def __init__(self):
        super().__init__()
        self.level = "N4"
        self.raw_directory = os.path.join(self.script_dir, '../JLPT_lists/raw_N4.txt')
        self.directory = os.path.join(self.script_dir, '../../JLPT_lists/N4.txt')