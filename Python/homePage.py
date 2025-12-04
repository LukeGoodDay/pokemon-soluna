import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import sqlHelperFunctions as sql
from teamPage import TeamPage

class HomePage(tk.Frame):
    teamids = []
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.control = controller

        self.greet = ttk.Label(self, text='Welcome!')
        self.greet.grid(row=0, column=0, padx=10, pady=10)

        self.teamlbl = ttk.Label(self, text='Your Teams:')
        self.teamlbl.grid(row=1, column=0, padx=5, pady=5)

        # Create Combobox
        self.teams = ttk.Combobox(self, values=[])
        self.teams.grid(row=2, column=0, padx=5, pady=5)

        self.new = ttk.Button(self, text="New Team", command=self.create)
        self.new.grid(row=3, column=0, padx=10, pady=10)

        # Bind selection event
        self.teams.bind("<<ComboboxSelected>>", self.select)
    
    def load(self, team=1, pokeid=0):
        name = sql.get_username(self.control.cursor, self.control.session)
        if name is not None:
            self.greet['text'] = f'Welcome {name[0]}!'
        tea = sql.get_user_teams(self.control.cursor, self.control.session)
        self.teams['values'] = [i[2] for i in tea]
        self.teamids = [i[0] for i in tea]

    def create(self, *args):
        name = simpledialog.askstring("Create Team", "What is the name of your team?")
        if name != '' and name is not None:
            sql.new_team(self.control.cursor, self.control.session, name)
            self.load()

    def select(self, *args):
        id = self.teams['values'].index(self.teams.get())
        self.teams.set('')
        teamid = self.teamids[id]
        self.control.show_frame(TeamPage, teamid)
