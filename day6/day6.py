import argparse
import numpy as np
import math
from pathlib import Path

def quadratic(a, b, c):
    r1 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    r2 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    return [r1, r2]

def main():
    '''
    y = distance
    x = time held 

    distance = speed * time
    speed = x
    time = race time time - x

    y = x * (race time - x)
    y = -x^2 + race time x 
    find x such that y > record
    min x = when y = record -> roots

    x = - race time += sqrt (race time^2 - 4 * -1 * -record) / 2 * -1
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')

    args = parser.parse_args()
    input = Path(args.input)

    with input.open() as f:
        lines = f.readlines()
        times = np.array(lines[0].split(':')[1].strip().split()).astype(int)
        distances = np.array(lines[1].split(':')[1].strip().split()).astype(int)
        RACES = list(zip(times, distances))

    total = 1

    # Part 1
    for race in RACES:
        roots = quadratic(-1, race[0], -race[1])
        roots = [math.floor(roots[0] + 1), math.ceil(roots[1] - 1)]
        ways = roots[1] - roots[0] + 1
        total *= ways

    print("Part 1: ", total)

    # Part 2
    with input.open() as f:
        lines = f.readlines()
        time = int(lines[0].strip().split(':')[1].replace(' ', ''))
        distance = int(lines[1].strip().split(':')[1].replace(' ', ''))

    total = 1

    roots = quadratic(-1, time, -distance)
    roots = [math.floor(roots[0] + 1), math.ceil(roots[1] - 1)]
    ways = roots[1] - roots[0] + 1
    total *= ways

    print("Part 2: ", total)

if __name__ == '__main__':
    main()