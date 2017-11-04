import glob
import random

class BooksList:
    def __init__(self, path):
        self.path = path
        self.books = glob.glob(self.path + '/**.fb2.zip') + glob.glob(self.path + '/**.fb2')
        random.seed()
    def shuffle(self):
        random.shuffle(self.books)

