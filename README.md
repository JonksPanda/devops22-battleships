# devops22-battleships

## To do-list

- [x] Create Repo
- [x] Make new branch
- [x] Make a plan on how to structure program
- [ ] Add all python-files neccesary for the base
- [ ] Code the base
  - [ ] Create a board-generator
  - [ ] Create a function to place all ships on board
    - [ ] Let player input placements
    - [ ] add so that AI can put ships on board
    - [ ] add a funtion to read file with AI-placements
  - [ ] Add funtion to let player shoot ships on board
    - [ ] Add so that AI also can shoot the players ship on board
  - [ ] Add function that that register who won and how many tries it took
- [ ] Add extra-stuff
  
---
## Structure

- main.py
  - *runs the program*
- menu.py
  - *runs a menu that let's the player start a new game, see stats etc.*
- board.py
  - *Where class for board should be*
- player.py
  - *Where class for player should be and player-releated tasks*
  - *Should probably add AI here aswell*
- game.py
  - *runs the game*
- statistics.py
  - *let's player se stats from previous games*