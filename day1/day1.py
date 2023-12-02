import argparse
import re
import numpy as np
from pathlib import Path

NUMERIC1 = re.compile("[0-9]")
MAP = {
    "one" : '1',
    "two" : '2',
    "three" : '3',
    "four" : '4',
    "five" : '5',
    "six" : '6',
    "seven" : '7',
    "eight" : '8',
    "nine" : '9',
    "zero" : '0',
    '1' : '1',
    '2' : '2',
    '3' : '3',
    '4' : '4',
    '5' : '5',
    '6' : '6',
    '7' : '7',
    '8' : '8',
    '9' : '9',
    '0' : '0'
}

NUMERIC2 = re.compile("(?=([0-9]|one|two|three|four|five|six|seven|eight|nine|zero))")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file', required=True)
    parser.add_argument('-p', '--part', help='part 1 or 2', required=True)

    args = parser.parse_args()
    input = Path(args.input)
    part = args.part

    with open(input, 'r') as f:
        lines = f.readlines()

        if part == '1':
            print("Part 1")
            num = [(np.array(re.findall(NUMERIC1, line))[0], np.array(re.findall(NUMERIC1, line))[-1]) for line in lines]
            sum = np.array([s[0] + s[1] for s in num]).astype(int).sum()
            print(sum)

        elif part == '2':
            print("Part 2")
            num = [(np.array(re.findall(NUMERIC2, line))[0], np.array(re.findall(NUMERIC2, line))[-1]) for line in lines]
            print(num)
            sum = np.array([MAP[s[0]] + MAP[s[1]] for s in num]).astype(int).sum()
            print(sum)          

if __name__ == '__main__':
    main()