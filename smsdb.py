import pymysql
from tkinter import messagebox



def connect_database():
    global myCursor, con
    try:
    #Connection to MYSQL
        con = pymysql.connect(host='localhost', user='root', password='Admin_12345')
    #Help mysql to execute mysql command
        myCursor = con.cursor()
    except:
        messagebox.showerror('Error','Something went wrong!, Please open MySQL app before running again')
        return

#CREATE TABLE
    myCursor.execute('CREATE DATABASE IF NOT EXISTS student_data')
    myCursor.execute('USE student_data')
    myCursor.execute('CREATE TABLE IF NOT EXISTS data (student_id INTEGER PRIMARY KEY AUTO_INCREMENT,firstname VARCHAR(60), lastname VARCHAR(60),gender VARCHAR(20), mobile INTEGER(20), course VARCHAR(50))')


def insert(student_id, firstname, lastname, gender, mobile, course):
    myCursor.execute('INSERT INTO data VALUES (%s,%s,%s,%s,%s,%s)', (student_id,firstname,lastname,gender,mobile,course))
    con.commit()

def student_id_exists(student_id):
    myCursor.execute('SELECT COUNT(*) FROM data WHERE student_id=%s', student_id)
    results = myCursor.fetchone()
    return results[0]>0

def fetch_students():
    myCursor.execute('SELECT * FROM data')
    results = myCursor.fetchall()
    return results

def update_students(student_id, new_firstname, new_lastname, new_gender, new_mobile, new_course):
    myCursor.execute('UPDATE data SET firstname=%s, lastname=%s, gender=%s, mobile=%s, course=%s WHERE student_id=%s', (new_firstname, new_lastname, new_gender, new_mobile, new_course, student_id))
    con.commit()

def delete_student(student_id):
    myCursor.execute('DELETE FROM data WHERE student_id=%s', student_id)
    con.commit()

'''def search(option, values):
    myCursor.execute(f'SELECT * FROM data WHERE {option}=%s', values)
   results = myCursor.fetchall()
    return results'''


def search(option, value):
    allowed_columns = {
        'Student ID': 'student_id',
        'First Name': 'firstname',
        'Last Name': 'lastname',
        'Gender': 'gender',
        'Mobile': 'mobile',
        'Course': 'course'
    }

    column = allowed_columns.get(option)
    if not column:
        raise ValueError("Invalid search option")

    query = f"SELECT * FROM data WHERE `{column}` = %s"  # use backticks to escape column name
    myCursor.execute(query, (value,))
    return myCursor.fetchall()

def deleteall_data():
    myCursor.execute('TRUNCATE TABLE data')
    con.commit()

connect_database()

