#avoid using * if you know what to specifically use
from tkinter import *
import tkinter as tk
# import image
from PIL import ImageTk, Image

#colour bar
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

x_offset = 0
y_offset = 0
#-------------------root--------------------------------------------------
root = Tk()
#name
root.title('pictures')

#icon 
root.iconbitmap(r'D:\emily\Documents\customize\folder icons\logo.ico')

#remove title
root.overrideredirect(True)

#colour
root.configure(bg='white')

#-----------------------main--------------------------------------------
#function move_app, check binding for more info
def move_app(e):
    global x_offset, y_offset
    x_offset = e.x
    y_offset = e.y
    root.geometry(f'+{e.x_root-x_offset}+{e.y_root-y_offset}')

def drag_app(e):
    root.geometry(f'+{e.x_root-x_offset}+{e.y_root-y_offset}')


#title bar
title_bar = Frame(root, bg='#9BE3F6',relief ='raised',bd = 0)
title_bar.grid(row = 0, column = 0,columnspan=4, sticky='ew' )

#bind title bar drag
title_bar.bind('<ButtonPress-1>', move_app)
title_bar.bind('<B1-Motion>', drag_app)

title_label = Label(title_bar, text='IMAGE', bg ='#9BE3F6',fg = 'white')
#title_label.pack(side = LEFT, pady =4)
title_label.grid(row = 0, column = 0)



#image 
my_img = ImageTk.PhotoImage(Image.open(r"D:\emily\Pictures\Saved Pictures\tooru.jpg"))
my_label = Label(image = my_img, borderwidth =5, highlightbackground="white")
my_label.grid(row = 2, column = 2, sticky='ew')

#close button
img_button = Image.open(r"D:\emily\Pictures\Saved Pictures\button0.png")

#close resize
new_size = (100, 30)
img = img_button.resize(new_size)

#arrow image
arrow_imgR =Image.open(r"D:\emily\Pictures\Saved Pictures\arrow0.png")
arrow_imgL =Image.open(r"D:\emily\Pictures\Saved Pictures\arrow1.png")

#icon color picker
color_imgP =Image.open(r"D:\emily\Pictures\Saved Pictures\iconpaint.png")

#resize arrow and color picker
sqe_size = (30, 30)
img_AR = arrow_imgR.resize(sqe_size)
img_AL = arrow_imgL.resize(sqe_size)
img_CP = color_imgP.resize(sqe_size)

#convert resize image to tkinter object
photo_img = ImageTk.PhotoImage(img)

photo_img1 = ImageTk.PhotoImage(img_AR)
photo_img2 = ImageTk.PhotoImage(img_AL)

photo_img3 = ImageTk.PhotoImage(img_CP)

#color click to reveal bar-------------------------------------------------

def colorp_click():
    
    #use tkinter slider for function and look
    # create a new frame to hold the colorbar
    colorbar_frame = tk.Frame(root)
    colorbar_frame.grid(row=1, column=2, padx=40, pady=4, sticky='ne')
    


    #create a figure and axes for the color bar (size)
    fig, ax = plt.subplots(figsize=(3, 0.3))

    cmap = mpl.cm.cool

    cbar= fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap),
                cax=ax, orientation='horizontal', label='Some Units')
    
    #removes outline
    cbar.outline.set_edgecolor('None')
    
    ax.tick_params(axis='both', which='both', length=0, labelbottom=False, labeltop=False,
                   labelleft=False, labelright=False)
    # create a new canvas to display the colorbar
    canvas = FigureCanvasTkAgg(fig, master=colorbar_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    
#button click to exit
def button_click():
    exit()
    
#---------------------------------buttons------------------------------------------
#exit button look with the command of button_click
button_quit = Button(root, image=photo_img, command=button_click, width=100, height=30, borderwidth=0, highlightthickness=0, bg="white")
button_quit.grid(row = 3, column = 2, padx = 1, pady =5)

#arrow button
button_AR = Button(root, image=photo_img1, command=button_click, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
button_AR.grid(row = 3, column = 2, padx = 50, pady =5,sticky='e')

button_AL = Button(root, image=photo_img2, command=button_click, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
button_AL.grid(row = 3, column = 2, padx = 50, pady =5, sticky='w')

#color button
button_CP = Button(root, image=photo_img3, command=colorp_click, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
button_CP.grid(row = 1, column = 2,pady = 5, padx = 5, sticky='ne')

root.mainloop()
