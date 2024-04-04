import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
from textblob import TextBlob

#I will be using the csv I made in apiCall.py rather than the one in scraping.py
#reading in 2 df's (api call data and google reviews data)
df1 = pd.read_csv('api_store_details.csv')
df2 = pd.read_csv('technicalAssessment-GoogleReviews.csv')

#debug
print(df1.head())
print(df2.head())

#merging the df's based on storeID
complete_df = pd.merge(df1, df2, on=['storeID'], how= 'inner')
print(complete_df.head())

#uncomment below line to export an updated version of the full data csv file
#complete_df.to_csv('fullData.csv')



#uncomment the block representing the graph you would like to view. You may uncomment all blocks simultaneously to view all visualizations. 



# #GRAPH 1 - locationName X overallRating
# #sort data by overall rating
# complete_df = complete_df.sort_values('overallRating', ascending=True)

# #plotting locationName based on overallRating
# plt.rcParams.update({'font.size': 8})
# plt.figure(figsize=(15, 9))
# sns.barplot(x='overallRating', y='locationName', data=complete_df, palette='viridis')
# plt.title('Overall Ratings by Location')
# plt.xlabel('Overall Rating')
# plt.ylabel('Location Name')
# plt.tight_layout()
# plt.show()





# #GRAPH 2 - locationName X numReviews
# #sort df by numberReviews
# complete_df = complete_df.sort_values('numberReviews', ascending=True)

# #plotting locationName based on number of reviews
# plt.figure(figsize=(15, 9))
# sns.barplot(x='numberReviews', y='locationName', data=complete_df, palette='viridis')
# plt.title('Number of Reviews by Location')
# plt.xlabel('Number of Reviews')
# plt.ylabel('Location Name')
# plt.tight_layout()
# plt.show()





# #GRAPH 3
# #plot locationName by geographical area, color coded by overallRating
# gdf = gpd.GeoDataFrame(complete_df, geometry=gpd.points_from_xy(complete_df.lng, complete_df.lat))

# #loading base map and getting US map
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# us_map = world[world.name == "United States of America"]

# #plotting basemap
# fig, ax = plt.subplots(figsize=(15, 10))
# us_map.plot(ax=ax, color='white', edgecolor='black')

# #plotting data on top of basemap
# gdf.plot(ax=ax, column='overallRating', cmap='RdYlGn', legend=True, 
#          legend_kwds={'label': "Store Rating", 'orientation': "horizontal"})
# plt.show()




# #GRAPH 4 - Same as 3 but zoomed in to clusters
# gdf = gpd.GeoDataFrame(complete_df, geometry=gpd.points_from_xy(complete_df.lng, complete_df.lat))
# bounds = gdf.total_bounds

# fig, ax = plt.subplots(figsize=(15, 10))

# #plot base map
# us_map.plot(ax=ax, color='white', edgecolor='black')

# #plotting data
# gdf.plot(ax=ax, column='overallRating', cmap='RdYlGn', legend=True,
#          legend_kwds={'label': "Store Rating", 'orientation': "horizontal"})

# #zooming on clusters
# ax.set_xlim([bounds[0], bounds[2]])
# ax.set_ylim([bounds[1], bounds[3]])
# plt.show()




# #analysis 5 - determining the top 10 reviewers and what ratings they typically give
# reviewer_counts = complete_df['reviewer'].value_counts()

# #finding range of reviews for each reviewer
# reviewer_stats = complete_df.groupby('reviewer')['reviewRating'].agg(['max', 'min'])

# #combining data
# reviewer_summary = reviewer_stats.merge(reviewer_counts.rename('count'), left_index=True, right_index=True)

# #finding top reviewers by who has left most reviews
# top_reviewers = reviewer_summary.sort_values(by='count', ascending=False).head(10)

# print(top_reviewers)





# #analysis 6 - overall sentiment of reviews by location, display 5 best and 5 worst 
# #making funciton to look into sentiment
# def get_textblob_sentiment(text):
#     return TextBlob(text).sentiment.polarity if pd.notna(text) else None

# #applying function
# complete_df['sentiment'] = complete_df['reviewText'].apply(get_textblob_sentiment)

# #group by locationName and calculate the mean sentiment for each location
# location_sentiments = complete_df.groupby('locationName')['sentiment'].mean()

# #getting top and bottom 5 location by avg sentiment
# best_sentiment = location_sentiments.nlargest(5)
# worst_sentiment = location_sentiments.nsmallest(5)

# print(best_sentiment)
# print(worst_sentiment)