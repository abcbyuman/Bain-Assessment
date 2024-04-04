The 3 tasks I was given:
-

1. Extract the la Madeleine Restaurant locations from their “Locations” page using JavaScript or Python
2. Associate the locations with the provided Google Reviews
3. Draft a single slide presentation highlighting any data-driven insights you have gleaned from the location data and reviews

My solution:
-
Step 1 is done 2 different ways:  
 a) I first scraped the webpage as I was more comfortable doing that and wanted to make sure I had something to show. This was done in the 'scraping.py' file.  
 b) I then looked into working with the API. This ended up being faster, so I opted to use this file moving forward - 'apiCall.py'  

Step 2 is done in the 'dataAnalytics.py' file. It combines the csv from google reviews with my csv from the api call to create 'fullData.csv' (accessible above). Then I conduct some basic data visualization to gain some insights.

Step 3 can be accessed at this link:
https://docs.google.com/presentation/d/1TLHagNDSG8zDxUm_erJTPd3-UwKmcBudOVyxsQ9e0eM/edit?usp=sharing
