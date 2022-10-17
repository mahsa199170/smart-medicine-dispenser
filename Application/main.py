# pylint: disable=W0614
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=wildcard-import

from tkinter import *
from tkinter import messagebox
from windows import *
from login   import LoginPage

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        LOGIN_WINDOW.destroy()

def gui_main():

    DOCTOR_WINDOW.withdraw()
    PATIENT_WINDOW.withdraw()

    LoginPage()

    LOGIN_WINDOW.protocol("WM_DELETE_WINDOW", on_closing)
    DOCTOR_WINDOW.protocol("WM_DELETE_WINDOW", on_closing)
    PATIENT_WINDOW.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == "__main__":

    gui_main()
    LOGIN_WINDOW.mainloop()
