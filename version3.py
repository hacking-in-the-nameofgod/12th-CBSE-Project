'''
Grade 12 Project: EduTrack
Made by: Vansh Aggarwal, Prad, Akash

Start Date: 9 August,2024
'''
#Importing all necessary functions for the code:

import mysql.connector as s
from random import choice
import bcrypt as b
from tabulate import tabulate as t

# creating a connection with sql
def sqlconnect():
    link = s.connect(host='localhost', user='root', passwd='sql123', database='EduTrack')
    return link

# Generating a primary key for the tables
   
def createid():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    #final = "".join(choice(chars) for i in range(8))
    final = ""
    for i in range (8):
        temp_opt = choice(chars)
        final += temp_opt

    return final

    
# creating auth functions for the code
def studentlogin():
    link = sqlconnect()
    if link is None:
        return ""
    
    cur = link.cursor()
    email = input("Enter email: ")
    passwd = input("Enter password: ").encode('utf-8')
    cur.execute("SELECT * FROM student WHERE email=%s;", (email,))
    l = cur.fetchall()

    if not l:
        print("No user found.")
        return ""
    else:
        stored_hash = l[0][3].encode('utf-8')
        if b.checkpw(passwd, stored_hash):
            print("Logged in successfully!")
            return l[0][0]
        else:
            print("Incorrect email or password.")
            return ""

def teacherlogin():
    link = sqlconnect()
    if link is None:
        return ""

    cur = link.cursor()
    email = input("Enter email: ")
    passwd = input("Enter password: ").encode('utf-8')
    cur.execute("SELECT * FROM teacher WHERE email=%s;", (email,))
    l = cur.fetchall()

    if not l:
        print("No user.")
        return ""
    else:
        stored_hash = l[0][3].encode('utf-8')
        if b.checkpw(passwd, stored_hash):
            print("Logged in successfully.")
            return l[0][0]
        else:
            print("Incorrect email or password.")
            return ""

def studentsignup():
    link = sqlconnect()
    if link is None:
        return ""

    cur = link.cursor()
    email = input("Enter email: ")
    passwd = input("Enter password (min 8 chars): ").encode('utf-8')
    studentname = input("Enter student name: ")
    classsec = input("Enter class and section (e.g., 12A): ")
    school = input("Enter school: ")

    cur.execute("SELECT * FROM student WHERE email=%s;", (email,))
    l = cur.fetchall()

    if l:
        print("This user already exists. Please login.")
    elif len(passwd) < 8:
        print("Password needs to be at least 8 characters long.")
    else:
        userid = createid()
        hashed_pw = b.hashpw(passwd, b.gensalt())
        cur.execute("INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s);", 
                       (userid, email, studentname, hashed_pw.decode('utf-8'), classsec, school))
        link.commit()
        print("Signed up successfully!")

def teachersignup():
    link = sqlconnect()
    if link is None:
        return

    cur = link.cursor()
    email = input("Enter email: ")
    passwd = input("Enter password (min 8 chars): ").encode('utf-8')
    teachername = input("Enter teacher name: ")
    school = input("Enter school: ")

    cur.execute("SELECT * FROM teacher WHERE email=%s;", (email,))
    l = cur.fetchall()

    if l:
        print("This user already exists. Please login.")
    elif len(passwd) < 8:
        print("Password needs to be at least 8 characters long.")
    else:
        userid = createid()
        hashed_pw = b.hashpw(passwd, b.gensalt())
        cur.execute("INSERT INTO teacher VALUES (%s, %s, %s, %s, %s);", 
                       (userid, teachername, email, hashed_pw.decode('utf-8'), school))
        link.commit()
        print("Signed up successfully!")


# student view functions

def s_manageclasses(userid):
    connection = sqlconnect()
    if connection is None:
        return

    cur = connection.cursor()
    cur.execute("SELECT class.classid, classname FROM studentmembership "
                   "JOIN class ON studentmembership.classid = class.classid "
                   "WHERE studentmembership.studentid = %s;", (userid,))
    l = cur.fetchall()
    print("Your classes:")
    print(t(l, ["Class ID", "Class Name"],  ))

def s_viewassignments():
    link = sqlconnect()
    if link is None:
        return
    cur = link.cursor()
    classid = input("Enter Class ID: ")
    cur.execute("SELECT * FROM assignment WHERE classid = %s;", (classid,))
    l = cur.fetchall()
    print("Your assignments:")
    print(t(l, ["Assignment ID", "Class ID", "Assignment Name", "Deadline"],  ))

def s_viewproblem():
    link = sqlconnect()
    if link is None:
        return

    cur = link.cursor()
    assignmentid = input("Enter Assignment ID: ")
    cur.execute("SELECT problemid FROM problem WHERE assignmentid = %s;", (assignmentid,))
    l = cur.fetchall()
    print("Problems in this assignment:")
    print(t(l, ["Problem ID"],  ))
    problemid = input("Enter Problem ID: ")

    cur.execute("SELECT problem FROM problem WHERE problemid = %s;", (problemid,))
    l = cur.fetchall()

    if not l:
        print("Invalid ID.")
    else:
        print(l[0][0])

def s_viewsubmission(userid):
    link = sqlconnect()
    if link is None:
        return

    cur = link.cursor()
    assignmentid = input("Enter Assignment ID: ")
    cur.execute("SELECT problemid FROM problem WHERE assignmentid = %s;", (assignmentid,))
    l = cur.fetchall()
    print("Problems in this assignment:")
    print(t(l, ["Problem ID"],  ))
    problemid = input("Enter Problem ID: ")

    cur.execute("SELECT submissionid, complete FROM submission WHERE problemid = %s;", (problemid,))
    l = cur.fetchall()
    print("Your submissions:")
    print(t(l, ["Submission ID", "Completed (0/1)"],))

    subid = input("Enter Submission ID: ")
    cur.execute("SELECT code, comments FROM submission WHERE submissionid = %s;", (subid,))
    l = cur.fetchall()

    if l:
        print(l[0][0])
        print("Teacher's comments:")
        print(l[0][1])
    else:
        print("No submission found with the provided ID.")

def s_submitcode():
    link = sqlconnect()
    if link is None:
        return

    cur = link.cursor()
    problemid = input("Enter Problem ID: ")
    path = input("Enter code path: ")

    try:
        with open(path, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print("File not found.")
        return

    subid = createid()
    cur.execute("INSERT INTO submission VALUES (%s, %s, %s, 0, '');", (subid, problemid, code))
    link.commit()
    print("Code submitted successfully!")


# teacher view functions

def t_createclass(userid):
    link = sqlconnect()
    if link is None:
        return

    cur = link.cursor()
    classid = createid()
    classname = input("Enter class name: ")

    cur.execute("INSERT INTO class VALUES (%s, %s);", (classid, classname))
    cur.execute("INSERT INTO teachermembership VALUES (%s, %s);", (classid, userid))
    link.commit()
    print(f"Class '{classname}' created successfully!")

def t_manageclasses(userid):
    link = sqlconnect()
    if link is None:
        return

    cur = link.cursor()
    cur.execute("SELECT class.classid, classname FROM teachermembership "
                   "JOIN class ON teachermembership.classid = class.classid "
                   "WHERE teachermembership.teacherid = %s;", (userid,))
    l = cur.fetchall()
    print("Your classes:")
    print(t(l, ["Class ID", "Class Name"],))

def t_viewassignments():
    link = sqlconnect()
    if link is None:
        return

    cur = link.cursor()
    classid = input("Enter Class ID: ")
    cur.execute("SELECT * FROM assignment WHERE classid = %s;", (classid,))
    l = cur.fetchall()
    print("Your assignments:")
    print(t(l, ["Assignment ID", "Class ID", "Assignment Name", "Deadline"],))

def t_addassignment():
    link = sqlconnect()
    if link is None:
        return

    cur = link.cursor()
    assignmentid = createid()
    classid = input("Enter class ID: ")
    assignmentname = input("Enter assignment name: ")
    deadline = input("Enter deadline (yyyy-mm-dd): ")

    cur.execute("INSERT INTO assignment VALUES (%s, %s, %s, %s);", (assignmentid, classid, assignmentname, deadline))
    link.commit()
    print("Assignment added successfully!")

def t_addproblem():
    link = sqlconnect()
    if link is None:
        return

    cur = link.cursor()
    problemid = createid()
    assignmentid = input("Enter Assignment ID: ")
    problem = input("Enter the problem: ")

    cur.execute("INSERT INTO problem VALUES (%s, %s, %s);", (problemid, assignmentid, problem))
    link.commit()
    print("Problem added successfully!")

def t_viewsubmission():
    link = sqlconnect()
    if link is None:
        return

    cur = link.cursor()
    assignmentid = input("Enter Assignment ID: ")
    cur.execute("SELECT problemid FROM problem WHERE assignmentid = %s;", (assignmentid,))
    l = cur.fetchall()
    print("Problems in this assignment:")
    print(t(l, ["Problem ID"],  ))
    problemid = input("Enter Problem ID: ")

    cur.execute("SELECT submissionid, complete FROM submission WHERE problemid = %s;", (problemid,))
    l = cur.fetchall()
    print("Submissions:")
    print(t(l, ["Submission ID", "Completed (0/1)"],  ))

    s = input("Enter Submission ID: ")
    cur.execute("SELECT code FROM submission WHERE submissionid = %s;", (s,))
    l = cur.fetchall()

    if l:
        print(l[0][0])
        inp = input("Do you want to enter any comments? (Y/N) ")
        if inp.lower() == "y":
            c = input("Enter comments: ")
            cur.execute("UPDATE submission SET comments=%s, complete=1 WHERE submissionid=%s;", (c, s))
            link.commit()
            print("Comments updated successfully!")
        else:
            print("No comments added.")
    else:
        print("No submission found with the provided ID.")





#Main Code execution functions:
def studentview(userid):
    while True:
        print('''
Welcome, student
              
1. Manage Classes
2. View Assignments
3. View Problem
4. View Submissions
5. Submit Code
6. Exit''')
        opt1 = input("Enter your option: ")

        if opt1 == "1":
            s_manageclasses(userid)
        elif opt1 == "2":
            s_viewassignments()
        elif opt1 == "3":
            s_viewproblem()
        elif opt1 == "4":
            s_viewsubmission(userid)
        elif opt1 == "5":
            s_submitcode()
        elif opt1 == "6":

            break
        else:
            print("Invalid option.")

def teacherview(userid):
    while True:
        print('''
Welcome, teacher
              
1. Create Class
2. Manage Classes
3. View Assignments 
4. Add Assignment 
5. Add Problem    
6. View Submissions  
7. Exit    ''')


        opt1 = input("Enter your option: ")

        if opt1 == "1":
            t_createclass(userid)
        elif opt1 == "2":
            t_manageclasses(userid)
        elif opt1 == "3":
            t_viewassignments()
        elif opt1 == "4":
            t_addassignment()
        elif opt1 == "5":
            t_addproblem()
        elif opt1 == "6":
            t_viewsubmission()
        elif opt1 == "7":
            break
        else:
            print("Invalid option!")

#Main Loop
while True:
    print('''
Welcome to EduTrack 
1. Student Login
2. Student Signup
3. Teacher Login
4. Teacher Signup
5. Exit''')
    opt2 = input("Enter your option: ")

    if opt2 == "1":
        userid = studentlogin()
        if userid:
            studentview(userid)
    elif opt2 == "2":
        studentsignup()
    elif opt2 == "3":
        userid = teacherlogin()
        if userid:
            teacherview(userid)
    elif opt2 == "4":
        teachersignup()
    elif opt2 == "5":
        print("Program will exit now.")
        break
    else:
        print("Invalid option. Please try again!!!")
