# CS180 Software Engineering Course Project
## Custom in memory data store with layered client-server architecture

We are using Django as the general framework for our web application. 

Upon cloning our repository, you should navigate to our application's "outer" directory (nfl_site) and run the following command (assuming Python and Django are installed on your local machine):
```{python}
python manage.py runserver
```
This will host our web application on your local machine on a local port (default to 8000)

## Notes about the application
1. All data in the application is based on data sources from https://www.kaggle.com/toddsteussie/nfl-play-statistics-dataset-2004-to-present
2. The application is split into differing sections - Player Management, Combine, Passing, Rushing, Receiving and League Standings.  This is due to the design of the underlying datasets available from Kaggle.  Our original intention was to join all player-level data into a larger dataset for analysis.  Unfortunately, the join keys are not consistent among the datasets (e.g. playerId in the receiving dataset for a particular player does not match the playerId in the rushing dataset for that same player).  This necessitated us analyzing each dataset "separately" (why the application separates the player statistics into different sections)
3. The Player Management site demonstrates add/edit/delete functionality to an in-memory dataset (players.csv), as well as save and load functionality
4. The Combine, Rushing, Receiving and Rushing sites demonstrate individual player statistics, add/edit/delete player functionality specific to the underlying datasets, and "incremental analytics" (e.g. small changes to the underlying data should not necessitate recomputing statistics from scratch, but should instead allow the statistics to update quickly.  Code execution time is returned to the site to demonstrate the improvement in processing time).
5. Team Standings site demonstrates data aggregation and dynamic rendering (team logos are all rendered dynamically in HTML based on the team name returned to the site via the user's selections on the page).


