# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 13:53:46 2018

@author: 21493806
"""


import image_select
from tkinter import *
from tkinter.filedialog import askopenfilename


def get_file():
    return askopenfilename()

root = Tk()

root.title('PCC')

# Create the whole window
f1 = Frame(root, bg='green', relief='ridge', bd=10, height=550, width=600)
f2 = Frame(f1, bg='white', height=550, width=600)
f1.pack(side=TOP)
f2.pack(side=TOP)

# Create the toolbar and image window
toolbar = Frame(f2, bg='black', width=600, height=10)
image_window = Frame(f2, bg='', width=600, height=540)
toolbar.pack(side=TOP, in_=f2)
image_window.pack(side=TOP)

get_train = Button(toolbar,
                   text='Select training image',
                   font='Helvetica 10 bold',
                   bg='Blue',
                   command=lambda: get_file())
get_train.pack(side=LEFT, fill=X, in_=toolbar)

train_model = Button(toolbar,
                   text='Train model',
                   font='Helvetica 10 bold',
                   bg='red')
train_model.pack(side=RIGHT, fill=X, in_=toolbar)

display = Entry(root, width=30, font='Helvetica 10 bold')
display.pack(side=LEFT)

entries = {}


root.mainloop()
