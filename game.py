import random
from collections import Counter

CATEGORIES = [
    'ones', 'twos', 'threes', 'fours', 'fives', 'sixes',
    'three_kind', 'four_kind', 'full_house',
    'small_straight', 'large_straight',
    'yahtzee',
    'chance'
]

def roll_dice():
    # randomly roll 5 dice as initial roll
    return [random.randint(1,6) for _ in range(5)]

def reroll(dice, keep):
    # if dice is not kept, randomly reroll the remaining dice
    return [dice[i] if keep[i] else random.randint(1,6) for i in range(5)]

def score(dice, category):
    counts = Counter(dice)
    total = sum(dice)

    # upper section scoring
    # score = category * # of category dice in hand
    if category == 'ones': 
        return counts[1]
    if category == 'twos': 
        return counts[2]*2
    if category == 'threes': 
        return counts[3]*3
    if category == 'fours': 
        return counts[4]*4
    if category == 'fives': 
        return counts[5]*5
    if category == 'sixes': 
        return counts[6]*6

    # lower section scoring
    # 3- and 4-of-a-kind are totals of the hand
    if category == 'three_kind':
        return total if max(counts.values()) >= 3 else 0

    if category == 'four_kind':
        return total if max(counts.values()) >= 4 else 0

    # full_house, straights, and yahtzee are fixed scores if in hand
    if category == "full_house":
        return 25 if sorted(counts.values()) == [2,3] else 0

    if category == "small_straight": # four dice straight
        sets = [{1,2,3,4},{2,3,4,5},{3,4,5,6}]
        return 30 if any(s.issubset(dice) for s in sets) else 0

    if category == "large_straight": # five dice straight
        return 40 if set(dice) in [{1,2,3,4,5},{2,3,4,5,6}] else 0

    if category == "yahtzee": # five of a kind
        return 50 if max(counts.values()) == 5 else 0

    if category == "chance": # sum of hand
        return total

def play_game(strategy):
    # keep track of all available categories as rounds progress
    available = set(CATEGORIES)
    
    # track overall score and upper section score for bonus
    total_score = 0
    upper_score = 0

    # 13 rounds/categories for full game 
    for _ in range(len(available)): 
        # ititial roll 
        dice = roll_dice()

        # remaining rolls
        for roll in range(2):
            keep = strategy.choose_dice(dice, available, rolls_left=2-roll)
            dice = reroll(dice, keep)

        # for each strategy, pick a remaining category based on final hand
        category = strategy.choose_category(dice, available)
        
        # keep score
        points = score(dice, category)
        total_score += points

        # upper section bonus scoring
        if category in ['ones','twos','threes','fours','fives','sixes']:
            upper_score += score(dice, category)
        
        # update available categories
        available.remove(category)
    
    # apply upper section bonus
    if upper_score >= 63:
        total_score += 35

    return total_score