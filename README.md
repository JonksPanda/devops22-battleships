# devops22-battleships

## Description
This battleship game is made as an examination-project for a Python-Course. For now, you can only play singleplayer vs AI. 
The program is written in Python and uses some SQL

---
## How to run the game

Start main.py to run the game properly.

---
## How to play

X
: Horizontal

Y
: Vertical

Direction
: left, right, up, down

1. Place ships on your board. Enter X-coordinate, Y-coordinate and direction. Ex. (6,7,down)
  - Rules:
   - The whole ship must be on the board
   - Ships can't be place on top of each other
   - Ships can't be placed adjacent to each other
2. Shoot opponents on board. Enter X-coordinate and Y-coordinate to decide where to shoot. Ex. (3,4)
  - Rules:
    - If a target is hit. The player can shoot again, until miss
    - The same coordinate can't be shot twice
3. First to destroy all opponent ships wins.

---
## Extra features added
- "Smarter" AI
- Automatic ship-placement for AI
- Statistics
- History of previously played games (winner, how many turns it took and time/date(Note that the timestamp is broken. It the returns time from wrong timezone))

---
## To do-list

- [x] Create Repo
- [x] Make new branch
- [x] Make a plan on how to structure program
- [x] Add all python-files neccesary for the base
- [x] Code the base
  - [x] Create a board-generator
  - [x] Create a function to place all ships on board
    - [x] Let player input placements
    - [x] add so that AI can put ships on board
    - [x] add a funtion to read file with AI-placements
  - [x] Add funtion to let player shoot ships on board
    - [x] Add so that AI also can shoot the players ship on board
  - [x] Add function that that register who won and how many tries it took
- [x] Add extra-stuff
  
---
## Structure

- main.py
  - Runs the program and adds neccessary folders
- menu.py
  - Main menu for the game
- board.py
  - Store functions related to displaying and populating the players board
- player.py
  - Where player and AI class is
  - All player/AI-related logic is here
- game.py
  - Prepares the game-settings and runs the game-loop
- statistics.py
  - SQL-related stuff. Shows general stats from games

---
## Possible Improvements

- Color to make features on board more visible
- ~~Ability to exit game~~
- Ability to save game