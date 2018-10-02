import os
import curses
from cards import CardDeck

rows, columns = os.popen('stty size', 'r').read().split() 
width = int(columns) - 3
height = int(rows) - 3

def cPrint(win, str, row=0, align="left", textMode=0):
    if textMode == 0:
        textMode = curses.color_pair(0)
    if align == "left":
        win.addstr(row, 0, str,textMode)
    elif align == "center":
        win.addstr(row, int((width-len(str))/2), str, textMode)
    elif align == "right":
        win.addstr(row, int(width-len(str.split('\n')[0])), str, textMode)


def printCard(win, x, y, cardCode):
    deck = CardDeck(True, False)
    card = deck.getCard(cardCode)
    suit = cardCode[-1]
    if suit == 'h' or suit == 'd':
        colorCode = 1
    else:
        colorCode = 0

    for line in card.split('\n'):
         win.addstr(y, x, line, curses.color_pair(colorCode))
         y += 1