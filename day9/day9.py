import argparse
import numpy as np
from pathlib import Path

def diff(arr):
    diff = np.array([arr[i] - arr[i-1] for i in range(1, len(arr))])
    return diff

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file")

    args = parser.parse_args()
    input = Path(args.input)

    with input.open() as f:
        HISTORY = f.readlines()
        HISTORY = [l.strip().split() for l in HISTORY]
        HISTORY = np.array(HISTORY).astype(int)

    sum_after = 0
    sum_before = 0
    for history in HISTORY:
        d = history
        last = []
        last.append(d[-1])
        first = []
        first.append(d[0])
        while d.sum() != 0:
            d = diff(d)
            last.append(d[-1])
            first.append(d[0])
        last = np.array(last).sum()
        even = np.array(first[::2]).sum()
        odd = np.array(first[1::2]).sum()
        first = even - odd

        sum_after += last
        sum_before += first
    print('Part 1: ', sum_after)
    print('Part 2: ', sum_before)

if __name__ == '__main__':
    main()