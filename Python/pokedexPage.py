import tkinter as tk
from tkinter import ttk
import sqlHelperFunctions as sql
import teamPage
import homePage

class PokedexPage(tk.Frame):
    teamid = 0
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        self.control = controller

        self.formlbl = ttk.Label(self, text ="Pokemon Form:")
        self.formlbl.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.form = ttk.Combobox(self, values=[])
        self.form.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.form.bind("<KeyRelease>", self.updateForm)
        self.form.bind("<<ComboboxSelected>>", self.updateForm)

        self.back = ttk.Button(self, text = "Back", command=self.goBack)
        self.back.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.dexnum = ttk.Label(self, text ="Pokedex: #")
        self.dexnum.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.passwordLbl = ttk.Label(self, text ="Password:")
        self.passwordLbl.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.password = ttk.Entry(self)
        self.password.grid(row = 3, column = 1, padx = 10, pady = 10)

    def load(self, teamid=0, pokeid=0):
        self.email.delete(0, tk.END)
        self.password.delete(0, tk.END)

    def submitPress(self):
        try:
            res = sql.login(self.control.cursor, self.email.get(), self.password.get())
            if res == None:
                print("Invalid Username or Password")
            else: 
                self.control.session = res
                self.control.show_frame(homePage.HomePage)
        except Exception as e:
            print(f"[STD ERROR] {e}")

    def goBack(self):
        self.control.show_frame(teamPage.TeamPage)