import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL
from datetime import datetime
import sqlHelperFunctions as sql
import homePage

class WonderTradePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.control = controller

        self.formlbl = ttk.Label(self, text ="Pokemon Form:")
        self.formlbl.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.form = ttk.Combobox(self, values=[])
        self.form.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.form.bind("<KeyRelease>", self.updateForm)
        self.form.bind("<<ComboboxSelected>>", self.updateForm)

        self.backbtn = ttk.Button(self, text="Back", command=self.back)
        self.backbtn.grid(row=0, column=1, pady=10, padx=10)

        self.genderlbl = ttk.Label(self, text ="Gender (Male/Female/None - M/F/N):")
        self.genderlbl.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.gender = ttk.Combobox(self, values=['M', 'F'])
        self.gender.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.gender.state(["readonly"])
        self.gender.set('M')

        self.naturelbl = ttk.Label(self, text ="Nature:")
        self.naturelbl.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.nature = ttk.Combobox(self, values=[])
        self.nature.grid(row = 3, column = 1, padx = 10, pady = 10)
        self.nature.bind("<KeyRelease>", self.updateNature)

        self.submit = ttk.Button(self, text = "Submit", command=self.validate)
        self.submit.grid(row = 4, column = 0, padx = 10, pady = 10, columnspan=2)

        self.errortxt = ttk.Label(self, text ="")
        self.errortxt.grid(row = 5, column = 0, padx = 10, pady = 10, columnspan=2)

    def load(self, teamid=0, pokeid=0):
        if teamid != -1:
            self.errortxt['text'] = ''
        self.form.set('')
        self.gender.state(["readonly"])
        self.gender.set('M')
        self.nature.set('')
        self.updateForm()
        self.updateNature()

    def back(self, *args):
        self.control.show_frame(homePage.HomePage)
    
    def updateForm(self, *args):
        form = self.form.get()
        result = sql.search_forms(self.control.cursor, self.control.session, form)
        form_options = [i[2] for i in result]
        self.form['values'] = form_options
        if form in form_options:
            forminfo = sql.get_form_details(self.control.cursor, self.control.session, result[0][1])
            gender = forminfo[20]
            if gender is None:
                self.gender.set('N')
                self.gender["state"] = DISABLED
            else:
                if self.gender.get() == 'N':
                    self.gender.set('M')
                self.gender["state"] = NORMAL
            return result[0][1]
        return

    def updateNature(self, *args):
        nature = self.nature.get()
        natures = sql.search_natures(self.control.cursor, 1, nature)
        opts = [i[1] for i in natures]
        self.nature['values'] = opts
        if nature in opts:
            return natures[0][0]
    
    def validate(self):
        id = self.updateForm()
        if id is None:
            self.errortxt['text'] = 'Invalid Pokemon Form'
            return
        nature = self.updateNature()
        if nature is None:
            self.errortxt['text'] = 'Invalid Nature'
            return
        gender = self.gender.get()
        if gender == '':
            gender = 'N'
        try:
            sql.add_wonder_trade(self.control.cursor, self.control.session, datetime.now(), id, gender, nature)
            self.errortxt['text'] = 'Submitted Wondertrade!'
            self.load(-1)
        except Exception as e:
            self.errortxt['text'] = e
