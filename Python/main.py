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

def pretty_print(cursor, leng=20):
    start = True
    for r in cursor:
        if start:
            counter = 0
            for key in r:
                if counter == 5:
                    print('|')
                    counter = 0
                key = str(key)
                if len(key) > leng:
                    print(f"|{key[:leng-3]}...", end='')
                else:
                    print(f"|{key.ljust(leng)}", end='')
                counter +=1
            print('|')
            start = False
        counter = 0
        for val in r.values():
            if counter == 5:
                print('|')
                counter = 0
            val = str(val)
            if len(val) > leng:
                print(f"|{val[:leng-3]}...", end='')
            else:
                print(f"|{val.ljust(leng)}", end='')
            counter +=1
        print('|')

def picker(cursor, leng = 15):
    cnt = 0
    options = []
    for r in cursor:
        cnt += 1
        options.append(r[0])
        print(f"{r[0]}. {r[1]}".ljust(leng), end=' ')
        if cnt == 4:
            cnt = 0
            print()
    print()
    while True:
        res = int(input('Option #: '))
        if res in options:
            return res
        print("Result not in list, try again")

def print_team(conn, teamid):
    cursor = conn.cursor(prepared=True)
    try:
        sql = '''SELECT *
            FROM teams
            WHERE team_id = %s;'''
        cursor.execute(sql, (teamid, ))
        row = cursor.fetchall()
        if len(row) == 0:
            print("Species not found, try again.")
            return -1
        row = row[0]
        print("Team Name:", row[2])
        for i in range(3, len(row)):
            poke_id = row[i]
            if poke_id is None:
                break
            sql = '''SELECT p.nickname, p.gender, f.form_name, n.nature_name, a.ability_name
                FROM pokemon p
                JOIN forms f
                ON f.form_id = p.form_id
                JOIN natures n
                ON n.nature_id = p.nature_id
                JOIN abilities a
                ON a.ability_id = p.ability_id
                WHERE pokemon_id = %s;'''
            cursor.execute(sql, (poke_id, ))
            res = cursor.fetchall()
            if len(res) == 0:
                print("Error while displaying team.")
                break
            res = res[0]
            print(f"slot {i-2} - {res[0]}: {res[1]}, {res[2]}, {res[3]}, {res[4]}")
        cursor.close()
    except Error as e:
        print_sql_error(e, "print_team")
        raise
    finally:
        cursor.close()

def create_pokemon_terminal(conn):
    cursor = conn.cursor(prepared=True)
    try:
        sid = []
        while len(sid) == 0:
            print("Please insert the name of the species")
            name = input("Species Name: ")
            if name == "exit":
                return -2
            sql = '''SELECT species_id
                FROM species
                WHERE species_name = %s;'''
            cursor.execute(sql, (name, ))
            sid = cursor.fetchall()
            if len(sid) == 0:
                print("Species not found, try again.")
        sid = sid[0][0]
        print(sid)
        sql = '''SELECT form_id, form_name
            FROM forms
            WHERE species_id = %s;'''
        cursor.execute(sql, (sid, ))
        fid = cursor.fetchall()
        if len(fid) == 1:
            print('Only one form, it has been picked.')
            fid = fid[0][0]
        elif len(fid) == 0:
            print("Unexpected Error - no forms.")
            return -1
        else:
            print("Multiple forms, pick which:")
            fid = picker(fid)
        print("Nickname your pokemon:")
        nick = input('nickname: ')
        print("Enter M for male or F for female:")
        gender = input("gender: ").upper()
        if gender != 'M' and gender != 'F':
            gender = None
        sql = '''SELECT nature_id, nature_name
            FROM natures;'''
        cursor.execute(sql)
        print("Enter the number of the nature:")
        nature = picker(cursor)
        aid = []
        while len(aid) == 0:
            print("Enter the ability:")
            able = input("ability: ")
            sql = '''SELECT ability_id
                FROM abilities
                WHERE ability_name = %s;'''
            cursor.execute(sql, (able, ))
            aid = cursor.fetchall()
            if len(aid) == 0:
                print("Ability not found, please try again.")
        aid = aid[0][0]
        print(fid, nick, gender, nature, aid)
        sql = '''INSERT INTO pokemon
            (form_id, nickname, gender, nature_id, ability_id)
            VALUES (%s, %s, %s, %s, %s);'''
        cursor.execute(sql, (fid, nick, gender, nature, aid))
        retid = cursor.lastrowid
        conn.commit()
        cursor.close()
        return retid
    except Error as e:
        print_sql_error(e, "create_pokemon_terminal")
        raise
    finally:
        cursor.close()

def create_team_terminal(conn):
    cursor = conn.cursor(prepared=True)
    try:
        print("What is the name of your team?")
        name = input("Team Name: ")
        sql = '''INSERT INTO teams
            (user_id, team_name)
            VALUES (%s, %s);'''
        cursor.execute(sql, (1, name))
        id = cursor.lastrowid
        conn.commit()
        for i in range(6):
            poke_id = create_pokemon_terminal(conn)
            if poke_id == -2:
                break
            sql = f'''UPDATE teams 
                SET pokemon_{i + 1} = %s 
                WHERE team_id = %s;'''
            cursor.execute(sql, (poke_id, id))
            conn.commit()
        print("Here is the team you created:")
        print_team(conn, id)
        cursor.close()
    except Error as e:
        print_sql_error(e, "create_team_terminal")
        raise
    finally:
        cursor.close()

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
        print('name', name)
        if name is not None:
            self.greet['text'] = f'Welcome {name[0]}!'
        tea = sql.get_user_teams(self.control.cursor, self.control.session)
        print('team', tea)
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
            self.labels.append(tk.Label(self, text = f"Pokemon #{i}: Empty"))
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
        self.control.closeCursor()
        self.control.reopenCursor()
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

        self.submit = ttk.Button(self, text = "Submit", command=self.validate)
        self.submit.grid(row = 12, column = 0, padx = 10, pady = 10)

        self.errortxt = ttk.Label(self, text ="")
        self.errortxt.grid(row = 13, column = 0, padx = 10, pady = 10)

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
        else:
            self.form.set('')
            self.name.delete(0, tk.END)
            self.gender.state(["readonly"])
            self.gender.set('M')
            self.nature.set('')
            self.ability.set('')
            self.item.set('')
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
    
    def load_values(self):
        self.updateForm()
        self.updateNature()
        self.updateItem()
    
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
        if self.pokeid == 0:
            sql.new_pokemon(self.control.cursor, 1, ids[0], gender, nature, self.teamid, nick, ids[1], item)
            print("Sucessfully created pokemon")
        else:
            sql.update_pokemon(self.control.cursor, 1, self.pokeid, ids[0], gender, nature, nick, ids[1], item)
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

        # create_team_terminal(conn)
        # Driver Code
        app = tkinterApp()
        app.initCursor(conn)
        app.mainloop()

    except Error as e:
        print_sql_error(e, "main")
    #except Exception as e:
    #    print(f"[STD ERROR] {e}")
    finally:
        app.closeCursor()
        if conn and conn.is_connected():
            conn.close()
            print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    main()