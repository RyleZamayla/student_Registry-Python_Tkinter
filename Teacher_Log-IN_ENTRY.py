from tkinter import *
import sqlite3
import os
from tkinter.font import Font
from tkinter import messagebox as mb

root = Tk()
root.title("Student Grading Registry")
width = 440
height = 340
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

def Database():
    global conn, cursor
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS admin (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
    cursor.execute("SELECT * FROM admin WHERE username = 'admin01' AND password = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO admin (username, password) VALUES('admin01', 'admin')")
    conn.commit()


def Action(event=None):
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        input_warning.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?",
                       (USERNAME.get(), PASSWORD.get()))

        if cursor.fetchone() is not None:
            Grading()
            USERNAME.set("")
            PASSWORD.set("")
            input_warning.config(text="")
        else:
            input_warning.config(text="Invalid username or password!", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
            cursor.close()
            conn.close()

def Grading():
    import tkinter.ttk as ttk
    import tkinter.messagebox as tkMessageBox
    import Grade_Data
    global Home
    global checker
    root.withdraw()
    Home = Toplevel()
    Home.title("GRADING SHEET")
    width = 1080
    height = 580
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2.3) - (height / 2)
    Home.resizable(0, 0)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))

    # ==================================METHODS============================================

    def computation():
        global checker
        try:
            checker = True
            global average
            int(STUDENT_NO.get())
            result = int(studentPRELIM.get()) + int(studentMIDTERM.get()) + int(studentFINAL.get())
            average = result // 3
            AVERAGE.set(average)

            if int(AVERAGE.get()) >= 95:
                GPE.set("1.00")
                REMARKS.set("Excellent")
            elif int(AVERAGE.get()) >= 91:
                GPE.set("1.25")
                REMARKS.set("Supperior")
            elif int(AVERAGE.get()) >= 88:
                GPE.set("1.50")
                REMARKS.set("Very Good")
            elif int(AVERAGE.get()) >= 86:
                GPE.set("1.75")
                REMARKS.set("Good")
            elif int(AVERAGE.get()) >= 84:
                GPE.set("2.00")
                REMARKS.set("Very Satisfactory")
            elif int(AVERAGE.get()) >= 82:
                GPE.set("2.25")
                REMARKS.set("High Average")
            elif int(AVERAGE.get()) >= 79:
                GPE.set("2.50")
                REMARKS.set("Average")
            elif int(AVERAGE.get()) >= 77:
                GPE.set("2.75")
                REMARKS.set("Fair")
            elif int(AVERAGE.get()) >= 75:
                GPE.set("3.00")
                REMARKS.set("Pass")
            elif int(AVERAGE.get()) >= 58:
                GPE.set("4.00")
                REMARKS.set("Conditional if Pass/Failing")
            else:
                GPE.set("5.00")
                REMARKS.set("Failing Final Grade")

        except ValueError:
            checker = False
            mb.showwarning("SYSTEM - ERROR", "Grade and Student ID must be Integer not String! Please Input again!")
            STUDENT_NO.set("")
            PRELIM.set("")
            MIDTERM.set("")
            FINAL.set("")


    def insertData():
        global checker
        if STUDENT_NO.get() == "" or STUDENT_NAME.get() == "" or comboCOURSE.get() == "" \
                or SUBJECT.get() == "" or PRELIM.get() == "" or MIDTERM.get() == "" or FINAL.get() == "":
            txt_result.config(text="Please complete the required field!", fg="red")

        else:
            computation()
            if checker:
                if int(AVERAGE.get()) > 100:
                    mb.showwarning("SYSTEM - ERROR", "Overlapping Grade! Please Input again!")
                    PRELIM.set("")
                    MIDTERM.set("")
                    FINAL.set("")
                else:
                    Grade_Data.Database()
                    Grade_Data.cursor.execute(
                        "INSERT INTO `admin` (student_no, student_name, course, subject, prelim, midterm, final, average, gpe, remarks)"
                        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            str(STUDENT_NO.get()), str(STUDENT_NAME.get()), str(comboCOURSE.get()), str(SUBJECT.get()),
                            str(PRELIM.get()), str(MIDTERM.get()), str(FINAL.get()), str(AVERAGE.get()),
                            str(GPE.get()), str(REMARKS.get())))

                    Grade_Data.conn.commit()
                    STUDENT_NO.set("")
                    STUDENT_NAME.set("")
                    comboCOURSE.set("")
                    SUBJECT.set("")
                    PRELIM.set("")
                    MIDTERM.set("")
                    FINAL.set("")
                    Grade_Data.cursor.close()
                    Grade_Data.conn.close()
                    txt_result.config(text="Grade successfully computed", fg="green")
                    displayData()

    def displayData():
        tree.delete(*tree.get_children())
        Grade_Data.Database()
        Grade_Data.cursor.execute("SELECT * FROM `admin` ORDER BY `student_no` ASC")
        fetch = Grade_Data.cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(
                data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10]))
        Grade_Data.cursor.close()
        Grade_Data.conn.close()

    def Exit():
        result = tkMessageBox.askquestion('Python - GRADING SHEET', 'Are you sure you want to exit?',
                                          icon="warning")
        if result == 'yes':
            Home.destroy()
        exit()

    def pick_COURSE(e):
        if department.get() == "CEA":
            comboCOURSE.config(value=CEA)
            comboCOURSE.current(0)
        elif department.get() == "CITC":
            comboCOURSE.config(value=CITC)
            comboCOURSE.current(0)
        elif department.get() == "CSTE":
            comboCOURSE.config(value=CSTE)
            comboCOURSE.current(0)
        else:
            comboCOURSE.config(value=COT)
            comboCOURSE.current(0)

    def contact_UsFacebook():
        os.system("start \"\" https://www.facebook.com/RyleZamayla")

    def contact_UsInstagram():
        os.system("start \"\" https://www.instagram.com/_rydealist/")

    def contact_UsTwitter():
        os.system("start \"\" https://twitter.com/_rydealist")



    # ==================================VARIABLES==============================================
    STUDENT_NO = StringVar()
    STUDENT_NAME = StringVar()
    SUBJECT = StringVar()
    PRELIM = StringVar()
    MIDTERM = StringVar()
    FINAL = StringVar()
    AVERAGE = StringVar()
    GPE = StringVar()
    REMARKS = StringVar()

    # ==================================PULLDOWN MENU==============================================
    menubar = Menu(Home)
    file = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file)
    file.add_command(label='New File', command=None)
    file.add_command(label='Open...', command=None)
    file.add_command(label='Save', command=None)
    file.add_separator()
    file.add_command(label='Exit', command=root.destroy)

    edit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Edit', menu=edit)
    edit.add_command(label='Cut', command=None)
    edit.add_command(label='Copy', command=None)
    edit.add_command(label='Paste', command=None)
    edit.add_command(label='Select All', command=None)
    edit.add_separator()
    edit.add_command(label='Find...', command=None)
    edit.add_command(label='Find again', command=None)

    contact = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Contact ME', menu=contact)
    contact.add_command(label='Facebook', command=contact_UsFacebook)
    contact.add_command(label='Instagram', command=contact_UsInstagram)
    contact.add_command(label='Twitter', command=contact_UsTwitter)

    help_ = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Help', menu=help_)
    help_.add_command(label='Tk Help', command=None)
    help_.add_command(label='Demo', command=None)
    help_.add_separator()
    help_.add_command(label='About Tk', command=None)

    Home.config(menu=menubar)
    # ==================================FRAME==============================================
    Top = Frame(Home, width=900, height=50, bd=8)
    Top.pack(side=TOP)
    Left = Frame(Home, width=330, height=500, bd=8, padx = 10)
    Left.pack(side=LEFT, padx = 12)
    Right = Frame(Home, width=600, height=500, bd=10, relief = "raise")
    Right.pack(side=TOP, expand = True)
    Forms = Frame(Left, width=330, height=450,bd=10, relief = "groove")
    Forms.pack(side=TOP)
    Buttons = Frame(Left, width=330, height=100, bd=8, relief="ridge")
    Buttons.pack(side=BOTTOM, pady = 13)
    RadioGroup = Frame(Forms)
    # ==================================LABEL WIDGET=======================================
    txt_title = Label(Top, width=900, font=(Title_Font), text="Python - Simple Grading System")
    txt_title.pack(anchor = "e", padx = 20, pady =8)
    txt_Header = Label(Forms, text = "INPUT YOUR DATA HERE", font = (Sub_titleFont), bd = 10)
    txt_Header.grid(row=0, columnspan = 2)
    txt_studentID = Label(Forms, text="Student ID:", font=(Sub_titleFont), bd=15)
    txt_studentID.grid(row=1, stick="w")
    txt_studentNAME = Label(Forms, text="Student Name:", font=(Sub_titleFont), bd=15)
    txt_studentNAME.grid(row=2, stick="w")
    txt_COURSE = Label(Forms, text="Course:", font=(Sub_titleFont), bd=15)
    txt_COURSE.grid(row=3, stick="w")
    txt_SUBJECT = Label(Forms, text="Subject:", font=(Sub_titleFont), bd=15)
    txt_SUBJECT.grid(row=4, stick="w")
    txt_Prelim = Label(Forms, text="Prelim Grade:", font=(Sub_titleFont), bd=15)
    txt_Prelim.grid(row=5, stick="w")
    txt_Midterm = Label(Forms, text="Midterm Grade:", font=(Sub_titleFont), bd=15)
    txt_Midterm.grid(row=6, stick="w")
    txt_Final = Label(Forms, text="Final Grade:", font=(Sub_titleFont), bd=15)
    txt_Final.grid(row=7, stick="w")
    txt_result = Label(Buttons)
    txt_result.pack(side=TOP)
    # ==================================ENTRY WIDGET=======================================
    studentNO = Entry(Forms, textvariable=STUDENT_NO, width=30)
    studentNO.grid(row = 1, column=1, sticky = "e", padx = 15)

    studentNAME = Entry(Forms, textvariable=STUDENT_NAME, width=30)
    studentNAME.grid(row = 2, column=1, sticky = "e", padx = 15)

    DEPARTMENTS = ["CEA", "CITC", "CSTE", "COT"]
    CEA = ["BSARCH", "BSCE", "BSEE", "BSECE", "BSME", "BSGE",
           "MEP-CE", "MEP-EE", "MEP-ECE", "MEP-ME", "MSEE", "MSSD", "PSM-PSEM"]
    CITC = ["BSCpE", "BSIT", "BSTCM", "BSDS",
            "MSTCM", "MIT"]
    CSTE = ["BSAM", "BSAP", "BSC", "BSES", "BSFT",
            "MSAM", "MSEST",
            "PHD-MS"]
    COT = ["BSAMT", "BSETM", "BSEMT", "BSECT"]


    department = ttk.Combobox(Forms, width = 5)
    department['values']= (DEPARTMENTS)
    department.current(0)
    department.grid(row = 3, column =1, sticky = "w", padx = 18)
    department.bind("<<ComboboxSelected>>", pick_COURSE)

    comboCOURSE = ttk.Combobox(Forms, width=12)
    comboCOURSE['values'] = ("")
    comboCOURSE.grid(row=3, column=1, sticky="e", padx=15)


    studentSUBJECT = Entry(Forms, textvariable=SUBJECT, width=30)
    studentSUBJECT.grid(row = 4, column=1, sticky = "e", padx = 15)

    studentPRELIM = Entry(Forms, textvariable=PRELIM, width=30)
    studentPRELIM.grid(row = 5, column=1, sticky = "e", padx = 15)

    studentMIDTERM = Entry(Forms, textvariable=MIDTERM, width=30)
    studentMIDTERM.grid(row = 6, column=1, sticky = "e", padx = 15)

    studentFINAL = Entry(Forms, textvariable=FINAL, width=30)
    studentFINAL.grid(row = 7, column=1, sticky = "e", padx = 15)
    # ==================================BUTTONS WIDGET=====================================
    btn_create = Button(Buttons, width=10, text="Compute", command=insertData, padx = 10)
    btn_create.pack(side=LEFT)
    btn_exit = Button(Buttons, width=10, text="Exit", command=Exit, padx = 13)
    btn_exit.pack(side=LEFT)
    # ==================================LIST WIDGET========================================
    scrollbary = Scrollbar(Right, orient=VERTICAL)
    scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
    tree = ttk.Treeview(Right, columns=("Student ID", "Student Name", "Course", "Subject",
                                        "Prelim", "Midterm", "Final", "Average", "GPE", "REMARKS"),
                        selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Student ID', text="Student ID", anchor=W)
    tree.heading('Student Name', text="Student Name", anchor=W)
    tree.heading('Course', text="Course", anchor=W)
    tree.heading('Subject', text="Subject", anchor=W)
    tree.heading('Prelim', text="Prelim", anchor=W)
    tree.heading('Midterm', text="Midterm", anchor=W)
    tree.heading('Final', text="Final", anchor=W)
    tree.heading('Average', text="Average", anchor=W)
    tree.heading('GPE', text="GPE", anchor=W)
    tree.heading('REMARKS', text="REMARKS", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=140)
    tree.column('#2', stretch=NO, minwidth=0, width=180)
    tree.column('#3', stretch=NO, minwidth=0, width=90)
    tree.column('#4', stretch=NO, minwidth=0, width=100)
    tree.column('#5', stretch=NO, minwidth=0, width=90)
    tree.column('#6', stretch=NO, minwidth=0, width=90)
    tree.column('#7', stretch=NO, minwidth=0, width=90)
    tree.column('#8', stretch=NO, minwidth=0, width=90)
    tree.column('#9', stretch=NO, minwidth=0, width=90)
    tree.column('#10', stretch=NO, minwidth=0, width=140)
    tree.pack()

# ================================  VARIABLES   ================================
USERNAME = StringVar()
PASSWORD = StringVar()
# ================================   FRAMES     ================================
topFrame = Frame(root)
topFrame.pack(side=TOP)
form = Frame(root, height=350, width=200, relief = "groove", bd = 10, padx = 10, pady = 10)
form.pack(side=TOP)
# ================================   FONTS      ================================
Title_Font = Font(
    family="Tahoma",
    size=17,
    weight="normal",
    slant="roman",
    underline=0,
    overstrike=0)
Sub_titleFont = Font(
    family="Helvetica",
    size=12,
    weight="normal",
    slant="roman",
    underline=0,
    overstrike=0)

title = Label(topFrame, text="Student GRADING Log-in\n"
                             "PLEASE INPUT LOG-IN CREDENTIALS", font=(Title_Font), fg="black")
title.pack(pady=20)
user_name = Label(form, text="Username:", font=(Sub_titleFont), fg="black", anchor="e", justify=LEFT)
user_name.grid(row=0, sticky="e")
user_name = Label(form, text="Password:", font=(Sub_titleFont), fg="black", anchor="e", justify=LEFT)
user_name.grid(row=2, sticky="e")
input_warning = Label(form)
input_warning.grid(row=3, columnspan=2)

# =============================== ENTRY WIDGETS ================================
username = Entry(form, textvariable=USERNAME, font=(Sub_titleFont))
username.grid(row=0, column=1)
password = Entry(form, textvariable=PASSWORD, show="*", font=(Sub_titleFont))
password.grid(row=2, column=1, pady=10)
# =============================== BUTTON WIDGETS ===============================
log_in = Button(form, text="Login", font=(Sub_titleFont), width=30, command=Action)
log_in.grid(pady=10, row=4, columnspan=2)
log_in.bind('<Return>', Action)
root.mainloop()