# Data analysis of a data set - BeerAdvocate

<br />

## Table of Contents

1. [Tackled questions](#tackled-questions)
    1. [Question 1](#question-1)
    2. [Question 2](#question-2)
2. [Worth noting](#worth-noting)

<br />

## Tackled questions
1. Which brewery produces the strongest beers by abv?
2. If you had to pick 3 beers to recommend to someone, how would you approach the problem?

<br />

### Question 1

<h4><b>Which brewery produces the strongest beers by abv?</b></h4>

<img src="images\breweries_abv_count.png" alt="breweries_abv_count"/>

### Summary

One can see that the <b><i>Schorschbräu</i></b> brewery has the highest average ratio of abv value among its beers. It also produces most number of beers among shown breweries.<br />
On the other hand, one cannot simply choose other breweries that produce the strongest beers. See that next brewery with the highest average ratio of abv is <b><i>Shoes Brewery</i></b>, it only produces 1 beer.<br /><br />

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

<br />

### Question 2

Update incomming

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