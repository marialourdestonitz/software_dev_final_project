import pymysql
from tkinter import messagebox
def connect_database():
    global myCursor, con
    try:
        con = pymysql.connect(host='localhost', user='root', password='12345')
        myCursor = con.cursor()
        myCursor.execute('CREATE DATABASE IF NOT EXISTS student_data')
        myCursor.execute('USE student_data')
        myCursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                student_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(60),
                lastname VARCHAR(60),
                gender VARCHAR(20),
                mobile VARCHAR(20),
                course VARCHAR(50)
            )
        ''')
        con.commit()
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'MySQL Error: {e}')
        if 'con' in locals() and con.is_connected():
            con.close()
        raise  # Re-raise to prevent silent failures


def insert(firstname, lastname, gender, mobile, course):
    myCursor.execute('INSERT INTO data (firstname, lastname, gender, mobile, course) VALUES (%s,%s,%s,%s,%s)', (firstname, lastname, gender, mobile, course))
    con.commit()
    myCursor.execute('SELECT LAST_INSERT_ID()')
    return myCursor.fetchone()[0]

def student_id_exists(student_id):
    myCursor.execute('SELECT COUNT(*) FROM data WHERE student_id=%s', (student_id,))
    results = myCursor.fetchone()
    return results[0] > 0

def fetch_students():
    myCursor.execute('SELECT * FROM data')
    results = myCursor.fetchall()
    return results

def update_students(student_id, new_firstname, new_lastname, new_gender, new_mobile, new_course):
    myCursor.execute('UPDATE data SET firstname=%s, lastname=%s, gender=%s, mobile=%s, course=%s WHERE student_id=%s', (new_firstname, new_lastname, new_gender, new_mobile, new_course, student_id))
    con.commit()

def delete_student(student_id):
    myCursor.execute('DELETE FROM data WHERE student_id=%s', (student_id,))
    con.commit()

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

    query = f"SELECT * FROM data WHERE `{column}` = %s"
    myCursor.execute(query, (value,))
    return myCursor.fetchall()

def deleteall_data():
    myCursor.execute('TRUNCATE TABLE data')
    con.commit()

connect_database()
