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
2. The application is split into differing sections - Player Management, Combine, Passing, Rushing, Receiving and League Standings.  This is due to the design of the underlying datasets available from Kaggle.  Our original intention was to join all player-level data into a larger dataset for analysis.  Unfortunately, the join keys are not consistent among the datasets (e.g. playerId in the receiving dataset for a particular player does not match the playerId in the rushing dataset for that same player).  This necessitated us analyzing each dataset "separately", which is why we have different sections of the site to 
