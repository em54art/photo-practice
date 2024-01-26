#avoid using * if you know what to specifically use
from tkinter import *
import customtkinter
# import image
from PIL import ImageTk, Image, ImageOps
from pathlib import Path
import os
import re
from tkinter import filedialog

sqe_size = (30, 30)
batch_size = 3
current_index = 0
current_findex = 0
change_array = 0
current_array = 0
#image for slider, full array           
img_paths =[]
#array with imported from batch array
img_batchlist = []
file_format = ['.png','.jpg']
appended_list = []
check_array = []        
final_array = []



#-------------------root--------------------------------------------------
root = customtkinter.CTk()

#resize
root.resizable(0, 0)

#remove title
root.overrideredirect(False)

#colour
root.configure(fg_color='white')

#drag and drop var
# x_offset = 0
# y_offset = 0

# #drag and drop
# def move_app(e):
#     global x_offset, y_offset
#     x_offset = e.x
#     y_offset = e.y
#     root.geometry(f'+{e.x_root-x_offset}+{e.y_root-y_offset}')
# 
# def drag_app(e):
#     root.geometry(f'+{e.x_root-x_offset}+{e.y_root-y_offset}')



# -------variables--------

# Initialize a list to store the resized images
resized_images = []

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
            color = default_color

# If the file doesn't exist or is empty, create the file with the default color
else:
    color = default_color
    if not os.path.exists(color_file):
        with open(color_file, "w") as f:
            f.write(color)


#reading color data from the file
with open("colorsave.txt","r") as color_data_r:
    color_data_RC = color_data_r.readline().strip()
    default_color = color_data_RC
    

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
            
            title_bar1.configure (bg = color_C)
            title_label1.configure (bg = color_C)
    
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


#---------title bar---------

#title bar
title_bar = Frame(root, bg= default_color,relief ='raised',bd = 0)
title_bar.grid(row = 0, column = 0,columnspan=4, sticky='ew' )

#title bar color
title_label = Label(title_bar, bg = default_color,fg = 'white',height = 2, padx = 5)
title_label.grid(row = 0, column = 0)

#bottom bar
title_bar1 = Frame(root, bg= default_color,relief ='raised',bd = 0)
title_bar1.grid(row = 4, column = 0,columnspan=4, sticky='ew' )

#bottom bar color
title_label1 = Label(title_bar1, bg = default_color,fg = 'white',height = 2, padx = 5)
title_label1.grid(row = 4, column = 0, sticky='s')

#bind title bar drag
# title_bar.bind('<ButtonPress-1>', move_app)
# title_bar.bind('<B1-Motion>', drag_app)

#------------

#back arrowL code
def back(full_batchlist):
    global current_index,current_array,current_findex,final_array
    print('back')
    # reduce current index
    current_index -= 1
    current_findex -= 1
    
    
    # Wrap around to the last 
    if current_array == 0 and current_index == -1:
        current_array = len(full_batchlist) - 1
        current_index = len(full_batchlist[-1]) -1
        
    if current_index < 0:
        current_array -= 1
        current_index = len(full_batchlist[current_array]) - 1
    
    if current_findex == 0:
        destroylb()
    
    delete_arrowR()
    img_load2(full_batchlist,check_array,appended_list)
    image_show()
    
    
#next arrowR code
def forward(full_batchlist):
    global current_index, current_array, current_findex,final_array
    print('next')
    # Increment current index
    current_index += 1
    current_findex += 1
    
    if current_index >= len(full_batchlist[current_array]):
        current_array += 1
        current_index = 0
        

    if current_array == len(full_batchlist):
        current_array = 0
        current_index = 0
    
    if current_findex == 1:
        destroylb()
    
    arrow_buttonR()
    img_load2(full_batchlist,check_array,appended_list)
    image_show()
    


#seperate R and L insert the function
def arrow_buttonR():
    global arrow_imgR, arrow_imgL, button_AR, button_AL, my_label,photo_img1,photo_img2, resized_images
    arrow_imgR =Image.open(r"python_pic\arrow0.png")
    img_AR = arrow_imgR.resize(sqe_size)
    photo_img1 = ImageTk.PhotoImage(img_AR)
    
    #arrow button
    button_AR = Button(root, image= photo_img1, command= lambda:forward(img_batchlist), width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_AR.grid(row = 3, column = 2, padx = 50, pady =5,sticky='e')
    
    delete_arrowR()

#-----------------arrow-------------------------
def arrow_button():
    global arrow_imgR, arrow_imgL, button_AR, button_AL, my_label,photo_img1,photo_img2, resized_images
        #arrow image
    arrow_imgL =Image.open(r"python_pic\arrow1.png")
    
    img_AL = arrow_imgL.resize(sqe_size)
    
    #convert resize image to tkinter object
    photo_img2 = ImageTk.PhotoImage(img_AL)
    
    # Update label with new image
    my_label.grid_forget()
    my_label = Label(image = final_array[current_findex], borderwidth=0, highlightbackground="white")
    my_label.grid(row=2, column=2, sticky='ew')
    
    

    button_AL = Button(root, image= photo_img2, command=lambda: back(img_batchlist), width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_AL.grid(row = 3, column = 2, padx = 50, pady =5, sticky='w')
    

    destroylb()
    
    
#-------image-------
def image_function():
    #use global to allow access
    global color_imgP,photo_img3
    
    #button click to exit
    def button_click():
            exit()
    
    #icon color picker
    color_imgP =Image.open(r"python_pic\iconpaint.png")
    
    #resize arrow and color picker
    sqe_size = (30, 30)
    img_CP = color_imgP.resize(sqe_size)
    

    #convert resize image to tkinter object
    photo_img3 = ImageTk.PhotoImage(img_CP)
    
        
    #---------------------------------buttons------------------------------------------
        
    #exit button look with the command of button_click
    button_quit = customtkinter.CTkButton(master=root, text = 'EXIT',width=140, height=30,
                                          border_color = '#9BE3F6', border_width = 2,
                                          fg_color = 'white',
                                          text_color = '#9BE3F6',
                                          hover = False,
                                          command=button_click)
    button_quit.grid(row = 3, column = 2, padx = 1, pady =5)

    #color button
    button_CP = Button(root, image= photo_img3, command=colorp_click, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
    button_CP.grid(row = 1, column = 2,pady = 5, padx = 5, sticky='ne')
    return final_array


DragAndDrop_enabled= None
my_label0 = None

def destroy_browsing():
    global DragAndDrop_enabled, my_label0
    my_label0.destroy()
    button.destroy()
    label_file_explorer.destroy()
    frame1.destroy()

def DragAndDrop_Img():
    global DragAndDrop_enabled
    
    if DragAndDrop_enabled:

        # update the state of the variable
        DragAndDrop_enabled = False
        destroy_browsing()

    else:

        DragAndDrop_enabled = True
        example()

        
#icon dragdrop
dragdrop_img = Image.open(r"python_pic\dragdropB.png")
sqe_size = (30, 30)
img_DD = dragdrop_img.resize(sqe_size)
photo_img4 = ImageTk.PhotoImage(img_DD)

#dragdrop button
button_CP = Button(root, image= photo_img4,command = DragAndDrop_Img, width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
button_CP.grid(row = 1, column = 2,pady = 5, padx = 5, sticky='nw')

#size for photos
target_size = (500,500)


#browse folder img
def example():
    global label_file_explorer,my_label0,button,label_file_explorer,frame1

    #image
    my_img0 =Image.open(r"python_pic\background.png")
    img5 = my_img0.resize(target_size)
    photo_img5 = ImageTk.PhotoImage(img5)
    
    #adds temp img
    my_label0 = Label(image= photo_img5, borderwidth=0, highlightbackground="white")
    my_label0.grid(row=2, column=2, sticky='ew')
    
    # Add reference to prevent garbage collection
    my_label0.image = photo_img5
    
    # Create Frame
    frame1 = Frame(root, background='white')
    frame1.grid(row=2, column=2 )
         
    #button
    button = customtkinter.CTkButton(frame1, text="Browse files",width=140, height=30,
                                    border_color = '#9BE3F6', border_width = 2,fg_color = 'white',
                                     text_color = '#9BE3F6',hover = False,command = browseFiles)
    button.grid(row=1, column=1)
    
    # Create a File Explorer label
    label_file_explorer = Label(frame1,
                                text = "File Explorer using Tkinter",
                                width = 65, height = 4,
                                fg ="#9BE3F6", bg = 'white')
    label_file_explorer.grid(row=2, column=1)


#--------------file pathing-----------------


#create file name
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname,'default_pics')

#add name after default pic dir and insert into img array

#name of txt
direc = "direct.txt"

#info in txt, if new
direc_default = f"{filename}"

#read from notepad and insert into img path
def checkFolderDir():
    #only checks for notepad existance
    if os.path.isfile(direc) and os.path.getsize(direc) > 0:
        with open(direc, "r") as d:
            directpath = d.readline().strip()
            if not directpath:
                directpath = direc_default
    else:
        directpath = direc_default
        with open (direc,"w") as w:
            w.write(directpath)
    

#function
checkFolderDir()
#when going the back array the current array isn't equal to appendedlist
def image_insert(array,flat):
    global current_array, current_findex
    
    #try appendedlist[current array]
    for path in flat[current_array]:
        img = Image.open(path)

        # Calculate aspect ratio
        width_ratio = target_size[0]/img.width
        height_ratio = target_size[1]/img.height
        min_ratio = min(width_ratio, height_ratio)
        
        # Compute new dimensions
        new_width = int(img.width * min_ratio)
        new_height = int(img.height * min_ratio)

        # Resize image
        img = img.resize((new_width, new_height))
        
        #insert into array
        array.append(ImageTk.PhotoImage(img))
        print('insert')
    
    
    

#shitty batch array
def batch_process(array, batch_size):
    batch = []
    
    for item in array:
        batch.append(item)
        
        if len(batch) == batch_size:
            #returns set of values only need to read once
            yield batch
            batch = []
    #if any item left in array, yield
    if batch:
        yield batch


#inserting file names into array
#read notepad
with open(direc,"r") as directname:
    #link is string in notepad
    for folder in directname:
        folder = folder.strip()
        if os.path.isdir(folder):
            #list file names, array
            dirlist = os.listdir(folder)
            #directory name
            strFolder = f"{folder}/"

            #os.path.splitext(x)[1] get extension of x(file), if extension is in file_format add to list.
            theNewList = [strFolder + x for x in dirlist if os.path.splitext(x)[1] in file_format]
            
            img_paths.extend(theNewList)
            
        else:
            print(f"Directory {folder} does not exist")

def batch_processing():
    #shove batch in imgbatchlist
    for batch in batch_process(img_paths,batch_size):
        img_batchlist.append(batch)

batch_processing()

def delete_arrowR():
    global button_AR,final_length ,final_batch,batch_math
    final_length = len(img_batchlist)
    final_batch = len(img_batchlist[-1])
    batch_math = batch_size * final_length - batch_size + (final_batch - 1)

    if current_findex == batch_math:
        print('True2')
        return button_AR.destroy()
    else:
        print('false')
        button_AR = Button(root, image= photo_img1, command= lambda:forward(img_batchlist), width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
        button_AR.grid(row = 3, column = 2, padx = 50, pady =5,sticky='e')


def destroylb():
    global button_AL
    
    #destroy only on the first image, keep bool
    if current_findex == 0:
        print('true')
        button_AL.destroy()
    else:
        print('false')
        button_AL = Button(root, image= photo_img2, command=lambda: back(img_batchlist), width=30, height=30, borderwidth=0, highlightthickness=0, bg="white")
        button_AL.grid(row = 3, column = 2, padx = 50, pady =5, sticky='w')



img_loaded =False 
#load first batch (image insert array is used on the first batch)
def img_load1(full_batchlist,check_array,appended_list):
    global final_array, img_loaded
    img_loaded =True 
    appended_list.append(full_batchlist[current_array])
    check_array.append(current_array)
    image_insert(final_array,appended_list)
    
    



img_load1(img_batchlist,check_array,appended_list)


def img_load2(full_batchlist, check_array,appended_list):
    global change_array, final_array, current_array, img_loaded
    img_loaded =False 

    print(f'current:{current_array} change: {change_array}')
    
    #if current array changes load in the array appended_list(check what is happening)
    if current_array != change_array:
        if current_array in check_array:
            print('do nothing')
        else:
            
            #append to appendedlist
            appended_list.append(full_batchlist[current_array])
            #append number to check
            check_array.append(current_array)
            #insert the appended_list again
            image_insert(final_array,appended_list)
            
    else:

        print('not changed')

# Function for opening the file explorer window
listchange = False

def browseFiles():
    global DragAndDrop_enabled, final_array,strFolder,check_array,appended_list
    global img_batchlist,img_paths,final_array,current_findex
    DragAndDrop_enabled = None
    listchange= True 
    filename = filedialog.askdirectory()
    
    if filename == '':
        #read inside notepad
        if strFolder.endswith('/'):
            strFolder = strFolder[:-1]
    else:
        #overwrite letters in txt with filename
        with open(direc,"w") as myFile:
            myFile.write(filename)
        strFolder = filename
    
    if len(final_array) > 0 :
        final_array.clear()
        img_paths.clear()
        img_batchlist.clear()
        appended_list.clear()
        check_array.clear()   
        final_array.clear()
        
    else:
        print('not clear')
        
    #goes through the directory
    for root, dirs, files in os.walk(strFolder):
        for file in files:
            #makes full path
            path = os.path.join(root, file)
            #removes double slashes
            normalise = os.path.normpath(path)
            
            #extracts last four characters
            fileType = normalise[-4]+normalise[-3]+normalise[-2]+normalise[-1]
            
            #checks if its in file_format. if not continue without executing
            if fileType not in file_format:
                continue
            #if it is continue appending final array called in insert
            img_paths.append(normalise)
    
    #does the data processing again
    batch_processing()
    img_load1(img_batchlist,check_array,appended_list)
    #image process
    image_insert(final_array,appended_list)
    if current_findex > 0:
        current_findex = 0
    destroy_browsing()
    image_show()


def image_show():
    global my_label,my_label0,frame1,final_array,current_findex
    #image
    my_img0 =Image.open(r"python_pic\background.png")
    img5 = my_img0.resize(target_size)
    photo_img5 = ImageTk.PhotoImage(img5)

    #adds temp img
    my_label0 = Label(image= photo_img5, borderwidth=0, highlightbackground="white")
    my_label0.grid(row=2, column=2, sticky='ew')

    # Add reference to prevent garbage collection
    my_label0.image = photo_img5

    # Create Frame
    frame1 = Frame(root, background='white')
    frame1.grid(row=2, column=2 )
    
    
    #img shown
    my_label = Label(frame1,image = final_array[current_findex], borderwidth =0, highlightbackground="white")
    my_label.grid(row = 2, column = 2, sticky='ew')
    


# functions
image_show()
arrow_button()
arrow_buttonR()
image_function()
root.mainloop()
#compare the current code with past code
#turn into exe
# https://www.blog.pythonlibrary.org/2021/05/27/pyinstaller-how-to-turn-your-python-code-into-an-exe-on-windows/

