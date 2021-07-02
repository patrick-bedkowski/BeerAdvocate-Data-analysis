'''
Could you provide an answer for the question:

- Which brewery produces the strongest beers by abv ?

And for ONE selected question out of the followings:
- If you had to pick 3 beers to recommend to someone, how would you approach the problem ?
- What are the factors that impacts the quality of beer the most ?
- I enjoy a beer which aroma and appearance matches the beer style. What beer should I buy?
'''
import pandas as pd
import numpy as np

# get the dataset and create a data frame
df = pd.read_csv('https://query.data.world/s/epkvquv6dgo5zi337wa2n23div4i3w')
# df = pd.read_csv('beer_reviews.csv')  # for running locally

# get the index of a beer with highest abv
max_abv_beer_index = list(df["beer_abv"]).index(max(df["beer_abv"]))

# print all the data representing beer with highest abv
# print(f'Maximum beer abv: {df.loc[max_abv_beer_index]}')

# print the name of the brewery that produces beer with highest abv
print(f'Beer with maximum abv is produced by brewery: {df["brewery_name"][max_abv_beer_index]}')