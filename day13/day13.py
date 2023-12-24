import argparse
import numpy as np
from math import floor
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file")
    args = parser.parse_args()

    input = Path(args.input)

    VALLEY = []

    with input.open() as f:
        
        line = f.readline()

        while line:
            valley = []

            while line != '\n' and line:
                valley.append([l for l in line.strip()])
                line = f.readline()

            VALLEY.append(np.array(valley))
            line = f.readline()

    sum = 0

    for valley in VALLEY:
        nr = len(valley)
        nc = len(valley[0])

        mirror = False
        # Check rows first
        for i in range(nr - 1):
            if i < floor(nr / 2):
                pattern = i + 1
                reflection = 2*i + 2
                top = valley[:pattern][::-1]
                bottom = valley[pattern:reflection]
            else:
                pattern = i + 1
                reflection = 2*pattern - nr
                top = valley[reflection:pattern][::-1]
                bottom = valley[pattern:]
            top = [''.join(l) for l in top.tolist()]
            bottom = [''.join(l) for l in bottom.tolist()]
            if top == bottom:
                sum += 100*pattern
                mirror = True
                break

        if mirror:
            continue
        
        valley = np.transpose(valley)

        for i in range(nc - 1):
            if i < floor(nc / 2):
                pattern = i + 1
                reflection = 2*i + 2
                left = valley[:pattern][::-1]
                right = valley[pattern:reflection]
            else:
                pattern = i + 1
                reflection = 2*pattern - nc
                left = valley[reflection:pattern][::-1]
                right = valley[pattern:]
            left = [''.join(l) for l in left.tolist()]
            right = [''.join(l) for l in right.tolist()]
            if left == right:
                sum += pattern
                break

    print(sum)
if __name__ == "__main__":
    main()
