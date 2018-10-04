from cards import CardDeck
import curses
from utility import *
from random import randint
import time

class BlackJack():
    def __init__(self):
        self.customCardVals = {'a': 1,'j': 10,'q': 10,'k': 10}
        self.deck = CardDeck(False, False, self.customCardVals)
        self.deck.shuffle()
        self.state = {
            #  Player : [mode, hand, handVal]
            'user': {"mode": 'play', "hand": []},
            'comp': {"mode": 'play', "hand": []},
            'point': 0,
            'bustPoint': 0,
        }

    def resetGame(self):
        self.deck = CardDeck(False, False, self.customCardVals)
        self.deck.shuffle()
        self.state['user'] = {"mode": 'play', "hand": []}
        self.state['comp'] = {"mode": 'play', "hand": []}
        self.state['point'] = 0
        self.state['bustPoint'] = 0

    def runCompTurn(self):
        return 0


    def getHandVal(self, hand):
        ret = 0
        for card in hand:
            ret += self.deck.getCardVal(card)
        return ret


    def compHit(self):
        # the randint addds a change the computer will take a risk
        if self.getHandVal(self.state['comp']['hand']) < 18 and randint(0,1) == 0:
            self.state['comp']['hand'].append(self.deck.drawCard())
            # check if bust
            if self.getHandVal(self.state['comp']['hand']) > 21:
                self.state['comp']['mode'] = 'bust'
        else:
            self.state['comp']['mode'] = 'stay'


    def userHit(self):
        self.state['user']['hand'].append(self.deck.drawCard())
        # check if bust
        if self.getHandVal(self.state['user']['hand']) > 21:
            self.state['user']['mode'] = 'bust'
        

    def update(self, key):

        if self.state['user']['mode'] == 'bust' or self.state['comp']['mode'] == 'bust' or (self.state['user']['mode'] == "stay" and self.state['comp']['mode'] == "stay"):
            if key == 'KEY_LEFT' or key == 'a':
                self.state['bustPoint'] = (self.state['bustPoint'] + 1) % 2
            elif key == 'KEY_RIGHT' or key == 'd':
                self.state['bustPoint'] = (self.state['bustPoint'] - 1) % 2
            elif key == '\n':
                if self.state['bustPoint'] == 0: 
                    self.resetGame()
                elif self.state['bustPoint'] == 1:
                    self.resetGame()
                    return 'menu'

        elif self.state['user']['mode'] == 'play' and self.state['comp']['mode'] in ['play', 'stay']:
            if self.state['user']['hand'] == []:
                self.state['user']['hand'] += [self.deck.drawCard(), self.deck.drawCard()]
                self.state['comp']['hand'] += [self.deck.drawCard(), self.deck.drawCard()]
            else:
                if key == 'KEY_LEFT' or key == 'a':
                    self.state['point'] = (self.state['point'] + 1) % 2
                elif key == 'KEY_RIGHT' or key == 'd':
                    self.state['point'] = (self.state['point'] - 1) % 2
                elif key == '\n':
                    #  Hit
                    if self.state['point'] == 0: 
                        self.userHit()
                        if self.state['user']['mode'] != 'bust':
                            self.compHit()
                    #  Stay
                    if self.state['point'] == 1:  
                        self.state['user']['mode'] = 'stay'

        if self.state['user']['mode'] == 'stay' and self.state['comp']['mode'] == 'play':
            while self.state['comp']['mode'] == 'play':
                self.compHit()
                        
      
        
        
    def drawPopup(self, win, message='You Lose', buttons=["Play Again", "Quit"]):
        top = 22
        cPrint(win, " +------------------------------------------+ ", top, "center")
        cPrint(win, " +                                          + ", top + 1, "center")
        cPrint(win, " + {0:^40} + ".format(message), top + 2, "center")
        cPrint(win, " +                                          + ", top + 3, "center")
        cPrint(win, " +                                          + ", top + 4, "center")
        cPrint(win, " +                                          + ", top + 5, "center")
        cPrint(win, " +------------------------------------------+ ", top + 6, "center")

        lButton = " " + buttons[0] + " "
        rButton = " " + buttons[1] + " "

        leftButton = int(width / 2 - len(lButton))
        rightButton = int(width / 2 + 4)

        if self.state['bustPoint'] == 0: 
            win.addstr(top + 4, leftButton, lButton, curses.color_pair(1))
        else:
            win.addstr(top + 4, leftButton,lButton)

        if self.state['bustPoint'] == 1: 
            win.addstr(top + 4, rightButton, rButton, curses.color_pair(1))
        else:
            win.addstr(top + 4, rightButton, rButton)

        

    def draw(self, win):
        if self.state['user']['hand'] == []:
            cPrint(win, "Press a key to be dealt a hand", 10, "center", curses.A_BOLD)
        else:
            # Draw computer cards
            x = width - 17
            for card in self.state['comp']['hand']:
                # If the game is over, show the comp cards
                if self.state['user']['mode'] == 'bust' or self.state['comp']['mode'] == 'bust' or self.state['user']['mode'] == "stay" and self.state['comp']['mode'] == "stay":
                    printCard(win, x, 3, card)
                else:
                    printCard(win, x, 3)
                x -= 15
                
            x = int((width - (len(self.state['user']['hand']) * 14)) / 2)

            # draw players cards
            for card in self.state['user']['hand']:
                printCard(win, x, 13, card)
                x += 15
            
            if self.state['point'] == 0: 
                win.addstr(28, 15, " Hit ", curses.color_pair(1))
            else:
                win.addstr(28, 15, " Hit ")

            if self.state['point'] == 1: 
                win.addstr(28, 22, " Stay ", curses.color_pair(1))
            else:
                win.addstr(28, 22, " Stay ")

        if self.state['user']['mode'] == "bust":
            self.drawPopup(win, "You're Bust!")

        if self.state['comp']['mode'] == "bust":
            self.drawPopup(win, "You Win, the computer went bust")

        if self.state['user']['mode'] == "stay" and self.state['comp']['mode'] == "stay":
            userScore = 21 - self.getHandVal(self.state['user']['hand'])
            compScore = 21 - self.getHandVal(self.state['comp']['hand'])
            # Draw
            if userScore == compScore:
                self.drawPopup(win, "Draw, you both had " + str(self.getHandVal(self.state['user']['hand'])))
            # You Win
            if userScore < compScore:
                self.drawPopup(win, "You Win, you were closer to 21")
            # Comp wins
            if userScore > compScore:
                self.drawPopup(win, "You Lost, the computer was closer to 21")