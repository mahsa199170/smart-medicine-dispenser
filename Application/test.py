#!/usr/bin/env python3
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

import unittest
from main import *
from login import *
from patient import *
from doctor import *
from windows import*
from database import *

class MyTest(unittest.TestCase):

    def test_main(self):

        gui_main()

        self.assertFalse(LOGIN_WINDOW.winfo_viewable())
        self.assertFalse(DOCTOR_WINDOW.winfo_viewable())
        self.assertFalse(PATIENT_WINDOW.winfo_viewable())

    def test_positive_login_page(self):
        login = LoginPage()
        self.assertEqual(login.title.cget("text"), "Smart Medicine Dispenser Login System")
        self.assertEqual(login.slot1.cget("text"), "Username/Email")
        self.assertEqual(login.slot2.cget("text"), "Password")

        login.username.insert(0, "")
        login.password.insert(0, "")
        login.login()
        self.assertEqual(login.info_label.cget("text"), "Empty username or password!")

        login.username.insert(0, "ADMIN")
        login.password.insert(0, "ADMIN")
        login.login()
        self.assertEqual(login.info_label.cget("text"), "Choose your role!")

        login.role.current(0)
        login.login()
        self.assertEqual(login.username.get(), "")
        self.assertEqual(login.password.get(), "")

        login.username.insert(0, "AfMIN")
        login.password.insert(0, "ADMIN")
        login.login()
        self.assertEqual(login.info_label.cget("text"), "Wrong username or password!")

        login.username.delete(0, END)
        login.password.delete(0, END)

        login.username.insert(0, "ADMIN")
        login.password.insert(0, "ADMIN")
        login.role.current(1)
        login.login()
        self.assertEqual(login.info_label.cget("text"), "Wrong username or password!")

        LOGIN_DB[0]["Username"] = "ADMIN"
        LOGIN_DB[0]["Password"] = "ADMIN"
        login.login()
        self.assertEqual(login.username.get(), "")
        self.assertEqual(login.password.get(), "")

    def test_negative_login_page(self):
        login = LoginPage()
        self.assertFalse(login.title.cget("text") == "Smart Medicine Dispenser")
        self.assertFalse(login.slot1.cget("text") == "Username")
        self.assertFalse(login.slot2.cget("text") == "password")

        login.username.insert(0, "")
        login.password.insert(0, "")
        login.login()
        self.assertFalse(login.info_label.cget("text") == "Empty username or password")

        login.username.insert(0, "ADMIN")
        login.password.insert(0, "ADMIN")
        login.login()
        self.assertFalse(login.info_label.cget("text") == "Choose your role")

        login.role.current(0)
        login.login()
        self.assertFalse(login.username.get(), " ")
        self.assertFalse(login.password.get(), " ")

        login.username.insert(0, "AfMIN")
        login.password.insert(0, "ADMIN")
        login.login()
        self.assertFalse(login.info_label.cget("text") == "Wrong username or password")

        login.username.delete(0, END)
        login.password.delete(0, END)

        login.username.insert(0, "ADMIN")
        login.password.insert(0, "ADMIN")
        login.role.current(1)
        login.login()
        self.assertFalse(login.info_label.cget("text") == "Wrong username or password")

        LOGIN_DB[0]["Username"] = "ADMIN"
        LOGIN_DB[0]["Password"] = "ADMIN"
        login.login()
        self.assertFalse(login.username.get(), " ")
        self.assertFalse(login.password.get(), " ")

    def test_positive_doctor_page(self):
        MEDICINE_DB[0] = {}
        MEDICINE_DB[1] = {}
        USERS_DB[0] = {"Name": "ABC", "Gender": "Male", "Contact": "9888888575", \
                       "Date of Birth": "26", "Address": "ABC", "E-Mail": "XYZ", "Disease": "QWE"}

        doctor = DoctorPage()
        self.assertEqual(doctor.head.cget("text"), "  Doctor's Dashboard")
        self.assertEqual(doctor.reg_menu.entrycget(0, "label"), "Register")
        self.assertEqual(doctor.log_menu.entrycget(0, "label"), "Log Out")

        doctor.view("ABC")
        doctor.edit("ABC")
        doctor.logout()
        doctor.registration()

        self.assertEqual(doctor.title.cget("text"), "Enter Patient's Registeration Details")
        self.assertEqual(doctor.name.cget("text"), "First Name:")
        self.assertEqual(doctor.lastname.cget("text"), "Last Name:")
        self.assertEqual(doctor.gender.cget("text"), "Gender:")
        self.assertEqual(doctor.contact.cget("text"), "Phone Number:")
        self.assertEqual(doctor.dob.cget("text"), "Date Of Birth:")
        self.assertEqual(doctor.address.cget("text"), "Address:")
        self.assertEqual(doctor.email.cget("text"), "E-mail Address:")
        self.assertEqual(doctor.disease.cget("text"), "Disease Name:")
        self.assertEqual(doctor.medicines.cget("text"), "Medicines")
        self.assertEqual(doctor.time_slot1.cget("text"), "  Time Slot 1")
        self.assertEqual(doctor.time_slot2.cget("text"), "  Time Slot 2")
        self.assertEqual(doctor.time_slot3.cget("text"), "  Time Slot 3")

        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "9888888575")
        doctor.address_e.insert("1.0", "Hello")
        doctor.email_e.insert(0, "abc@gmail.com")
        doctor.disease_e.insert("1.0", "ABC")
        doctor.medicine_e[0][0].insert(0, "Arostate")
        doctor.medicine_e[0][1].insert(0, "10:00 PM")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()

    def test_negative_doctor_page(self):
        MEDICINE_DB[0] = {}
        MEDICINE_DB[1] = {}
        USERS_DB[0] = {"Name": "ABC", "Gender": "Male", "Contact": "9888888575", \
                       "Date of Birth": "26", "Address": "ABC", "E-Mail": "XYZ", "Disease": "QWE"}

        doctor = DoctorPage()
        self.assertEqual(doctor.head.cget("text"), "  Doctor's Dashboard")

        doctor.view("ABC")
        doctor.edit("ABC")
        doctor.logout()
        doctor.registration()

        doctor.name_e.insert(0, "Mukul1")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "")
        doctor.lastname_e.insert(0, "")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "asd")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "98888888888")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "9888888575")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "9888888575")
        doctor.address_e.insert("1.0", "Hello")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "9888888575")
        doctor.address_e.insert("1.0", "Hello")
        doctor.email_e.insert(0, "abc@gasdjhmail.com")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "9888888575")
        doctor.address_e.insert("1.0", "Hello")
        doctor.email_e.insert(0, "abc@gmail.com")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "9888888575")
        doctor.address_e.insert("1.0", "Hello")
        doctor.email_e.insert(0, "abc@gmail.com")
        doctor.disease_e.insert("1.0", "ABC")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "9888888575")
        doctor.address_e.insert("1.0", "Hello")
        doctor.email_e.insert(0, "abc@gmail.com")
        doctor.disease_e.insert("1.0", "ABC")
        doctor.medicine_e[0][0].insert(0, "Arostate")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "9888888575")
        doctor.address_e.insert("1.0", "Hello")
        doctor.email_e.insert(0, "abc@gmail.com")
        doctor.disease_e.insert("1.0", "ABC")
        doctor.medicine_e[0][0].insert(0, "Arostate")
        doctor.medicine_e[0][1].insert(0, "10:00")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

        doctor.topm = Toplevel()
        dte = date(2023, 8, 19)
        doctor.dob_e.set_date(dte)
        doctor.name_e.insert(0, "Mukul")
        doctor.lastname_e.insert(0, "Taneja")
        doctor.gender_e.set("Male")
        doctor.contact_e.insert(0, "9888888575")
        doctor.topm.after(2000, doctor.topm.destroy)
        doctor.validate_and_register()
        doctor.clear_entry()

    def test_positive_patient_page(self):
        patient = PatientPage(0)
        self.assertEqual(patient.head.cget("text"), "Patient's Dashboard")
        self.assertEqual(patient.app_menu.entrycget(0, "label"), "Book an appointment")
        self.assertEqual(patient.view_menu.entrycget(0, "label"), "View")
        self.assertEqual(patient.log_menu.entrycget(0, "label"), "Log Out")

        patient.appointment()
        self.assertEqual(patient.current_appointment.cget("text"), "Current Appointment")
        self.assertEqual(patient.appointment_date.cget("text"), "")

        patient.book_appointment()
        self.assertEqual(patient.appointment_date.cget("text"), APPOINTMENT_DB[0])

        dte = date(2021, 8, 19)
        patient.calender.set_date(dte)
        patient.book_appointment()
        self.assertEqual(patient.error.cget("text"), "Appointment Date cannot be in past")

        USERS_DB[0] = {"Name": "ABC", "Gender": "Male", "Contact": "9888888575", \
                       "Date of Birth": "26", "Address": "ABC", "E-Mail": "XYZ", "Disease": "QWE"}
        MEDICINE_DB[0] = {"Arostat":"10:30 PM"}
        patient.view()

        self.assertEqual(patient.title.cget("text"), "Patient Information")
        self.assertEqual(patient.user_id.cget("text"), "Patient ID: ")
        self.assertEqual(patient.user_id_value.cget("text"), 1)
        self.assertEqual(patient.medicines.cget("text"), "Medicines")
        self.assertEqual(patient.time_slot1.cget("text"), "Time Slot 1")
        self.assertEqual(patient.time_slot2.cget("text"), "Time Slot 2")
        self.assertEqual(patient.time_slot3.cget("text"), "Time Slot 3")
        self.assertEqual(patient.timetitle.cget("text"), "Current Time: ")

        patient.current_time()

        string = strftime('%I:%M:%S %p')
        self.assertEqual(patient.current_time_label.cget("text"), string)

        patient.logout()

    def test_negative_patient_page(self):
        patient = PatientPage(1)
        self.assertFalse(patient.head.cget("text") == "Patient Dashboard")
        self.assertFalse(patient.app_menu.entrycget(0, "label") == "Book appointment")
        self.assertFalse(patient.view_menu.entrycget(0, "label") == "view")
        self.assertFalse(patient.log_menu.entrycget(0, "label") == "LogOut")

        patient.appointment()
        self.assertFalse(patient.current_appointment.cget("text") == "Current appointment")
        self.assertFalse(patient.appointment_date.cget("text") == " ")

        patient.book_appointment()
        self.assertFalse(patient.appointment_date.cget("text") == "")

        dte = date(2021, 8, 19)
        patient.calender.set_date(dte)
        patient.book_appointment()
        self.assertFalse(patient.error.cget("text") == "Appointment Date cannot be in the past")

        USERS_DB[1] = {"Name": "ABC", "Gender": "Male", "Contact": "9888888575",\
                       "Date of Birth": "26", "Address": "ABC", "E-Mail": "XYZ", "Disease": "QWE"}
        MEDICINE_DB[1] = {"Arostat":"10:30 PM"}
        patient.view()

        self.assertFalse(patient.title.cget("text") == "Doctor Information")
        self.assertFalse(patient.user_id.cget("text") == "Doctor ID: ")
        self.assertFalse(patient.user_id_value.cget("text") == 1)
        self.assertFalse(patient.medicines.cget("text") == "Prescription")
        self.assertFalse(patient.time_slot1.cget("text") == "Time Slot 3")
        self.assertFalse(patient.time_slot2.cget("text") == "Time Slot 1")
        self.assertFalse(patient.time_slot3.cget("text") == "Time Slot 2")
        self.assertFalse(patient.timetitle.cget("text") == "Time: ")

        patient.current_time()

        string = strftime('%I:%M:%S')
        self.assertFalse(patient.current_time_label.cget("text") == string)

        patient.logout()

if __name__ == '__main__':
    unittest.main()
