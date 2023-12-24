import argparse
import numpy as np
from math import floor
from pathlib import Path

def levenshstein(str1, str2):
    # Initializing distance matrix
    matrix = np.zeros((len(str1) + 1, len(str2) + 1))
    matrix[0, :] = np.arange(0, len(str2) + 1)
    matrix[:, 0] = np.arange(0, len(str1) + 1)

    # Traversing the matrix
    for i in range(len(str1)):
        for j in range(len(str2)):
            grid = matrix[i:i + 2, j:j + 2]
            if str1[i] == str2[j]:
                matrix[i + 1, j + 1] = grid[0, 0]
            else:
                matrix[i + 1, j + 1] = min(grid[0, 0], grid[0, 1], grid[1, 0]) + 1

    return matrix[-1,-1]

def clean(l1, l2):
    sum = 0
    for i in range(len(l1)):
        score = levenshstein(l1[i], l2[i])
        sum += score
        if score == 1:
            idx = i
            arr = l2[i]
    if sum == 1:
        l1[idx] = arr
        return l1, l2, True
    else:
        return l1, l2, False

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

    for j, valley in enumerate(VALLEY):
        nr = len(valley)
        nc = len(valley[0])

        smudge = False

        # Check rows first
        for i in range(nr - 1):
            if i < floor(nr / 2):
                pattern = i + 1
                reflection = 2*i + 2
                top = valley[:pattern][::-1]
                bottom = valley[pattern:reflection]
                if not smudge:
                    top, bottom, smudge = clean(top, bottom)
            else:
                pattern = i + 1
                reflection = 2*pattern - nr
                top = valley[reflection:pattern][::-1]
                bottom = valley[pattern:]
                if not smudge:
                    top, bottom, smudge = clean(top, bottom)
            if smudge:
                top = [''.join(l) for l in top.tolist()]
                bottom = [''.join(l) for l in bottom.tolist()]
                if top == bottom:
                    sum += 100*pattern
                    break

        if smudge:
            continue

        valley = np.transpose(valley)
        
        for i in range(nc - 1):
            if i < floor(nc / 2):
                pattern = i + 1
                reflection = 2*i + 2
                left = valley[:pattern][::-1]
                right = valley[pattern:reflection]
                if not smudge:
                    left, right, smudge = clean(left, right)
            else:
                pattern = i + 1
                reflection = 2*pattern - nc
                left = valley[reflection:pattern][::-1]
                right = valley[pattern:]
                if not smudge:
                    left, right, smudge = clean(left, right)
            if smudge:
                left = [''.join(l) for l in left.tolist()]
                right = [''.join(l) for l in right.tolist()]
                if left == right:
                    sum += pattern
                    break
        if not smudge:
            print(j, 'ERROR')

    print(sum)
if __name__ == "__main__":
    main()
