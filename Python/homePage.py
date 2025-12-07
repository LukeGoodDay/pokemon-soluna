import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import sqlHelperFunctions as sql
import teamPage
import loginPage
import pokedexPage
import statsPage
import wonderTradePage

class HomePage(tk.Frame):
    teamids = []
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.control = controller

        self.greet = ttk.Label(self, text='Welcome!')
        self.greet.grid(row=0, column=0, padx=10, pady=10)

        self.logout = ttk.Button(self, text="Logout", command=self.pressLogout)
        self.logout.grid(row=0, column=1, padx=10, pady=10)

        self.teamlbl = ttk.Label(self, text='Your Teams:')
        self.teamlbl.grid(row=1, column=0, padx=5, pady=5)

        # Create Combobox
        self.teams = ttk.Combobox(self, values=[])
        self.teams.grid(row=2, column=0, padx=5, pady=5)

        self.new = ttk.Button(self, text="New Team", command=self.create)
        self.new.grid(row=3, column=0, padx=10, pady=10)

        self.dex = ttk.Button(self, text="Pokedex", command=self.pokedex)
        self.dex.grid(row=3, column=1, padx=10, pady=10)

        self.stat = ttk.Button(self, text="Statistics", command=self.stats)
        self.stat.grid(row=4, column=0, padx=10, pady=10)

        self.wonder = ttk.Button(self, text="Wonder Trades", command=self.wonderld)
        self.wonder.grid(row=4, column=1, padx=10, pady=10)

        self.errortxt = ttk.Label(self, text ="")
        self.errortxt.grid(row = 5, column = 0, columnspan=3)

        # Bind selection event
        self.teams.bind("<<ComboboxSelected>>", self.select)
    
    def load(self, team=0, pokeid=0):
        if team != 1:
            self.errortxt['text'] = ''
        name = sql.get_username(self.control.cursor, self.control.session)
        if name is not None:
            self.greet['text'] = f'Welcome {name[0]}!'
        tea = sql.get_user_teams(self.control.cursor, self.control.session)
        self.teams['values'] = [i[2] for i in tea]
        self.teamids = [i[0] for i in tea]

    def create(self, *args):
        name = simpledialog.askstring("Create Team", "What is the name of your team?")
        if name != '' and name is not None:
            try:
                sql.new_team(self.control.cursor, self.control.session, name)
                self.load(1)
            except Exception as e:
                self.errortxt['text'] = e
        else:
            self.errortxt['text'] = "Invalid Team Name"
    
    def pokedex(self, *args):
        self.control.show_frame(pokedexPage.PokedexPage, 0)

    def stats(self, *args):
        self.control.show_frame(statsPage.StatsPage, 0)

    def wonderld(self, *args):
        self.control.show_frame(wonderTradePage.WonderTradePage)

    def select(self, *args):
        id = self.teams['values'].index(self.teams.get())
        self.teams.set('')
        teamid = self.teamids[id]
        self.control.show_frame(teamPage.TeamPage, teamid)

    def pressLogout(self):
        sql.logout(self.control.cursor, self.control.session)
        self.control.show_frame(loginPage.LoginPage)
