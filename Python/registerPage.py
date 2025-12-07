import tkinter as tk
from tkinter import ttk
import sqlHelperFunctions as sql
import mysql.connector.errors as sqlerrors
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

        self.errortxt = ttk.Label(self, text ="")
        self.errortxt.grid(row = 6, column = 0, columnspan=3)

        self.submit = ttk.Button(self, text = "Submit", command=self.submitPress)
        self.submit.grid(row = 7, column = 0, padx = 10, pady = 10, columnspan=2)

        self.submit = ttk.Button(self, text = "Login Instead", command=self.swapLogin)
        self.submit.grid(row = 8, column = 0, padx = 10, pady = 10, columnspan=2)

    def load(self, teamid=0, pokeid=0):
        self.email.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.name.delete(0, tk.END)
        self.errortxt['text'] = ''

    def submitPress(self):
        try:
            name = self.name.get()
            email = self.email.get()
            password = self.password.get()
            if name == '':
                self.errortxt['text'] = "Name can't be blank"
                return
            if '@' not in email:
                self.errortxt['text'] = "Invalid Email Address"
                return
            if password == '':
                self.errortxt['text'] = "Password can't be blank"
                return
            self.control.session = sql.register(self.control.cursor, name, email, password)
            self.control.show_frame(homePage.HomePage)
        except sqlerrors.IntegrityError as e:
            self.errortxt['text'] = "User Already Exists"
        except Exception as e:
            self.errortxt['text'] = e

    def swapLogin(self):
        self.control.show_frame(loginPage.LoginPage)