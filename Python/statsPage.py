import tkinter as tk
from tkinter import ttk
import sqlHelperFunctions as sql
import statsTypePage
import homePage

class StatsPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        self.control = controller

        self.pokeLbl = ttk.Label(self, text ="Pokemon Ranking:")
        self.pokeLbl.grid(row = 0, column = 1, padx = 10, pady = 10)
        # Create a Treeview widget
        self.poke = ttk.Treeview(self)

        # Define the columns
        self.poke['columns'] = ('Rank', 'Name', 'Count', 'Percent')

        # Format the columns
        self.poke.column('#0', width=0, stretch=tk.NO)
        self.poke.column('Rank', anchor=tk.W, width=50)
        self.poke.column('Name', anchor=tk.W, width=200)
        self.poke.column('Count', anchor=tk.W, width=50)
        self.poke.column('Percent', anchor=tk.W, width=100)

        # Create the headings
        self.poke.heading('#0', text='', anchor=tk.W)
        self.poke.heading('Rank', text='Rank', anchor=tk.W)
        self.poke.heading('Name', text='Name', anchor=tk.W)
        self.poke.heading('Count', text='Count', anchor=tk.W)
        self.poke.heading('Percent', text='Percent', anchor=tk.W)

        self.poke.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

        self.pokebtn = ttk.Button(self, text="Pokemon Stats", command=lambda:self.update(0))
        self.pokebtn.grid(row=2, column=0, pady=10, padx=10)

        self.typebtn = ttk.Button(self, text="Type Stats", command=lambda:self.update(1))
        self.typebtn.grid(row=2, column=1, pady=10, padx=10)

        self.itembtn = ttk.Button(self, text="Item Stats", command=lambda:self.update(2))
        self.itembtn.grid(row=2, column=2, pady=10, padx=10)

        self.movebtn = ttk.Button(self, text="Move Stats", command=lambda:self.update(3))
        self.movebtn.grid(row=3, column=0, pady=10, padx=10)

        self.backbtn = ttk.Button(self, text="Back", command=self.back)
        self.backbtn.grid(row=3, column=2, pady=10, padx=10)

    def load(self, teamid=0, pokeid=0):
        self.update(teamid)

    def update(self, i, *args):
        if i == 1:
            self.control.show_frame(statsTypePage.StatsTypePage)
            return
        for item in self.poke.get_children():
            self.poke.delete(item)
        idx = 4
        if i == 0: 
            stats = sql.get_pokemon_popularity(self.control.cursor, self.control.session)
            self.pokeLbl['text'] = "Pokemon Ranking:"
            idx = 5
        elif i == 2:
            stats = sql.get_item_popularity(self.control.cursor, self.control.session)
            self.pokeLbl['text'] = "Item Ranking:"
        else:
            stats = sql.get_move_popularity(self.control.cursor, self.control.session)
            self.pokeLbl['text'] = "Move Ranking:"
        for i, stat in enumerate(stats):
            self.poke.insert(parent='', index=i, values=(stat[2], stat[idx], stat[1], f"{stat[3]}%"))

    def back(self, *args):
        self.control.show_frame(homePage.HomePage)