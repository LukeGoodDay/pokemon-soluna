import tkinter as tk
from homePage import HomePage
from teamPage import TeamPage
from pokeEditPage import PokeEditPage
from loginPage import LoginPage
from registerPage import RegisterPage
from statsPage import StatsPage
from pokedexPage import PokedexPage

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
        for F in (LoginPage, RegisterPage, HomePage, TeamPage, PokeEditPage, StatsPage, PokedexPage):
 
            frame = F(container, self)
 
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        self.show_frame(LoginPage)
    
    def initCursor(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.frames[LoginPage].load()
    
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

# For quick testing when not connected to database
if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()