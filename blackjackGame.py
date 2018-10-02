from cards import CardDeck
import curses
from utility import *

class BlackJack():
    def __init__(self):
        self.deck = CardDeck()
        self.deck.shuffle()
        self.state = {
            'hand': [],
            'point': 0
        }

    def update(self, key):
        if self.state['hand'] == []:
            self.state['hand'] += [self.deck.drawCard(), self.deck.drawCard()]
        else:
            if key == 'KEY_LEFT' or key == 'a':
                self.state['point'] = (self.state['point'] + 1) % 2
            elif key == 'KEY_RIGHT' or key == 'd':
                self.state['point'] = (self.state['point'] - 1) % 2
            elif key == '\n':
                #  Hit
                if self.state['point'] == 0: self.state['hand'] += [self.deck.drawCard()]
                #  Stay
                # if self.state['point'] == 0: 


    def draw(self, win):
        if self.state['hand'] == []:
            cPrint(win, "Press a key to be dealt a hand", 10, "center", curses.A_BOLD)
        else:
            x = int((width - (len(self.state['hand']) * 14)) / 2)

            for card in self.state['hand']:
                printCard(win, x, 6, card)
                x += 15
            
            if self.state['point'] == 0: 
                win.addstr(20, 15, " Hit ", curses.color_pair(1))
            else:
                win.addstr(20, 15, " Hit ")

            if self.state['point'] == 1: 
                win.addstr(20, 22, " Stay ", curses.color_pair(1))
            else:
                win.addstr(20, 22, " Stay ")