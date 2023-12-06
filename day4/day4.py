import argparse
import re
import numpy as np
from pathlib import Path 

# rip tail recursion, curse you python
# def determine_win(game, cards, num, copies):
#     match = len(game[0].intersection(game[1]))

#     if copies == 0:
#         return
#     elif match == 0:
#         return
#     else:
#         # Win one card for the next MATCH cards
#         for i in range(num + 1, num + match + 1):
#             if i > len(cards) - 1:
#                 break
#             else:
#                 cards[i] += 1

#         return determine_win(game, cards, num, copies - 1)

def determine_win(game, cards, num):
    match = len(game[0].intersection(game[1]))

    if match == 0:
        return
    else:
        # Win one card for the next MATCH cards
        for i in range(num + 1, num + match + 1):
            if i > len(cards) - 1:
                break
            else:
                cards[i] += 1
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file")

    args = parser.parse_args()
    input = Path(args.input)

    with input.open() as f:
        games = f.readlines()
        games = [l.split(':')[1] for l in games]
        games = [l.split('|') for l in games]
        games = [[l[0].strip().split(), l[1].strip().split()] for l in games]
        games = [[set(l[0]), set(l[1])] for l in games]

    total = 0
    cards = np.ones(len(games))

    # Part 1
    for game in games:
        match = len(game[0].intersection(game[1]))
        if match == 0:
            continue

        score = 2 ** (match - 1)
        total += score

    print("Part 1: ", total)

    total = 0

    # Part 2
    # for i, game in enumerate(games):
    #     determine_win(game, cards, i, cards[i])

    for i, game in enumerate(games):
        while cards[i] > 0:
            determine_win(game, cards, i)
            cards[i] -= 1
            total += 1

    print("Part 2: ", total)
    
if __name__ == '__main__':
    main()