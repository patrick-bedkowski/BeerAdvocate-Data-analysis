import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, ScalarFormatter

# https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_label_demo.html

def plot_mean_abv(brewery_count_abv: pd.DataFrame) -> None:
    
    x_label = list(brewery_count_abv.index.values)[:10]
    y_label = list(brewery_count_abv['beer_abv'])[:10]
    annotations = list(brewery_count_abv['count'])[:10]

    y_pos = np.arange(len(x_label))
    fig, ax = plt.subplots(1, 2, figsize=(24, 10), sharey=True, gridspec_kw={'width_ratios':[2.75, 1]})

    # PLOT 1
    hbars = ax[0].barh(y_pos, y_label, align='center')
    ax[0].set_xticks(range(0, 28, 1))
    ax[0].set_xticklabels(labels=range(0, 28), fontsize=17)
    ax[0].set_yticks(y_pos)
    ax[0].set_yticklabels(x_label, fontsize=20)
    ax[0].invert_yaxis()  # labels read top-to-bottom
    ax[0].set_xlabel('ABV value [%]', fontsize=20)
    ax[0].set_title('ABV mean for each brewery', fontsize=22, pad=20)

    # Label with specially formatted floats
    ax[0].set_xlim(right=27)  # adjust xlim to fit labels
    ax[0].grid(color='grey', linestyle='-', linewidth=0.25)
    ax[0].bar_label(hbars, labels=y_label,
                padding=8, fontsize=20)
    

    # PLOT 2
    hbars2 = ax[1].barh(y_pos, annotations, align='center')
    ax[1].set_xticks(range(0, 61, 5))
    ax[1].set_xticklabels(labels=range(0, 61, 5), fontsize=17)
    ax[1].set_yticks(y_pos)
    ax[1].set_yticklabels(x_label, fontsize=20)
    ax[1].invert_yaxis()  # labels read top-to-bottom
    ax[1].set_xlabel('Number of beers produced', fontsize=20)
    ax[1].set_title('Number of beers produced by each brewery', fontsize=22, pad=20)

    # Label with specially formatted floats
    ax[1].set_xlim(right=60)  # adjust xlim to fit labels
    ax[1].grid(color='grey', linestyle='-', linewidth=0.25)
    ax[1].bar_label(hbars2, labels=annotations,
                padding=8, fontsize=20)

    # plt.xticks(np.arange(min(x_label), max(x_label)+1, 1.0))

    fig.tight_layout()
    plt.savefig("breweries_abv_count_15.png", dpi=100, bbox_inches='tight')


def plot_distribution_abv(brewery_data: pd.DataFrame) -> None:
    abv_values = list(brewery_data['beer_abv'])

    n_bins = 50

    kwargs = dict(alpha=1, bins=n_bins)
    fig, ax = plt.subplots()

    plt.figure(figsize=(16,10))
    plt.hist(abv_values, **kwargs, rwidth=0.85)
    plt.gca().set(title='Distribution of beer ABV', xlabel ='ABV value', ylabel='Number of beers')

    plt.grid(color='grey', linestyle='-', linewidth=0.25)
    plt.gca().xaxis.set_major_formatter(PercentFormatter(100))
    plt.box(False)  # borderless

    plt.savefig("abv_distribution.png", dpi=100, bbox_inches='tight')

def plot_reviews_number(reviews_data: pd.DataFrame) -> None:
    reviews_count = list(reviews_data['group_reviews'])
    n_of_reviews = list(reviews_data['n_of_reviews'])
    
    fig, ax = plt.subplots(figsize=(16,10))
    # plt.bar(n_of_reviews, reviews_count,width=0.5)
    # wdh = [0.5*(10**x) for x in range(0,len(reviews_count))]
    ax.plot(n_of_reviews, reviews_count, 'o')

    ax.set_xscale('log')
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    
    ax.set_xlabel('Number of reviews')
    ax.set_ylabel('Number of reviewers')

    plt.grid(color='grey', linestyle='-', linewidth=0.25)

    plt.box(False)  # borderless

    plt.savefig("reviews_number.png", dpi=100, bbox_inches='tight')
