import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import sqlHelperFunctions as sql
import homePage
import pokeEditPage
import pokedexPage

class TeamPage(tk.Frame): 
    teamid = 0
    pokeids = [0, 0, 0, 0, 0, 0]
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.control = controller
        # adding a label to the root window
        self.name = tk.Label(self, text = "Team Name: ")
        self.name.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        self.labels = []
        self.edits = []
        self.deletes = []
        self.dexs = []
        for i in range(6):
            self.labels.append(tk.Label(self, text = f"Pokemon #{i+1}: Empty"))
            self.edits.append(ttk.Button(self, text="Edit", command= lambda i=i: self.edit(i)))
            self.deletes.append(ttk.Button(self, text="Delete", command= lambda i=i: self.delete(i)))
            self.dexs.append(ttk.Button(self, text="Info", command= lambda i=i: self.dexview(i)))
        self.back = ttk.Button(self, text="Back", command= lambda: self.control.show_frame(homePage.HomePage))
        self.back.grid(row=7, column=0, padx=10, pady=10)
        self.removebutton = ttk.Button(self, text="Delete", command=self.remove)
        self.removebutton.grid(row=7, column=1, padx=10, pady=10)
        self.renamebtn = ttk.Button(self, text="Rename Team", command=self.rename)
        self.renamebtn.grid(row=7, column=2, padx=10, pady=10)

        self.errortxt = ttk.Label(self, text ="")
        self.errortxt.grid(row = 5, column = 0, columnspan=3)
    
    def load(self, teamid, pokeid=0):
        self.teamid = teamid
        teams = sql.get_user_teams(self.control.cursor, self.control.session)
        teamname = ''
        for team in teams:
            if team[0] == teamid:
                teamname = team[2]
                break
        self.name['text'] = f"Team Name: {teamname}"
        if teamname != '':
            pokemons = sql.get_team_pokemon(self.control.cursor, self.control.session, teamid)
            count = len(pokemons)
            for i in range(6):
                if i < count:
                    pokemon = pokemons[i]
                    self.pokeids[i] = pokemon[0]
                    nick = pokemon[2]
                    if nick is None:
                        nick=sql.get_form_details(self.control.cursor, self.control.session, pokemon[1])[3]
                    self.labels[i]['text'] = f"Pokemon #{i}: {nick}"
                    self.labels[i].grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
                    self.edits[i]['text'] = 'Edit'
                    self.edits[i].grid(row=i+1, column=1, padx=5, pady=5)
                    self.deletes[i].grid(row=i+1, column=2, padx=5, pady=5)
                    self.dexs[i].grid(row=i+1, column=3, padx=5, pady=5)
                elif i == count:
                    self.pokeids[i] = 0
                    self.labels[i]['text'] = f"Pokemon #{i}: Empty"
                    self.edits[i]['text'] = 'Create'
                    self.labels[i].grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
                    self.edits[i].grid(row=i+1, column=1, padx=5, pady=5)
                    self.deletes[i].grid_forget()
                    self.dexs[i].grid_forget()
                else:
                    self.pokeids[i] = 0
                    self.labels[i].grid_forget()
                    self.edits[i].grid_forget()
                    self.deletes[i].grid_forget()
                    self.dexs[i].grid_forget()

    def edit(self, i, *args):
        self.control.show_frame(pokeEditPage.PokeEditPage, self.teamid, self.pokeids[i])

    def dexview(self, i, *args):
        self.control.show_frame(pokedexPage.PokedexPage, self.teamid, self.pokeids[i])

    def delete(self, i, *args):
        id = self.pokeids[i]
        if id != 0:
            sql.remove_pokemon(self.control.cursor, self.control.session, id)
            self.load(self.teamid)
    
    def remove(self, *args):
        sql.remove_team(self.control.cursor, self.control.session, self.teamid)
        self.control.show_frame(homePage.HomePage)

    def rename(self, *args):
        name = simpledialog.askstring("Rename Team", "What is the new name of your team?")
        if name != '' and name is not None:
            try:
                sql.update_team_name(self.control.cursor, self.control.session, self.teamid, name)
                self.load(self.teamid)
            except Exception as e:
                self.errortxt['text'] = e
        else:
            self.errortxt['text'] = "Invalid Team Name"
