
from customtkinter import *
from PIL import Image
from tkinter import ttk, messagebox
import smsdb

# FUNCTIONS
def selection(event):
    selected_item = tree.selection()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        firstNameEntry.insert(0, row[1])
        lastNameEntry.insert(0, row[2])
        genderBox.set(row[3])
        mobileEntry.insert(0, row[4])
        courseBox.set(row[5])

def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    firstNameEntry.delete(0, END)
    lastNameEntry.delete(0, END)
    genderBox.set('Male')
    mobileEntry.delete(0, END)
    courseBox.set('Communication Engineering')

def mainview_data():
    students = smsdb.fetch_students()
    tree.delete(*tree.get_children())
    for student in students:
        # Convert integer ID to 'STU' format
        formatted_id = f"STU{student[0]}"
        tree.insert('', 'end', values=(formatted_id, *student[1:]))


# ADD STUDENT FUNCTION
def add_student():
    if firstNameEntry.get()=='' or lastNameEntry.get()=='' or genderBox.get()=='' or mobileEntry.get()=='' or courseBox.get()=='':
        messagebox.showerror('Error','Please fill all fields')
    else:
        student_id = smsdb.insert(firstNameEntry.get(), lastNameEntry.get(), genderBox.get(), mobileEntry.get(), courseBox.get())
        formatted_id = f"STU{student_id}"
        tree.insert('', 'end', values=(formatted_id, firstNameEntry.get(), lastNameEntry.get(), genderBox.get(), mobileEntry.get(), courseBox.get()))
        clear()
        messagebox.showinfo('Success', f'Data added. Student ID: {formatted_id}')


# UPDATE STUDENT FUNCTION
def update_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select a data to update.')
    else:
        row = tree.item(selected_item)['values']

        # 🛠️ Strip STU prefix to get the real integer ID
        real_id = int(str(row[0]).replace("STU", ""))

        smsdb.update_students(real_id, firstNameEntry.get(), lastNameEntry.get(), genderBox.get(), mobileEntry.get(), courseBox.get())
        mainview_data()
        clear()
        messagebox.showinfo('Success', 'Data Updated')


# DELETE STUDENT FUNCTION
def delete_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select a data to delete.')
    else:
        row = tree.item(selected_item)['values']
        try:
            real_id = int(str(row[0]).replace("STU", ""))
            smsdb.delete_student(real_id)
            mainview_data()
            clear()
            messagebox.showinfo('Success', 'Data Deleted')
        except ValueError:
            messagebox.showerror('Error', 'Invalid Student ID format')

# SEARCH STUDENT FUNCTION
def search_student():
    if searchEntry.get() == '':
        messagebox.showerror('Error', 'Enter keyword to search')
    elif searchBox.get() == 'Search By':
        messagebox.showerror('Error', 'Please select an option')
    else:
        option = searchBox.get()
        value = searchEntry.get()

        # 🛠️ Strip STU prefix if searching by ID
        if option == 'Student ID' and value.upper().startswith('STU'):
            value = value[3:]

        searched_data = smsdb.search(option, value)
        tree.delete(*tree.get_children())
        for student in searched_data:
            display_id = f"STU{student[0]}"
            tree.insert('', 'end', values=(display_id, *student[1:]))


# SHOW ALL FUNCTION
def show_all():
    mainview_data()
    searchEntry.delete(0, END)
    searchBox.set('Search By')

# DELETE ALL STUDENT DATA FUNCTION
def delete_all():
    results = messagebox.askyesno('Confirm', 'Do you really want to delete all data?')
    if results:
        smsdb.deleteall_data()
        mainview_data()
        clear()

## GUI START HERE
student_window = CTk()
student_window.geometry('980x580+100+100')
student_window.resizable(False,False)
student_window.title('Student Management System')
student_window.configure(fg_color='#00827f')

# Import Image
imageLogo = CTkImage(Image.open('LOGO_FHK.png'), size=(280,100))

# Add Image in the window
imageLabel = CTkLabel(student_window, image=imageLogo, text='')
imageLabel.grid(row=0, column=0)

# Left Frame
leftFrame = CTkFrame(student_window, fg_color='#00827f')
leftFrame.grid(row=1, column=0)

# Add First Name Label
nameLabel = CTkLabel(leftFrame, text='First Name:', font=('Arial', 18, 'bold'))
nameLabel.grid(row=0, column=0, padx=20, pady=15, sticky=W)

firstNameEntry = CTkEntry(leftFrame, font=('Arial', 15), width=180)
firstNameEntry.grid(row=0, column=1)

# Add Last Name Label
lastNameLabel = CTkLabel(leftFrame, text='Last Name:', font=('Arial', 18, 'bold'))
lastNameLabel.grid(row=1, column=0, padx=20, pady=15, sticky=W)

lastNameEntry = CTkEntry(leftFrame, font=('Arial', 15), width=180)
lastNameEntry.grid(row=1, column=1)

# Add Gender Label
genderLabel = CTkLabel(leftFrame, text='Gender:', font=('Arial', 18, 'bold'))
genderLabel.grid(row=2, column=0, padx=20, pady=15, sticky=W)

gender_options = ['Male', 'Female']
genderBox = CTkComboBox(leftFrame, values=gender_options, width=180, font=('Arial', 18))
genderBox.grid(row=2, column=1, padx=20, pady=15, sticky=W)
genderBox.set(gender_options[0])

# Add Mobile Label
mobileLabel = CTkLabel(leftFrame, text='Mobile:', font=('Arial', 18, 'bold'))
mobileLabel.grid(row=3, column=0, padx=20, pady=15, sticky=W)

mobileEntry = CTkEntry(leftFrame, font=('Arial', 15), width=180)
mobileEntry.grid(row=3, column=1)

# Add Course Label
courseLabel = CTkLabel(leftFrame, text='Course:', font=('Arial', 18, 'bold'))
courseLabel.grid(row=4, column=0, padx=20, pady=15, sticky=W)

course_options = ['Communication Engineering', 'Medical Engineering', 'Data Science']
courseBox = CTkComboBox(leftFrame, values=course_options, width=180, font=('Arial', 18))
courseBox.grid(row=4, column=1, padx=20, pady=15, sticky=W)
courseBox.set(course_options[0])

# Right Frame
rightFrame = CTkFrame(student_window)
rightFrame.grid(row=1, column=1)

# Add Search Option
search_options = ['Student ID', 'First Name', 'Last Name', 'Gender', 'Mobile', 'Course']
searchBox = CTkComboBox(rightFrame, values=search_options)
searchBox.grid(row=0, column=0)
searchBox.set('Search By')

searchEntry = CTkEntry(rightFrame)
searchEntry.grid(row=0, column=1)

searchButton = CTkButton(rightFrame, text='Search', width=85, command=search_student)
searchButton.grid(row=0, column=2, pady=5)

showAllButton = CTkButton(rightFrame, text='Show All', width=85, command=show_all)
showAllButton.grid(row=0, column=3)

tree = ttk.Treeview(rightFrame, height=13)
tree.grid(row=1, column=0, columnspan=4)

tree['columns'] = ('Student ID', 'First Name', 'Last Name', 'Gender', 'Mobile', 'Course')

tree.heading('Student ID', text='Student ID')
tree.heading('First Name', text='First Name')
tree.heading('Last Name', text='Last Name')
tree.heading('Gender', text='Gender')
tree.heading('Mobile', text='Mobile')
tree.heading('Course', text='Course')

tree.configure(show='headings')

tree.column('Student ID', width=100)
tree.column('First Name', width=100)
tree.column('Last Name', width=100)
tree.column('Gender', width=100)
tree.column('Mobile', width=150)
tree.column('Course', width=200)

style = ttk.Style()
style.configure('Treeview.Heading', font=('Arial', 12, 'bold'))
style.configure('Treeview', font=('Arial', 15, 'bold'), rowheight=30, background='#00827f', foreground='white')

scrollbar = ttk.Scrollbar(rightFrame, orient='vertical')
scrollbar.grid(row=1, column=4, sticky='ns')

# Button Frame
buttonFrame = CTkFrame(student_window, fg_color='#00827f')
buttonFrame.grid(row=2, column=0, columnspan=2, pady=20)

stuButton = CTkButton(buttonFrame, text='New Student', font=('Arial', 15, 'bold'), width=160, corner_radius=5, command=lambda: clear(True))
stuButton.grid(row=0, column=0, pady=5)

addButton = CTkButton(buttonFrame, text='Add Student', font=('Arial', 15, 'bold'), width=160, corner_radius=5, command=add_student)
addButton.grid(row=0, column=1, padx=5, pady=5)

updateButton = CTkButton(buttonFrame, text='Update Student', font=('Arial', 15, 'bold'), width=160, corner_radius=5, command=update_student)
updateButton.grid(row=0, column=2, padx=5, pady=5)

deleteButton = CTkButton(buttonFrame, text='Delete Student', font=('Arial', 15, 'bold'), width=160, corner_radius=5, command=delete_student)
deleteButton.grid(row=0, column=3, padx=5, pady=5)

deleteAllButton = CTkButton(buttonFrame, text='Delete All Student', font=('Arial', 15, 'bold'), width=160, corner_radius=5, command=delete_all)
deleteAllButton.grid(row=0, column=4, padx=5, pady=5)

mainview_data()

student_window.bind('<ButtonRelease>', selection)

student_window.mainloop()