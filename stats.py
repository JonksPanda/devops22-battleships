import sqlite3
import os

class stats:
    
    def __init__(self) -> None:
        self.path = f"{os.path.dirname(os.path.realpath(__file__))}/data/game_data.db" #https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
        
        #used example https://github.com/fictive-reality/devops22-python/blob/master/lesson_11/examples/7_sql_basics.py
        #Stores all stats from previous games
        self.CREATE_TABLE_STATS = '''
                CREATE TABLE IF NOT EXISTS statistics(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    winner TEXT,
                    turns INT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                )
                '''
        
        

    def save_stats(self, winner, turns):
        #used example https://github.com/fictive-reality/devops22-python/blob/master/lesson_11/examples/7_sql_basics.py
        with sqlite3.connect(self.path, isolation_level=None) as conn:
            conn.execute(self.CREATE_TABLE_STATS)
            conn.execute("INSERT INTO statistics(winner, turns) VALUES(?, ?)", (winner, turns))
    
    def load_stats(self):
        with sqlite3.connect(self.path, isolation_level=None) as conn:
            conn.execute(self.CREATE_TABLE_STATS)
            cursor = conn.cursor()
            cursor.execute("SELECT winner, turns, timestamp FROM statistics")

            rows = cursor.fetchall()

            for row in rows:
                print(row)
            input()

def main():
    stats().load_stats()

if __name__ == "__main__":
    main()