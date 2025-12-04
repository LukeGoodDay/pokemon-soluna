import tkinter as tk
from tkinter import ttk
import sqlHelperFunctions as sql
import teamPage

class PokeEditPage(tk.Frame):
    teamid = 1
    pokeid = 0
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.control = controller

        self.formlbl = ttk.Label(self, text ="Pokemon Form:")
        self.formlbl.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.form = ttk.Combobox(self, values=[])
        self.form.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.form.bind("<KeyRelease>", self.updateForm)
        self.form.bind("<<ComboboxSelected>>", self.updateForm)

        self.namelbl = ttk.Label(self, text ="Pokemon Nickname (12 char max):")
        self.namelbl.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.name = ttk.Entry(self)
        self.name.grid(row = 3, column = 0, padx = 10, pady = 10)

        self.genderlbl = ttk.Label(self, text ="Gender (Male/Female/None - M/F/N):")
        self.genderlbl.grid(row = 4, column = 0, padx = 10, pady = 10)
        self.gender = ttk.Combobox(self, values=['M', 'F'])
        self.gender.grid(row = 5, column = 0, padx = 10, pady = 10)
        self.gender.state(["readonly"])
        self.gender.set('M')

        self.naturelbl = ttk.Label(self, text ="Nature:")
        self.naturelbl.grid(row = 6, column = 0, padx = 10, pady = 10)
        self.nature = ttk.Combobox(self, values=[])
        self.nature.grid(row = 7, column = 0, padx = 10, pady = 10)
        self.nature.bind("<KeyRelease>", self.updateNature)

        self.abilitylbl = ttk.Label(self, text ="Ability:")
        self.abilitylbl.grid(row = 8, column = 0, padx = 10, pady = 10)
        self.ability = ttk.Combobox(self, values=[''])
        self.ability.grid(row = 9, column = 0, padx = 10, pady = 10)
        self.ability.state(["readonly"])

        self.itemlbl = ttk.Label(self, text ="Item:")
        self.itemlbl.grid(row = 10, column = 0, padx = 10, pady = 10)
        self.item = ttk.Combobox(self, values=[''])
        self.item.grid(row = 11, column = 0, padx = 10, pady = 10)
        self.item.bind("<KeyRelease>", self.updateItem)

        self.move1lbl = ttk.Label(self, text ="Move 1:")
        self.move1lbl.grid(row = 12, column = 0)
        self.move1 = ttk.Combobox(self, values=[''])
        self.move1.grid(row = 13, column = 0, padx = 10, pady = 10)
        self.move1.bind("<KeyRelease>", lambda x: self.updateMove(1, x))

        self.move2lbl = ttk.Label(self, text ="Move 2:")
        self.move2lbl.grid(row = 14, column = 0)
        self.move2 = ttk.Combobox(self, values=[''])
        self.move2.grid(row = 15, column = 0, padx = 10, pady = 10)
        self.move2.bind("<KeyRelease>", lambda x: self.updateMove(2, x))

        self.move3lbl = ttk.Label(self, text ="Move 3:")
        self.move3lbl.grid(row = 16, column = 0)
        self.move3 = ttk.Combobox(self, values=[''])
        self.move3.grid(row = 17, column = 0, padx = 10, pady = 10)
        self.move3.bind("<KeyRelease>", lambda x: self.updateMove(3, x))

        self.move4lbl = ttk.Label(self, text ="Move 4:")
        self.move4lbl.grid(row = 18, column = 0)
        self.move4 = ttk.Combobox(self, values=[''])
        self.move4.grid(row = 19, column = 0, padx = 10, pady = 10)
        self.move4.bind("<KeyRelease>", lambda x: self.updateMove(4, x))

        self.submit = ttk.Button(self, text = "Submit", command=self.validate)
        self.submit.grid(row = 20, column = 0, padx = 10, pady = 10)

        self.errortxt = ttk.Label(self, text ="")
        self.errortxt.grid(row = 21, column = 0, padx = 10, pady = 10)

    def load(self, teamid, pokeid=0):
        self.teamid = teamid
        self.pokeid = pokeid
        # If editing existing pokemon
        if self.pokeid != 0:
            pokemon = sql.get_pokemon_details(self.control.cursor, self.control.session, self.pokeid)
            print(pokemon)
            forminfo = sql.get_form_details(self.control.cursor, self.control.session, pokemon[1])
            self.form.set(forminfo[3])
            self.name.delete(0, tk.END)
            if pokemon[2] is not None:
                self.name.insert(0, pokemon[2])
            if pokemon[7] is not None:
                move = sql.get_move_details(self.control.cursor, self.control.session, pokemon[7])
                self.move1.set(move[1])
            else:
                self.move1.set('')
            if pokemon[8] is not None:
                move = sql.get_move_details(self.control.cursor, self.control.session, pokemon[8])
                self.move2.set(move[1])
            else:
                self.move2.set('')
            if pokemon[9] is not None:
                move = sql.get_move_details(self.control.cursor, self.control.session, pokemon[9])
                self.move3.set(move[1])
            else:
                self.move3.set('')
            if pokemon[10] is not None:
                move = sql.get_move_details(self.control.cursor, self.control.session, pokemon[10])
                self.move4.set(move[1])
            else:
                self.move4.set('')
            natureinfo = sql.get_nature_details(self.control.cursor, self.control.session, pokemon[4])
            self.nature.set(natureinfo[1])
            abilityinfo = sql.get_ability_details(self.control.cursor, self.control.session, pokemon[5])
            self.ability.set(abilityinfo[1])
            if pokemon[6] is not None:
                iteminfo = sql.get_item_details(self.control.cursor, self.control.session, pokemon[6])
                self.item.set(iteminfo[1])
            else:
                self.item.set('')
            self.load_values()
            gender = pokemon[3]
            if gender is not None:
                self.gender.set(gender)
                self.gender.state(["readonly"])
        else:
            self.form.set('')
            self.name.delete(0, tk.END)
            self.gender.state(["readonly"])
            self.gender.set('M')
            self.nature.set('')
            self.ability.set('')
            self.item.set('')
            self.move1.set('')
            self.move2.set('')
            self.move3.set('')
            self.move4.set('')
            self.load_values()
    
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
                self.gender.state(["disabled"])
            else:
                if self.gender.get() == 'N':
                    self.gender.set('M')
                self.gender.state(["readonly"])
            moves = sql.search_moves(self.control.cursor, self.control.session, result[0][1])
            movelist = [i[5] for i in moves]
            self.move1['values'] = movelist
            self.move2['values'] = movelist
            self.move3['values'] = movelist
            self.move4['values'] = movelist
            abilityids = list(forminfo[11:14])
            abilities = []
            id = 0
            if abilityids[id] is not None and abilityids[id] != abilityids[id+1]:
                abilities.append(sql.get_ability_details(self.control.cursor, 1, abilityids[id])[1])
                id += 1
            else:
                del abilityids[id]
            if abilityids[id] is not None:
                abilities.append(sql.get_ability_details(self.control.cursor, 1, abilityids[id])[1])
                id += 1
            else:
                del abilityids[id]
            if abilityids[id] is not None:
                abilities.append(sql.get_ability_details(self.control.cursor, 1, abilityids[id])[1])
                id += 1
            else:
                del abilityids[id]
            self.ability['values'] = abilities
            able = self.ability.get()
            if able in abilities:
                if able == '':
                    return result[0][1], None
                else:
                    id = abilities.index(able)
                    return result[0][1], abilityids[id-1]
            return result[0][1], None
        return

    def updateNature(self, *args):
        nature = self.nature.get()
        natures = sql.search_natures(self.control.cursor, 1, nature)
        opts = [i[1] for i in natures]
        self.nature['values'] = opts
        if nature in opts:
            return natures[0][0]

    def updateItem(self, *args):
        item = self.item.get()
        items = sql.search_items(self.control.cursor, 1, self.item.get())
        opts = [i[1] for i in items]
        self.item['values'] = opts
        if item in opts:
            return items[0][0]
        
    def updateMove(self, i, *args):
        movevals = []
        form = self.form.get()
        result = sql.search_forms(self.control.cursor, self.control.session, form)
        if i == 1 or i == 5:
            move = self.move1.get()
            moves = sql.search_moves(self.control.cursor, self.control.session, result[0][1], move)
            movelist = [i[5] for i in moves]
            self.move1['values'] = movelist
            if move in movelist:
                idx = movelist.index(move)
                movevals.append(moves[idx][2])
        if i == 2 or i == 5:
            move = self.move2.get()
            moves = sql.search_moves(self.control.cursor, self.control.session, result[0][1], move)
            movelist = [i[5] for i in moves]
            self.move2['values'] = movelist
            if move in movelist:
                idx = movelist.index(move)
                if moves[idx][2] not in movevals:
                    movevals.append(moves[idx][2])
        if i == 3 or i == 5:
            move = self.move3.get()
            moves = sql.search_moves(self.control.cursor, self.control.session, result[0][1], move)
            movelist = [i[5] for i in moves]
            self.move3['values'] = movelist
            if move in movelist:
                idx = movelist.index(move)
                if moves[idx][2] not in movevals:
                    movevals.append(moves[idx][2])
        if i == 4 or i == 5:
            move = self.move4.get()
            moves = sql.search_moves(self.control.cursor, self.control.session, result[0][1], move)
            movelist = [i[5] for i in moves]
            self.move4['values'] = movelist
            if move in movelist:
                idx = movelist.index(move)
                if moves[idx][2] not in movevals:
                    movevals.append(moves[idx][2])
        movevals.append(None)
        movevals.append(None)
        movevals.append(None)
        movevals.append(None)
        return movevals
    
    def load_values(self):
        self.updateForm()
        self.updateNature()
        self.updateItem()
        self.updateMove(5)
    
    def validate(self):
        ids = self.updateForm()
        if ids is None:
            self.errortxt['text'] = 'Invalid Pokemon Form'
            return
        nature = self.updateNature()
        if nature is None:
            self.errortxt['text'] = 'Invalid Nature'
            return
        if ids[1] is None:
            self.errortxt['text'] = 'Please Select an Ability'
            return
        item = self.updateItem()
        gender = self.gender.get()
        if gender == '':
            gender = 'N'
        nick = self.name.get()
        if len(nick) == 0:
            nick = None
        elif len(nick) > 12:
            nick = nick[0:12]
        move = self.updateMove(5)
        if self.pokeid == 0:
            sql.new_pokemon(self.control.cursor, 1, ids[0], gender, nature, self.teamid, nick, ids[1], item, move[0], move[1], move[2], move[3])
            print("Sucessfully created pokemon")
        else:
            sql.update_pokemon(self.control.cursor, 1, self.pokeid, ids[0], gender, nature, nick, ids[1], item, move[0], move[1], move[2], move[3])
            print('Sucessfully updated pokemon')
        self.errortxt['text'] = ''
        self.control.show_frame(teamPage.TeamPage, self.teamid, self.pokeid)
