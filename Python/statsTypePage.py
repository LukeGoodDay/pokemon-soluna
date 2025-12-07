import tkinter as tk
from tkinter import ttk
import sqlHelperFunctions as sql
import statsPage
import homePage

class StatsTypePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        self.control = controller

        self.typeLbl = ttk.Label(self, text ="Type Ranking:")
        self.typeLbl.grid(row = 0, column = 1, padx = 10, pady = 10)
        # Create a Treeview widget
        self.type = ttk.Treeview(self)

        # Define the columns
        self.type['columns'] = ('Rank', 'Primary', 'Secondary', 'Count', 'Percent')

        # Format the columns
        self.type.column('#0', width=0, stretch=tk.NO)
        self.type.column('Rank', anchor=tk.W, width=50)
        self.type.column('Primary', anchor=tk.W, width=100)
        self.type.column('Secondary', anchor=tk.W, width=100)
        self.type.column('Count', anchor=tk.W, width=50)
        self.type.column('Percent', anchor=tk.W, width=100)

        # Create the headings
        self.type.heading('#0', text='', anchor=tk.W)
        self.type.heading('Rank', text='Rank', anchor=tk.W)
        self.type.heading('Primary', text='Primary', anchor=tk.W)
        self.type.heading('Secondary', text='Secondary', anchor=tk.W)
        self.type.heading('Count', text='Count', anchor=tk.W)
        self.type.heading('Percent', text='Percent', anchor=tk.W)

        self.type.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

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
        self.update(1)

    def update(self, i, *args):
        if i != 1: 
            self.control.show_frame(statsPage.StatsPage, i)
            return
        for item in self.type.get_children():
            self.type.delete(item)
        stats = sql.get_type_popularity(self.control.cursor, self.control.session)
        for stat in stats:
            self.type.insert(parent='', index=stat[0], values=(stat[2], stat[4], stat[5], stat[1], f"{stat[3]}%"))
    
    def back(self, *args):
        self.control.show_frame(homePage.HomePage)