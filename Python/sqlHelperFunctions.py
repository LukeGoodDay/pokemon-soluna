from datetime import datetime
import hashlib

##########
#
# INSERT
#
##########

# register - registers the user for the app
# connector mysql_cursor - the link to the database
# string username - the username of the user (30 char max)
# string email - the email of the user (265 char max must be unique)
# password - the password of the user (256 char max)
# returns int - a session token
def register(mysql_cursor, username : str, email : str, password : str) -> int:
    mysql_cursor.execute(
    f"""
        INSERT INTO users(username) VALUES("{username}");
    """)
    mysql_cursor.execute(
    f"""
        INSERT INTO
            user_auth (user_id, email, hashed_password)
        SELECT
            user_id,
            "{email}",
            "{hashlib.sha256(password.encode('utf-8')).hexdigest()}"
        FROM users WHERE username = "{username}";
    """)
    mysql_cursor.execute(
    f"""
        INSERT
            sessions(user_id, started, ended)
        SELECT
            user_id,
            "{datetime.now()}",
            NULL
        FROM users WHERE username = "{username}";
    """)
    mysql_cursor.execute(
    f"""
        SELECT 
            session_id 
        FROM 
            sessions NATURAL JOIN users
        WHERE 
            users.username = "{username}" AND sessions.ended IS NULL;
    """)
    res = mysql_cursor.fetchone()
    if res is None:
        return res
    else:
        return res[0]

# login - logs a user into the app
# connector mysql_cursor - the link to the database
# string email - the email of the user (265 char max must be unique)
# password - the password of the user (256 char max)
# returns int - a session token
def login(mysql_cursor, email : str, password : str) -> int:
    mysql_cursor.execute(
    f"""
        INSERT INTO
            sessions(user_id, started, ended)
        SELECT
            user_id,
            "{datetime.now()}",
            NULL
        FROM 
            users NATURAL JOIN user_auth
        WHERE 
            user_auth.email = "{email}" AND user_auth.hashed_password = "{hashlib.sha256(password.encode('utf-8')).hexdigest()}";
    """)
    mysql_cursor.execute(
    f"""
        SELECT 
            session_id 
        FROM 
            sessions NATURAL JOIN user_auth
        WHERE 
            user_auth.email = "{email}" AND user_auth.hashed_password = "{hashlib.sha256(password.encode('utf-8')).hexdigest()}" AND sessions.ended IS NULL
        ORDER BY
            sessions.started DESC
        LIMIT 1;
    """)
    res = mysql_cursor.fetchone()
    if res is None:
        return res
    else:
        return res[0]

# log - logs an action taken by the current user
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# string action_taken - what the user did (30 char max)
# returns nothing
def log(mysql_cursor, session_id : int, action_taken : str) -> None:
    mysql_cursor.execute(
    f"""
        INSERT INTO activity_log(session_id, action_taken, action_time) VALUES ("{session_id}", "{action_taken}", "{datetime.now()}");
    """)

# new_team - creates a new team for the current user
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# string team_name - the name of the team (max 30 char)
# returns nothing
def new_team(mysql_cursor, session_id : int, team_name : str) -> None:
    log(mysql_cursor, session_id, "CREATE team")
    mysql_cursor.execute(
    f"""
        INSERT INTO teams(user_id, team_name) SELECT user_id, "{team_name}" FROM sessions WHERE session_id = {session_id};
    """)
    
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
    log(mysql_cursor, session_id, "CREATE pokemon")
    mysql_cursor.execute(
    f"""
        INSERT INTO pokemon(form_id, nickname, gender, nature_id, ability_id, item_id, move_1, move_2, move_3, move_4, team_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (form_id, nickname, None if gender == 'N' else gender, nature_id, ability_id, item_id, move_1, move_2, move_3, move_4, team_id))
    update_pokemon_popularity(mysql_cursor, session_id)
    update_type_popularity(mysql_cursor, session_id)
    update_item_popularity(mysql_cursor, session_id)
    update_move_popularity(mysql_cursor, session_id)

# add_wonder_trade - adds a user found wonder trade
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# datetime trade_time - when the trade took place
# int form_id - which pokemon this is
# char gender - the pokemon's gender ('M", 'F', 'N')
# int nature_id - the pokemon's nature
# returns nothing
def add_wonder_trade(mysql_cursor, session_id : int, trade_time : datetime, form_id : int, gender : str, nature_id : int) -> None:
    log(mysql_cursor, session_id, "CREATE wonder_trade")
    mysql_cursor.execute(
    f"""
        INSERT INTO wonder_trades(trade_time, form_id, gender, nature_id)
        VALUES (%s, %s, %s, %s);
    """, (trade_time, form_id, None if gender == 'N' else gender, nature_id))

##########
#
# UPDATE
#
##########

# logout - ends a session
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns nothing
def logout(mysql_cursor, session_id : int) -> None:
    mysql_cursor.execute(
    f"""
        UPDATE sessions SET ended = "{datetime.now()}" WHERE session_id = {session_id};
    """)

# update_team_name - updates a team's name
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int team_id - the team to update
# string name - the new team name
# returns nothing
def update_team_name(mysql_cursor, session_id : int, team_id : int, name : str) -> None:
    log(mysql_cursor, session_id, "UPDATE teams")
    mysql_cursor.execute(
    f"""
        UPDATE teams SET team_name = "{name}" WHERE team_id = {team_id};
    """)

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
    log(mysql_cursor, session_id, "UPDATE pokemon")
    mysql_cursor.execute(
    f"""
        UPDATE pokemon
        SET 
            form_id = %s, 
            nickname = %s, 
            gender = %s, 
            nature_id = %s, 
            ability_id = %s, 
            item_id = %s, 
            move_1 = %s, 
            move_2 = %s, 
            move_3 = %s, 
            move_4 = %s
        WHERE pokemon_id = {pokemon_id};
    """, (form_id, nickname, None if gender == 'N' else gender, nature_id, ability_id, item_id, move_1, move_2, move_3, move_4))
    update_pokemon_popularity(mysql_cursor, session_id)
    update_type_popularity(mysql_cursor, session_id)
    update_item_popularity(mysql_cursor, session_id)
    update_move_popularity(mysql_cursor, session_id)

# update_pokemon_popularity - updates the data in the pokemon popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns nothing
def update_pokemon_popularity(mysql_cursor, session_id : int) -> None:
    log(mysql_cursor, session_id, "UPDATE pokemon_popularity")
    mysql_cursor.execute(
    f"""
        UPDATE 
            pokemon_popularity
        INNER JOIN
        (
            SELECT
            form_id,
            COUNT(form_id) AS count,
            RANK() OVER (ORDER BY COUNT(form_id) DESC) AS popularity_rank,
            (COUNT(form_id) / (SELECT COUNT(*) FROM pokemon) * 100) AS total_percentage
            FROM pokemon GROUP BY form_id
        ) AS count_table ON count_table.form_id = pokemon_popularity.form_id
        SET
            pokemon_popularity.count = count_table.count,
            pokemon_popularity.popularity_rank = count_table.popularity_rank,
            pokemon_popularity.total_percentage = count_table.total_percentage;
    """)

# update_type_popularity - updates the data in the type popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns nothing
def update_type_popularity(mysql_cursor, session_id : int) -> None:
    log(mysql_cursor, session_id, "UPDATE type_popularity")
    mysql_cursor.execute(
    f"""
        UPDATE 
            type_popularity
        INNER JOIN
        (
            SELECT
                type_id,
                COUNT(type_id) AS count,
                RANK() OVER (ORDER BY COUNT(type_id) DESC) AS popularity_rank,
                (COUNT(type_id) / (SELECT COUNT(*) FROM pokemon) * 100) AS total_percentage
            FROM pokemon INNER JOIN forms ON pokemon.form_id = forms.form_id GROUP BY type_id
        ) AS count_table ON count_table.type_id = type_popularity.type_id
        SET
            type_popularity.count = count_table.count,
            type_popularity.popularity_rank = count_table.popularity_rank,
            type_popularity.total_percentage = count_table.total_percentage;
    """)

# update_item_popularity - updates the data in the item popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns nothing
def update_item_popularity(mysql_cursor, session_id : int) -> None:
    log(mysql_cursor, session_id, "UPDATE item_popularity")
    mysql_cursor.execute(
    f"""
        UPDATE 
            item_popularity
        INNER JOIN
        (
            SELECT
                item_id,
                COUNT(item_id) AS count,
                RANK() OVER (ORDER BY COUNT(item_id) DESC) AS popularity_rank,
                (COUNT(item_id) / (SELECT COUNT(*) FROM pokemon WHERE item_id IS NOT NULL) * 100) AS total_percentage
            FROM pokemon WHERE item_id IS NOT NULL GROUP BY item_id
        ) AS count_table ON count_table.item_id = item_popularity.item_id
        SET
            item_popularity.count = count_table.count,
            item_popularity.popularity_rank = count_table.popularity_rank,
            item_popularity.total_percentage = count_table.total_percentage;
    """)

# update_move_popularity - updates the data in the move popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns nothing
def update_move_popularity(mysql_cursor, session_id : int) -> None:
    log(mysql_cursor, session_id, "UPDATE move_popularity")
    # mysql_cursor.execute(
    # f"""
    #     UPDATE 
    #         move_popularity
    #     INNER JOIN
    #     (
    #         SELECT
    #             move_id,
    #             COUNT(move_id) AS count,
    #             RANK() OVER (ORDER BY COUNT(move_id) DESC) AS popularity_rank,
    #             (COUNT(move_id) / (SELECT COUNT(*) FROM pokemon) * 100) AS total_percentage
    #         FROM  
    #         (
    #             SELECT *
    #             FROM pokemon
    #             CROSS JOIN LATERAL
    #                 (VALUES ROW(pokemon.form_id, pokemon.move_1), ROW(pokemon.form_id, pokemon.move_2), ROW(pokemon.form_id, pokemon.move_3), ROW(pokemon.form_id, pokemon.move_4)) AS p (form_id, move_id)
    #             WHERE p.move_id IS NOT NULL
    #         ) AS move_table
    #         GROUP BY move_id
    #     ) AS count_table ON count_table.move_id = move_popularity.move_id
    #     SET
    #         move_popularity.count = count_table.count,
    #         move_popularity.popularity_rank = count_table.popularity_rank,
    #         move_popularity.total_percentage = count_table.total_percentage;
    # """)

##########
#
# DELETE
#
##########

# remove_team - removes an existing team
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int team_id - the team to remove
# returns nothing
def remove_team(mysql_cursor, session_id : int, team_id : int) -> None:
    log(mysql_cursor, session_id, "DELETE team")
    mysql_cursor.execute(
    f"""
        DELETE FROM pokemon WHERE team_id = {team_id};
    """)
    mysql_cursor.execute(
    f"""
        DELETE FROM teams WHERE team_id = {team_id};
    """)
    update_pokemon_popularity(mysql_cursor, session_id)
    update_type_popularity(mysql_cursor, session_id)
    update_item_popularity(mysql_cursor, session_id)
    update_move_popularity(mysql_cursor, session_id)

# remove_pokemon - removes an existing pokemon
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int pokemon_id - the current pokemon
# returns nothing
def remove_pokemon(mysql_cursor, session_id : int, pokemon_id : int) -> None:
    log(mysql_cursor, session_id, "DELETE pokemon")
    mysql_cursor.execute(
    f"""
        DELETE FROM pokemon WHERE pokemon_id = {pokemon_id};
    """)
    update_pokemon_popularity(mysql_cursor, session_id)
    update_type_popularity(mysql_cursor, session_id)
    update_item_popularity(mysql_cursor, session_id)
    update_move_popularity(mysql_cursor, session_id)

##########
#
# READ
#
##########

# get_username - gets the user's name
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns - the user's name
def get_username(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT users.username FROM users INNER JOIN sessions ON sessions.session_id = {session_id} AND users.user_id = sessions.user_id;
    """)
    return mysql_cursor.fetchone()

# get_ability_details - gets the details about an ability
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int ability_id - the ability to check
# returns - the ability's details
def get_ability_details(mysql_cursor, session_id : int, ability_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM abilities WHERE ability_id = {ability_id};
    """)
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
    return mysql_cursor.fetchone()

# get_form_details - gets the details about a pokemon form
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int form_id - the form to check
# returns - the form's details
def get_form_details(mysql_cursor, session_id : int, form_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM forms NATURAL JOIN form_info NATURAL JOIN species NATURAL JOIN type_chart WHERE form_id = {form_id};
    """)
    return mysql_cursor.fetchone()

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
    return mysql_cursor.fetchall()

# get_image - gets the image of a pokemon
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int form_id - the form id of the pokemon
# returns str - the path of the image
def get_image(mysql_cursor, session_id : int, form_id : int) -> str:
    mysql_cursor.execute(
    f"""
        SELECT image_path FROM images WHERE form_id = {form_id};
    """)
    res = mysql_cursor.fetchone()
    if res is None:
        return res
    else:
        return res[0]

# get_move_details - gets the details about a move
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int move_id - the move to check
# returns - the move's details
def get_move_details(mysql_cursor, session_id : int, move_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM moves WHERE move_id = {move_id};
    """)
    return mysql_cursor.fetchone()

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
    return mysql_cursor.fetchall()

# get_item_details - gets the details about an item
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int item_id - the item to check
# returns - the item's details
def get_item_details(mysql_cursor, session_id : int, item_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM items WHERE item_id = {item_id};
    """)
    return mysql_cursor.fetchone()

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
    return mysql_cursor.fetchall()

# get_nature_details - gets the details about a nature
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int nature_id - the nature to check
# returns - the nature's details
def get_nature_details(mysql_cursor, session_id : int, nature_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM natures WHERE nature_id = {nature_id};
    """)
    return mysql_cursor.fetchone()

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
    return mysql_cursor.fetchall()

# get_user_teams - gets all teams belonging to the current user
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns - the list of the active user's teams
def get_user_teams(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT teams.team_id, sessions.user_id, teams.team_name FROM teams INNER JOIN sessions ON sessions.session_id = {session_id} AND teams.user_id = sessions.user_id;
    """)
    return mysql_cursor.fetchall()

# get_team_pokemon - gets all pokemon on a specific team
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int team_id - the team to query
# returns - the list of the pokemon on the team
def get_team_pokemon(mysql_cursor, session_id : int, team_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM pokemon WHERE team_id = {team_id};
    """)
    return mysql_cursor.fetchall()

# get_pokemon_details - gets the details about a pokemon
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# int pokemon_id - the pokemon to check
# returns - the pokemon's details
def get_pokemon_details(mysql_cursor, session_id : int, pokemon_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM pokemon WHERE pokemon_id = {pokemon_id};
    """)
    return mysql_cursor.fetchone()

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
    return mysql_cursor.fetchone()

# get_pokemon_popularity - gets the data in the pokemon popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns the pokemon popularity table
def get_pokemon_popularity(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM pokemon_popularity NATURAL JOIN forms;
    """)
    return mysql_cursor.fetchall()

# get_type_popularity - gets the data in the type popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns the type popularity table
def get_type_popularity(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM type_popularity NATURAL JOIN type_chart;
    """)
    return mysql_cursor.fetchall()

# get_item_popularity - gets the data in the item popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns the item popularity table
def get_item_popularity(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM item_popularity NATURAL JOIN items;
    """)
    return mysql_cursor.fetchall()

# get_move_popularity - gets the data in the move popularity table
# connector mysql_cursor - the link to the database
# int session_id - the current session token
# returns the move popularity table
def get_move_popularity(mysql_cursor, session_id : int):
    mysql_cursor.execute(
    f"""
        SELECT * FROM move_popularity NATURAL JOIN moves;
    """)
    return mysql_cursor.fetchall()
