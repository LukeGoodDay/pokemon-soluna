import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlHelperFunctions as sql
import teamPage
import homePage

class PokedexPage(tk.Frame):
    teamid = 0
    img = None
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        self.control = controller

        self.formlbl = ttk.Label(self, text ="Pokemon Form:")
        self.formlbl.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.form = ttk.Combobox(self, values=[])
        self.form.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.form.bind("<KeyRelease>", self.updateForm)
        self.form.bind("<<ComboboxSelected>>", self.updateForm)

        self.classlbl = ttk.Label(self, text ="Class:")
        self.classlbl.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.classtxt = ttk.Label(self, text ="")
        self.classtxt.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.back = ttk.Button(self, text = "Back", command=self.goBack)
        self.back.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.dexnum = ttk.Label(self, text ="Pokedex: #")
        self.dexnum.grid(row = 1, column = 2, padx = 10, pady = 10)

        self.hp = ttk.Label(self, text ="HP: ")
        self.hp.grid(row = 2, column = 0, padx = 10, pady = 10)

        self.attack = ttk.Label(self, text ="Attack: ")
        self.attack.grid(row = 2, column = 1, padx = 10, pady = 10)

        self.defense = ttk.Label(self, text ="Defense: ")
        self.defense.grid(row = 2, column = 2, padx = 10, pady = 10)

        self.speed = ttk.Label(self, text ="Speed: ")
        self.speed.grid(row = 3, column = 0, padx = 10, pady = 10)

        self.spattack = ttk.Label(self, text ="Special Attack: ")
        self.spattack.grid(row = 3, column = 1, padx = 10, pady = 10)

        self.spdefense = ttk.Label(self, text ="Special Defense: ")
        self.spdefense.grid(row = 3, column = 2, padx = 10, pady = 10)

        self.able1 = ttk.Label(self, text ="Ability 1: ")
        self.able1.grid(row = 4, column = 0, padx = 10, pady = 10)

        self.able2 = ttk.Label(self, text ="Ability 2: ")
        self.able2.grid(row = 4, column = 1, padx = 10, pady = 10)

        self.ableh = ttk.Label(self, text ="Hidden Ability: ")
        self.ableh.grid(row = 4, column = 2, padx = 10, pady = 10)

        self.male = ttk.Label(self, text ="Male Percent: %")
        self.male.grid(row = 5, column = 0, padx = 10, pady = 10)

        self.female = ttk.Label(self, text ="Female Percent: %")
        self.female.grid(row = 5, column = 1, padx = 10, pady = 10)

        self.weight = ttk.Label(self, text ="Weight: lbs")
        self.weight.grid(row = 5, column = 2, padx = 10, pady = 10)

        self.egg1 = ttk.Label(self, text ="Egg Group 1: ")
        self.egg1.grid(row = 6, column = 0, padx = 10, pady = 10)

        self.egg2 = ttk.Label(self, text ="Egg Group 2: ")
        self.egg2.grid(row = 6, column = 1, padx = 10, pady = 10)

        self.height = ttk.Label(self, text ="Height: in")
        self.height.grid(row = 6, column = 2, padx = 10, pady = 10)

        self.primary = ttk.Label(self, text ="Primary Type: ")
        self.primary.grid(row = 7, column = 0, padx = 10, pady = 10)

        self.secondary = ttk.Label(self, text ="Secondary Type: ")
        self.secondary.grid(row = 7, column = 1, padx = 10, pady = 10)

        self.steps = ttk.Label(self, text ="Hatch Steps: ")
        self.steps.grid(row = 7, column = 2, padx = 10, pady = 10)

        self.imgbox = ttk.Label(self)
        self.imgbox.grid(row = 0, column=3, rowspan=7, columnspan=2)

    def load(self, teamid=0, pokeid=0):
        self.teamid = teamid
        self.updateForm()
    
    def updateForm(self, *args):
        form = self.form.get()
        result = sql.search_forms(self.control.cursor, self.control.session, form)
        form_options = [i[2] for i in result]
        self.form['values'] = form_options
        if form in form_options:
            f = sql.get_form_details(self.control.cursor, self.control.session, result[0][1])
            self.classtxt['text'] = f[18]
            self.dexnum['text'] = f"Pokedex: #{f[1]}"
            self.hp['text'] = f"HP: {f[4]}"
            self.attack['text'] = f"Attack: {f[5]}"
            self.defense['text'] = f"Defense: {f[6]}"
            self.speed['text'] = f"Speed: {f[9]}"
            self.spattack['text'] = f"Special Attack: {f[7]}"
            self.spdefense['text'] = f"Special Defense: {f[8]}"

            able = "None"
            if f[11] is not None:
                able = sql.get_ability_details(self.control.cursor, self.control.session, f[11])[1]
            self.able1['text'] = f"Ability 1: {able}"

            able = "None"
            if f[12] is not None:
                able = sql.get_ability_details(self.control.cursor, self.control.session, f[12])[1]
            self.able2['text'] = f"Ability 2: {able}"

            able = "None"
            if f[13] is not None:
                able = sql.get_ability_details(self.control.cursor, self.control.session, f[13])[1]
            self.ableh['text'] = f"Hidden Ability: {able}"

            self.weight['text'] = f"Weight: {f[14]} lbs"
            self.height['text'] = f"Height: {f[15]} in"
            self.male['text'] = f"Male Percent: {f[19]*100}%"
            self.female['text'] = f"Female Percent: {f[20]*100}%"
            self.egg1['text'] = f"Egg Group 1: {f[23]}"
            self.egg2['text'] = f"Egg Group 2: {f[24]}"
            self.primary['text'] = f"Primary Type: {f[25]}"
            self.secondary['text'] = f"Secondary Type: {f[26]}"

            steps = sql.get_hatching_steps(self.control.cursor, self.control.session, f[1])
            if steps is not None:
                steps = steps[0]
            self.steps['text'] = f"Hatch Steps: {steps}"

            loc = sql.get_image(self.control.cursor, self.control.session, f[2])
            self.img = Image.open(loc)
            self.img = ImageTk.PhotoImage(self.img)
            self.imgbox['image'] = self.img


    def goBack(self):
        self.control.show_frame(teamPage.TeamPage, self.teamid)