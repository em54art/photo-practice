#avoid using * if you know what to specifically use
from tkinter import *
import tkinter as tk
# import image
from PIL import ImageTk, Image
import os.path

#drag and drop var
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
color_data = open("colorsave.txt","w")
color_file = "colorsave.txt"



def title_bar_function():
    
    global title_bar,title_label, default_color
    
    #color for the bar
    default_color = '#9BE3F6'

    #reading color data from the file
    with open("colorsave.txt","r") as color_data_r:
        # read the color data from the file
        color_data_RC = color_data_r.readline().strip()
        default_color = color_data_RC

    #drag and drop
    def move_app(e):
        global x_offset, y_offset
        x_offset = e.x
        y_offset = e.y
        root.geometry(f'+{e.x_root-x_offset}+{e.y_root-y_offset}')

    def drag_app(e):
        root.geometry(f'+{e.x_root-x_offset}+{e.y_root-y_offset}')

    #---------title bar---------

    #title bar
    title_bar = Frame(root, bg= default_color,relief ='raised',bd = 0)
    title_bar.grid(row = 0, column = 0,columnspan=4, sticky='ew' )

    #bind title bar drag
    title_bar.bind('<ButtonPress-1>', move_app)
    title_bar.bind('<B1-Motion>', drag_app)

    #title bar color
    title_label = Label(title_bar, text='IMAGE', bg = default_color,fg = 'white')
    title_label.grid(row = 0, column = 0)

#------color click to reveal bar-------------------------------------------------
color_picker_enabled = False
# initialize the bar slider and b_cc button
bar_slider = None
b_cc = None

def colorp_click():
    global color_picker_enabled, bar_slider, b_cc

    if color_picker_enabled == True:
        
        # update the state of the variable
        color_picker_enabled = False
        
        # destroy the bar slider
        bar_slider.destroy()
        
        # destroy the save button
        b_cc.destroy()
        
    else:
        
        # update the state of the variable
        color_picker_enabled = True
        
        # update bg colour of b_cc
        def my_upd(v):
            global color_C
            red = bar_slider.get()
            green = 200 - int(int(v) * 0.7)
            blue = 227 - int(int(v) * 0.3)
        
            #changes color with bar slider
            color_C = '#{0:02x}{1:02x}{2:02x}'.format(red,green, blue)
            #changes the var items to the color_C
            b_cc.config(bg=color_C, text = color_C)
            bar_slider.config(fg = color_C)
        
            #title bar
            title_bar.config (bg = color_C)
            title_label.config (bg = color_C)
        

        # bar slider
        bar_slider = Scale(root, from_=255, to=0, orient=HORIZONTAL,
                        bg='white',
                       highlightbackground='white',
                       highlightthickness=1,
                       fg='#9BE3F6',
                       font='Arial 13',
                       troughcolor='white',
                        length = 150,
                        width =11,
                        sliderlength= 30,
                       command=my_upd)

        bar_slider.grid(row=1, column=2, padx=40, pady=2, sticky='ne')
    
        # sets the bar slider to num
        bar_slider.set(255)
    
        # save color
        def button_color_save():
            bg_color = b_cc.cget('bg')
        
            #overwrites existing text
            with open("colorsave.txt", "w") as color_data:
                # save color
                color_data.write(bg_color)
        
        

        # button
        b_cc = Button(root, text='Color', bg='#9BE3F6', font='10', width=8, borderwidth=0, fg = 'white', command = button_color_save)
        b_cc.grid(row=1, column=2, padx=200, pady=3, sticky='se')
    
        # update initial background color of button
        my_upd(0)

#-------image-------
def image_function():
    
    #button click to exit
    def button_click():
            exit()
    #use global to allow access
    global my_img, img_button, arrow_imgR, arrow_imgL, color_imgP, photo_img, photo_img1, photo_img2, photo_img3
    
    #image 
    my_img = ImageTk.PhotoImage(Image.open(r"python_pic\tooru.jpg"))
    my_label = Label(image = my_img, borderwidth =0, highlightbackground="white")
    my_label.grid(row = 2, column = 2, sticky='ew')
        
    #close button
    img_button = Image.open(r"python_pic\button0.png")

    #close resize
    new_size = (100, 30)
    img = img_button.resize(new_size)

    #arrow image
    arrow_imgR =Image.open(r"python_pic\arrow0.png")
    arrow_imgL =Image.open(r"python_pic\arrow1.png")

    #icon color picker
    color_imgP =Image.open(r"python_pic\iconpaint.png")

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
        
    #---------------------------------buttons------------------------------------------
        
    #exit button look with the command of button_click
    button_quit = Button(root, image= photo_img, command=button_click, width=100, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_quit.grid(row = 3, column = 2, padx = 1, pady =5)

    #arrow button
    button_AR = Button(root, image= photo_img1, command=button_click, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_AR.grid(row = 3, column = 2, padx = 50, pady =5,sticky='e')

    button_AL = Button(root, image= photo_img2, command=button_click, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_AL.grid(row = 3, column = 2, padx = 50, pady =5, sticky='w')

    #color button
    button_CP = Button(root, image= photo_img3, command=colorp_click, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_CP.grid(row = 1, column = 2,pady = 5, padx = 5, sticky='ne')

# functions
title_bar_function()
image_function()
root.mainloop()