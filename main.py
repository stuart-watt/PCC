# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 13:53:46 2018

@author: 21493806
"""


import image_select
import cv2
import tkinter as TK
import tkinter.messagebox as tkmb
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

model, filename = None, None
imgtk = None

def get_file():
    global filename, display, w, imgtk
    imgtk = None
    filename = askopenfilename()
    
    # Display the file path
    display.delete(0, TK.END)
    display.insert(0, filename)
    # Load an color image
    img = cv2.imread(filename)
    # Resize the image to fit the window height
    scale_f = max(img.shape)/550
    img = cv2.resize(img, (0,0), fx=1/scale_f, fy=1/scale_f)
    
    #Rearrang the color channel from BGR to RGB
    b,g,r = cv2.split(img)
    img = cv2.merge((r,g,b))
    
    # Convert to ImageTK object
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im) 
    
    w.config(image = imgtk)

def train():
    global model
    if filename is not None:
        tkmb.showinfo('Selecting training segments', 
                      '''How to collect training data:\n
                      1. Click/drag to create box around plant segments.
                      2. Draw as many as required.
                      3. Press 'c' to save segments and continue.
                      4. Press 'r' to clear the selections and refresh.
                      5. Repeat for the background segments.''')
        model = image_select.train_plants(filename)
    else:
        tkmb.showerror('Error', 'No image selected')
    
def subtract(model):
    global w, imgtk
    imgtk = None
    
    if model is not None:
        
        new_image = image_select.remove_back(filename, model)
        scale_f = max(new_image.shape)/550
        new_image = cv2.resize(new_image, (0,0), fx=1/scale_f, fy=1/scale_f)
        #Rearrang the color channel from BGR to RGB
        b,g,r = cv2.split(new_image)
        img = cv2.merge((r,g,b))
        
        # Convert to ImageTK object
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im) 
        w.config(image = imgtk)
    
    else:
        tkmb.showerror('Model Error', 
                       'No model trained.\n Select an image and train the model first')
    
    
    
root = TK.Tk()

filename = None

root.title('PCC')

# Create the whole window
f1 = TK.Frame(root, bg='green', relief='ridge', bd=10, height=590, width=550)
f2 = TK.Frame(f1, bg='white', height=590, width=550)

# Create the toolbar and image window
toolbar = TK.Frame(f2, bg='gray', height=40, width=550)
image_window = TK.Frame(f2, bg='white', height=550, width=550)


for frame in (f1, f2):
    frame.pack(side=TK.TOP)
    frame.pack_propagate(0)
    
toolbar.place(height=40, width=550)
image_window.place(y=40, height=550, width=550)
image_window.pack_propagate(0)

w = TK.Label(image_window, bg='white')
w.place(height=550, width=550)

# Define the buttons
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
train_model.pack(side=TK.LEFT, fill=TK.Y)

display = TK.Entry(root, font='Helvetica 10 bold')
display.pack(side=TK.LEFT, fill=TK.X, expand=True)
display.insert(0, 'No file selected')


root.mainloop()
