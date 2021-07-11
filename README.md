# Data analysis of a data set - BeerAdvocate

<br />

## Table of Contents

1. [Tackled questions](#tackled-questions)
    1. [Preface](#preface)
    2. [Question 1](#question-1)
    3. [Question 2](#question-2)
2. [Worth noting](#worth-noting)

<br />

## Tackled questions
1. Which brewery produces the strongest beers by abv?
2. If you had to pick 3 beers to recommend to someone, how would you approach the problem?

<br />

### Preface

Firstly, 68'136 rows in the dataset contain at least one NULL value. That's ~ 4.29% of all reviews. I'm removing this data for further discussion.

<br />

### Question 1

<h4><b>Which brewery produces the strongest beers by abv?</b></h4>

To answer this question, we need to answer some questions that might direct us towards the answer. Let's plot a bar graph of abv value distribution among all beers.

<img src="images\abv_distribution.png" alt="breweries_abv_count"/>

One can see that the vast majority of beers have less than 10% abv. Furthermore, beers that have 20% or more abv are not visible on the graph.
From the following QUERY, one can find out that there are only <b>18</b> of these beers!

```
SELECT count(DISTINCT beer_name) FROM beer_reviews where beer_abv > 20
```

It might not be clear how to answer question of which brewery produces the strongest beers. But let's take a look at which brewery has the highest mean of abv among produced beers.

<img src="images\breweries_abv_count.png" alt="breweries_abv_count"/>

One can see that the <b><i>Schorschbräu</i></b> brewery has the highest average ratio of abv value among its beers. It also produces most number of beers among shown breweries.<br />
On the other hand, one cannot simply choose other breweries that produce the strongest beers, because some of them produce only 1 beer. See that next brewery with the highest average ratio of abv is <b><i>Shoes Brewery</i></b>, it only produces 1 beer.

The next step that could lead us to the answer might be looking at the median of beers produced by breweries. It is 4, because of that it seems resonable to choose only these breweries that produce more or equal to 4 beers. 

<img src="images\breweries_abv_count_mean.png" alt="breweries_abv_count_mean"/>

Now that we know the abv mean and how many beers are produced by each brewery, we can try to answer the given question.

<h4><b>Which brewery produces the strongest beers by abv?</b></h4>

1. <b>Schorschbräu</b> - is at the top because of the overwhelming abv mean, even though they only make 10 beers.

2. <b>AleSmith Brewing Company</b> - is another brewery worth considering. They make over 50 beers which is almost 3 times more than a mean of number of beers produced by these top 10. Its mean abv sits strong in the top 4.

<br />

<h4><b>SQL Query verification</b></h4>
To confirm the obtained results, one can run queries:<br /><br />

- How many distinct beers does each brewery produce
```
SELECT COUNT ( DISTINCT beer_beerid ) FROM beer_reviews WHERE brewery_name="<BREWERY_NAME>" AND (brewery_id IS NOT NULL) AND (brewery_name IS NOT NULL) AND (review_time IS NOT NULL) AND (review_overall IS NOT NULL) AND (review_aroma IS NOT NULL) AND (review_appearance IS NOT NULL) AND (review_profilename IS NOT NULL) AND (beer_style IS NOT NULL) AND (review_palate IS NOT NULL) AND (review_taste IS NOT NULL) AND (beer_name IS NOT NULL) AND (beer_abv IS NOT NULL) AND (beer_beerid IS NOT NULL);
```
- Number of breweries
```
SELECT COUNT ( DISTINCT brewery_name ) FROM beer_reviews WHERE (brewery_id IS NOT NULL) AND (brewery_name IS NOT NULL) AND (review_time IS NOT NULL) AND (review_overall IS NOT NULL) AND (review_aroma IS NOT NULL) AND (review_appearance IS NOT NULL) AND (review_profilename IS NOT NULL) AND (beer_style IS NOT NULL) AND (review_palate IS NOT NULL) AND (review_taste IS NOT NULL) AND (beer_name IS NOT NULL) AND (beer_abv IS NOT NULL) AND (beer_beerid IS NOT NULL);
```

<br /><br />

### Question 2

Update incomming

<br />

<h4><b>If you had to pick 3 beers to recommend to someone, how would you approach the problem?</b></h4><br />

To answer question 2. I will break down the solution into the following parts:
1. Create a data stating how many times each beer have received __maximum overall score__. __Bypassing false__ data from the database (*),
2. Find 3 beers which __have the most number of maximum overall reviews__ and __are of different beer style__.

(*) Found problems:
When the following query is run:
```
SELECT review_appearance, review_aroma, review_palate, review_taste, review_overall FROM beer_reviews where review_time = 1235954167
```

One can see that the review of __review_time = 1235954167__ has review_overall of 5.0,
but all the partial reviews are in range 2.0 - 3.0. This indicates that dataset contains false data.

To eliminate this problem I filter the data indecies which each partial review is smaller that __stated constant__ value (in this case 4.0).  
To apply those changes in mysql query, one can run:
```
SELECT review_appearance, review_aroma, review_palate, review_taste, review_overall
FROM beer_reviews WHERE review_appearance >=4 AND review_aroma>=4 AND review_palate>=4
AND review_taste>=4 GROUP BY review_time
HAVING AVG(review_appearance + review_aroma + review_palate + review_taste) >= 4
```

### Solution
<img src="images\exercise_2.png" alt="exercise_2"/>

## Worth noting

I. There might be corrupted data where a brewery with the same name is identified by different brewery_id