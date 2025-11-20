import mysql.connector
from mysql.connector import Error

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
    while True:
        res = int(input('Option #: '))
        if res in options:
            print()
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
        gender = input("gender: ")
        if gender != 'M' or gender != 'F':
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

def main():
    cfg = DbConfig()
    try:
        # Step 1: Connect to MySQL server (without specifying database yet)
        conn = mysql.connector.connect(
            host=cfg.host,
            port=cfg.port,
            user=cfg.user,
            password=cfg.password,
            # no database arg yet
        )
        if conn.is_connected():
            print("✅ Successfully connected to MySQL server")
        else:
            print("❌ Failed to connect to MySQL server")
            return

        conn.database = cfg.database

        create_team_terminal(conn)

    except Error as e:
        print_sql_error(e, "main")
    except Exception as e:
        print(f"[STD ERROR] {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    main()