import mysql.connector
from mysql.connector import Error
import mysql.connector.errors as sqlerrors
from app import tkinterApp
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
 
def main():
    cfg = DbConfig()
    conn = None
    app = None
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

    except (sqlerrors.InterfaceError, sqlerrors.ConnectionTimeoutError) as e:
        print("Error conecting to database - Have you changed the database config to your setup?")
        print(f"Details: [SQL ERROR @ main] {e.msg} | errno: {e.errno} | sqlstate: {e.sqlstate}")
    except (sqlerrors.ProgrammingError) as e:
        print(f"[SQL ERROR @ main] {e.msg} | errno: {e.errno} | sqlstate: {e.sqlstate}")
        print("Please ensure your database has all the required tables")
    except Error as e:
        print(f"[SQL ERROR @ main] {e.msg} | errno: {e.errno} | sqlstate: {e.sqlstate}")
    except Exception as e:
        print(f"[STD ERROR] {e}")
    finally:
        if conn and conn.is_connected():
            if app:
                if app.session != 0:
                    sql.logout(app.cursor, app.session)
                    print("Successfully logged out.")
                app.closeCursor()
            conn.close()
            print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    main()