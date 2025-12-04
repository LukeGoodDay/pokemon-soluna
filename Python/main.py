import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import sqlHelperFunctions as sql

# Configuration struct equivalent
class DbConfig:
    def __init__(self,
                 host="192.168.1.164",
                 port=3306,
                 user="default",
                 password="Password123!",
                 database="final_project"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

def print_sql_error(e: Error, where: str):
    # Print detailed error info
    print(f"[SQL ERROR @ {where}] {e.msg} | errno: {e.errno} | sqlstate: {e.sqlstate}")

LARGEFONT =("Verdana", 35)
 
class tkinterApp(tk.Tk):
    cursor = 0
    session = 1
    conn=1
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        
        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
 
        # initializing frames to an empty array
        self.frames = {}  
 
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (LoginPage, RegisterPage, HomePage, TeamPage, PokeEditPage):
 
            frame = F(container, self)
 
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        self.show_frame(HomePage)
    
    def initCursor(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.frames[HomePage].load()
    
    def closeCursor(self):
        self.cursor.close()
    
    def reopenCursor(self):
        self.cursor = self.conn.cursor()
 
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont, team=1, pokemon=0):
        frame = self.frames[cont]
        frame.tkraise()
        if self.cursor != 0:
            frame.load(team, pokemon)
 
# first window frame startpage
 
class LoginPage(tk.Frame):
    # TODO Actually make login page
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)


class RegisterPage(tk.Frame):
    # TODO Actually make register page
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)        
 
 
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
   

# third window frame page2
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
        for i in range(6):
            self.labels.append(tk.Label(self, text = f"Pokemon #{i+1}: Empty"))
            self.edits.append(ttk.Button(self, text="Edit", command= lambda i=i: self.edit(i)))
            self.deletes.append(ttk.Button(self, text="Delete", command= lambda i=i: self.delete(i)))
        self.back = ttk.Button(self, text="Back", command= lambda: self.control.show_frame(HomePage))
        self.back.grid(row=7, column=0, padx=10, pady=10)
        self.removebutton = ttk.Button(self, text="Delete", command=self.remove)
        self.removebutton.grid(row=7, column=1, padx=10, pady=10)
    
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
                        nick='Unnamed'
                    self.labels[i]['text'] = f"Pokemon #{i}: {nick}"
                    self.labels[i].grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
                    self.edits[i]['text'] = 'Edit'
                    self.edits[i].grid(row=i+1, column=1, padx=5, pady=5)
                    self.deletes[i].grid(row=i+1, column=2, padx=5, pady=5)
                elif i == count:
                    self.pokeids[i] = 0
                    self.labels[i]['text'] = f"Pokemon #{i}: Empty"
                    self.edits[i]['text'] = 'Create'
                    self.labels[i].grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
                    self.edits[i].grid(row=i+1, column=1, padx=5, pady=5)
                    self.deletes[i].grid_forget()
                else:
                    self.pokeids[i] = 0
                    self.labels[i].grid_forget()
                    self.edits[i].grid_forget()
                    self.deletes[i].grid_forget()

    def edit(self, i, *args):
        self.control.show_frame(PokeEditPage, self.teamid, self.pokeids[i])

    def delete(self, i, *args):
        id = self.pokeids[i]
        if id != 0:
            sql.remove_pokemon(self.control.cursor, self.control.session, id)
            self.load(self.teamid)
    
    def remove(self, *args):
        sql.remove_team(self.control.cursor, self.control.session, self.teamid)
        self.control.show_frame(HomePage)


# third window frame page2
class PokeEditPage(tk.Frame): 
    # TODO Handle Moves
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
            self.form.set(forminfo[2])
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
                abilities.append(sql.lookup_ability(self.control.cursor, 1, abilityids[id])[0][1])
                id += 1
            else:
                del abilityids[id]
            if abilityids[id] is not None:
                abilities.append(sql.lookup_ability(self.control.cursor, 1, abilityids[id])[0][1])
                id += 1
            else:
                del abilityids[id]
            if abilityids[id] is not None:
                abilities.append(sql.lookup_ability(self.control.cursor, 1, abilityids[id])[0][1])
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
        self.control.show_frame(TeamPage, self.teamid, self.pokeid)


def main():
    cfg = DbConfig()
    try:
        # Step 1: Connect to MySQL server (without specifying database yet)
        conn = mysql.connector.connect(
            host=cfg.host,
            port=cfg.port,
            user=cfg.user,
            password=cfg.password,
            autocommit=True
            # no database arg yet
        )
        if conn.is_connected():
            print("✅ Successfully connected to MySQL server")
        else:
            print("❌ Failed to connect to MySQL server")
            return

        conn.database = cfg.database

        # Driver Code
        app = tkinterApp()
        app.initCursor(conn)
        app.mainloop()

    except Error as e:
        print_sql_error(e, "main")
    except Exception as e:
       print(f"[STD ERROR] {e}")
    finally:
        if conn and conn.is_connected():
            app.closeCursor()
            conn.close()
            print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    main()