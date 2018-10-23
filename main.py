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


def get_file():
    global filename, display, w
    
    filename = askopenfilename()
    # Display the file path
    display.delete(0, TK.END)
    display.insert(0, filename)
    # Load an color image
    img = cv2.imread(filename)
    # Resize the image to fit the window (width, height)
    img = cv2.resize(img, (500, 500))
    #Rearrang the color channel from BGR to RGB
    b,g,r = cv2.split(img)
    img = cv2.merge((r,g,b))
    
    # Convert to ImageTK object
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im) 
    
    # This next line creates a new tkinter reference to the image
    # Otherwise, the garbage collector will delete the reference and image no show
    w.config(image = imgtk)
    w.image = imgtk

def train():
    global model
    model = image_select.train_plants(filename)
    
def subtract(model):
    global w
    new_image = image_select.remove_back(filename, model)
    new_image = cv2.resize(new_image, (500, 500))
    #Rearrang the color channel from BGR to RGB
    b,g,r = cv2.split(new_image)
    img = cv2.merge((r,g,b))
    
    # Convert to ImageTK object
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im) 
    w.config(image = imgtk)
    w.image = imgtk
    
    
root = TK.Tk()

filename = None

root.title('PCC')

# Create the whole window
f1 = TK.Frame(root, bg='green', relief='ridge', bd=10, height=540, width=500)
f2 = TK.Frame(f1, bg='white', height=540, width=500)

# Create the toolbar and image window
toolbar = TK.Frame(f2, bg='gray', height=40, width=1000)
image_window = TK.Frame(f2, bg='', height=500, width=500)


for frame in (f1, f2, toolbar, image_window):
    frame.pack(side=TK.TOP, expand=True)
    frame.pack_propagate(0)

w = TK.Label(image_window, image='')
w.pack(side=TK.TOP)

get_image = TK.Button(toolbar,
                   text='Select training image',
                   font='Helvetica 10 bold',
                   bg='blue',
                   command=lambda: get_file())

select_segments = TK.Button(toolbar,
                   text='Train Model',
                   font='Helvetica 10 bold',
                   bg='green',
                   command=lambda: train())

train_model = TK.Button(toolbar,
                   text='Subtract background',
                   font='Helvetica 10 bold',
                   bg='red',
                   command=lambda: subtract(model))

get_image.pack(side=TK.LEFT, fill=TK.Y)
select_segments.pack(side=TK.LEFT, fill=TK.Y)
train_model.pack(side=TK.RIGHT, fill=TK.Y)

display = TK.Entry(root, font='Helvetica 10 bold')
display.pack(side=TK.LEFT, fill=TK.X, expand=True)

entries = {}


root.mainloop()
