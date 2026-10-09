class Strategy:
    def choose_dice(self, dice, available, rolls_left):
        raise NotImplementedError

    def choose_category(self, dice, available):
        raise NotImplementedError

import random

# baseline strategy
class RandomStrategy(Strategy):
    # for each die in hand, randomly pick which die to keep/reroll in hand
    def choose_dice(self, dice, available, rolls_left):
        return [random.choice([True, False]) for _ in dice]
    
    # randomly pick an available category for each round
    def choose_category(self, dice, available):
        return random.choice(list(available))

from collections import Counter
from game import score

# short-term maximize points (take the best immediate score each round)
class GreedyStrategy(Strategy):
    def choose_dice(self, dice, available, rolls_left):
        counts = Counter(dice) # count how many of each die in hand
        val, freq = counts.most_common(1)[0] # find the number with the highest frequency

        # if hand has at least 3 of a kind
        if freq >= 3:
            return [d == val for d in dice] # keep all die of the most common value 
        
        # check for hands with almost straights
        if len(set(dice)) >= 4: # if have at least 4 unique die
            # if on last roll, keep the small straight
            if rolls_left == 0:
                return [True]*5 
            return [dice.count(d) == 1 for d in dice]

        # check if hand has the central straight (most flexibility for creating straights) and keep those values
        if set(dice).intersection({2,3,4,5}):
            return [d in [2,3,4,5] for d in dice]

        # otherwise, just keep the most frequent number
        return [d == val for d in dice]

    def choose_category(self, dice, available):
        # track best category found so far
        best_cat = None
        best_score = -1

        # calculate score for each possible category
        for cat in available:
            s = score(dice, cat)

            # small penalty for using chance early
            if cat == "chance":
                s -= 5

            # keep the highest scoring category
            if s > best_score:
                best_score = s
                best_cat = cat

        # plan b: if there is no best cat, sacrifice the least scoring category
        if best_cat is None:
            best_cat = min(available, key=lambda c: score(dice, c))

        return best_cat

# greedy + sacrificing plan 
class HeuristicStrategy(Strategy):
    def choose_dice(self, dice, available, rolls_left):
        # find the most fequent die
        counts = Counter(dice)
        val, freq = counts.most_common(1)[0]

        # keep high match for yahztee or 4 of a kind
        if freq >= 3:
            return [d == val for d in dice]

        # if at least straight, keep it
        if len(set(dice)) >= 4:
            return [True]*5 if rolls_left == 0 else [d in set(dice) for d in dice]

        # check for and keep central straight values
        if set(dice).intersection({2,3,4,5}):
            return [d in [2,3,4,5] for d in dice]

        # otherwise, keep most frequent value (greedy approach)
        return [d == val for d in dice]
    
    def choose_category(self, dice, available):
        # calc score for each cat all at once
        scores = {cat: score(dice, cat) for cat in available}

        # pick the cat with the highest score
        best_cat = max(scores, key=scores.get)

        # if there are any positive scores, take it (prioritize immediate reward unless everything bad)
        if scores[best_cat] > 0:
            return best_cat

        # determine rank for dumping bad rolls
        # low-value first, high-value last
        sacrifice_order = [
            "ones",
            "twos",
            "threes",
            "fours",
            "chance",
            "three_kind",
            "four_kind",
            "fives","sixes",
            "full_house",
            "small_straight",
            "large_straight",
            "yahtzee"
        ]

        # plan b: pick first available category by sacrifice rank
        for cat in sacrifice_order:
            if cat in available:
                return cat