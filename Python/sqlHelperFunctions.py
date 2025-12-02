from datetime import datetime
import hashlib

# log - logs an action taken by the current user
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# string action_taken - what the user did (30 char max)
# returns nothing
def log(mysql_cursor, session_id : int, action_taken : str) -> None:
    mysql_cursor.execute(
    f"""
        INSERT activity_log(session_id, action_taken, action_time) VALUES ("{session_id}", "{action_taken}", "{datetime.now()}");
    """)

# register - registers the user for the app
# connector mysql_cursor - the link to the database
# string username - the username of the user (30 char max)
# string email - the email of the user (265 char max must be unique)
# password - the password of the user (256 char max)
# returns int - a session token
def register(mysql_cursor, username : str, email : str, password : str) -> int:
    mysql_cursor.execute(
    f"""
        INSERT users(username) SELECT "{username}";

        INSERT 
            user_auth (user_id, email, hashed_password)
        SELECT
            user_id,
            "{email}",
            "{hashlib.sha256(password.encode('utf-8')).hexdigest()}"
        FROM users WHERE username = "{username}";

        INSERT
            sessions(user_id, started, ended)
        SELECT
            user_id,
            "{datetime.now()}",
            NULL
        FROM users WHERE username = "{username}";

        SELECT 
            session_id 
        FROM 
            sessions NATURAL JOIN users
        WHERE 
            users.username = "{username}" AND sessions.ended = NULL;
    """)
    return mysql_cursor.fetchone()


# login - logs a user into the app
# connector mysql_cursor - the link to the database
# string email - the email of the user (265 char max must be unique)
# password - the password of the user (256 char max)
# returns int - a session token
def login(mysql_cursor, email : str, password : str) -> int:
    mysql_cursor.execute(
    f"""
        INSERT
            sessions(user_id, started, ended)
        SELECT
            user_id,
            "{datetime.now()}",
            NULL
        FROM 
            users 
        WHERE 
            user_auth.email = "{email}" AND user_auth.hashed_password = "{hashlib.sha256(password.encode('utf-8')).hexdigest()}";

        SELECT 
            session_id 
        FROM 
            sessions NATURAL JOIN users NATURAL JOIN user_auth
        WHERE 
            user_auth.email = "{email}" AND user_auth.hashed_password = "{hashlib.sha256(password.encode('utf-8')).hexdigest()}" AND sessions.ended = NULL;
    """)
    return mysql_cursor.fetchone()

# logout - ends a session
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns nothing
def logout(mysql_cursor, session_id : int) -> None:
    mysql_cursor.execute(
    f"""
        UPDATE sessions SET ended = "{datetime.now()}" WHERE session_id = {session_id};
    """)

# get_user_teams - gets all teams belonging to the current user
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns - the list of the active user's teams
def get_user_teams(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT team_id, user_id, team_name FROM teams INNER JOIN sessions ON sessions.session_id = {session_id} AND teams.user_id = sessions.user_id;
    """)
    log(mysql_cursor, session_id, "SEARCH teams")
    return mysql_cursor.fetchall()

# get_team_pokemon - gets all pokemon on a specific team
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int team_id - the team to querry
# returns - the list of the pokemon on the team
def get_user_teams(mysql_cursor, session_id : int, team_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM pokemon WHERE team_id = {team_id};
    """)
    log(mysql_cursor, session_id, "SEARCH team pokemon")
    return mysql_cursor.fetchall()

# new_team - creates a new team for the current user
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# string team_name - the name of the team (max 30 char)
# returns nothing
def new_team(mysql_cursor, session_id : int, team_name : str) -> None:
    mysql_cursor.execute(
    f"""
        INSERT teams(user_id, team_name) SELECT user_id, "{team_name}" FROM sessions WHERE session_id = {session_id};
    """)
    log(mysql_cursor, session_id, "CREATE team")

# remove_team - removes an existing team
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int team_id - the team to remove
# returns nothing
def remove_team(mysql_cursor, session_id : int, team_id : int) -> None:
    mysql_cursor.execute(
    f"""
        DELETE FROM teams WHERE team_id = {team_id};

        DELETE FROM pokemon WHERE team_id = {team_id};
    """)
    log(mysql_cursor, session_id, "DELETE team")

# get_pokemon_details - gets the details about a pokemon
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int pokemon_id - the pokemon to update
# returns - the pokemon's details
def get_pokemon_details(mysql_cursor, session_id : int, pokemon_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM pokemon WHERE pokemon_id = {pokemon_id};
    """)
    log(mysql_cursor, session_id, "SEARCH pokemon")
    return mysql_cursor.fetchone()

# new_pokemon - creates a new pokemon
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int form_id - which pokemon this is
# string | None nickname - the nickname of the pokemon (max 12 char)
# char gender - the pokemon's gender ('M", 'F', 'N')
# int nature_id - the pokemon's nature
# int team_id - the team to add the pokemon to (1-6)
# int | None ability_id - the pokemon's ability
# int | None item_id - the pokemon's held item
# int | None move_1 - the pokemon's first move
# int | None move_2 - the pokemon's second move
# int | None move_3 - the pokemon's third move
# int | None move_4 - the pokemon's fourth move
# returns nothing
def new_pokemon(mysql_cursor, session_id : int, form_id : int, gender : str, nature_id : int, team_id : int, nickname : str = None, ability_id : int = None, item_id : int = None, move_1 : int = None, move_2 : int = None, move_3 : int = None, move_4 : int = None) -> None:
    mysql_cursor.execute(
    f"""
        INSERT pokemon(form_id, nickname, gender, nature_id, ability_id, item_id, move_1, move_2, move_3, move_4, team_id)
        VALUES ({form_id}, "{nickname}", {None if gender == 'N' else '"' + gender + '"'}, {nature_id}, {ability_id}, {item_id}, {move_1}, {move_2}, {move_3}, {move_4}, {team_id});
    """)
    log(mysql_cursor, session_id, "CREATE pokemon")

# update_pokemon - updates an existing pokemon
# connector mysql_cursor - the link to the database
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
# returns nothing
def update_pokemon(mysql_cursor, session_id : int, pokemon_id : int, form_id : int, gender : str, nature_id : int, nickname : str = None, ability_id : int = None, item_id : int = None, move_1 : int = None, move_2 : int = None, move_3 : int = None, move_4 : int = None) -> None:
    mysql_cursor.execute(
    f"""
        UPDATE pokemon
        SET 
            form_id = {form_id}, 
            gender = {None if gender == 'N' else '"' + gender + '"'}, 
            nature_id = {nature_id}, 
            nickname = "{nickname}", 
            ability_id = {ability_id}, 
            item_id = {item_id}, 
            move_1 = {move_1}, 
            move_2 = {move_2}, 
            move_3 = {move_3}, 
            move_4 = {move_4}
        WHERE pokemon_id = {pokemon_id};
    """)
    log(mysql_cursor, session_id, "UPDATE pokemon")

# remove_pokemon - removes an existing pokemon
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int pokemon_id - the current pokemon
# returns nothing
def remove_pokemon(mysql_cursor, session_id : int, pokemon_id : int) -> None:
    mysql_cursor.execute(
    f"""
        DELETE FROM pokemon WHERE pokemon_id = {pokemon_id};
    """)
    log(mysql_cursor, session_id, "DELETE pokemon")

# search_forms - searches for pokemon forms by name
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# string name - the name to search by
# returns - the list of relavant results
def search_forms(mysql_cursor, session_id : int, name : str):
    mysql_cursor.execute(
    f"""
        SELECT * FROM forms WHERE form_name LIKE "%{name}%";
    """)
    log(mysql_cursor, session_id, "SEARCH forms")
    return mysql_cursor.fetchall()

# search_items - searches for items by name
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# string name - the name to search by
# returns - the list of relavant results
def search_items(mysql_cursor, session_id : int, name : str):
    mysql_cursor.execute(
    f"""
        SELECT * FROM items WHERE item_name LIKE "%{name}%";
    """)
    log(mysql_cursor, session_id, "SEARCH items")
    return mysql_cursor.fetchall()

# search_moves - searches for moves by pokemon, optional level, optional name
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int form_id - the form of the pokemon
# string name - the name to search by (optional)
# returns - the list of relavant results
def search_moves(mysql_cursor, session_id : int, form_id : int, name : str = ""):
    mysql_cursor.execute(
    f"""
        SELECT * FROM 
            form_move INNER JOIN moves ON form_move.move_id = moves.move_id 
        WHERE 
            form_move.form_id = {form_id} AND moves.move_name LIKE "%{name}%";
    """)
    log(mysql_cursor, session_id, "SEARCH moves")
    return mysql_cursor.fetchall()

# search_natures - searches for natures by name
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# string name - the name to search by
# returns - the list of relavant results
def search_natures(mysql_cursor, session_id : int, name : str):
    mysql_cursor.execute(
    f"""
        SELECT * FROM natures WHERE nature_name LIKE "%{name}%";
    """)
    log(mysql_cursor, session_id, "SEARCH natures")
    return mysql_cursor.fetchall()

# update_move_popularity - updates the data in the move popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns nothing
def update_move_popularity(mysql_cursor, session_id : int) -> None:
    mysql_cursor.execute(
    f"""
        WITH count_table AS (
            SELECT
                move_id,
                COUNT(move_id) AS count,
                RANK() OVER (ORDER BY COUNT(move_id) DESC) AS popularity_rank,
                (COUNT(move_id) / (SELECT COUNT(*) FROM pokemon) * 100) AS total_percentage
            FROM  
            (
                SELECT *
                FROM (VALUES ROW(form_id, pokemon.move_1), ROW(form_id, pokemon.move_2), ROW(form_id, pokemon.move_3), ROW(form_id, pokemon.move_4)) AS p (form_id, move_id)
                WHERE p.move_id IS NOT NULL
            )
            GROUP BY move_id
        )
        UPDATE 
            move_popularity
        SET
            count = count_table.count,
            popularity_rank = count_table.popularity_rank,
            total_percentage = count_table.total_percentage
        WHERE
            count_table.move_id = move_popularity.move_id;
    """)
    log(mysql_cursor, session_id, "UPDATE move_popularity")

# get_move_popularity - gets the data in the move popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns the move popularity table
def get_move_popularity(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM move_popularity;
    """)
    log(mysql_cursor, session_id, "SEARCH move_popularity")
    return mysql_cursor.fetchall()

# update_pokemon_popularity - updates the data in the pokemon popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns nothing
def update_pokemon_popularity(mysql_cursor, session_id : int) -> None:
    mysql_cursor.execute(
    f"""
        WITH count_table AS (
            SELECT
                form_id,
                COUNT(form_id) AS count,
                RANK() OVER (ORDER BY COUNT(form_id) DESC) AS popularity_rank,
                (COUNT(form_id) / (SELECT COUNT(*) FROM pokemon) * 100) AS total_percentage
            FROM pokemon GROUP BY form_id
        )
        UPDATE 
            pokemon_popularity
        SET
            count = count_table.count,
            popularity_rank = count_table.popularity_rank,
            total_percentage = count_table.total_percentage
        WHERE
            count_table.form_id = pokemon_popularity.form_id;
    """)
    log(mysql_cursor, session_id, "UPDATE pokemon_popularity")

# get_pokemon_popularity - gets the data in the pokemon popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns the pokemon popularity table
def get_pokemon_popularity(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM pokemon_popularity;
    """)
    log(mysql_cursor, session_id, "SEARCH pokemon_popularity")
    return mysql_cursor.fetchall()

# update_item_popularity - updates the data in the item popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns nothing
def update_item_popularity(mysql_cursor, session_id : int) -> None:
    mysql_cursor.execute(
    f"""
        WITH count_table AS (
            SELECT
                item_id,
                COUNT(item_id) AS count,
                RANK() OVER (ORDER BY COUNT(item_id) DESC) AS popularity_rank,
                (COUNT(item_id) / (SELECT COUNT(*) FROM pokemon WHERE item_id IS NOT NULL) * 100) AS total_percentage
            FROM pokemon WHERE item_id IS NOT NULL GROUP BY item_id
        )
        UPDATE 
            item_popularity
        SET
            count = count_table.count,
            popularity_rank = count_table.popularity_rank,
            total_percentage = count_table.total_percentage
        WHERE
            count_table.item_id = item_popularity.item_id;
    """)
    log(mysql_cursor, session_id, "UPDATE item_popularity")

# get_item_popularity - gets the data in the item popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns the item popularity table
def get_item_popularity(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM item_popularity;
    """)
    log(mysql_cursor, session_id, "SEARCH item_popularity")
    return mysql_cursor.fetchall()

# update_type_popularity - updates the data in the type popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns nothing
def update_type_popularity(mysql_cursor, session_id : int) -> None:
    mysql_cursor.execute(
    f"""
        WITH count_table AS (
            SELECT
                type_id,
                COUNT(type_id) AS count,
                RANK() OVER (ORDER BY COUNT(type_id) DESC) AS popularity_rank,
                (COUNT(type_id) / (SELECT COUNT(*) FROM pokemon) * 100) AS total_percentage
            FROM pokemon INNER JOIN forms ON pokemon.form_id = forms.form_id GROUP BY type_id
        )
        UPDATE 
            type_popularity
        SET
            count = count_table.count,
            popularity_rank = count_table.popularity_rank,
            total_percentage = count_table.total_percentage
        WHERE
            count_table.type_id = type_popularity.type_id;
    """)
    log(mysql_cursor, session_id, "UPDATE type_popularity")

# get_type_popularity - gets the data in the type popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns the type popularity table
def get_type_popularity(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM type_popularity;
    """)
    log(mysql_cursor, session_id, "SEARCH type_popularity")
    return mysql_cursor.fetchall()

# get_image - gets the image of a pokemon
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int form_id - the form id of the pokemon
# returns the image of the form
def get_image(mysql_cursor, session_id : int, form_id : int):
    pass

# find_wondertrade - tries to find a wondertrade for the specified pokemon
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int form_id - the form id of the pokemon
# returns the wondertrade if found otherwise None
def find_wondertrade(mysql_cursor, session_id : int, form_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM wonder_trades WHERE form_id = {form_id};
    """)
    log(mysql_cursor, session_id, "SEARCH wonder_trades")
    return mysql_cursor.fetchone()

# get_hatching_steps - gets the number of steps to hatch an egg
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int species_id - the species id of the pokemon
# returns the number of steps to hatch the pokemon
def get_hatching_steps(mysql_cursor, session_id : int, species_id : int) -> int:
    mysql_cursor.execute(
    f"""
        SELECT steps FROM hatching WHERE species_id = {species_id};
    """)
    log(mysql_cursor, session_id, "SEARCH hatching")
    return mysql_cursor.fetchone()
