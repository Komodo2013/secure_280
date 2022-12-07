import random
import tkinter
import tkinter as tk
from time import sleep
from random import randint
from PIL import ImageTk, Image
from dictionary import Dictionary

random_banter = (
    ["I already know what it is ;)", "There's no way you'll win", "", "This is too easy!"],
    ["I'm pretty sure you changed your answer...", "", "I think you made this up..."]
)

button_pos = {'no': ((360, 340), (465, 415)),
              'mabey': ((165, 340), (335, 415)),
              'yes': ((40, 340), (145, 415))}


# first question is living/place/thing
# Then use a set of specific questions for each category


def think():
    banter.set('Hmmmmm.....')
    label3.update()
    sleep(2)


def bant(above20):
    if above20:
        r = randint(0, len(random_banter[1]) - 1)
        banter.set(random_banter[1][r])
    else:
        r = randint(0, len(random_banter[0]) - 1)
        banter.set(random_banter[0][r])



def update(button, index, q):
    think()

    if index < len(dictionary.questions()):
        q = dictionary.questions()[index]

    index += 1
    if index < len(dictionary.questions()):
        if button == 'yes':
            dictionary.similarity_handler.adjs.append(q.yes_tag)
        elif button == 'no':
            dictionary.similarity_handler.adjs.append(q.no_tag)
        elif button == 'mabey':
            dictionary.similarity_handler.adjs.append(q.mabey_tag)

        q = dictionary.questions()[index]
        question.set(q.prompt)
        label2.update()
        bant(False)
    elif index == len(dictionary.questions()):
        best = dictionary.get_best_match(dictionary.similarity_handler.adjs)
        print(best)
        question.set(str.format("Is it a {name}?", name=best.name))
        label2.update()
    else:
        if button == 'yes':
            banter.set("Haha! I knew it all along!")
        elif button == 'no':
            banter.set("You got lucky...")


def mouse_event(event):
    position = {'x': event.x, 'y': event.y}
    button = ''

    if is_within(position, button_pos['no']):
        button = 'no'
    elif is_within(position, button_pos['mabey']):
        button = 'mabey'
    elif is_within(position, button_pos['yes']):
        button = 'yes'

    dictionary.question_index += 1
    update(button, dictionary.question_index, current_question)


def is_within(pos, box):
    if box[0][0] <= pos['x'] <= box[1][0] and box[0][1] <= pos['y'] <= box[1][1]:
        return True
    else:
        return False


print("Which of these best describes 'it'? Alive, Place, Thing")
category = input().strip().lower()

root = tk.Tk()
root.title('Phyton')

back = tk.Frame(master=root, width = 500, height = 700)
back.pack()

root.resizable(0, 0)

background_image = Image.open('PhytonGame.gif')
background_image = background_image.resize((500, 700), Image.ANTIALIAS)
background = ImageTk.PhotoImage(background_image)

label1 = tkinter.Label(image = background)
label1.place(x = 0, y = 0, width = 500, height = 700)

question = tkinter.StringVar()
question.set('Here is one question, which is super long and will wrap...')

banter = tkinter.StringVar()
banter.set('Here is some banter that I will say and hopefully this works')

label2 = tkinter.Label(textvariable = question, bg = '#fec2c2', wraplength = 400, font = ('Arial', 25), fg = '#5c5c5c')
label2.place(x = 50, y = 125)

label3 = tkinter.Label(textvariable = banter, bg = '#ffffff', wraplength = 275, font = ('Arial', 10), fg = '#5c5c5c')
label3.place(x = 210, y = 500)

root.bind("<Button-1>", mouse_event)

dictionary = Dictionary('dict.txt', category)  # TODO

current_question = dictionary.questions()[0]
question.set(current_question.prompt)

root.mainloop()



