import argparse
import numpy as np
import re
from pathlib import Path

# Global Variables
CUBE = {
    "red": 12,
    "green": 13,
    "blue": 14
}
COLOUR = re.compile("(\d+ \w+)")
RED = re.compile("(\d+ red)")
GREEN = re.compile("(\d+ green)")
BLUE = re.compile("(\d+ blue)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file', required=True)
    args = parser.parse_args()

    input = Path(args.input)

    with input.open() as f:
        lines = f.readlines()

    games = [s.split(':') for s in lines]

    # Part 1
    ALL = np.arange(1, len(games)+1).sum()
    err = []

    # Part 2
    sum = 0

    for game in games:
        # Part 2
        reds = re.findall(RED, game[1])
        greens = re.findall(GREEN, game[1])
        blues = re.findall(BLUE, game[1])

        reds = [int(r.split()[0]) for r in reds]
        greens = [int(g.split()[0]) for g in greens]
        blues = [int(b.split()[0]) for b in blues]

        power = max(reds) * max(greens) * max(blues)
        sum += power

        rounds = re.findall(COLOUR, game[1])
        for round in rounds:
            # Part 1
            guess = int(round.split()[0])
            actual = CUBE[round.split()[1]]
            if guess > actual:
                err.append(int(game[0].split()[1]))
                break

    err = np.array(err).sum()
    print("Part 1: ", ALL - err)
    print("Part 2: ", sum)

if __name__ == '__main__':
    main()