import sqlite3 as sql, random, string, time
from Tkinter import *

class ValidatingEntry(Entry):
    # base class for validating entry widgets

    def __init__(self, master, value="", **kw):
        apply(Entry.__init__, (self, master), kw)
        self.__value = value
        self.__variable = StringVar()
        self.__variable.set(value)
        self.__variable.trace("w", self.__callback)
        self.config(textvariable=self.__variable)

    def __callback(self, *dummy):
        value = self.__variable.get()
        newvalue = self.validate(value)
        if newvalue is None:
            self.__variable.set(self.__value)
        elif newvalue != value:
            self.__value = newvalue
            self.__variable.set(self.newvalue)
        else:
            self.__value = value

    def validate(self, value):
        # override: return value, new value, or None if invalid
        return value

class MaxLengthEntry(ValidatingEntry):

    def __init__(self, master, value="", maxlength=None, **kw):
        self.maxlength = maxlength
        apply(ValidatingEntry.__init__, (self, master), kw)

    def validate(self, value):
        if self.maxlength is None or len(value) <= self.maxlength:
            return value
        return None # new value too long

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

game_info = ['', '']
def get_game_info(game_info):
    test_word = word_contained_entry.get()
    cur.execute('SELECT word, def FROM eng_dict WHERE def LIKE ?', ('%' + test_word + '%',))
    search_results = cur.fetchall()
    game_info_tuple = random.choice(search_results)
    game_info[0] = game_info_tuple[0].lower()[3:]
    game_info[1] = game_info_tuple[1].lower()
    print game_info
    return game_info

correct_letter_indices = []
incorrect_letter_spaces = []
correct_letter_spaces = []
correctLetters = StringVar()
incorrectLetters = StringVar()
incorrectLettersCount = [0]

def initial_correct_letter_space(correctLetters, letter_spaces):
    for i in range(len(game_info[0])):
        letter_spaces += '_'
    string_letter_spaces = string.join(letter_spaces)
    correctLetters.set(string_letter_spaces)
    word_frame_game_info = Label(word_frame, font = 40, textvariable = correctLetters , bg = 'white')
    word_frame_game_info.pack(padx = 4, pady = 4)
    return letter_spaces

def initial_incorrect_letter_space(incorrectLetters):
    incorrectLetters.set('Incorrect Tries: ' + str(incorrectLettersCount[0]) + '\n' + string.join(incorrect_letter_spaces))
    letters_frame_incorrect_tries = Label(letters_frame, font = 40, textvariable = incorrectLetters, bg = 'white')
    letters_frame_incorrect_tries.pack()

match = ['False']
def match_check(match):
    match[0] = 'False'
    guess = letter_guess_entry.get()
    for i in range(len(game_info[0])):
        if(guess == game_info[0][i]):
            match[0] = 'True'
    return match
    
def match_action(indices, letters, match):
    guess = letter_guess_entry.get()
    if (match[0] == 'True'):
        for i in range(len(game_info[0])):
            if(guess == game_info[0][i]):
                indices.append(i)
        return indices
    if(match[0] == 'False'):
        letters.append(guess)
        return letters

def edit_letter_space(letter_spaces, count, indices = None):
    if (indices != None):
        for i in indices:
            letter_spaces[i] = game_info[0][i]
            correctLetters.set(string.join(letter_spaces))
        return letter_spaces
    if (indices == None):
        count += 1
        print count
        incorrectLetters.set('Incorrect Tries: ' + str(count) + '\n' + string.join(letter_spaces))
        return count

    

def game_over():
    top_frame.pack_forget()
    middle_frame.pack_forget()
    bottom_frame.pack_forget()
    game_over_frame = Frame(bg = 'red')
    game_over_frame.pack(expand = YES, fill = BOTH)
    game_over_label = Label(game_over_frame, bg = 'white', font = 40, text = 'GAME OVER!')
    game_over_label.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
    try_again = Button(game_over_frame, text = 'Try again?', font = 40, relief = RAISED)
    try_again.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
    
    
    
    
def letter_guess_button_cmd():
    match_check(match)
    match_action(correct_letter_indices, incorrect_letter_spaces, match)
    if (match[0] == 'True'):
        edit_letter_space(correct_letter_spaces, incorrectLettersCount[0], correct_letter_indices)
    if (match[0] == 'False'):
        incorrectLettersCount[0] = edit_letter_space(incorrect_letter_spaces, incorrectLettersCount[0])
    letter_guess_entry.delete(0, END)
    if (incorrectLettersCount[0] == 10):
        game_over()
           

letter_guess_entry = MaxLengthEntry(bottom_frame, width = 2, maxlength = 1, font = 40)
letter_guess_button = Button(bottom_frame, text = 'Submit letter guess', command = letter_guess_button_cmd)

def word_contained_button_cmd():
    get_game_info(game_info)
    initial_correct_letter_space(correctLetters, correct_letter_spaces)
    initial_incorrect_letter_space(incorrectLetters)
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



