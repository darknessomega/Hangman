import sqlite3 as sql, random, string
from Tkinter import * ##for GUI


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

##Allow for restriction of entry length
class MaxLengthEntry(ValidatingEntry): 

    def __init__(self, master, value="", maxlength=None, **kw):
        self.maxlength = maxlength
        apply(ValidatingEntry.__init__, (self, master), kw)

    def validate(self, value):
        if self.maxlength is None or len(value) <= self.maxlength:
            return value
        return None # new value too long

##List to be used to store game word and game definition
game_info = ['', '']

##Connect to English dictionary database
conn = sql.connect('dictionary.db') 
conn.text_factory = str
cur = conn.cursor()

##Main GUI window created
root = Tk()
# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen


def window_position(window, width, height):
    window_width = width
    window_height = height
    window_x = (ws/2) - (width/2)
    window_y = (hs/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (window_width, window_height, window_x, window_y))
    window.resizable(width = FALSE, height = FALSE)
##Post-condition: window will be centered on-screen

##Title and background of main GUI window set-up
root.title("Modified Hangman")
root_bg_image = PhotoImage(file = 'Background.gif')
root_bg = Label(root, image = root_bg_image)
root_bg.root_bg_image = root_bg_image
root_bg.place(x=0, y=0, relwidth=1, relheight=1)    
window_position(root, 1000, 500)

##Main GUI windows split into three horizontal frames
top_frame = Frame(root)
middle_frame = Frame(root)
bottom_frame = Frame(root, bg = 'white')
bottom_frame.pack(side = BOTTOM, expand = YES)

##Entry box and prompt
entry_label_text = StringVar()
entry_label_text.set('Please enter a search word:')
entry_label = Label(bottom_frame, bg = 'white', font = 32, textvariable = entry_label_text)
entry_label.pack(side = LEFT, anchor = S, padx = 1, pady = 1)
word_contained_entry = Entry(bottom_frame, font = 32)
word_contained_entry.pack(side = LEFT, anchor = S, padx = 1, pady = 1)

##Smaller frames within three large frames
word_frame = Frame(top_frame, bg = 'white')
hangman_frame = Frame(top_frame, bg = 'white')
letters_frame = Frame(middle_frame, bg = 'white')

##Set-up of hangman images
hangman_canvas = Canvas(hangman_frame, bg = 'white', width = 200, height = 250)
hangman_image1 = PhotoImage(file = 'stage1.gif')
hangman_image2 = PhotoImage(file = 'stage2.gif')
hangman_image3 = PhotoImage(file = 'stage3.gif')
hangman_image4 = PhotoImage(file = 'stage4.gif')
hangman_image5 = PhotoImage(file = 'stage5.gif')
hangman_image6 = PhotoImage(file = 'stage6.gif')
hangman_image7 = PhotoImage(file = 'stage7.gif')
hangman_image8 = PhotoImage(file = 'stage8.gif')
hangman_image9 = PhotoImage(file = 'stage9.gif')

def begin_button_cmd():
    welcome_screen.withdraw()
    pick_easy.configure(state = DISABLED)
    pick_hard.configure(state = DISABLED)
    root.deiconify()
##Post-condition: Welcome screen is replaced with main game screen

##Welcome screen set-up
welcome_screen = Toplevel()
welcome_screen.title('Modified Hangman')
window_position(welcome_screen, 1000, 500)

##Button to begin game
welcome_screen_canvas = Canvas(welcome_screen, width = 1000, height = 500)
begin_button = Button(welcome_screen, text = 'Let''s play!', font = 40, relief = RAISED, state = DISABLED, command = begin_button_cmd)
begin_button.configure(width = 40)

##Difficulty options set-up
diff_var = IntVar()
pick_easy = Radiobutton(welcome_screen, text = "Easy: 10 attempts", font = 20, variable = diff_var, value = 1,
                        command = lambda: begin_button.config(state = NORMAL), relief = RAISED)
pick_hard = Radiobutton(welcome_screen, text = "Hard: 5 attempts", font = 20, variable = diff_var, value = 2,
                        command = lambda: begin_button.config(state = NORMAL), relief = RAISED)
##Necessary for better aesthetic of difficulty option button after the first round
dummy_diff = Radiobutton(welcome_screen, variable = diff_var, value = 3)

##Welcome screen background and text set-up
welcome_screen_bg_image = PhotoImage(file = 'Background2.gif')
welcome_screen_bg = welcome_screen_canvas.create_image(0, 0, image = welcome_screen_bg_image)
welcome_screen_instructions_text = """Once you select a difficulty below and press begin, you will be prompted to enter a
word, let's call it the search word. The dictionary will be searched for the words, let's call them
game words, that have the search word in their definitions. Of these game words, one will be
randomly selected. It is this word that you will be guessing.
We like losers and winners equally here, so have no fear, and enjoy!"""

##Logo of game
welcome_screen_logo_image = PhotoImage(file = 'Logo.gif')
welcome_screen_logo = welcome_screen_canvas.create_image(500, 130, image = welcome_screen_logo_image)

welcome_screen_instructions = welcome_screen_canvas.create_text(480, 390, font = ("Arial", 16, "bold"), text = welcome_screen_instructions_text)
welcome_screen_canvas.pack()
##End: Welcome screen set-up

def instructions_button_cmd():
    root.withdraw()
    welcome_screen.deiconify()
instructions_button = Button(bottom_frame, text = 'How to play', font = 20, relief = RAISED, command = instructions_button_cmd)
instructions_button.pack(side = RIGHT, anchor = E, padx = 2, pady = 1, expand = YES, fill = BOTH)
##Post-condition: Welcome screen back on screen; main game window hidden

def welcome():
    begin_button_window = welcome_screen_canvas.create_window(771, 478, window = begin_button)
    pick_easy_button_window = welcome_screen_canvas.create_window(100, 480, window = pick_easy)
    pick_hard_button_window = welcome_screen_canvas.create_window(290, 480, window = pick_hard)
    root.withdraw()
##Post-condition: Welcome screen buttons placed on welcome screen; main game window hidden
    
welcome()


not_found_window = Toplevel(root, bg = 'red')
def not_found_button_cmd():
    not_found_window.withdraw()
    not_found_window.grab_release()
##Post-condition: Issues warning that inputted search word isn't in the dictionary definitions

##Set-up: of "not found" warning
not_found_label = Label(not_found_window, font = 40, text = "Search word not found in dictionary definitions. Random word selected.", bg = 'white')
not_found_label.pack(fill = BOTH, expand = YES, padx = 2, pady = 2)
not_found_button = Button(not_found_window, font = 40, text = "Ok", relief = RAISED, command = not_found_button_cmd)
not_found_button.pack(padx = 2, pady = 2)
window_position(not_found_window, 750, 100)
not_found_window.withdraw()


def get_game_info(game_info):
    test_word = word_contained_entry.get()
    cur.execute('SELECT word, def FROM eng_dict WHERE def LIKE ?', ('% ' + test_word + ' %',))
    temp_results = cur.fetchall()
##If search word match is not found
    while (temp_results == []):
        cur.execute('SELECT word FROM eng_dict')
        words = cur.fetchall()
        random_word = string.join(random.choice(words))
        cur.execute('SELECT word, def FROM eng_dict WHERE word LIKE ?', (random_word,))
        temp_results = cur.fetchall()
        not_found_window.deiconify()
        not_found_window.grab_set()
    else:
        search_results = temp_results
    game_info_tuple = random.choice(search_results)
    game_info[0] = game_info_tuple[0].lower()[3:]
    game_info[1] = game_info_tuple[1].lower()
    has_letter = ['false']
    game_word = string.join(game_info[0])
##If word doesn't contain letters, a new word is picked
    for i in range(len(game_word)):
        if (game_word[i].isalpha):
            has_letter[0] = 'true'
    if (has_letter[0] == 'false'):
        get_game_info(game_info)
    return game_info
##Word to be guessed and its definition are returned
##Mutable globals set-up
##String positions of correctly guessed letters
correct_letter_indices = []

##List of incorrect letters
incorrect_letter_spaces = []

##List of correct letters
correct_letter_spaces = []

##Correct and incorrect letter spaces in GUI
correct_letters = StringVar()
incorrect_letters = StringVar()

##Incorrect guess counter 
incorrect_letters_count = [0]

##Correct letter space in GUI set-up
word_frame_game_info = Label(word_frame, font = 40, textvariable = correct_letters , bg = 'white')

def initial_correct_letter_space(correct_letters, correct_letter_spaces):
    for i in range(len(game_info[0])):
        correct_letter_spaces += '_'
    string_letter_spaces = string.join(correct_letter_spaces)
    correct_letters.set(string_letter_spaces)
    return correct_letter_spaces
##Post-condition: Empty spaces for each letter in the game word displayed

##Incorrect letter space in GUI set-up
letters_frame_incorrect_tries = Label(letters_frame, font = 40, textvariable = incorrect_letters, bg = 'white')


def initial_incorrect_letter_space(incorrect_letters):
    incorrect_letters.set('Incorrect Tries: ' + str(incorrect_letters_count[0]) + '\n' + string.join(incorrect_letter_spaces))
##Incorrect letter guesses and count displayed

def make_word_contained_button():
    if (len(word_contained_entry.get()) > 0):
        word_contained_button_cmd()
    else:
        search_reminder()
##Post-condition: Function reminding user to input a search word is called; otherwise search word submitted
##Button that submits search word is displayed
word_contained_button = Button(bottom_frame, text = 'Submit search word', font = 40, command = make_word_contained_button)
word_contained_button.pack(side = LEFT, anchor = S, pady = 1)


def word_contained_button_cmd():
    middle_frame.pack(side = TOP, expand = YES)
    top_frame.pack(side = TOP, expand = YES)
    word_frame.pack(side = LEFT, expand = YES)
    hangman_frame.pack(side = LEFT, expand = YES)
    letters_frame.pack(side = RIGHT, expand = YES)
    letters_frame_incorrect_tries.pack()
    get_game_info(game_info)
    initial_correct_letter_space(correct_letters, correct_letter_spaces)
    initial_incorrect_letter_space(incorrect_letters)
    word_contained_entry.delete(0, END)
    word_contained_entry.pack_forget()  
    letter_guess_entry.pack(side = LEFT, anchor = S, padx = 1, pady = 1)
    word_contained_button.pack_forget()
    word_frame_game_info.pack(padx = 4, pady = 4)
    letter_guess_button.pack(side = LEFT, anchor = S, pady = 1)
    entry_label_text.set('Please enter a letter guess:')
##Post-condition: Various GUI elements set-up or displayed; entry box cleared


def search_warning_button_cmd():
    search_warning.withdraw()
    search_warning.grab_release()
##Post-condition: Search word reminder minimized; main window re-enabled

##Search word input reminder set-up
search_warning = Toplevel(bg = 'red')
search_warning.withdraw()
search_warning_message = Label(search_warning, text = 'Please make sure to enter a search word!', font = 40, bg = 'white')
search_warning_button = Button(search_warning, text = 'Try again', font = 32, command = search_warning_button_cmd, relief = RAISED)
search_warning.title('Modified Hangman')
window_position(search_warning, 750, 100)


def search_reminder():
    search_warning.deiconify()
    search_warning.grab_set()
    search_warning_message.pack(padx = 6, pady = 6)
    search_warning_button.pack()
##Post-condition: Search reminder set-up and displayed

##Clue capability set-up
clue_frame = Frame(middle_frame, bg = 'white')
clue_frame.pack(side = LEFT, fill = BOTH, expand = YES)
clue_label_text = StringVar()
clue_label = Label(clue_frame, textvariable = clue_label_text, font = 32, wraplength = 300, justify = LEFT)
def clue_button_cmd():
    clue_label_text.set(game_info[1])
    clue_label.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
    clue_button.pack_forget()
##Post-condition: Clue set
clue_button = Button(clue_frame, text = 'Show clue', font = 32, relief = RAISED, command = clue_button_cmd)

match = ['False']
def match_check(match):
    match[0] = 'False'
    guess = letter_guess_entry.get()
    for i in range(len(game_info[0])):
        if(guess == game_info[0][i]):
            match[0] = 'True'
    return match
##Post-condition: Returns whether or not letter guess is in the game word
    
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
##Post-condition: If guess is correct, added to correct letter list; if guess is incorrect, added to incorrect letter list

def edit_letter_space(correct_letter_spaces, count, indices = None):
    if (indices != None):
        for i in indices:
            correct_letter_spaces[i] = game_info[0][i]
            correct_letters.set(string.join(correct_letter_spaces))
        return correct_letter_spaces
    if (indices == None):
        count += 1
        print count
        incorrect_letters.set('Incorrect Tries: ' + str(count) + '\n' + string.join(correct_letter_spaces))
        return count
##Post-condition: Correct and incorrect letter GUI spaces updated

def edit_hangman_space(incorrect_letters_count):
    if (diff_var.get() == 1):
        if (incorrect_letters_count[0] == 1):
            hangman_canvas.pack()
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image1)
        if (incorrect_letters_count[0] == 2):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image2)
        if (incorrect_letters_count[0] == 3):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image3)
        if (incorrect_letters_count[0] == 4):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image4)
        if (incorrect_letters_count[0] == 5):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image5)
        if (incorrect_letters_count[0] == 6):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image6)
        if (incorrect_letters_count[0] == 7):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image7)
        if (incorrect_letters_count[0] == 8):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image8)
        if (incorrect_letters_count[0] == 9):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image9)
    if (diff_var.get() == 2):
        if (incorrect_letters_count[0] == 1):
            hangman_canvas.pack()
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image1)
        if (incorrect_letters_count[0] == 2):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image3)
        if (incorrect_letters_count[0] == 3):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image5)
        if (incorrect_letters_count[0] == 4):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image7)
        if (incorrect_letters_count[0] == 5):
            hangman_display = hangman_canvas.create_image(100, 125, image = hangman_image9)
##Post-condition: Hangman image GUI space updated            

##Entry box allowing no more than one character to be entered set-up
letter_guess_entry = MaxLengthEntry(bottom_frame, width = 2, maxlength = 1, font = 40)
def letter_guess_button_cmd():
    match_check(match)
    match_action(correct_letter_indices, incorrect_letter_spaces, match)
    if (match[0] == 'True'):
        edit_letter_space(correct_letter_spaces, incorrect_letters_count[0], correct_letter_indices)
    if (match[0] == 'False'):
        incorrect_letters_count[0] = edit_letter_space(incorrect_letter_spaces, incorrect_letters_count[0])
    letter_guess_entry.delete(0, END)
    edit_hangman_space(incorrect_letters_count)
    if ('_' not in correct_letter_spaces):
        game_won()
    if (diff_var.get() == 1):
        if (incorrect_letters_count[0] == 5):
            clue_button.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
        if (incorrect_letters_count[0] == 10):
            game_over()
    if (diff_var.get() == 2):
        if (incorrect_letters_count[0] == 3):
            clue_button.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
        if (incorrect_letters_count[0] == 5):
            game_over()
##Post-condition: Calls appropriate letter space edit function; checks for and indicates game over or game won status
				##Also checks for satisfaction of condition to display clue option

##Button for submission of letter guess
letter_guess_button = Button(bottom_frame, text = 'Submit letter guess', font = 40, command = letter_guess_button_cmd)

def clear_setup():
    correct_letter_spaces[:] = []
    incorrect_letter_spaces[:] = []
    correct_letter_indices[:] = []
    incorrect_letters_count[0] = 0
    clue_label.pack_forget()
    clue_button.pack_forget()    
    incorrect_letters.set(initial_incorrect_letter_space(incorrect_letters))
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
##Post-condition: GUI and globals re-set for new round of game

def try_again_button_cmd():
    game_over_window.withdraw()
    game_over_window.grab_release()
    game_won_window.withdraw()
    game_won_window.grab_release()
    dummy_diff.select()
    pick_easy.configure(state = NORMAL)
    pick_hard.configure(state = NORMAL)
    welcome_screen.deiconify()
    welcome()
    begin_button.config(state = DISABLED)
    hangman_canvas.pack_forget()
    clear_setup()
##Post-condition: Resets and returns to welcome screen

##Game won window set-up
game_won_window = Toplevel(bg = 'green')
game_won_window.title('Modified Hangman')
window_position(game_won_window, 750, 100)
game_won_message = Label(game_won_window, bg = 'white', font = 40, text = 'Congratulations! You won! How about another round?')
game_won_message.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
try_again2 = Button(game_won_window, text = 'Try again?', font = 40, relief = RAISED, command = try_again_button_cmd)
try_again2.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
game_won_window.withdraw()

##Game over window set-up
game_over_window = Toplevel(bg = 'red')
game_over_window.title('Modified Hangman')
window_position(game_over_window, 750, 100)
game_over_message = Label(game_over_window, bg = 'white', font = 40, text = 'GAME OVER!')
game_over_message.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
try_again = Button(game_over_window, text = 'Try again?', font = 40, relief = RAISED, command = try_again_button_cmd)
try_again.pack(expand = YES, fill = BOTH, padx = 6, pady = 6)
game_over_window.withdraw()

def game_over():
    game_over_window.deiconify()
    game_over_window.grab_set()
##Post-condition: Game over window displayed

def game_won():
    game_won_window.deiconify()
    game_won_window.grab_set()
##Post-condition: Game won window displayed
   
mainloop()
