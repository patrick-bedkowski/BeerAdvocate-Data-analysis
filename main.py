import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from torch.utils.data.dataset import random_split
from plotter import plot_mean_abv, plot_distribution_abv, plot_reviews_number

def distribution_abv(df: pd.DataFrame) -> None:
    # drop unnecessary columns
    brewery_data = df.drop(columns=['review_time', 'review_overall', 'review_aroma', 'review_appearance', 'review_profilename', 'beer_style', 'review_palate', 'review_taste', 'beer_beerid', 'brewery_id', 'brewery_name'])

    # drop beer duplicates
    
    brewery_data = brewery_data.drop_duplicates(subset = 'beer_name')
    
    # plot abv distribution
    # plot_distribution_abv(brewery_data)

def task_1(df: pd.DataFrame) -> None:
    # ================================================== #
    # Which brewery produces the strongest beers by abv? #
    # ================================================== #

    # drop unnecessary columns
    brewery_data = df.drop(columns=['review_time', 'review_overall', 'review_aroma', 'review_appearance', 'review_profilename', 'beer_style', 'review_palate', 'review_taste', 'beer_name'])
    # rename column
    brewery_data = brewery_data.rename(columns={'beer_beerid': 'beer_id'})
    
    # remove duplicates of beer's. Now there is single id of each beer
    brewery_data = brewery_data.drop_duplicates(subset = 'beer_id')

    # group data by brewery names and count how many beers does one brewery offer
    brewery_beers = brewery_data.groupby('brewery_name').size().reset_index(name='count')

    # what is the median mean of how may beers brevery produces?
    print(f'Median of beers produced by brevery is: {np.median(list(brewery_beers["count"]))}')

    # calculate mean of beers abv produced by each brewery
    brewery_abv = brewery_data.groupby('brewery_name').mean().reset_index()
    brewery_abv = brewery_abv.drop(columns=['brewery_id', 'beer_id'])

    # merge dataframes so it contains: brewery name, mean abv, how many beers they produce
    brewery_count_abv = brewery_beers.merge(brewery_abv, on="brewery_name", how = 'inner')
    brewery_count_abv = brewery_count_abv.sort_values(by=['beer_abv'], ascending=False)  # sort values by beer abv mean
    brewery_count_abv['beer_abv'] = brewery_count_abv['beer_abv'].round(decimals=2)  # round the abv values
    brewery_count_abv = brewery_count_abv.set_index('brewery_name')

    # Filter breweries that produce more than 3 beers  
    brewery_count_abv = brewery_count_abv[(brewery_count_abv['count'] >= 4)]

    print(brewery_count_abv.head(10))
    # plot_mean_abv(brewery_count_abv)  # plot the data

'''
def task_2(df: pd.DataFrame) -> None:

    # drop unnecessary columns
    reviews_df = df.drop(columns=['review_time', 'review_overall', 'review_aroma', 'review_appearance', 'beer_style', 'review_palate', 'review_taste', 'beer_name', 'brewery_name', 'beer_abv', 'beer_beerid', 'brewery_id'])

    # how many reviews does each user posted
    reviews_df = reviews_df.groupby('review_profilename').size().reset_index(name='n_of_reviews')

    # group each review number with number of reviewers
    reviews_df = reviews_df.groupby('n_of_reviews').size().reset_index(name='group_reviews')

    print(reviews_df.head())
    # plot_reviews_number(reviews_df)

def reccommend() -> pd.DataFrame:
    df = pd.read_csv('beer_reviews.csv')  # for running locally
    df = df.dropna()  # delete rows that contain NULL value

    # drop unnecessary columns
    ratings_df = df.drop(columns=['review_time', 'review_aroma', 'review_appearance', 'beer_style', 'review_palate', 'review_taste', 'beer_name', 'brewery_name', 'beer_abv', 'brewery_id'])
    
    ratings_df['user_id'] = ratings_df.groupby('review_profilename').ngroup()
    # sorted
    ratings_df = ratings_df.sort_values(by=['user_id'], ascending=True)

    # drop profilename
    ratings_df = ratings_df.drop(columns=['review_profilename'])

    # rename column
    ratings_df = ratings_df.rename(columns={'beer_beerid': 'beer_id', 'review_overall': 'rating'})
    
    user_ratings = ratings_df.pivot_table(index=['user_id'],columns=['beer_id'],values='rating')
    print(user_ratings.head())'''


def task_2(df: pd.DataFrame) -> None:

    # =================================================== #
    # If you had to pick 3 beers to recommend to someone, #
    # how would you approach the problem?                 #
    # =================================================== #

    '''
    My solution regards recommending specific beers based on number of best overall reviews.

    To answer this question, I will break down the solution into the following parts:
        0. Bypasse false data from the database (*)
        1. Create a data stating mean score of each beer
        2. Find 3 beers which have the most number of maximum overall reviews
        and are of different beer style

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

    # print(tabulate(best_beers, tablefmt="fancy_grid", headers=["Rank", "Beer name", "Number of best reviews", 'Beer style'], showindex=[1,2,3]))


if __name__ == '__main__':

    # get the dataset and create a data frame
    df = pd.read_csv('https://query.data.world/s/epkvquv6dgo5zi337wa2n23div4i3w')
    #df = pd.read_csv('beer_reviews.csv')  # for running locally
    df = df.dropna()  # delete rows that contain NULL value

    # task_1(df)
    # distribution_abv(df)
    task_2(df)
