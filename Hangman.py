import sqlite3 as sql
import random
import string
from Tkinter import *

 

conn = sql.connect('dictionary.db')
conn.text_factory = str
cur = conn.cursor()

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

def search_dict():
    test_word = retrieve_word_contained()
    cur.execute('SELECT word FROM eng_dict WHERE def LIKE ?', ('%' + test_word + '%',))
    return cur.fetchall()

game_word = ['']
def get_game_word(game_word):
    search_results = search_dict()
    game_word_tuple = random.choice(search_results)
    game_word[0] = string.join(game_word_tuple).lower()[3:]
    return game_word


correct_letter_indices = []
incorrect_letter_spaces = []
correct_letter_spaces = []
correctLetters = StringVar()
incorrectLetters = StringVar()

def initial_correct_letter_space(correctLetters, letter_spaces):
    for i in range(len(game_word[0])):
        letter_spaces += '_'
    string_letter_spaces = string.join(letter_spaces)
    correctLetters.set(string_letter_spaces)
    word_frame_game_word = Label(word_frame, font = 40, textvariable = correctLetters , bg = 'white')
    word_frame_game_word.pack(padx = 4, pady = 4)
    return letter_spaces

def initial_incorrect_letter_space(incorrectLetters):
    incorrectLetters.set('')
    letters_frame_incorrect_tries = Label(letters_frame, font = 40, textvariable = incorrectLetters, bg = 'white')
    letters_frame_incorrect_tries.pack()

match = ['False']
def match_check(match):
    match[0] = 'False'
    guess = letter_guess_entry.get()
    for i in range(len(game_word[0])):
        if(guess == game_word[0][i]):
            match[0] = 'True'
    return match
    
def match_action(indices, letters, match):
    guess = letter_guess_entry.get()
    if (match[0] == 'True'):
        for i in range(len(game_word[0])):
            if(guess == game_word[0][i]):
                indices.append(i)
        return indices
    if(match[0] == 'False'):
        letters.append(guess)
        return letters

def edit_letter_space(letter_spaces, indices = None):
    if (indices != None):
        for i in indices:
            letter_spaces[i] = game_word[0][i]
            correctLetters.set(string.join(letter_spaces))
        return letter_spaces
    if (indices == None):
            incorrectLetters.set(string.join(letter_spaces))
    

def letter_guess_button_cmd():
    match_check(match)
    match_action(correct_letter_indices, incorrect_letter_spaces, match)
    if (match[0] == 'True'):
        edit_letter_space(correct_letter_spaces, correct_letter_indices)
    if (match[0] == 'False'):
        edit_letter_space(incorrect_letter_spaces)
    

        

letter_guess_entry = Entry(bottom_frame)
letter_guess_button = Button(bottom_frame, text = 'Submit letter guess', command = letter_guess_button_cmd)

def word_contained_button_cmd():
    get_game_word(game_word)
    initial_correct_letter_space(correctLetters, correct_letter_spaces)
    initial_incorrect_letter_space(incorrectLetters)
    print game_word[0]
    word_contained_entry.pack_forget()  
    letter_guess_entry.pack(side = LEFT, anchor = S, padx = 1, pady = 1)
    word_contained_button.pack_forget()
    letter_guess_button.pack(side = LEFT, anchor = S, pady = 1)
    

word_contained_button = Button(bottom_frame, text = 'Submit search word', command = word_contained_button_cmd)
word_contained_button.pack(side = LEFT, anchor = S, pady = 1)


##Entry Frame END##

##Word Frame BEGIN##

word_frame = Frame(top_frame, bg = 'red')
word_frame.pack(side = LEFT, fill = BOTH, expand = YES)
word_frame_label = Label(word_frame, text = 'Word')
word_frame_label.pack()



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



