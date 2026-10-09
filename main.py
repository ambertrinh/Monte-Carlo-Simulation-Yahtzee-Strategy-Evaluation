import numpy as np
from game import play_game
from strategies import RandomStrategy, GreedyStrategy, HeuristicStrategy
from analysis import summarize, compare, plot

# 100,000 trials
def run(strategy, N=100000):
    return np.array([play_game(strategy) for _ in range(N)])

def main():
    print("Running simulations...")

    random_scores = run(RandomStrategy())
    greedy_scores = run(GreedyStrategy())
    heuristic_scores = run(HeuristicStrategy())

    print("\n--- Results ---")

    for name, scores in {
        "Random": random_scores,
        "Greedy": greedy_scores,
        "Heuristic": heuristic_scores
    }.items():
        mean, ci = summarize(scores)
        print(f"{name}: Mean={mean:.2f}, CI={ci}")

    print("\n--- Hypothesis Test (Greedy vs Random) ---")
    t, p = compare(greedy_scores, random_scores)
    print(f"t={t:.3f}, p={p:.5f}")

    print("\n--- Hypothesis Test (Heuristic vs Random) ---")
    t, p = compare(heuristic_scores, random_scores)
    print(f"t={t:.3f}, p={p:.5f}")

    print("\n--- Hypothesis Test (Greedy vs Heuristic) ---")
    t, p = compare(greedy_scores, heuristic_scores)
    print(f"t={t:.3f}, p={p:.5f}")

    plot({
        'Random': random_scores,
        'Greedy': greedy_scores,
        'Heuristic': heuristic_scores
    })

if __name__ == "__main__":
    main()
