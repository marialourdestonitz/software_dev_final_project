
from customtkinter import *
from PIL import  Image
from customtkinter import CTkImage
from tkinter import messagebox
import smsdb




#login Function
def login():
    if usernameEntry.get()=='' and passwordEntry.get()=='':
        messagebox.showerror('Error','Please fill all fields')
    elif usernameEntry.get()=='marry' and passwordEntry.get()=='12345':
        messagebox.showinfo('Success','Login successfully')
        main_window.destroy()
    else:
        messagebox.showerror('Error','Wrong Credentials')



#Create TCK Window
main_window = CTk()

#Change the Width and Height of the window
main_window.geometry('940x478')
main_window.resizable(False,False)
main_window.title('Student Management System')

#Import Image
image = CTkImage(Image.open('LOGO_FHK.png'), size=(630,178))

#Add Image in the window
imageLabel = CTkLabel(main_window, image=image, text='')
imageLabel.place(x=280, y=100)

#Add Heading Label
headingLabel = CTkLabel(main_window, text='Login', font=('Goudy Old Style', 20, 'bold'))
headingLabel.place(x=100, y=150)

#Create User Text Input
usernameEntry = CTkEntry(main_window, placeholder_text='Enter your Username', width=180)
usernameEntry.place(x=50, y=185)

passwordEntry = CTkEntry(main_window, placeholder_text='Enter your Password', width=180, show='*')
passwordEntry.place(x=50, y=220)

#Create Login Button
loginButton = CTkButton(main_window, text='Login', width=180, cursor = 'hand2' , command=login)
loginButton.place(x=50, y=260)

#For us to see the Window continuously
main_window.mainloop()