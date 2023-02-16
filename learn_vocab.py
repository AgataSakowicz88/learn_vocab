from tkinter import *
import random



#####################################

## a simple application for learning vocabulary
## Python 3.6
## developed to support 4 dictionary files: Portuguese, German, Spanish and French (it's easy to change it, though)
## in order to use it, adjust the path variable and the file names, and create the dictionary files needed, in the following format:

## you; tu
## night; a noite

#####################################



## todo: wrap in a class

## todo: enable 2-ways translations
# int(not 1)

## todo: ignore commas etc.

## todo: account for different separators

#n todo: clean the file reading


#####################################

##### global variables

#####################################

path = '../'
filename_port = 'eng_port.txt'
filename_esp = 'es.txt'
filename_de = 'eng_de.txt'
filename_fr = 'eng_fr.txt'


word_dict = {}
score_dict = {}
word_dict_inverse = {}

## number of words retrieved for the questioning
MAX_WORDS = 20

master = Tk()





#####################################

##### utility functions

#####################################



def open_dictionary(path_to_file, max_words = None):
    '''
    reads the dictionary file from disk
    :param path_to_file: string; full path to the dictionary file
    :return:
    wird_dict: dictionary of form {word in the base language: word in the target language}
    score_dict: dictionary of form {word in the base language: score};
        score is fixed to -1 to never ask for the same word if the answer was correct the first time
    word_dict_inverse: dictionary of form {word in the target language: word in the base language}
    '''
    with open(path_to_file, encoding="utf8") as f:
        word_dict = {line.split(';')[0].strip(): line.split(';')[1].replace('\n', '').strip() for
                     line in f
                     if (line != '\n' and not line.startswith('#') )}
        if max_words and max_words < len(word_dict):
            word_dict = dict(random.sample(list(word_dict.items()), max_words))

    score_dict = {key: -1 for key in word_dict.keys()}
    word_dict_inverse = {value: key for key, value in word_dict.items()}

    return word_dict, score_dict, word_dict_inverse




def set_window_position(width = 200, height = 100):
    '''
    sets position for the pop-up window
    :param width: num; width of the window
    :param height: num; height of the window
    '''
    ## get screen width and height
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()

    ## calculate position coordinates
    x = (screen_width/2) - (width/2)
    y = screen_height/2 - height
    master.geometry('%dx%d+%d+%d' % (width, height, x, y))





#####################################

##### window layout

#####################################



##### set language you want to learn; by default Portugeuse

target_language = StringVar()
target_language.set('Spanish')

dict_label = Label(master, text='What language would you like to learn?')
dict_label.pack(side = TOP)

dict_options_dict = {"Portuguese": filename_port, "Spanish": filename_esp, 'German': filename_de, 'French': filename_fr}
dict_option = OptionMenu(master, target_language, *dict_options_dict.keys())
dict_option.pack()


##### set window position

set_window_position(500, 150)


##### display the window in the front (doesn't seem to work with the terminal though)

master.lift()
## todo: check




#####################################

##### application variables

#####################################



## has to appear in the code after the creation of Tk()

##points = IntVar()
##points.set('0')


##### new word to be asked for

new_question = StringVar()
new_question.set('')

##### to enable translation from the target language; 0 means translating to target language

inverse_dict = IntVar()
inverse_dict.set(0)

##### input box

label = Label(master, text='press ENTER to start')
label.pack(side = TOP)

entry = Entry(master, bd = 5, width = 50)
entry.pack()

##### info about if the response was correct (OK / WRONG)

response_label = Label(master, text='')
response_label.pack()

##### correct translation display

response_label2 = Label(master, text='')
response_label2.pack()





#####################################

##### application logic

#####################################



def callback(event):
    '''
    interacts with the user by reading random words from a given dictionary, asking for their translation and providing corrections

    callback function when used with a button, can't take any arguments
    when used with a bind function, it has to take an event argument
    '''
    global word_dict
    global score_dict
    global word_dict_inverse

    ## read the dictionary file if it has not been read yet
    if not word_dict:
        word_dict, score_dict, word_dict_inverse = open_dictionary(path + dict_options_dict[target_language.get()])

    input = entry.get()

    ## delete text from the input box
    entry.delete(0, END)

    query = new_question.get()
    inverse_d = inverse_dict.get()      ## for now fixed to 0 (one way translation only)

    ## get key to be used to store the score and the query correct translation
    if query != '':
        if inverse_d:
            score_key = word_dict_inverse[query]
            translation = word_dict_inverse[query]
        else:
            score_key = query
            translation = word_dict[query]

        ## if: the response was correct (case insensitive)
        if (not inverse_d and input.lower() == word_dict[query].lower()) \
                or (inverse_d and input.lower() == word_dict_inverse[query].lower()):
            response_label.config(text='OK!!')
            response_label2.config(text=translation, fg='green')
            ## add 1 to the score for this word
            score_dict[score_key] = score_dict.get(score_key) + 1
        else:
            response_label.config(text='WRONG!!')
            response_label2.config(text=translation, fg='red')
            ## substract 1 from the score for this word
            score_dict[score_key] = score_dict.get(score_key) - 1

    ##todo: if this option was chosen, pick randomly the direction of the query
    #inverse_dict.set(random.choice([0,1]))

    ## draw only from keys that have negative score
    keys_to_draw = [key for key, score in score_dict.items() if score < 0]

    ## generate a new query
    if len(keys_to_draw) > 0:
        new_word = random.choice(keys_to_draw)
        if inverse_dict.get():
            new_question.set(word_dict[new_word])
        else:
            new_question.set(new_word)
    else:
        new_question.set('')
    label.config(text=new_question.get())



##### associate pressing enter with the callback function

master.bind('<Return>', callback)


##### start

master.mainloop()




