import tkinter as tk
from tkinter import ttk
import sqlHelperFunctions as sql
import loginPage
import homePage

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        self.control = controller

        self.nameLbl = ttk.Label(self, text ="Username:")
        self.nameLbl.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.name = ttk.Entry(self)
        self.name.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.emailLbl = ttk.Label(self, text ="Email:")
        self.emailLbl.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.email = ttk.Entry(self)
        self.email.grid(row = 3, column = 1, padx = 10, pady = 10)

        self.passwordLbl = ttk.Label(self, text ="Password:")
        self.passwordLbl.grid(row = 4, column = 1, padx = 10, pady = 10)
        self.password = ttk.Entry(self)
        self.password.grid(row = 5, column = 1, padx = 10, pady = 10)

        self.submit = ttk.Button(self, text = "Submit", command=self.submitPress)
        self.submit.grid(row = 6, column = 0, padx = 10, pady = 10, columnspan=2)

        self.submit = ttk.Button(self, text = "Login Instead", command=self.swapLogin)
        self.submit.grid(row = 7, column = 0, padx = 10, pady = 10, columnspan=2)

    def load(self, teamid=0, pokeid=0):
        pass

    def submitPress(self):
        try:
            self.control.session = sql.register(self.control.cursor, self.name.get(), self.email.get(), self.password.get())
            self.control.show_frame(homePage.HomePage)
        except Exception as e:
            print(f"[STD ERROR] {e}")

    def swapLogin(self):
        self.control.show_frame(loginPage.LoginPage)