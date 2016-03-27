# Mini-project #6 - Blackjack
# http://www.codeskulptor.org/#user39_huPIFmJ6UJ_16.py
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
outcome_dealer = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        ans = "Hand contains "
        for card in self.hand:
            ans += card.get_suit()
            ans += card.get_rank()
            ans += " "
        return ans

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        sum = 0
        check = False
        for card in self.hand:
            sum += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                check = True
        if check:
            if sum + 10 <= 21:
                sum += 10 
                return sum
            else:	
                return sum
        else: 
            return sum
  
    def draw(self, canvas, pos):
        for card in self.hand:
            card.draw(canvas, pos)
            pos[0] += 72 + 20
        

# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS: 
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)
        
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        ans = "Deck contains "
        for card in self.deck:
            ans += card.get_suit()
            ans += card.get_rank()
            ans += " "
        return ans

# some global variables 
player = Hand()
dealer = Hand()
deck = Deck()

#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score, outcome_dealer
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    outcome = "Hit or stand?"
    outcome_dealer = ""
    in_play = True

def hit():
    global player, deck, outcome, score, in_play, outcome_dealer
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
            if player.get_value() > 21:
                outcome_dealer = "You went busted and lose"
                score -= 1
                outcome = "New deal?"
                in_play = False
    else:
        pass
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global player, deck, outcome, score, in_play, outcome_dealer
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            outcome_dealer = "Dealer has busted and you win!"
            outcome = "New deal?"
            score += 1
            in_play = False
        else:
            if dealer.get_value() >= player.get_value():
                outcome_dealer = "You lose."
                outcome = "New deal?"
                in_play = False
                score += -1
            else:
                outcome_dealer = "You win!"
                outcome = "New deal?"
                score += 1
                in_play = False
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [50, 60], 40, "Blue")
    canvas.draw_text("Score " + str(score), [280, 60], 30, "Black")
    
    canvas.draw_text("Dealer", [50, 130], 30, "Black")
    canvas.draw_text(outcome_dealer, [180, 130], 30, "Black")
    dealer.draw(canvas, [50, 170])
    
    # cover the first card of the dealer
    if in_play:
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [50 + 36, 170 + 48], CARD_SIZE)
        
    canvas.draw_text("Player", [50, 360], 30, "Black")
    canvas.draw_text(outcome, [180, 360], 30, "Black")
    player.draw(canvas, [50, 400])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()


# remember to review the gradic rubric