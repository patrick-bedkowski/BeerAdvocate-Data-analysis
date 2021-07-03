'''
And for ONE selected question out of the followings:
- If you had to pick 3 beers to recommend to someone, how would you approach the problem?
- What are the factors that impacts the quality of beer the most?
- I enjoy a beer which aroma and appearance matches the beer style. What beer should I buy?
'''
import pandas as pd
import numpy as np

# get the dataset and create a data frame
df = pd.read_csv('https://query.data.world/s/epkvquv6dgo5zi337wa2n23div4i3w')
# df = pd.read_csv('beer_reviews.csv')  # for running locally

# ================================================== #
# Which brewery produces the strongest beers by abv? #
# ================================================== #

'''Get the index of a beer with highest abv'''

max_abv_value = max(df["beer_abv"])
max_abv_beers_indecies = [list(df["beer_abv"]).index(max_abv_value) for beer_abv in list(df["beer_abv"]) if beer_abv == max_abv_value]
max_abv_beer_index = list(df["beer_abv"]).index(max_abv_value)

if len(max_abv_beers_indecies) > 1:
    # print the name of the brewery that produces beer with highest abv
    print(f'Beer with maximum abv is produced by brewery: {df["brewery_name"][max_abv_beer_index]}')
else:
    print('Beer with maximum abv are produced by breweries:')
    for index in max_abv_beers_indecies:
        print(df["brewery_name"][index])

# =================================================== #
# If you had to pick 3 beers to recommend to someone, #
# how would you approach the problem?                 #
# =================================================== #

max_score = max(df['review_overall'])  # max score achieved by any beer
number_of_rows = len(list(df['review_overall']))  # number of rows from dataframe

'''Find which beers achieved maximum overall review'''

# best_beers = []

# for index in range(number_of_rows):
#     if df['review_overall'][index] == max_score:
#         if df['beer_name'][index] not in best_beers:
#             best_beers.append(df['beer_name'][index])

# print(best_beers)

'''Find 3 beers which have the most number of maximum overall reviews'''

n_of_beer_reviews = {}  # dict that holds beer names and number of 5.0 reviews

for index in range(number_of_rows):
    if df['review_overall'][index] == max_score:
        beer_name = df['beer_name'][index]
        if beer_name not in n_of_beer_reviews.keys():
            n_of_beer_reviews[beer_name] = 1
        else:
            n_of_beer_reviews[beer_name] += 1

# sort a dictionary by value
sorted = {k: v for k, v in sorted(n_of_beer_reviews.items(), key=lambda item: item[1])}

print(list(sorted.items())[-3:])  # print 3 last elements from dict converted to a list
