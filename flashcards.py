import os
from datetime import date
import pandas as pd

# class     
class card(object):
    """card in which you will store the info of the word you want to learn."""
    def __init__(self):
        super(card, self).__init__()
        
    def set(self,word:str,desc:str='',example:list=[],comments:str=[],tags:list=[],id:int=-1) -> None:
        """set card info
        Args:
            word (str): String of the word.
            desc (str, optional): Description of the word.
            example (str, optional): List of the example sentences. Defaults to [].
            comments (list, optional): List of any comments. Defaults to [].
            tags (list, optional): List of tags you want to assign. Defaults to [].
            ids (str,optional): ID.
        """
        self.word = word
        self.desc = desc
        self.example = example
        self.comments = comments
        self.tags = tags
        self.id =id
        self.score = [0,0] # [correct, total]

# method
def list2str(alist:list,sep='\t') -> str:
    """Merge String objects in a list, separating each element with the separator.

    Args:
        alist (list): list where the String objects are stored
        sep (str, optional): Separator. Defaults to '\t'.

    Returns:
        str: a single merged String object.
    """
    astr = ''
    for val in alist:
        astr += str(val) + sep
    return astr[0:-1]
    
def card2str(card:card,setname:str='',folder:str = '',format:str = '.txt',sep='\t') -> str:
    """save a card info 

    Args:
        card (card): A card object.
        setname (str, optional): name of set. If none, the name will be 'set_[current date].txt', if the set already exist, it will add the card to the existing text file.
        folder (str, optional): Folder path where you want to save the set. Defaults to ''.
        format (str, optional): Defaults to '.txt'.
    """
    # today = date.today()
    # file path for saving
    # word
    # desc_line = card.word + sep + list2str(card.desc,sep=sep)
    desc_line = card.word + sep + card.desc
    # exam_line = card.word + sep + list2str(card.example,sep=sep)
    # comm_line = card.word + sep + list2str
    return desc_line


def save_cards(cards:list,savepath:str)->None:
    output = ''
    for card in cards:
        # output += card2str(card) + '\n'
        output += card2str(card) + '\n'
    savefile = open(savepath,"w")
    n = savefile.write(output)
    savefile.close()

def getCardsFromWords(words:list,cards:list)->list:
    selected_cards = []
    for word in words:
        for card in cards:
            if card.word == word:
                selected_cards.append(card)
    return selected_cards

def get_CardSelectedIndexesFromWords(words:list,cards:list,selected_indexes:list) -> list:
    for i in range(len(cards)):
        acarad = cards[i]
        for j in range(len(words)):
            if acarad.word == words[j]:
                selected_indexes[i] = True
    return selected_indexes

def setFalseforUnselectedCards(words:list,cards:list,selected_indexes:list)->list:
    for i in range(len(cards)):
        acarad = cards[i]
        for j in range(len(words)):
            if acarad.word == words[j]:
                selected_indexes[i] = False
    return selected_indexes

def getCardsFromBooleans(cards:list,bools:list)->list:
    selected_cards = []
    for i, isSelected in enumerate(bools):
        if isSelected:
            selected_cards.append(cards[i])
    return selected_cards