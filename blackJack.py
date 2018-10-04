from cards import CardDeck
import curses
from utility import *
import time
import copy
from blackjackGame import BlackJack


def setupColour(win):
    # Uses default terminal colours
    curses.use_default_colors()
    curses.init_pair(0, 0, -1)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)


def main(win):
    # sets sursor to invisible
    curses.curs_set(0)
    win.nodelay(True)
    win.clear() 
    setupColour(win)
    
    # Set up the deck of cards for the menu
    deck = CardDeck(True, False)

    # Set up the game for the game view mode
    game = BlackJack()

    # Mode for view
    state = {"mode": 'menu', 'point': 0, 'game': game.state, 'gameUpdateOutput': None}

    drawMenu(win, state, deck)

    oldState = 0
    key = ""
    while 1:  
        oldState = copy.deepcopy(state)
        try:
            key = win.getkey() 

            if state["mode"] == 'menu':
                if key == 'q':
                    return
                # reset the point incase we have been at the menu before
                if oldState['mode'] != 'menu':
                    state['point'] = 0
                # We use mod 1 below because there are only 2 menu items, 0 and 1 (play and quit)
                if key == 'KEY_UP' or key == 'w':
                    state['point'] = (state['point'] - 1) % 2
                elif key == 'KEY_DOWN' or key == 's':
                    state['point'] = (state['point'] + 1) % 2


                if state['point'] == 1:
                    if key == '\n':
                        return
                elif state['point'] == 0:
                    if key == '\n':
                        state['mode'] = 'game'
                
            elif state["mode"] == 'landing':
                if key == 'q':
                    return
                else:
                    state['mode'] = 'menu'

            elif state['mode'] == 'game':
                if key == 'q':
                    state['mode'] = 'menu'
                    game.resetGame()
                else:
                    state["gameUpdateOutput"] = game.update(key)
                    if state["gameUpdateOutput"] == 'menu':
                        state['mode'] = 'menu'
                    
        except Exception as e:
            # No input   
            if str(e) != 'no input':
                win.addstr(35, 0, ' ' * 100)
                win.addstr(35, 0, "ERROR: {0}".format(e))
            pass  

        # If an update the state is found, redraw the page
        if oldState == state:
            continue

        # Clear the window is always needed
        win.clear() 

        # Helpful debug
        win.addstr(30, 0, "Key: " + str(key) + "\n  State: " + str(state))
        win.addstr(34, 0, "User: " + str(state['game']['user']))
        win.addstr(35, 0, "Computer: " + str(state['game']['comp']))

        # Print the menu
        if state["mode"] == 'menu':
            drawMenu(win, state, deck)


        if state['mode'] == 'game':
            game.draw(win)


def drawMenu(win, state, deck):
    # Load logo
    logo = '''
  ____  _            _    _            _    
 |  _ \| |          | |  (_)          | |   
 | |_) | | __ _  ___| | ___  __ _  ___| | __
 |  _ <| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
 | |_) | | (_| | (__|   <| | (_| | (__|   < 
 |____/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\
                        _/ |                
                       |__/   '''

    cPrint(win, logo, marginLeft=3)

    if state['point'] == 0: 
        win.addstr(9, 7, " Play ", curses.color_pair(1))
    else:
        win.addstr(9, 7, " Play ")

    if state['point'] == 1: 
        win.addstr(11, 7, " Quit ", curses.color_pair(1))
    else:
        win.addstr(11, 7, " Quit ")

    printCard(win, width-15, 5, deck.drawCard(infinite=False, random=True))
    printCard(win, width-30, 5, deck.drawCard(infinite=False, random=True))
    deck.reset()

def gameScreen(win, deck):
    # Draw two cards for the user
    hand = []
    hand.append(deck.drawCard())
    hand.append(deck.drawCard())

    win.addstr(4, 0, deck.getRowCards(hands), curses.color_pair(1))

curses.wrapper(main)