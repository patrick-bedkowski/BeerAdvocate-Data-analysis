# Recruitment tasks

1. Which brewery produces the strongest beers by abv ?
2. If you had to pick 3 beers to recommend to someone, how would you approach the problem ?

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

## Solution
<img src="exercise_2.png" alt="exercise_2"/>