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

game_info = ['', '']

conn = sql.connect('dictionary.db')
conn.text_factory = str
cur = conn.cursor()

root = Tk()
root.title("Modified Hangman")
root.resizable(width = FALSE, height = FALSE)
root_bg_image = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\Background.GIF')
root_bg = Label(root, image = root_bg_image)
root_bg.root_bg_image = root_bg_image
root_bg.place(x=0, y=0, relwidth=1, relheight=1)

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
def window_position(window, width, height):

    window_width = width
    window_height = height
    window_x = (ws/2) - (width/2)
    window_y = (hs/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (window_width, window_height, window_x, window_y))
    
window_position(root, 750, 500)



top_frame = Frame(root)

middle_frame = Frame(root)


bottom_frame = Frame(root, bg = 'white')
bottom_frame.pack(side = BOTTOM, expand = YES)

entry_label_text = StringVar()
entry_label_text.set('Please enter a search word:')
entry_label = Label(bottom_frame, bg = 'white', font = 32, textvariable = entry_label_text)
entry_label.pack(side = LEFT, anchor = S, padx = 1, pady = 1)
word_contained_entry = Entry(bottom_frame)
word_contained_entry.pack(side = LEFT, anchor = S, padx = 1, pady = 1)

word_frame = Frame(top_frame, bg = 'white')
hangman_frame = Frame(top_frame, bg = 'white')
letters_frame = Frame(middle_frame, bg = 'white')


canvas = Canvas(hangman_frame, bg = 'white', width = 200, height = 250)
hangman_image1 = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\stage1.GIF')
hangman_image2 = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\stage2.GIF')
hangman_image3 = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\stage3.GIF')
hangman_image4 = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\stage4.GIF')
hangman_image5 = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\stage5.GIF')
hangman_image6 = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\stage6.GIF')
hangman_image7 = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\stage7.GIF')
hangman_image8 = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\stage8.GIF')
hangman_image9 = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\stage9.GIF')


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

word_frame_game_info = Label(word_frame, font = 40, textvariable = correctLetters , bg = 'white')

def initial_correct_letter_space(correctLetters, correct_letter_spaces):
    for i in range(len(game_info[0])):
        correct_letter_spaces += '_'
    string_letter_spaces = string.join(correct_letter_spaces)
    correctLetters.set(string_letter_spaces)
    return correct_letter_spaces

letters_frame_incorrect_tries = Label(letters_frame, font = 40, textvariable = incorrectLetters, bg = 'white')


def initial_incorrect_letter_space(incorrectLetters):
    incorrectLetters.set('Incorrect Tries: ' + str(incorrectLettersCount[0]) + '\n' + string.join(incorrect_letter_spaces))
   

def make_word_contained_button():
    if (len(word_contained_entry.get()) > 0):
        word_contained_button_cmd()
    else:
        search_reminder()
word_contained_button = Button(bottom_frame, text = 'Submit search word', command = make_word_contained_button)
word_contained_button.pack(side = LEFT, anchor = S, pady = 1)

def word_contained_button_cmd():
    middle_frame.pack(side = TOP, expand = YES)
    top_frame.pack(side = TOP, expand = YES)
    word_frame.pack(side = LEFT, expand = YES)
    hangman_frame.pack(side = LEFT, expand = YES)
    letters_frame.pack(side = RIGHT, expand = YES)
    letters_frame_incorrect_tries.pack()
    get_game_info(game_info)
    initial_correct_letter_space(correctLetters, correct_letter_spaces)
    initial_incorrect_letter_space(incorrectLetters)
    word_contained_entry.delete(0, END)
    word_contained_entry.pack_forget()  
    letter_guess_entry.pack(side = LEFT, anchor = S, padx = 1, pady = 1)
    word_contained_button.pack_forget()
    word_frame_game_info.pack(padx = 4, pady = 4)
    letter_guess_button.pack(side = LEFT, anchor = S, pady = 1)
    entry_label_text.set('Please enter a letter guess:')

def search_warning_button_cmd():
    search_warning.withdraw()
    root.deiconify()

search_warning = Toplevel(bg = 'red')
search_warning.withdraw()
search_warning_message = Label(search_warning, text = 'Please make sure to enter a search word!', font = 40, bg = 'white')
search_warning_button = Button(search_warning, text = 'Try again', font = 32, command = search_warning_button_cmd, relief = RAISED)
search_warning.title('Modified Hangman')

def search_reminder():
    search_warning.deiconify()
    search_warning_message.pack(padx = 6, pady = 6)
    search_warning_button.pack()
    ##root.withdraw()
    ##search_warning.mainloop()

clue_frame = Frame(middle_frame, bg = 'white')
clue_frame.pack(side = LEFT, fill = BOTH, expand = YES)
clue_label_text = StringVar()
clue_label = Label(clue_frame, textvariable = clue_label_text, font = 32, wraplength = 300, justify = LEFT)
def clue_button_cmd():
    clue_label_text.set(game_info[1])
    clue_label.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
    clue_button.pack_forget()
##clue_frame_label = Label(clue_frame, text = 'Clue')
##clue_frame_label.pack()
clue_button = Button(clue_frame, text = 'Show clue', font = 32, relief = RAISED, command = clue_button_cmd)

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
        if(guess not in letters):
            letters.append(guess)
        return letters

def edit_letter_space(correct_letter_spaces, count, indices = None):
    if (indices != None):
        for i in indices:
            correct_letter_spaces[i] = game_info[0][i]
            correctLetters.set(string.join(correct_letter_spaces))
        return correct_letter_spaces
    if (indices == None):
        count += 1
        print count
        incorrectLetters.set('Incorrect Tries: ' + str(count) + '\n' + string.join(correct_letter_spaces))
        return count

def edit_hangman_space(IncorrectLettersCount):
    if (IncorrectLettersCount[0] == 1):
        canvas.pack()
        hangman_display = canvas.create_image(100, 125, image = hangman_image1)
    if (IncorrectLettersCount[0] == 2):
        hangman_display = canvas.create_image(100, 125, image = hangman_image2)
    if (IncorrectLettersCount[0] == 3):
        hangman_display = canvas.create_image(100, 125, image = hangman_image3)
    if (IncorrectLettersCount[0] == 4):
        hangman_display = canvas.create_image(100, 125, image = hangman_image4)
    if (IncorrectLettersCount[0] == 5):
        hangman_display = canvas.create_image(100, 125, image = hangman_image5)
    if (IncorrectLettersCount[0] == 6):
        hangman_display = canvas.create_image(100, 125, image = hangman_image6)
    if (IncorrectLettersCount[0] == 7):
        hangman_display = canvas.create_image(100, 125, image = hangman_image7)
    if (IncorrectLettersCount[0] == 8):
        hangman_display = canvas.create_image(100, 125, image = hangman_image8)
    if (IncorrectLettersCount[0] == 9):
        hangman_display = canvas.create_image(100, 125, image = hangman_image9)

letter_guess_entry = MaxLengthEntry(bottom_frame, width = 2, maxlength = 1, font = 40)
def letter_guess_button_cmd():
    match_check(match)
    match_action(correct_letter_indices, incorrect_letter_spaces, match)
    if (match[0] == 'True'):
        edit_letter_space(correct_letter_spaces, incorrectLettersCount[0], correct_letter_indices)
    if (match[0] == 'False'):
        incorrectLettersCount[0] = edit_letter_space(incorrect_letter_spaces, incorrectLettersCount[0])
    letter_guess_entry.delete(0, END)
    edit_hangman_space(incorrectLettersCount)
    if (incorrectLettersCount[0] == 5):
        ##clue_label.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
        clue_button.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
    if (incorrectLettersCount[0] == 10):
        game_over()
letter_guess_button = Button(bottom_frame, text = 'Submit letter guess', command = letter_guess_button_cmd)

def clear_setup():
    correct_letter_spaces[:] = []
    clue_label.pack_forget()
    clue_button.pack_forget()
    incorrectLettersCount[0] = 0
    incorrectLetters.set(initial_incorrect_letter_space(incorrectLetters))
    entry_label_text.set('Please enter a search word:')
    letter_guess_entry.pack_forget()
    letter_guess_button.pack_forget()
    entry_label.pack(side = LEFT, anchor = S, padx = 1, pady = 1)
    word_contained_entry.pack(side = LEFT, anchor = S, padx = 1, pady = 1)
    word_contained_button.pack(side = LEFT, anchor = S, pady = 1)
    middle_frame.pack_forget()
    top_frame.pack_forget()
    word_frame.pack_forget()
    hangman_frame.pack_forget()
    
    

def try_again_button_cmd():
    game_over_window.withdraw()
    clear_setup()
    root.deiconify()
    
    
game_over_window = Toplevel(bg = 'red')
game_over_window.title('Modified Hangman')
game_over_message = Label(game_over_window, bg = 'white', font = 40, text = 'GAME OVER!')
game_over_message.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
try_again = Button(game_over_window, text = 'Try again?', font = 40, relief = RAISED, command = try_again_button_cmd)
try_again.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
game_over_window.withdraw()

def game_over():
    root.withdraw()
    game_over_window.deiconify()

welcome_screen = Toplevel(bg = 'white')
welcome_screen.title('Modified Hangman')
welcome_screen.resizable(width = FALSE, height = FALSE)
welcome_screen.geometry('{}x{}'.format(740, 620))

window_position(welcome_screen, 740, 620)


def instructions_button_cmd():
    root.withdraw()
    welcome_screen.deiconify()

instructions_button = Button(bottom_frame, text = 'How to play', font = 40, relief = RAISED, command = instructions_button_cmd)
instructions_button.pack(side = RIGHT, anchor = E, padx = 2, pady = 1, expand = YES, fill = BOTH)

def begin_button_cmd():
    welcome_screen.withdraw()
    root.deiconify()

def welcome():
    welcome_screen_text = PhotoImage(file = 'C:\Users\Yevgeniy\OneDrive\Documents\CSCI 23300\GitHub Repos\Hangman\Hangman images\Welcome_Screen.GIF')
    background = Label(welcome_screen, image = welcome_screen_text)
    background.welcome_screen_text = welcome_screen_text
    background.pack()
    begin_button = Button(welcome_screen, text = 'Let''s play!', font = 40, relief = RAISED, command = begin_button_cmd)
    begin_button.pack(expand = YES, fill = X, anchor = N)
    root.withdraw()
    
welcome()
##root_bg.pack()
mainloop()
