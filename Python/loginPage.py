import tkinter as tk
from tkinter import ttk
import sqlHelperFunctions as sql
import registerPage
import homePage

class LoginPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        self.control = controller

        self.emailLbl = ttk.Label(self, text ="Email:")
        self.emailLbl.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.email = ttk.Entry(self)
        self.email.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.passwordLbl = ttk.Label(self, text ="Password:")
        self.passwordLbl.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.password = ttk.Entry(self)
        self.password.grid(row = 3, column = 1, padx = 10, pady = 10)

        self.submit = ttk.Button(self, text = "Submit", command=self.submitPress)
        self.submit.grid(row = 5, column = 0, padx = 10, pady = 10, columnspan=2)

        self.errortxt = ttk.Label(self, text ="")
        self.errortxt.grid(row = 4, column = 0, columnspan=3)

        self.submit = ttk.Button(self, text = "Register Instead", command=self.swapRegister)
        self.submit.grid(row = 6, column = 0, padx = 10, pady = 10, columnspan=2)

    def load(self, teamid=0, pokeid=0):
        self.email.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.errortxt['text'] = ""

    def submitPress(self):
        try:
            res = sql.login(self.control.cursor, self.email.get(), self.password.get())
            if res == None:
                self.errortxt['text'] = "Invalid Username or Password"
            else: 
                self.control.session = res
                self.control.show_frame(homePage.HomePage)
        except Exception as e:
            self.errortxt['text'] = e

    def swapRegister(self):
        self.control.show_frame(registerPage.RegisterPage)