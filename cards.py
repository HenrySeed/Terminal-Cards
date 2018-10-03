from random import randint, shuffle 


def blackOnRed(str):
    return '\x1b[30;41m' + str + '\033[0m'

def blackOnWhite(str):
    return '\x1b[30;107m' + str + '\033[0m'

def dim(str):
    return '\x1b[2m' + str + '\033[0m'

class CardDeck():
    def __init__(self, jokers=False, useColor=True, customCardVals=None):
        self.customCardVals = customCardVals
        self.spades = []
        self.clubs = []
        self.diamonds = []
        self.hearts = []
        self.jokers = []
        self.cardBack = ""
        self.cardHeight = 8
        self.cardWidth = 10
        self.useColor = useColor

        self.availableCards = []
        self.reset()

        count = 0
        tempStr = ""
        cardCount = 0
        aceLines = []
        for line in open('cards.txt').readlines():
            if cardCount >= 12:
                aceLines.append(line)
            else:
                tempStr += line
                if count == self.cardHeight:
                    count = 0
                    self.spades.append(tempStr.replace('S', '♠').strip())
                    self.clubs.append(tempStr.replace('S', '♣').strip())
                    self.diamonds.append(tempStr.replace('S', '◆').strip())
                    self.hearts.append(tempStr.replace('S', '♥').strip())
                    cardCount += 1
                    tempStr = ""
                else:
                    count += 1

        tempStr = ""
        cardCount = 0
        aceCards = []
        for line in aceLines:
                tempStr += line
                if count == self.cardHeight:
                    count = 0
                    if len(aceCards) == 4:
                        if len(self.jokers) == 2:
                            self.cardBack = tempStr.strip()
                        else:
                            self.jokers.append(tempStr.strip())
                    else:
                        aceCards.append(tempStr.strip())
                    tempStr = ""
                else:
                    count += 1

        self.spades = [aceCards[0]] + self.spades
        self.clubs = [aceCards[1]] + self.clubs
        self.hearts = [aceCards[2]] + self.hearts
        self.diamonds = [aceCards[3]] + self.diamonds

    '''
        Returns the given card art for a given code eg: 
            3h -> 3 of Hearts
            as -> Ace of Spades
            kc -> King of Clubs
    '''
    def getCard(self, code='00'):
        # if code == '00':
        #     code = self.drawCard(True)
        card = str(code[0:-1]).lower()
        suit = str(code[-1]).lower()

        #  Joker
        if suit == 'r' and card == 'j':
            if self.useColor:
                output = ""
                index = 0
                for line in self.jokers[0].split('\n'):
                    output += blackOnRed(line) + '\n'
                return output
            else:
                return self.jokers[0]
        elif suit == 'b' and card == 'j':
            return self.jokers[1]

        cardIndex = ['a','2','3','4','5','6','7','8','9','10','j','q','k']
        cardStr = ""
        if suit == 's': cardStr = self.spades[cardIndex.index(card)]
        if suit == 'c': cardStr = self.clubs[cardIndex.index(card)]
        if suit == 'h': cardStr = self.hearts[cardIndex.index(card)]
        if suit == 'd': cardStr = self.diamonds[cardIndex.index(card)]

        output = ""
        if (suit == 'd' or suit == 'h') and self.useColor:
            index = 0
            for line in cardStr.split('\n'):
                output += blackOnRed(line) + '\n'
        else:
            output = cardStr

        return output

    def getCardVal(self, code):
        card = str(code[0:-1]).lower()
        values = {
            'a': 1,
            'j': 11,
            'q': 12,
            'k': 13,
        }
        if self.customCardVals != None:
            values = self.customCardVals

        if card in ['a', 'j', 'q', 'k']:
            return values[card]
        else:
            return int(card)

    def shuffle(self):
        shuffle(self.availableCards)

    def reset(self):
        self.availableCards = []
        for card in ['a','2','3','4','5','6','7','8','9','10','j','q','k']:
            codes = []
            for suit in ['s', 'c', 'h', 'd']:
                self.availableCards.append(card + suit)
        if self.jokers:
            self.availableCards += ['jr', 'jb']

    def storeCards(self, codes):
        for code in codes:
            self.availableCards = [code] + self.availableCards
        cards = []

    def drawCard(self, infinite=False, random=False):
        if infinite:
            return self.availableCards[randint(0, len(self.availableCards)-1)]
        else:
            if random:
                return self.availableCards.pop(randint(0, len(self.availableCards)-1))
            else:
                return self.availableCards.pop()

    def getRowCards(self, codes):
        output = ""
        # We have to print row by row of each card
        for row in range(0, self.cardHeight+1): 
            for card in codes:
                output += self.getCard(card).split('\n')[row] + " "
            output += '\n'
        return output.strip()


    def __str__(self):
        print("Deck Contents ----------")
        toRet = ""
        for suit in ['s', 'c', 'h', 'd']:
            line = ""
            for card in ['a','2','3','4','5','6','7','8','9','10','j','q','k']:
                cardCode = card + suit
                if cardCode in self.availableCards:
                    line += cardCode + ' '
                else:
                    line += dim(cardCode) + ' '
                
            toRet += line + '\n'
        
        for joker in ['jb', 'jr']:
            if joker in self.availableCards:
                toRet += joker + " "
            else:
                toRet += dim(joker) + ' '
            

            
        return toRet.strip()








