# log - logs an action taken by the current user
# connector mysql_connector - the link to the database
# int session_id - the current session token
# string action_taken - what the user did (30 char max)
# returns nothing
def log(mysql_connector, session_id, action_taken):
    pass

# register - registers the user for the app
# connector mysql_connector - the link to the database
# string username - the username of the user (30 char max)
# string email - the email of the user (265 char max must be unique)
# password - the password of the user (256 char max)
# returns int - a session token
def register(mysql_connector, username, email, password):
    pass

# login - logs a user into the app
# connector mysql_connector - the link to the database
# string email - the email of the user (265 char max must be unique)
# password - the password of the user (256 char max)
# returns int - a session token
def login(mysql_connector, email, password):
    pass

# logout - ends a session
# connector mysql_connector - the link to the database
# int session_id - the current session token
# returns nothing
def logout(mysql_connector, session_id):
    pass

# get_user_teams - gets all teams belonging to the current user
# connector mysql_connector - the link to the database
# int session_id - the current session token
# returns - the list of the active user's teams
def get_user_teams(mysql_connector, session_id):
    pass

# new_team - creates a new team for the current user
# connector mysql_connector - the link to the database
# int session_id - the current session token
# returns int - the team id
def new_team(mysql_connector, session_id):
    pass

# remove_team - removes an existing team
# connector mysql_connector - the link to the database
# int session_id - the current session token
# int team_id - the team to add the pokemon to
# returns nothing
def remove_team(mysql_connector, session_id, team_id):
    pass

# get_pokemon_details - gets the details about a pokemon
# connector mysql_connector - the link to the database
# int session_id - the current session token
# int pokemon_id - the pokemon to update
# returns - the pokemon's details
def get_pokemon_details(mysql_connector, session_id, pokemon_id):
    pass

# new_pokemon - creates a new pokemon
# connector mysql_connector - the link to the database
# int session_id - the current session token
# int team_id - the team to add the pokemon to
# int form_id - which pokemon this is
# string | None nickname - the nickname of the pokemon (max 12 char)
# char gender - the pokemon's gender ('M", 'F', 'N')
# int nature_id - the pokemon's nature
# int | None ability_id - the pokemon's ability
# int | None item_id - the pokemon's held item
# int | None move_1 - the pokemon's first move
# int | None move_2 - the pokemon's second move
# int | None move_3 - the pokemon's third move
# int | None move_4 - the pokemon's fourth move
# returns int - the pokemon's id
def new_pokemon(mysql_connector, session_id, team_id, form_id, nickname, gender, nature_id, ability_id, item_id, move_1, move_2, move_3, move_4):
    pass

# update_pokemon - updates an existing pokemon
# connector mysql_connector - the link to the database
# int session_id - the current session token
# int pokemon_id - the pokemon to update
# int form_id - which pokemon this is
# string | None nickname - the nickname of the pokemon (max 12 char)
# char gender - the pokemon's gender ('M", 'F', 'N')
# int nature_id - the pokemon's nature
# int | None ability_id - the pokemon's ability
# int | None item_id - the pokemon's held item
# int | None move_1 - the pokemon's first move
# int | None move_2 - the pokemon's second move
# int | None move_3 - the pokemon's third move
# int | None move_4 - the pokemon's fourth move
# returns int - the pokemon's id
def update_pokemon(mysql_connector, session_id, pokemon_id, form_id, nickname, gender, nature_id, ability_id, item_id, move_1, move_2, move_3, move_4):
    pass

# remove_pokemon - removes an existing pokemon
# connector mysql_connector - the link to the database
# int session_id - the current session token
# int pokemon_id - the current pokemon
# returns nothing
def remove_pokemon(mysql_connector, session_id, pokemon_id):
    pass

# search_forms - searches for pokemon forms by name
# connector mysql_connector - the link to the database
# int session_id - the current session token
# string name - the name to search by
# returns - the list of relavant results
def search_forms(mysql_connector, session_id):
    pass

# search_items - searches for items by name
# connector mysql_connector - the link to the database
# int session_id - the current session token
# string name - the name to search by
# returns - the list of relavant results
def search_items(mysql_connector, session_id, name):
    pass

# search_moves - searches for moves by pokemon, optional level, optional name
# connector mysql_connector - the link to the database
# int session_id - the current session token
# int form_id - the form of the pokemon
# int | None pokemon_level - the pokemon's level
# string | None name - the name to search by
# returns - the list of relavant results
def search_moves(mysql_connector, session_id, form_id, pokemon_level, name):
    pass

# search_natures - searches for natures by name
# connector mysql_connector - the link to the database
# int session_id - the current session token
# string name - the name to search by
# returns - the list of relavant results
def search_natures(mysql_connector, session_id, name):
    pass
