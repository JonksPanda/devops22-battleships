import sqlite3
import os
import menu

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
        #Initiates sql-connection
        self.conn = sqlite3.connect(self.path, isolation_level=None)
        self.conn.execute(self.CREATE_TABLE_STATS)
        

    def save_stats(self, winner, turns):
        #used example https://github.com/fictive-reality/devops22-python/blob/master/lesson_11/examples/7_sql_basics.py
        self.conn.execute("INSERT INTO statistics(winner, turns) VALUES(?, ?)", (winner, turns))
    
    def load_stats(self, player):
        cursor = self.conn.cursor()
        if player == "":
            cursor.execute("SELECT winner, turns, timestamp FROM statistics")
        else:
            cursor.execute("SELECT winner, turns, timestamp FROM statistics WHERE winner LIKE ?", [player])

        rows = cursor.fetchall()
        turns = []
        most_wins = []

        print("Winner | Turns | Time")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]}")
            turns.append(row[1])
            most_wins.append(row[0])
        print(f"Most wins: {max(set(most_wins), key = most_wins.count)} | total games played: {len(rows)} | Average turns: {sum(turns) / len(turns)}\n") #How to get average https://www.geeksforgeeks.org/find-average-list-python/ https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/

    
    def stats_menu(self, player=""):
        self.load_stats(player)
        print("""
1. search player
2. exit to menu
        """)
        choice = input("option: ")
        if choice == "1":
            name = input("input name to search: ")
            os.system("cls")
            self.stats_menu(name)
        elif choice == "2":
            menu.main()
        else:
            os.system("cls")
            self.stats_menu()

def main():
    statistics = stats()
    statistics.stats_menu()

if __name__ == "__main__":
    main()