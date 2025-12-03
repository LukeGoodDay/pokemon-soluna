# Pokémon Soluna
### Team Members: Kyle Chiasson, Will Krietemeyer, Luke Welday
## Goal
&emsp;Pokémon Soluna will act as a Pokémon Sun and Moon companion app. It will provide detailed information on all the Pokémon, moves, and items found throughout the game. This app will also allow users to create and save potential teams within the app to help map out their playthroughs.  
## Set Up
&emsp;1.&emsp;Set up MySQL Environment (https://dev.mysql.com/)  
&emsp;2.&emsp;In your MySQL Environment, run [DatabaseStaging.sql](./SQL/DatabaseStaging.sql)  
&emsp;3.&emsp;Run [DatabaseTables.sql](./SQL/DatabaseTables.sql)  
&emsp;4.&emsp;Run [DatabaseCleaning.sql](./SQL/DatabaseCleaning.sql)  
&emsp;5.&emsp;Run [RegisterDefaultUser.sql](./SQL/RegisterDefaultUser.sql)  
&emsp;6.&emsp;Run "pip install mysql-connector-python" in your terminal  
&emsp;7.&emsp;Finally, run [Python.py](./Python/main.py)
## Datasets
&emsp;•&emsp;Pokémon Sun and Moon Data - https://www.kaggle.com/datasets/mylesoneill/pokemon-sun-and-moon-gen-7-stats/data?select=pokemon.csv  
&emsp;•&emsp;Pokémon Images - https://www.kaggle.com/datasets/arenagrenade/the-complete-pokemon-images-data-set  
&emsp;•&emsp;Pokémon Sun and Moon Wonder Trade Stats - https://data.world/notgibs/pokemon-wonder-trade-results  
&emsp;•&emsp;Steps Required to Hatch Pokémon - https://www.kaggle.com/datasets/rachellecha/egg-hatching-step-counts-in-pokemon  
## ER Diagram
![Alt text](./FinalProjectDiagram.png)
## Interaction
### Accounts
&emsp;•&emsp;Users can sign up / log in / log out  
### Team Building
&emsp;•&emsp;Users can create / edit / delete Pokémon teams  
&emsp;•&emsp;Users can prompt the software for the type matchups/coverage for Pokémon team  
### Wonder Trades
&emsp;•&emsp;App will provide information on wonder trade chance for each Pokémon  
&emsp;•&emsp;Users can submit data on pokemon they recieve through wonder trades 
### Pokedex
&emsp;•&emsp;App will provide information on all Pokémon, moves, and items found throughout the game  
### Insights
&emsp;•&emsp;App will provide statistics on most popular Pokémon, items, moves, and types  
&emsp;•&emsp;App will provide statistics on Wonder Trade chances
## Video
[Download Video](https://raw.githubusercontent.com/LukeGoodDay/pokemon-soluna/main/checkpoint2.mp4)
