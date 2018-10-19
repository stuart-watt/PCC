# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 13:53:46 2018

@author: 21493806
"""


import image_select
import cv2
import tkinter as TK
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image


def get_file(display, location):
    global filename 
    filename = askopenfilename()
    # Display the file path
    display.insert(0, filename)
    
    # Display the image
    image = Image.open(filename)
    photo = ImageTk.PhotoImage(image)
    w = TK.Label(location, image=photo)
    w.pack(side=TK.TOP, expand=True)
    image.close()
        


root = TK.Tk()

root.title('PCC')

# Create the whole window
f1 = TK.Frame(root, bg='green', relief='ridge', bd=10, height=500, width=1000)
f2 = TK.Frame(f1, bg='white', height=500, width=1000)

# Create the toolbar and image window
toolbar = TK.Frame(f2, bg='gray', height=40, width=1000)
image_window = TK.Frame(f2, bg='', height=460, width=1000)


for frame in (f1, f2, toolbar, image_window):
    frame.pack(side=TK.TOP, expand=True)
    frame.pack_propagate(0)

get_train = TK.Button(toolbar,
                   text='Select training image',
                   font='Helvetica 10 bold',
                   bg='Blue',
                   command=lambda: get_file(display, image_window))

train_model = TK.Button(toolbar,
                   text='Train model',
                   font='Helvetica 10 bold',
                   bg='red')

get_train.pack(side=TK.LEFT, fill=TK.Y)
train_model.pack(side=TK.RIGHT, fill=TK.Y)

display = TK.Entry(root, font='Helvetica 10 bold')
display.pack(side=TK.LEFT, fill=TK.X, expand=True)

entries = {}


root.mainloop()
