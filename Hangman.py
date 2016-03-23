import sqlite3 as sql
import random
from Tkinter import *
print sql.sqlite_version
 

conn = sql.connect('dictionary.db')
conn.text_factory = str
cur = conn.cursor()

cur.execute('SELECT word, pos, def FROM eng_dict WHERE word LIKE "%Abaist"')
                  
all_rows = cur.fetchall()
print all_rows

cur.execute('SELECT word, def FROM eng_dict WHERE word LIKE "%Abaist"')
print cur.fetchall()

    


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

word_contained_entry = Entry(bottom_frame)
word_contained_entry.pack(side = LEFT, anchor = S, padx = 1, pady = 1)

def retrieve_word_contained():
    return_word = word_contained_entry.get()
    return return_word

user_word = retrieve_word_contained

def search_dict():
    test_word = "   Flower"
    cur.execute('SELECT word, def FROM eng_dict WHERE word LIKE ?', (test_word,))
    return cur.fetchall()


def word_contained_button_cmd():
    retrieve_word_contained
    search_dict

word_contained_button = Button(bottom_frame, text = 'Submit', command = word_contained_button_cmd)
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



