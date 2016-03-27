# implementation of card game - Memory
# http://www.codeskulptor.org/#user41_aC5ZKCxVL0yJbDe.py

import simplegui
import random

card1 = [1,2,3,4,5,6,7,8]
card2 = [1,2,3,4,5,6,7,8]
cards = []
cards_pos = range(16)
exposed = range(16)
mouse_pos = ()
state = 0
turn = 0
fst_choice = 10
snd_choice = 11

# helper function to initialize globals
def new_game():
    global card1, card2, cards, exposed, cards_pos, state, turn, fst_choice, snd_choice
    state = 1
    cards = card1 + card2
    #random.shuffle(cards)
    cur_pos = 0
    turn = 0
    fst_choice = 10
    snd_choice = 11
    for i in range(16):
        exposed[i] = False
        cards_pos[i] = cur_pos
        cur_pos += 50 
     
#define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, fst_choice, snd_choice, exposed, turn
    index = pos[0] // 50
    # avoid duplicated choice
    if(exposed[index] == True):
        pass
    else:
        if(state == 0):
            turn += 1
            state = 1
            fst_choice = show_card(pos)
        elif state == 1 :
            if cards[fst_choice] == cards[snd_choice]:
                pass
            else:
                exposed[fst_choice] = False
                exposed[snd_choice] = False
            state = 2
            fst_choice = show_card(pos)
        else:
            snd_choice = show_card(pos)
            turn += 1
            state = 1
          
def show_card(pos):
    global exposed  
    for i in range(16):
        if pos[0] >= cards_pos[i] and pos[0] <= cards_pos[i] + 50:
            exposed[i] = True
            break
    return i
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    cur_pos = 0
    for i in range(16):
        if exposed[i] == False:
            canvas.draw_polygon([[cur_pos, 0], [cur_pos + 50, 0], [cur_pos + 50, 100], [cur_pos, 100]], 2, 'Red', 'Green')
        else:
            canvas.draw_text(str(cards[i]), (cur_pos - 4 + 25, 60), 40, 'White')
        cur_pos += 50
        
    label.set_text("Turns = " + str(turn))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric