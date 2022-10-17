# pylint: disable=W0614
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=wildcard-import
# pylint: disable=too-many-instance-attributes

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from windows import LOGIN_WINDOW, PATIENT_WINDOW, DOCTOR_WINDOW
from database import *
from doctor  import DoctorPage
from patient import PatientPage

class LoginPage():

    def __init__(self):
        self.root = LOGIN_WINDOW
        self.username = None
        self.img = None
        self.password = None
        self.entry_slots = None
        self.info_label = Label()
        self.role = None
        self.conn = None

        self.root.title("Smart Medicine Dispenser")

        self.root.geometry("1200x700")

        self.root.resizable(False, False)

        self.img = ImageTk.PhotoImage(Image.open("images/mainframe.jpg"))

        self.login_page()

    def clear_info_label(self):
        if self.info_label.place_info():
            self.info_label.place_forget()

    def set_info_label(self, frame, text):
        self.info_label = Label(frame, text=text, font=('optima', 14), fg="red",
                                bg="white")
        self.info_label.place(x=55, y=80)


    def login_page(self):

        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=0, y=0, height=700, width=1200)

        Label(login_frame, image=self.img).place(x=0, y=0, width=1200, height=700)

        self.entry_slots = Frame(login_frame, bg='white')
        self.entry_slots.place(x=480, y=130, height=450, width=650)
        self.title = Label(self.entry_slots, text="Smart Medicine Dispenser Login System",
                           font=('optima', 20, 'bold'), fg='black', bg='white')
        self.title.place(x=20, y=20)

        self.slot1 = Label(self.entry_slots, text="Username/Email", font=('optima', 20, 'bold'),
                           fg='orangered', bg='white')
        self.slot1.place(x=55, y=110)

        self.slot2 = Label(self.entry_slots, text="Password", font=('optima', 20, 'bold'),
                           fg='orangered', bg='white')
        self.slot2.place(x=55, y=210)

        self.username = Entry(self.entry_slots, font=('times new roman', 15, 'bold'),
                              bg='lightgray')
        self.username.place(x=55, y=145, width=300, height=35)

        self.password = Entry(self.entry_slots, font=('times new roman', 15, 'bold'),
                              bg='lightgray', show="*")
        self.password.place(x=55, y=245, width=300, height=35)

        login_button = Button(self.entry_slots, command=self.login, text="LOGIN HERE", fg="black",
                              bg="#ff884d", font=('times new roman', 20, 'bold'))
        login_button.place(x=80, y=320)

        self.role = ttk.Combobox(self.entry_slots, width="10", values=("Doctor", "Patient"),
                                 background='white')
        self.role.place(x=380, y=80)


    def login(self):

        if self.username.get() == "" or self.password.get() == "":
            self.clear_info_label()
            self.set_info_label(self.entry_slots, "Empty username or password!")
        elif self.role.get() == "":
            self.clear_info_label()
            self.set_info_label(self.entry_slots, "Choose your role!")
        else:
            if self.role.get() == "Doctor":
                self.doctor_validation()
            else:
                self.patient_validation()

    def login_entry_clear(self):
        self.username.delete(0, END)
        self.password.delete(0, END)

    def doctor_validation(self):
        self.clear_info_label()

        if self.username.get().upper() == "ADMIN" and self.password.get().upper() == "ADMIN":
            self.login_entry_clear()

            DoctorPage()
            self.root.withdraw()
            DOCTOR_WINDOW.deiconify()

        else:
            self.set_info_label(self.entry_slots, "Wrong username or password!")

    def patient_validation(self):
        self.clear_info_label()

        for index in range(NUM_OF_USERS_SUPPORTED):

            if len(LOGIN_DB[index]) != 0 and self.username.get() == LOGIN_DB[index]["Username"] and\
               self.password.get() == LOGIN_DB[index]["Password"]:
                self.login_entry_clear()

                PatientPage(index)
                self.root.withdraw()
                PATIENT_WINDOW.deiconify()
                break

            if (index + 1) == len(LOGIN_DB):
                self.set_info_label(self.entry_slots, "Wrong username or password!")
