import numpy as np
from scipy import stats

# calc summary stats
def summarize(scores):
    # measure performance 
    mean = np.mean(scores)
    std = np.std(scores)

    # measure uncertainty
    n = len(scores)
    ci = 1.96 * std / np.sqrt(n) # 95% CI
    return mean, (mean-ci, mean+ci)

# compare strategies
def compare(a, b):
    # independent two-sample t-test
    return stats.ttest_ind(a, b)

import matplotlib.pyplot as plt

# plot distribution score vs. freq for each strategy
def plot(scores_dict):
    for name, scores in scores_dict.items():
        plt.hist(scores, bins=50, alpha=0.5, label=name)

    plt.legend()
    plt.title("Score Distribution")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.show()