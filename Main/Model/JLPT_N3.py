from Main.Model.JLPT import JLPT
import os

class JLPT_N3(JLPT):

    def __init__(self):
        super().__init__()
        self.level = "N3"
        self.raw_directory = os.path.join(self.script_dir, '../JLPT_lists/raw_N3.txt')
        self.directory = os.path.join(self.script_dir, '../../JLPT_lists/N3.txt')