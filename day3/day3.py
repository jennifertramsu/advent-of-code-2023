import argparse
import re
import numpy as np
from pathlib import Path

NUMBERS = re.compile('\d+')
SYMBOLS = re.compile('[^(.\d)]')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file")

    args = parser.parse_args()
    input = Path(args.input)

    engine = input.open().read().splitlines()
    nr = len(engine)
    nc = len(engine[0])

    # Part 1
    sum = 0
    
    for i, row in enumerate(engine):
        nums = np.array(re.findall(NUMBERS, row))
        rowsum = nums.astype(int).sum()

        first = 0
        last = -1

        # For each number, find position of first and last digit
        for num in nums:
            first = row.find(num[0], last + 1) 
            last = row.rfind(num[-1], first, first + 3)

            range = [first - 1, last + 1]

            # Correcting range if out of bounds
            if range[0] < 0:
                range[0] = 0
            if range[1] > nc - 1:
                range[1] = nc - 1

            if i > 0:
                before = engine[i - 1]
                syms = re.findall(SYMBOLS, before[range[0]: range[1] + 1])
                if len(syms) > 0:
                    continue
            
            same = row
            syms = re.findall(SYMBOLS, same[range[0]: range[1] + 1])
            if len(syms) > 0:
                continue

            if i + 1 < nr:
                after = engine[i + 1]
                syms = re.findall(SYMBOLS, after[range[0]: range[1] + 1])
                if len(syms) > 0:
                    continue

            rowsum -= int(num)
        sum += rowsum

    print("Part 1: ", sum)

    # Part 2
    sum = 0

    for i, row in enumerate(engine):
        # Search for *
        gear = row.find('*')

        while gear != -1:
            range = [gear - 3, gear + 3]
            adj_range = [2, 4]
            parts = []

            # Correcting range if out of bounds
            if adj_range[0] < 0:
                adj_range[0] = 0
                range[0] = 0
            if adj_range[1] > nc - 1:
                adj_range[1] = len(range) - 1
                range[1] = nc - 1

            if i > 0:
                before = engine[i - 1][range[0]: range[1] + 1]
                nums = re.findall(NUMBERS, before)
                if len(nums) > 0:
                    first = 0
                    last = first - 1
                    for num in nums:
                        first = before.find(num[0], last + 1)
                        last = before.rfind(num[-1], first, first + 3)
                        if ((adj_range[1] - first <= 2) or (adj_range[1] - last <= 2)) and ((adj_range[1] - first >= 0) or (adj_range[1] - last) >= 0):
                            parts.append(num)

            same = row[range[0]: range[1] + 1]
            nums = re.findall(NUMBERS, same)
            if len(nums) > 0:
                first = 0
                last = first - 1
                for num in nums:
                    first = same.find(num[0], last + 1) 
                    last = same.rfind(num[-1], first, first + 3)
                    if (first == adj_range[1]) or (last == adj_range[0]):
                        parts.append(num)

            if i + 1 < nr:
                after = engine[i + 1][range[0]: range[1] + 1]
                nums = re.findall(NUMBERS, after)
                if len(nums) > 0:
                    first = 0
                    last = first - 1
                    for num in nums:
                        first = after.find(num[0], last + 1)
                        last = after.rfind(num[-1], first, first + 3)
                        if ((adj_range[1] - first <= 2) or (adj_range[1] - last <= 2)) and ((adj_range[1] - first >= 0) or (adj_range[1] - last) >= 0):
                            parts.append(num)

            if len(parts) == 2:
                ratio = np.array(parts).astype(int).prod()
                sum += ratio
            
            gear = row.find('*', gear + 1)

    print("Part 2: ", sum)
if __name__ == '__main__':
    main()