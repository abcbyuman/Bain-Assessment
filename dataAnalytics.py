import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#I will be using the csv I made in apiCall.py rather than the one in scraping.py
#reading in 2 df's from api data and google reviews data
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

#sort data by overall rating
complete_df = complete_df.sort_values('overallRating', ascending=True)

#plotting locationName based on overallRating
plt.rcParams.update({'font.size': 8})
plt.figure(figsize=(15, 9))
sns.barplot(x='overallRating', y='locationName', data=complete_df, palette='viridis')
plt.title('Overall Ratings by Location')
plt.xlabel('Overall Rating')
plt.ylabel('Location Name')
plt.tight_layout()
plt.show()

#sort df by numberReviews
complete_df = complete_df.sort_values('numberReviews', ascending=True)

#plotting locationName based on number of reviews
plt.figure(figsize=(15, 9))
sns.barplot(x='numberReviews', y='locationName', data=complete_df, palette='viridis')
plt.title('Number of Reviews by Location')
plt.xlabel('Number of Reviews')
plt.ylabel('Location Name')
plt.tight_layout()
plt.show()


#print(complete_df.head())