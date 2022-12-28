import re
import nltk
from typing import List

nltk.download('punkt')

def separate_string(string: str) -> List:
    
  sentences = nltk.sent_tokenize(string)
  return sentences
   
def split_on_new_lines(strings):
  split_strings = [s.split("\n") for s in strings]
  split_strings = [word for sublist in split_strings for word in sublist]
  return list(filter(None, split_strings))


