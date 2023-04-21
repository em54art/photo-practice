#avoid using * if you know what to specifically use
from tkinter import *
import customtkinter
# import image
from PIL import ImageTk, Image
import os
import re

#drag and drop var
x_offset = 0
y_offset = 0

#-------------------root--------------------------------------------------
root = customtkinter.CTk()

#remove title
root.overrideredirect(True)

#colour
root.configure(fg_color='white')

#-----------------------file information--------------------------------------------  
color_file = "colorsave.txt"
#color for the bar
default_color = '#9BE3F6'

# If the file exists and has data in it, read the color from the file
if os.path.isfile(color_file) and os.path.getsize(color_file) > 0:
    with open(color_file, "r") as f:
        color = f.readline().strip()
        
        # Check if the color read from the file is valid
        if not color or not re.match(r'^#[0-9a-fA-F]{6}$', color):
            # Default color if the file is empty or doesn't contain a valid color code
            color = default_color

# file doesn't exist, create the file with the default color
else:
    # Default color if the file doesn't exist
    color = default_color
    if not os.path.exists(color_file):
        with open(color_file, "w") as f:
            f.write(color)


#reading color data from the file
with open("colorsave.txt","r") as color_data_r:
    # read the color data from the file
    color_data_RC = color_data_r.readline().strip()
    default_color = color_data_RC
    

#---------title bar---------

#drag and drop
def move_app(e):
    global x_offset, y_offset
    x_offset = e.x
    y_offset = e.y
    root.geometry(f'+{e.x_root-x_offset}+{e.y_root-y_offset}')

def drag_app(e):
    root.geometry(f'+{e.x_root-x_offset}+{e.y_root-y_offset}')

#title bar
title_bar = Frame(root, bg= default_color,relief ='raised',bd = 0)
title_bar.grid(row = 0, column = 0,columnspan=4, sticky='ew' )

#bind title bar drag
title_bar.bind('<ButtonPress-1>', move_app)
title_bar.bind('<B1-Motion>', drag_app)

#title bar color
title_label = Label(title_bar, text='IMAGE', bg = default_color,fg = 'white',height = 2, font = 'Ariel 12', padx = 5)
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
            
            # Convert values to integers
            red_int = int(red)
            green_int = int(green)
            blue_int = int(blue)
        
            #changes color with bar slider
            color_C = '#{0:02x}{1:02x}{2:02x}'.format(red_int,green_int, blue_int)
            
            #changes the var items to the color_C
            b_cc.configure(fg_color =color_C, text = color_C)

            #changes title bar color
            title_bar.configure (bg = color_C)
            title_label.configure (bg = color_C)
    
        # bar slider
        bar_slider = customtkinter.CTkSlider(master=root, from_=255, to=0,
                                             orientation = HORIZONTAL,
                                             width= 110,
                                             height = 20,
                                             fg_color = '#f8bff3',
                                             progress_color = '#9BE3F6',
                                             button_color = '#5353c6',
                                             command=my_upd)
        

        bar_slider.grid(row=1, column=2, padx=40, pady=2, sticky='e')
    
        # sets the bar slider to num
        bar_slider.set(0)
    
        # save color
        def button_color_save():
            bg_color = b_cc.cget('fg_color')
        
            #overwrites existing text
            with open("colorsave.txt", "w") as color_data:
                # save color
                color_data.write(bg_color)
        
        # button
        b_cc = customtkinter.CTkButton(root, text='Color',fg_color ='white',height = 25,width = 70, command = button_color_save)
        b_cc.grid(row=1, column=2, padx=155, pady=3, sticky='e')
    
        # update initial background color of button
        my_upd(0)

#-------image-------
def image_function():
    
    #button click to exit
    def button_click():
            exit()
            
    #use global to allow access
    global my_img0, img_button, arrow_imgR, arrow_imgL, color_imgP, photo_img, photo_img1, photo_img2, photo_img3
    global my_label,current_index, photo_img4
    
    
    #image for slider
    my_img0 = ImageTk.PhotoImage(Image.open(r"python_pic\tooru.jpg").resize((500, 500)))
    my_img1 = ImageTk.PhotoImage(Image.open(r"python_pic\바요.Tobio.png").resize((500, 500)))
    
    #img S show
    my_label = Label(image = my_img0, borderwidth =0, highlightbackground="white")
    my_label.grid(row = 2, column = 2, sticky='ew')
        
    #img list
    image_list = [my_img0, my_img1]
    
    # Initialize current index to 0
    current_index = 0
    
    #next arrowR code
    def forward():
    
        global current_index, button_AR, button_AL, my_label
        
        # Increment current index
        current_index += 1
        
        # Wrap around to beginning if at end of list
        if current_index >= len(image_list):
            current_index = 0
        
        # Update label with new image
        my_label.grid_forget()
        my_label = Label(image=image_list[current_index], borderwidth=0, highlightbackground="white")
        my_label.grid(row=2, column=2, sticky='ew')
        
    #back arrowL code
    def back():
        global current_index, button_AR, button_AL, my_label
        
        # Increment current index
        current_index -= 1
        
        # Wrap around to beginning if at end of list
        if current_index >= len(image_list):
            current_index = 0
        
        # Update label with new image
        my_label.grid_forget()
        my_label = Label(image=image_list[current_index], borderwidth=0, highlightbackground="white")
        my_label.grid(row=2, column=2, sticky='ew')
        

    #arrow image
    arrow_imgR =Image.open(r"python_pic\arrow0.png")
    arrow_imgL =Image.open(r"python_pic\arrow1.png")

    #icon color picker
    color_imgP =Image.open(r"python_pic\iconpaint.png")
    
    #icon dragdrop
    dragdrop_img = Image.open(r"python_pic\dragdropB.png")

    #resize arrow and color picker
    sqe_size = (30, 30)
    img_AR = arrow_imgR.resize(sqe_size)
    img_AL = arrow_imgL.resize(sqe_size)
    img_CP = color_imgP.resize(sqe_size)
    img_DD = dragdrop_img.resize(sqe_size)

    #convert resize image to tkinter object
    photo_img1 = ImageTk.PhotoImage(img_AR)
    photo_img2 = ImageTk.PhotoImage(img_AL)

    photo_img3 = ImageTk.PhotoImage(img_CP)
    photo_img4 = ImageTk.PhotoImage(img_DD)
        
    #---------------------------------buttons------------------------------------------
        
    #exit button look with the command of button_click
    button_quit = customtkinter.CTkButton(master=root, text = 'EXIT',width=140, height=30,
                                          border_color = '#9BE3F6', border_width = 2,
                                          fg_color = 'white',
                                          text_color = '#9BE3F6',
                                          hover = False,
                                          command=button_click)
    button_quit.grid(row = 3, column = 2, padx = 1, pady =5)

    #arrow button
    button_AR = Button(root, image= photo_img1, command=forward, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_AR.grid(row = 3, column = 2, padx = 50, pady =5,sticky='e')

    button_AL = Button(root, image= photo_img2, command=back, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_AL.grid(row = 3, column = 2, padx = 50, pady =5, sticky='w')

    #color button
    button_CP = Button(root, image= photo_img3, command=colorp_click, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_CP.grid(row = 1, column = 2,pady = 5, padx = 5, sticky='ne')
    
    #dragdrop button
    button_CP = Button(root, image= photo_img4, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_CP.grid(row = 1, column = 2,pady = 5, padx = 5, sticky='nw')

# functions
image_function()
root.mainloop()
