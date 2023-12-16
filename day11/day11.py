from math import floor, sqrt
import numpy as np
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file")
    args = parser.parse_args()

    input = Path(args.input)

    with input.open() as f:
        GALAXY = f.readlines()

    # Find all galaxies
    galaxies = []
    rows = np.arange(len(GALAXY)).tolist()
    cols = np.arange(len(GALAXY[0])).tolist()
    for i, galaxy in enumerate(GALAXY):
        star = galaxy.find('#')
        while star != -1:
            if i in rows:
                rows.remove(i)
            if star in cols:
                cols.remove(star)
            galaxies.append([i, star])
            star = galaxy.find('#', star + 1)

    # Expand universe
    expanded = galaxies.copy()
    for r in rows:
        expanded = [[expanded[i][0] + 1000000 - 1, expanded[i][1]] if galaxies[i][0] > r else [expanded[i][0], expanded[i][1]] for i in range(len(galaxies))]
    for c in cols:
        expanded = [[expanded[i][0], expanded[i][1] + 1000000 - 1] if galaxies[i][1] > c else [expanded[i][0], expanded[i][1]] for i in range(len(galaxies))]

    galaxies = expanded

    sum = 0
    for i in range(len(galaxies)):
        star = galaxies[i]
        for j in range(i + 1, len(galaxies)):
            other = galaxies[j]
            sum += abs(other[1] - star[1]) + abs(other[0] - star[0])

    print(sum)

if __name__ == "__main__":
    main()
