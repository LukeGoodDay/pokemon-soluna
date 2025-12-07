import tkinter as tk
from tkinter import ttk
import sqlHelperFunctions as sql
import registerPage
import homePage

class StatsPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        self.control = controller

        self.pokebox = ttk.Frame(self)

        self.pokeLbl = ttk.Label(self, text ="Pokemon Ranking:")
        self.pokeLbl.grid(row = 0, column = 1, padx = 10, pady = 10)
        # Create a Treeview widget
        self.poke = ttk.Treeview(self.pokebox)

        # Define the columns
        self.poke['columns'] = ('Rank', 'Name', 'Count', 'Percent')

        # Format the columns
        self.poke.column('#0', width=0, stretch=tk.NO)
        self.poke.column('Rank', anchor=tk.W, width=100)
        self.poke.column('Name', anchor=tk.W, width=200)
        self.poke.column('Count', anchor=tk.W, width=100)
        self.poke.column('Percent', anchor=tk.W, width=100)

        # Create the headings
        self.poke.heading('#0', text='', anchor=tk.W)
        self.poke.heading('Rank', text='Rank', anchor=tk.W)
        self.poke.heading('Name', text='Name', anchor=tk.W)
        self.poke.heading('Count', text='Count', anchor=tk.W)
        self.poke.heading('Percent', text='Percent', anchor=tk.W)

        self.poke.pack(expand=True, fill=tk.BOTH)

        # Create vertical scrollbar
        self.pokesb = ttk.Scrollbar(self.pokebox, orient="vertical", command=self.poke.yview)
        self.pokesb.pack(side='right', fill='y')
        self.poke.configure(yscrollcommand=self.pokesb.set)

        self.pokebox.grid(row=1, column=0, columnspan=3, pady=5, padx=5)

    def load(self, teamid=0, pokeid=0):
        pokestat = sql.get_pokemon_popularity(self.control.cursor, self.control.session)
        print(pokestat[0])
        for stat in pokestat:
            self.poke.insert(parent='', index=stat[0], values=(stat[2], stat[5], stat[1], f"{stat[3]}%"))