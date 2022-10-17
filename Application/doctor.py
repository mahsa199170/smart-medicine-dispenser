# pylint: disable=W0614
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=wildcard-import
# pylint: disable=too-many-instance-attributes
# pylint: disable=attribute-defined-outside-init
# pylint: disable=consider-using-enumerate
# pylint: disable=too-many-statements
# pylint: disable=global-statement
# pylint: disable=bare-except
# pylint: disable=too-many-public-methods
# pylint: disable=cell-var-from-loop
# pylint: disable=unreachable
# pylint: disable=too-many-branches

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import strftime, sleep
from datetime import datetime, date
import socket
from threading import Thread
from tkcalendar import DateEntry
from email_validator import validate_email, EmailNotValidError
from PIL import ImageTk, Image
from windows import LOGIN_WINDOW, DOCTOR_WINDOW
from database import *
from notify import notify

def send_msg(send_string):

    print(send_string)
    sleep(5)
    return #"""Need to remove this return after successfully integrating with SMD32 module"""
    ip_addr = "127.0.0.1"
    port = 4455
    addr = (ip_addr, port)
    #size = 1024
    fmt = "utf-8"

    #""" TCP Socket """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)

    #""" Recv data """
    #"""client.recv(size).decode(fmt)"""

    #""" Send data """
    client.send(send_string.encode(fmt))

    #""" Close connection """
    client.close()

class DoctorPage():
    def __init__(self):

        self.master = DOCTOR_WINDOW
        self.master.title("Smart Medicine Dispenser")
        self.master.geometry("330x100")
        self.master.resizable(0, 0)
        self.master.configure(bg="#081E1A")
        self.edit_window = None

        self.doctor_dashboard()
        self.trigger_notification()

    def doctor_dashboard(self):

        self.head = Label(self.master, text="  Doctor's Dashboard", font=("Algerian", 20, "bold"),
                          bg='#081E1A', fg='white')
        self.head.place(x=0, y=30)
        # create menubar

        self.dr_menu = Menu(self.master)  #we want to put this menue in root
        self.master.config(menu=self.dr_menu) # this is just telling tkinter: use my menu as menu
        # create a menu items
        self.reg_menu = Menu(self.dr_menu, tearoff=False)  # this is main menu
        self.dr_menu.add_cascade(label="Register", menu=self.reg_menu)  # this is the submenu
        self.reg_menu.add_command(label="Register", command=self.registration)

        #create view appointment item
        self.view_menu = Menu(self.dr_menu, tearoff=False)
        self.dr_menu.add_cascade(label="View Appointment", menu=self.view_menu)

        for i in range(NUM_OF_USERS_SUPPORTED):
            if len(USERS_DB[i]) != 0:
                self.view_menu.add_command(label=USERS_DB[i]["Name"], command=lambda
                    name=USERS_DB[i]["Name"]: self.view(name))

        #create edit item
        self.edit_menu = Menu(self.dr_menu, tearoff=False)
        self.dr_menu.add_cascade(label="Edit", menu=self.edit_menu)  # this is the submenu

        for i in range(NUM_OF_USERS_SUPPORTED):
            if len(USERS_DB[i]) != 0:
                self.edit_menu.add_command(label=USERS_DB[i]["Name"], command=lambda
                    name=USERS_DB[i]["Name"]: self.edit(name))

        # create logout item
        self.log_menu = Menu(self.dr_menu, tearoff=False)
        self.dr_menu.add_cascade(label="Log Out", menu=self.log_menu)
        self.log_menu.add_command(label="Log Out", command=self.logout)

        #click command
    def registration(self):
        self.register_patient()

    def view(self, name):
        for index in range(NUM_OF_USERS_SUPPORTED):
            if USERS_DB[index]["Name"] == name:
                break

        self.app = Toplevel()
        self.app.title("Smart Medicine Dispenser")
        self.app.geometry("400x300")
        self.app.configure(bg="#081E1A")
        self.app.resizable(0, 0)

        self.current_appointment = Label(self.app, text="Current Appointment", font=("Bold", 20),
                                         bg="#081E1A", fg="white")
        self.current_appointment.place(x=50, y=10)

        self.appointment_date = Label(self.app, text=APPOINTMENT_DB[index], font=("Bold", 20),
                                      bg="#081E1A", fg="white")
        self.appointment_date.place(x=70, y=50)

        self.calender = DateEntry(self.app, background="#081E1A", foreground="white", bd=2,
                                  state="readonly")
        self.calender.place(x=50, y=100, width="100")

        self.hour_select = Spinbox(self.app, from_=1, to=12, bg="#081E1A", fg="white", width=4)
        self.hour_select.place(x=200, y=100)

        self.min_select = Spinbox(self.app, width=4, values=("00", "15", "30", "45"), bg="#081E1A",
                                  fg="white")
        self.min_select.place(x=250, y=100)

        self.p_select = Spinbox(self.app, width=4, values=("AM", "PM"), bg="#081E1A", fg="white")
        self.p_select.place(x=300, y=100)

        self.book = Button(self.app, text="Book", activebackground="dark green", bg="#ADD8E6",
                           command=lambda: self.book_appointment(index))
        self.book.place(x=150, y=150)

        self.error = Label(self.app, fg="red", bg="#081E1A")
        self.error.place(x=50, y=180)

    def book_appointment(self, index):

        self.error.config(text="")

        tdy = date.today()
        date_e = datetime.strptime(self.calender.get(), "%Y-%m-%d").date()

        if date_e < tdy:
            self.error.config(text="Wrong Appointment Date, it cannot be in past")
            return

        appointment_string = self.calender.get() + "  " + self.hour_select.get() + ":" \
                            + self.min_select.get() + ":" + self.p_select.get()

        notify_string = "True#" + appointment_string

        if APPOINTMENT_DB[index] == appointment_string:
            notify_string = "False#" + APPOINTMENT_DB[index]

        APPOINTMENT_DB[index] = appointment_string
        self.appointment_date.config(text=appointment_string)
        notify(USERS_DB[index]["Name"], USERS_DB[index]["Contact"], USERS_DB[index]["E-Mail"],
               notify_string)


    def edit(self, name):

        for index in range(NUM_OF_USERS_SUPPORTED):
            if USERS_DB[index]["Name"] == name:
                break

        self.edit_entry = True

        self.edit_window = Toplevel()
        self.edit_window.title("Smart Medicine Dispenser")
        self.edit_window.geometry("1920x1080")
        self.edit_window.configure(bg="#081E1A")

        self.background_image = ImageTk.PhotoImage(Image.open("images/doctor.jpg"))
        self.background_image_label = Label(self.edit_window, image=self.background_image)
        self.background_image_label.place(x=-200, y=0)

        self.title = Label(self.edit_window, text="Enter Patient's Registeration Details",
                           font=("Algerian", 32, "bold"), bg='#081E1A', fg='white')
        self.title.place(x=100, y=10)
        self.name = Label(self.edit_window, text="First Name:", font=("Berlin Sans FB", "16"),
                          bg='#081E1A', fg='white')
        self.name.place(x=10, y=100)
        self.lastname = Label(self.edit_window, text="Last Name:", font=("Berlin Sans FB", "16"),
                              bg='#081E1A', fg='white')
        self.lastname.place(x=10, y=140)
        self.gender = Label(self.edit_window, text="Gender:", font=("Berlin Sans FB", "16"),
                            bg='#081E1A', fg='white')
        self.gender.place(x=10, y=180)
        self.contact = Label(self.edit_window, text="Phone Number:", font=("Berlin Sans FB", "16"),
                             bg='#081E1A', fg='white')
        self.contact.place(x=10, y=220)
        self.dob = Label(self.edit_window, text="Date Of Birth:", font=("Berlin Sans FB", "16"),
                         bg='#081E1A', fg='white')
        self.dob.place(x=10, y=260)
        self.address = Label(self.edit_window, text="Address:", font=("Berlin Sans FB", "16"),
                             bg='#081E1A', fg='white')
        self.address.place(x=10, y=300)
        self.email = Label(self.edit_window, text="E-mail Address:", font=("Berlin Sans FB", "16"),
                           bg='#081E1A', fg='white')
        self.email.place(x=10, y=420)
        self.disease = Label(self.edit_window, text="Disease Name:", font=("Berlin Sans FB", "16"),
                             bg='#081E1A', fg='white')
        self.disease.place(x=10, y=460)
        self.medicines = Label(self.edit_window, text="Medicines", font=("Berlin Sans FB", "16"),
                               bg='#081E1A', fg='white')
        self.medicines.place(x=10, y=580)
        self.time_slot1 = Label(self.edit_window, text="  Time Slot 1",
                                font=("Berlin Sans FB", "16"), bg='#081E1A', fg='white')
        self.time_slot1.place(x=160, y=580)
        self.time_slot2 = Label(self.edit_window, text="  Time Slot 2",
                                font=("Berlin Sans FB", "16"), bg='#081E1A', fg='white')
        self.time_slot2.place(x=310, y=580)
        self.time_slot3 = Label(self.edit_window, text="  Time Slot 3",
                                font=("Berlin Sans FB", "16"), bg='#081E1A', fg='white')
        self.time_slot3.place(x=460, y=580)

        self.canvas_doc_button = Canvas(self.edit_window, height=200, width=200, bg="#081E1A")
        self.canvas_doc_button.place(x=625, y=140)

        self.name_e = Entry(self.edit_window)
        self.name_e.insert(END, USERS_DB[index]["Name"])
        self.name_e.place(x=200, y=100, width="300", height="20")

        self.lastname_e = Entry(self.edit_window)
        self.lastname_e.place(x=200, y=140, width="300", height="20")

        self.contact_e = Entry(self.edit_window)
        self.contact_e.insert(END, USERS_DB[index]["Contact"])
        self.contact_e.place(x=200, y=220, width="300", height="20")

        self.email_e = Entry(self.edit_window)
        self.email_e.insert(END, USERS_DB[index]["E-Mail"])
        self.email_e.place(x=200, y=420, width="300", height="20")

        self.medicine_e = [[0 for j in range(NUM_OF_TIME_SLOT_SUPPORTED + 1)] for i in
                           range(NUM_OF_MEDICINE_SLOT_SUPPORTED)]

        for i in range(NUM_OF_MEDICINE_SLOT_SUPPORTED):
            for j in range(NUM_OF_TIME_SLOT_SUPPORTED + 1):
                self.medicine_e[i][j] = Entry(self.edit_window)
                self.medicine_e[i][j].place(x=(150 * (j % 4)), y=(620 + (i * 20)))

        i = 0

        for medicines, time_slots in MEDICINE_DB[index].items():
            j = 1

            if medicines != "NUM_MEDICINES_PRESCRIBED":
                self.medicine_e[i][0].insert(END, medicines)

                for t_s in time_slots:
                    self.medicine_e[i][j].insert(END, t_s)
                    j += 1
                i += 1


        self.gender_e = ttk.Combobox(self.edit_window, state="readonly")
        self.gender_e['values'] = ('', 'Male', 'Female', 'Other')
        self.gender_e.set(USERS_DB[index]["Gender"])
        self.gender_e.place(x=200, y=180, width="100")

        self.address_e = Text(self.edit_window)
        self.address_e.insert("1.0", USERS_DB[index]["Address"])
        self.address_e.place(x=200, y=300, width="300", height="100")

        self.disease_e = Text(self.edit_window)
        self.disease_e.insert("1.0", USERS_DB[index]["Disease"])
        self.disease_e.place(x=200, y=460, width="300", height="100")

        self.dob_e = DateEntry(self.edit_window, background="#081E1A", foreground="white", bd=2,
                               state="readonly")
        self.dob_e.place(x=200, y=260, width="100")

        self.edit_button = Button(self.edit_window, text="EDIT", activebackground="dark green",
                                  bg="#ADD8E6", command=self.validate_and_register, width="12",
                                  font="Algerian")
        self.edit_button.place(x=640, y=180)

        self.clear = Button(self.edit_window, text="CLEAR", activebackground="dark green",
                            bg="#ADD8E6", command=self.clear_entry, width="12", font="Algerian")
        self.clear.place(x=640, y=240)



    def logout(self):
        self.dr_menu.delete(0, END)
        self.master.withdraw()
        LOGIN_WINDOW.deiconify()

    def register_patient(self):
        self.top = Toplevel()
        self.topm = Toplevel()
        self.topm.withdraw()

        self.top.title("Smart Medicine Dispenser")
        self.top.geometry("1920x1080")

        self.edit_entry = False

        self.background_image = ImageTk.PhotoImage(Image.open("images/doctor.jpg"))
        self.background_image_label = Label(self.top, image=self.background_image)
        self.background_image_label.place(x=-200, y=0)

        self.title = Label(self.top, text="Enter Patient's Registeration Details",
                           font=("Algerian", 32, "bold"), bg='#081E1A', fg='white')
        self.title.place(x=100, y=10)
        self.name = Label(self.top, text="First Name:", font=("Berlin Sans FB", "16"),
                          bg='#081E1A', fg='white')
        self.name.place(x=10, y=100)
        self.lastname = Label(self.top, text="Last Name:", font=("Berlin Sans FB", "16"),
                              bg='#081E1A', fg='white')
        self.lastname.place(x=10, y=140)
        self.gender = Label(self.top, text="Gender:", font=("Berlin Sans FB", "16"), bg='#081E1A',
                            fg='white')
        self.gender.place(x=10, y=180)
        self.contact = Label(self.top, text="Phone Number:", font=("Berlin Sans FB", "16"),
                             bg='#081E1A', fg='white')
        self.contact.place(x=10, y=220)
        self.dob = Label(self.top, text="Date Of Birth:", font=("Berlin Sans FB", "16"),
                         bg='#081E1A', fg='white')
        self.dob.place(x=10, y=260)
        self.address = Label(self.top, text="Address:", font=("Berlin Sans FB", "16"),
                             bg='#081E1A', fg='white')
        self.address.place(x=10, y=300)
        self.email = Label(self.top, text="E-mail Address:", font=("Berlin Sans FB", "16"),
                           bg='#081E1A', fg='white')
        self.email.place(x=10, y=420)
        self.disease = Label(self.top, text="Disease Name:", font=("Berlin Sans FB", "16"),
                             bg='#081E1A', fg='white')
        self.disease.place(x=10, y=460)
        self.medicines = Label(self.top, text="Medicines", font=("Berlin Sans FB", "16"),
                               bg='#081E1A', fg='white')
        self.medicines.place(x=10, y=580)
        self.time_slot1 = Label(self.top, text="  Time Slot 1", font=("Berlin Sans FB", "16"),
                                bg='#081E1A', fg='white')
        self.time_slot1.place(x=160, y=580)
        self.time_slot2 = Label(self.top, text="  Time Slot 2", font=("Berlin Sans FB", "16"),
                                bg='#081E1A', fg='white')
        self.time_slot2.place(x=310, y=580)
        self.time_slot3 = Label(self.top, text="  Time Slot 3", font=("Berlin Sans FB", "16"),
                                bg='#081E1A', fg='white')
        self.time_slot3.place(x=460, y=580)

        self.canvas_doc_button = Canvas(self.top, height=200, width=200, bg="#081E1A")
        self.canvas_doc_button.place(x=625, y=140)

        self.name_e = Entry(self.top)
        self.name_e.place(x=200, y=100, width="300", height="20")

        self.lastname_e = Entry(self.top)
        self.lastname_e.place(x=200, y=140, width="300", height="20")

        self.contact_e = Entry(self.top)
        self.contact_e.place(x=200, y=220, width="300", height="20")

        self.email_e = Entry(self.top)
        self.email_e.place(x=200, y=420, width="300", height="20")

        self.medicine_e = [[0 for j in range(NUM_OF_TIME_SLOT_SUPPORTED + 1)] for i in
                           range(NUM_OF_MEDICINE_SLOT_SUPPORTED)]

        for i in range(NUM_OF_MEDICINE_SLOT_SUPPORTED):
            for j in range(NUM_OF_TIME_SLOT_SUPPORTED + 1):
                self.medicine_e[i][j] = Entry(self.top)
                self.medicine_e[i][j].place(x=(150 * (j % 4)), y=(620 + (i * 20)))

        self.gender_e = ttk.Combobox(self.top, state="readonly")
        self.gender_e['values'] = ('', 'Male', 'Female', 'Other')
        self.gender_e.place(x=200, y=180, width="100")

        self.address_e = Text(self.top)
        self.address_e.place(x=200, y=300, width="300", height="100")

        self.disease_e = Text(self.top)
        self.disease_e.place(x=200, y=460, width="300", height="100")

        self.dob_e = DateEntry(self.top, background="#081E1A", foreground="white", bd=2,
                               state="readonly")
        self.dob_e.place(x=200, y=260, width="100")

        self.register_button = Button(self.top, text="REGISTER", activebackground="dark green",
                                      bg="#ADD8E6", command=self.validate_and_register, width="12",
                                      font="Algerian")
        self.register_button.place(x=640, y=180)

        self.clear = Button(self.top, text="CLEAR", activebackground="dark green", bg="#ADD8E6",
                            command=self.clear_entry, width="12", font="Algerian")
        self.clear.place(x=640, y=240)


    def validate_and_register(self):
        if self.validate_fields():
            self.register()
            self.top.destroy()
            if (self.edit_window is not None) and self.edit_window.winfo_exists():
                self.edit_window.destroy()

    def validate_fields(self):
        return_code = True

        if not self.validate_patient_name():
            return_code = False
        elif not self.validate_gender():
            return_code = False
        elif not self.validate_contact():
            return_code = False
        elif not self.validate_date_of_birth():
            return_code = False
        elif not self.validate_address():
            return_code = False
        elif not self.validate_email():
            return_code = False
        elif not self.validate_disease():
            return_code = False
        elif not self.validate_medicine():
            return_code = False
        elif not self.validate_time_slot():
            return_code = False

        return return_code

    def validate_patient_name(self):
        return_code = True

        self.fullname = self.name_e.get() + " " + self.lastname_e.get()

        if self.name_e.get() == "" or self.lastname_e.get() == "":
            messagebox.showerror("Error", "Name Field is Mandatory!!", parent=self.topm)
            return_code = False
        else:
            name = self.fullname.replace(" ", "")

            if name.isalpha():
                return_code = True
            else:
                messagebox.showerror("Error", "Only Alphabets Allowed in Names", parent=self.topm)
                return_code = False

        return return_code

    def validate_gender(self):
        return_code = True

        if self.gender_e.get() == "":
            messagebox.showerror("Error", "Gender Field is Mandatory!!", parent=self.topm)
            return_code = False

        return return_code

    def validate_contact(self):
        return_code = True

        if self.contact_e.get() == "":
            messagebox.showerror("Error", "Contact Field is Mandatory!!", parent=self.topm)
            return_code = False
        elif self.contact_e.get().isdigit():
            return_code = True
        else:
            messagebox.showerror("Error", "Only Numbers Allowed", parent=self.topm)
            return_code = False

        if return_code and len(self.contact_e.get()) != 10:
            messagebox.showerror("Error", "Total Number count should be 10", parent=self.topm)
            return_code = False

        if not self.edit_entry:
            try:
                if any(d['Password'] == self.contact_e.get() for d in LOGIN_DB):
                    messagebox.showerror("Error", "Contact Already Registered!!", parent=self.topm)
                    return_code = False
            except:
                pass

        return return_code

    def validate_date_of_birth(self):
        return_code = True
        today = date.today()
        date_e = datetime.strptime(self.dob_e.get(), "%Y-%m-%d").date()

        if date_e > today:
            messagebox.showerror("Error", "Date of Birth cannot be in future", parent=self.topm)
            return_code = False

        return return_code

    def validate_address(self):
        return_code = True

        if self.address_e.get("1.0", END).isspace():
            messagebox.showerror("Error", "Address Field is Mandatory!!", parent=self.topm)
            return_code = False

        return return_code

    def validate_email(self):
        return_code = True

        if self.email_e.get() == "":
            messagebox.showerror("Error", "E-Mail Field is Mandatory!!", parent=self.topm)
            return False

        try:
            validate_email(self.email_e.get())  # validate and get info
            #email = val["email"]  # replace with normalized form
            return_code = True
        except EmailNotValidError:
            messagebox.showerror("Error", "E-Mail is Invalid!!", parent=self.topm)
            return_code = False

        if not self.edit_entry:
            try:
                if any(d['Username'] == self.email_e.get() for d in LOGIN_DB):
                    messagebox.showerror("Error", "Email Already Registered!!", parent=self.topm)
                    return_code = False
            except:
                pass

        return return_code

    def validate_disease(self):
        return_code = True

        if self.disease_e.get("1.0", END).isspace():
            messagebox.showerror("Error", "Disease Field is Mandatory!!", parent=self.topm)
            return_code = False

        return return_code

    def validate_medicine(self):
        return_code = False

        for i in range(NUM_OF_MEDICINE_SLOT_SUPPORTED):
            if self.medicine_e[i][0].get() != "":
                return_code = True
                break

        if not return_code:
            messagebox.showerror("Error", "Atleast 1 Medicine Needs to be Prescribed!!",
                                 parent=self.topm)

        return return_code

    def validate_time_slot(self):
        return_code = False
        entry_found = False

        for i in range(NUM_OF_MEDICINE_SLOT_SUPPORTED):
            for j in range(NUM_OF_TIME_SLOT_SUPPORTED):
                if self.medicine_e[i][j+1].get() != "":
                    entry_found = True
                    try:
                        datetime.strptime(self.medicine_e[i][j+1].get(), "%I:%M %p")
                        return_code = True
                    except ValueError:
                        messagebox.showerror("Error", "Wrong Format, Expected Hours:Minutes AM/PM",
                                             parent=self.topm)
                        return_code = False
                        break

        if not entry_found:
            messagebox.showerror("Error", "Atleast 1 Time Slot Needs to be Allocated!!",
                                 parent=self.topm)

        return return_code

    def register(self):

        users_dict_value_list = []
        users_dict_value_list.insert(0, self.fullname)
        users_dict_value_list.append(self.gender_e.get())
        users_dict_value_list.append(self.contact_e.get())
        users_dict_value_list.append(self.dob_e.get())
        users_dict_value_list.append(self.address_e.get("1.0", END))
        users_dict_value_list.append(self.email_e.get())
        users_dict_value_list.append(self.disease_e.get("1.0", END))

        num_of_medicine = 0
        temp_users_db = {}
        temp_medicine_db = {}
        temp_time_slot_list = []
        temp_login_db = {}

        for k, j in zip(USERS_DICT_KEY_LIST, users_dict_value_list):
            temp_users_db[k] = j

        for i in range(NUM_OF_MEDICINE_SLOT_SUPPORTED):

            time_slot_index = 0
            temp_time_slot_list.clear()

            if self.medicine_e[i][0].get() != "":
                num_of_medicine += 1

                for j in range(NUM_OF_TIME_SLOT_SUPPORTED):

                    if self.medicine_e[i][j+1].get() != "":
                        temp_time_slot_list.insert(time_slot_index, self.medicine_e[i][j+1].get())
                        time_slot_index += 1
#                    else:
#                        break

                temp_time_slot_list.sort()
                temp_time_slot_tupple = tuple(temp_time_slot_list)
                temp_medicine_db[self.medicine_e[i][0].get()] = temp_time_slot_tupple

#            else:
#                break

        temp_medicine_db["NUM_MEDICINES_PRESCRIBED"] = num_of_medicine

        temp_login_db["Username"] = self.email_e.get()
        temp_login_db["Password"] = self.contact_e.get()

        if self.edit_entry:
            for i in range(NUM_OF_USERS_SUPPORTED):
                if USERS_DB[i]["Name"] == self.fullname:
                    MEDICINE_DB[i] = temp_medicine_db
                    USERS_DB[i] = temp_users_db
                    LOGIN_DB[i] = temp_login_db
                    break

        else:


            global USER_NUM

            MEDICINE_DB[USER_NUM] = temp_medicine_db
            USERS_DB[USER_NUM] = temp_users_db
            LOGIN_DB[USER_NUM] = temp_login_db

            USER_NUM += 1

        messagebox.showinfo("Info", "Patient "+ self.fullname +" successfully Registered!!",
                            parent=self.topm)


        date_e = date.today()

        for i in range(NUM_OF_MEDICINE_SLOT_SUPPORTED):

            send_string = ""

            if self.edit_entry:
                send_string = "2 "
            else:
                send_string = "1 "

            if self.medicine_e[i][0].get() == "":
                continue

            time_e = datetime.strptime(self.medicine_e[i][1].get(), '%I:%M %p')
            send_string += date_e.strftime('%d%m%Y') + " " + time_e.strftime("%I%M") + " " \
                           + str(i) + " " + self.medicine_e[i][0].get()

            Thread(target=send_msg, args=(send_string,)).start()

        self.doctor_dashboard()
        self.clear_entry()

    def clear_entry(self):
        self.name_e.delete(0, 'end')
        self.lastname_e.delete(0, 'end')
        self.gender_e.set("")
        self.contact_e.delete(0, 'end')
        self.dob_e.delete(0, END)
        self.address_e.delete("1.0", END)
        self.email_e.delete(0, 'end')
        self.disease_e.delete("1.0", END)

        for i in range(NUM_OF_MEDICINE_SLOT_SUPPORTED):
            for j in range(NUM_OF_TIME_SLOT_SUPPORTED + 1):
                self.medicine_e[i][j].delete(0, 'end')

    def trigger_notification(self):
        string = strftime('%I:%M:%S %p')
        for i in range(NUM_OF_USERS_SUPPORTED):
            for medicines, time_slots in MEDICINE_DB[i].items():
                if medicines != "NUM_MEDICINES_PRESCRIBED":
                    for t_s in time_slots:
                        time = datetime.strptime(t_s, '%I:%M %p')
                        time = time.strftime('%I:%M:%S %p')
                        if string == time:
                            notify(USERS_DB[i]["Name"], USERS_DB[i]["Contact"],
                                   USERS_DB[i]["E-Mail"], "")
                            break
                        break

        LOGIN_WINDOW.after(990, self.trigger_notification)
