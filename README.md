# Retail-Database
This application is used to search for sales within a randomly generated dataset given some query. Made with python3 and sqlite. python3 library tkinter is used as the UI. sqlite3 is used to connect to a database.

Below "Please input search criteria" is the primary command dropbox followed by the subcommand dropbox. The "Edit" command is not finished yet and cannot be used. All the other commands require a subcommand to specify what type of query you are searching for.

Search by ID: searches by Sales Team ID, Customer ID, Store ID, or Product ID.

Search by Location: searches by City Name, State Code, Time Zone, County and Region. The data regarding these queries exist in an entirely different table within the database, so a JOIN is called.

Search by Other: searches by Order Number, Sales Channel, or Warehouse Code. This function searches based off of some thematically miscellaneous criteria. 

Edit: a work in progress. It's meant to add, delete, or update existing data.
