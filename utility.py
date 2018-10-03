import os
import curses
from cards import CardDeck

rows, columns = os.popen('stty size', 'r').read().split() 
width = int(columns) - 3
height = int(rows) - 3

def cPrint(win, text, row=0, align="left", textMode=0, marginLeft=0, marginRight=0, marginTop=0):
    left = 0
    if textMode == 0:
        textMode = curses.color_pair(0)

    if align == "left": left = 0
    elif align == "center": left = int((width-len(text))/2)
    elif align == "right": left = int(width-len(text.split('\n')[0]))
    
    if '\n' in text:
        for line in text.split('\n'):
            win.addstr(row + marginTop, left + marginLeft - marginRight, line, textMode)
            row += 1
    else:
        win.addstr(row + marginTop, left + marginLeft - marginRight, text, textMode)


def printCard(win, x, y, cardCode=None):
    deck = CardDeck(True, False)
    if cardCode == None:
        card = deck.cardBack
        colorCode = 0
    else:
        card = deck.getCard(cardCode)

        suit = cardCode[-1]
        if suit == 'h' or suit == 'd':
            colorCode = 1
        else:
            colorCode = 0

    for line in card.split('\n'):
         win.addstr(y, x, line, curses.color_pair(colorCode))
         y += 1