import os
import time
from cards import CardDeck

# while(1):
#     deck = CardDeck(jokers=True)
#     deck.shuffle()
#     os.system('clear')
#     print(deck)

#     for i in range(0, 4):
#         hand = []
#         for i in range(0, 5):
#             hand.append(deck.drawCard())

#         print(deck.getRowCards(hand))
#         print(' ')

#     print(deck)
#     time.sleep(0.5)

deck = CardDeck(True, False)
print(deck.getCardVal('js'))
