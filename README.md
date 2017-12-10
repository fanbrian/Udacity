# Udacity

Python code and jupyter notebook used for a data wrangling project for Udacity's Data Analyst Nanodegree course. The task was to audit, clean, and prepare OpenStreetMap data (XML) for insertion into a database. A local database was created using SQL and queried to find any residual issues.

First, a custom API call was made to the Overpass API to pull the XML data for the Seattle metropolitan area (~250MB). A small sample of this larger file was utilized to test the preliminary code. The XML data was then parsed using ElementTree in python to create dictionaries for different data types. These python dictionaries were then used to create a local SQL database that was queried to detect problems with the data, and python parsing functions were updated to remedy the issues found (fixing double entries, truncating postal codes, etc.) and the XML data was reprocessed. The reprocessed data was then loaded into another SQL database for final verification that problems were addressed.

(the jupyter notebook is rather large so might fail to load on the first try)
