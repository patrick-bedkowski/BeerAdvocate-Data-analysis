import pandas as pd
import numpy as np
from tabulate import tabulate
from typing import List

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

if len(max_abv_beers_indecies) < 2:  # if there is only one beer with the highest abv
    # print the name of the brewery that produces beer with highest abv
    print(f'Beer with maximum abv is produced by brewery: \n\t> {df["brewery_name"][max_abv_beer_index]}')
else:
    print('Beers with maximum abv are produced by breweries:')
    for index in max_abv_beers_indecies:
        print(f'\t> {df["brewery_name"][index]}')


# =================================================== #
# If you had to pick 3 beers to recommend to someone, #
# how would you approach the problem?                 #
# =================================================== #

'''
My solution regards recommending specific beers based on number of best overall reviews.

To answer this question, I will break down the solution into the following parts:
    1. Create a data stating how many times each beer have received maximum score.
    Bypassing data from the database (*)
    2. Find 3 beers which have the most number of maximum overall reviews
    and are of different beer style

(*) Found problems:
When you run the query:
SELECT
review_appearance, review_aroma, review_palate, review_taste, review_overall
FROM beer_reviews where review_time=1235954167

You can see that the review of review_time=1235954167 has review_overall of 5.0,
but all the partial reviews are in range 2.0-3.0. This indicates that in the dataset
there is some false data.

To eliminate the false data you can run the query:
SELECT
review_appearance, review_aroma, review_palate, review_taste, review_overall
FROM beer_reviews WHERE review_appearance >=4 AND review_aroma>=4 AND review_palate>=4
AND review_taste>=4 GROUP BY review_time
HAVING AVG(review_appearance+review_aroma+review_palate+review_taste) >= 4
'''

max_score = max(df['review_overall'])  # max score achieved by any beer
n_of_indecies = len(df.index)  # number of rows from dataframe

n_of_beer_reviews = {}  # dict that holds how many times specific beer has received max score reviews and its style
GOOD_REVIEW = 4.0  # parameter that indicates if review is considered good 
# The results heavly depends on this parameter 

def partialReview(index: int) -> bool:
    '''
    Returns TRUE, if all partial reviews of specific index are greater than 
    constant value. Otherwises, returns False. 
    '''
    # create partial reviews list
    p_review_list =  [
            df['review_appearance'][index],
            df['review_aroma'][index],
            df['review_palate'][index],
            df['review_taste'][index]
        ]

    for review in p_review_list:  # iterate through each review value
        if review >= GOOD_REVIEW:  # if review greater or equal than parameter
            continue
        else:
            return False
    return True
    '''Average equal to overall review
    average = np.average(p_review_list)
    return True if average == df['review_overall'][index] else False'''

for index in range(n_of_indecies):  # iterate through indecies
    if df['review_overall'][index] == max_score:  # if review is max score
        # (*) Filter the false data here
        if partialReview(index):  # if every partial review is greater than parameter 
            beer_name = df['beer_name'][index]
            beer_style = df['beer_style'][index]
            if beer_name not in n_of_beer_reviews.keys():  # if beer name not in dictionary
                n_of_beer_reviews[beer_name] = [1, beer_style]
            else:
                n_of_beer_reviews[beer_name][0] += 1  # increase number of max score reviews
        else:
            continue

# sort a dictionary by descending value using lambda function
n_of_beer_reviews = {k: v for k, v in sorted(n_of_beer_reviews.items(), key=lambda item: item[1], reverse=True)}

best_beers = [] # best beers data
for beer_name, [beer_score, beer_style] in n_of_beer_reviews.items():  # iterate through dictionary
    if len(best_beers) == 3:
        break
    else:
        beer_styles = (beer_data[2] for beer_data in best_beers)
        if beer_style in beer_styles: # if there is a beer with the same style
            continue
        else:
            best_beers.append([beer_name, beer_score, beer_style])

print(tabulate(best_beers, tablefmt="fancy_grid", headers=["Rank", "Beer name", "Number of best reviews", 'Beer style'], showindex=[1,2,3]))
