# pylint: disable=W0614
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=wildcard-import
# pylint: disable=too-many-instance-attributes
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate

from tkinter import *
from time import strftime
from datetime import datetime, date
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from windows import LOGIN_WINDOW, PATIENT_WINDOW
from database import *

PATIENT_BG = "#E6C9A8"

class PatientPage():
    def __init__(self, index):

        self.master = PATIENT_WINDOW
        self.master.title("Smart Medicine Dispenser")
        self.master.geometry("310x100")
        self.master.resizable(0, 0)
        self.master.configure(bg=PATIENT_BG)
        self.index = index

        self.patient_dashboard()

    def patient_dashboard(self):

        #self.backGround_image = ImageTk.PhotoImage(Image.open("images/patient.jpg"))
        #self.backGround_imageLabel = Label(self.master, image=self.backGround_image)
        #self.backGround_imageLabel.place(x=-600, y=0)
        self.head = Label(self.master, text="Patient's Dashboard", font=("Algerian", 20, "bold"),
                          bg=PATIENT_BG, fg='black')
        self.head.place(x=0, y=30)

        # create menubar

        self.pat_menu = Menu(self.master)  # we want to put this menue in root
        self.master.config(menu=self.pat_menu)  # this is just telling tkinter: use my menu as menu
        # create appointment item
        self.app_menu = Menu(self.pat_menu, tearoff=False)  # this is main menu
        self.pat_menu.add_cascade(label="Book an appointment", menu=self.app_menu) # submenu
        self.app_menu.add_command(label="Book an appointment", command=self.appointment)
        # self.reg_menu.add_separator()
        # self.reg_menu.add_command(label="Exit window", command=self.master.quit)

        # create view item
        self.view_menu = Menu(self.pat_menu, tearoff=False)
        self.pat_menu.add_cascade(label="View", menu=self.view_menu)  # this is the submenu
        self.view_menu.add_command(label="View", command=self.view)


        # create logout item
        self.log_menu = Menu(self.pat_menu, tearoff=False)
        self.pat_menu.add_cascade(label="Log Out", menu=self.log_menu)
        self.log_menu.add_command(label="Log Out", command=self.logout)

        # click command

    def appointment(self):

        self.app = Toplevel()
        self.app.title("Smart Medicine Dispenser")
        self.app.geometry("400x300")
        self.app.configure(bg=PATIENT_BG)
        self.app.resizable(0, 0)

        self.current_appointment = Label(self.app, text="Current Appointment", font=("Bold", 20),
                                         bg=PATIENT_BG, fg="black")
        self.current_appointment.place(x=50, y=10)

        self.appointment_date = Label(self.app, text=APPOINTMENT_DB[self.index], font=("Bold", 20),
                                      bg=PATIENT_BG, fg="black")
        self.appointment_date.place(x=70, y=50)

        self.calender = DateEntry(self.app, background=PATIENT_BG, foreground="black", bd=2,
                                  state="readonly")
        self.calender.place(x=50, y=100, width="100")

        self.hour_select = Spinbox(self.app, from_=1, to=12, bg=PATIENT_BG, width=4)
        self.hour_select.place(x=200, y=100)

        self.min_select = Spinbox(self.app, width=4, values=("00", "15", "30", "45"), bg=PATIENT_BG)
        self.min_select.place(x=250, y=100)

        self.p_select = Spinbox(self.app, width=4, values=("AM", "PM"), bg=PATIENT_BG)
        self.p_select.place(x=300, y=100)

        self.book = Button(self.app, text="Book", activebackground="khaki1", bg="white",
                           command=self.book_appointment)
        self.book.place(x=150, y=150)

        self.error = Label(self.app, fg="red", bg=PATIENT_BG)
        self.error.place(x=50, y=180)

    def book_appointment(self):

        self.error.config(text="")

        today = date.today()
        date_e = datetime.strptime(self.calender.get(), "%Y-%m-%d").date()

        if date_e < today:
            self.error.config(text="Appointment Date cannot be in past")
            return


        appointment_string = self.calender.get() + "  " + self.hour_select.get() + ":" \
                            + self.min_select.get() + ":" + self.p_select.get()
        APPOINTMENT_DB[self.index] = appointment_string
        self.appointment_date.config(text=appointment_string)

    def view(self):

        self.top = Toplevel()
        self.top.title("Smart Medicine Dispenser")
        self.top.geometry("1920x1080")
        self.top.configure(background=PATIENT_BG)

        self.canvas_img = Canvas(self.top, height=1000, width=990, bg=PATIENT_BG)
        self.canvas_img.place(x=900, y=0)

        self.canvas_pat = Canvas(self.top, height=1000, width=900, bg=PATIENT_BG)
        self.canvas_pat.place(x=0, y=0)


        self.background_image = ImageTk.PhotoImage(Image.open("images/patient.jpg"))
        self.background_image_label = Label(self.canvas_img, image=self.background_image)
        self.background_image_label.place(x=-700, y=0)

        self.title = Label(self.canvas_pat, text="Patient Information", font=("Bold", 40),
                           bg=PATIENT_BG, fg="black")
        self.title.place(x=200, y=10)

        self.user_id = Label(self.canvas_pat, text="Patient ID: ", font=("Bold"), bg=PATIENT_BG,
                             fg="black")
        self.user_id.place(x=20, y=100)

        self.user_id_value = Label(self.canvas_pat, text=(self.index + 1), bg=PATIENT_BG,
                                   fg="black")
        self.user_id_value.place(x=200, y=100)


        for k in range(len(USERS_DICT_KEY_LIST)):
            self.key = Label(self.canvas_pat, text=USERS_DICT_KEY_LIST[k] + ": ", font=("Bold"),
                             bg=PATIENT_BG, fg="black")
            self.key.place(x=20, y=(150+(50*k)))
            self.value = Label(self.canvas_pat, text=USERS_DB[self.index][USERS_DICT_KEY_LIST[k]],
                               bg=PATIENT_BG, fg="black")
            self.value.place(x=200, y=(150+(50*k)))

        self.medicines = Label(self.canvas_pat, text="Medicines", font=("Bold"), bg=PATIENT_BG,
                               fg="black")
        self.medicines.place(x=20, y=600)
        self.time_slot1 = Label(self.canvas_pat, text="Time Slot 1", font=("Bold"), bg=PATIENT_BG,
                                fg="black")
        self.time_slot1.place(x=150, y=600)
        self.time_slot2 = Label(self.canvas_pat, text="Time Slot 2", font=("Bold"), bg=PATIENT_BG,
                                fg="black")
        self.time_slot2.place(x=300, y=600)
        self.time_slot3 = Label(self.canvas_pat, text="Time Slot 3", font=("Bold"), bg=PATIENT_BG,
                                fg="black")
        self.time_slot3.place(x=450, y=600)

        i = 0

        for medicines, time_slots in MEDICINE_DB[self.index].items():
            j = 1

            if medicines != "NUM_MEDICINES_PRESCRIBED":
                self.medicine = Label(self.canvas_pat, text=medicines, bg=PATIENT_BG, fg="black")
                self.medicine.place(x=20, y=(625+(i*25)))

                for t_s in time_slots:
                    self.time_slots = Label(self.canvas_pat, text=t_s, bg=PATIENT_BG, fg="black")
                    self.time_slots.place(x=(150*(j%4)), y=(625+(i*25)))
                    j += 1

                i += 1


        self.timetitle = Label(self.canvas_pat, text="Current Time: ", font=("Bold"), bg=PATIENT_BG,
                               fg="black")
        self.timetitle.place(x=600, y=100)

        self.current_time_label = Label(self.canvas_pat, bg=PATIENT_BG, fg="black")
        self.current_time_label.place(x=720, y=100)

        self.current_time()

    def current_time(self):
        string = strftime('%I:%M:%S %p')
        self.current_time_label.config(text=string, font=("Bold"))
        self.current_time_label.after(1000, self.current_time)


    def logout(self):
        self.pat_menu.delete(0, END)
        self.master.withdraw()
        LOGIN_WINDOW.deiconify()
