import sqlite3 as sql
import random
from Tkinter import *

conn = sql.connect('dictionary.db')
conn.text_factory = str
cur = conn.cursor()

print cur.execute('SELECT word, pos, def FROM eng_dict WHERE word LIKE "%Abaist"')
                  
all_rows = cur.fetchall()
print('1):', all_rows)

conn.close()


root = Tk()
root.title("Modified Hangman")

top_frame = Frame(root)
top_frame.pack(side = TOP, fill = BOTH, expand = YES)

middle_frame = Frame(root)
middle_frame.pack(side = TOP, fill = BOTH, expand = YES)

##Entry Frame BEGIN##

bottom_frame = Frame(root, bg = 'yellow')
bottom_frame.pack(side = BOTTOM, fill = BOTH, expand = YES)

bottom_frame_label = Label(bottom_frame, anchor = S, text = 'Entry')
bottom_frame_label.pack()

word_contained = Entry(bottom_frame)
word_contained.pack(side = LEFT, anchor = S, padx = 1, pady = 1)

def retrieve_input():
    user_word = word_contained.get("1.0", 'end-1c')

word_contained_button = Button(bottom_frame, text = 'Submit', command = retrieve_input)
word_contained_button.pack(side = LEFT, anchor = S, pady = 1)
                                                     

##Entry Frame END##

##Word Frame BEGIN##

word_frame = Frame(top_frame, bg = 'red')
word_frame.pack(side = LEFT, fill = BOTH, expand = YES)
word_frame_label = Label(word_frame, text = 'Word')
word_frame_label.pack()

mystery_word = Text (word_frame, height = 4)
mystery_word.pack()

##Word Frame END##

##Hangman Frame BEGIN##

hangman_frame = Frame(top_frame, bg = 'purple')
hangman_frame.pack(side = LEFT, fill = BOTH, expand = YES)
hangman_frame_label = Label(hangman_frame, text = 'Hangman')
hangman_frame_label.pack()

##Hangman Frame END##

##Clue Frame BEGIN##

clue_frame = Frame(middle_frame, bg = 'light green')
clue_frame.pack(side = LEFT, fill = BOTH, expand = YES)
clue_frame_label = Label(clue_frame, text = 'Clue')
clue_frame_label.pack()

##Clue Frame END##

##Letters Frame BEGIN##

letters_frame = Frame(middle_frame, bg = 'orange')
letters_frame.pack(side = RIGHT, fill = BOTH, expand = YES)
letters_frame_label = Label(letters_frame, text = 'Letters Tried')
letters_frame_label.pack()

##Letters Frame END#

mainloop()



