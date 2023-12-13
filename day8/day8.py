import argparse
import re
from itertools import cycle
from pathlib import Path

alpha = re.compile('\w+')
START = 'AAA'
END = 'ZZZ'

class Node:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

    def set_node(self, node, step):
        if step == 'L':
            self.left = node
        elif step == 'R':
            self.right = node

    def get_node(self, step):
        if step == 'L':
            return self.left
        elif step == 'R':
            return self.right
        
    def __repr__(self) -> str:
        return self.name
    
    def __eq__(self, other):
        return self.name == other.name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file")

    args = parser.parse_args()
    input = Path(args.input)

    with input.open() as f:
        INSTRUCTIONS = f.readline().strip()
        f.readline() # \n

        map = f.readlines()
        NAMES = [l.strip().split('=')[0].strip() for l in map]
        STEPS = [l.strip().split('=')[1].strip() for l in map]
        STEPS = [re.findall(alpha, step) for step in STEPS]

    NODES = [Node(n) for n in NAMES]
    MAP = {name: node for name, node in zip(NAMES, NODES)}

    for i, step in enumerate(STEPS):
        node = NODES[i]
        left = MAP[step[0]]
        right = MAP[step[1]]

        node.set_node(left, 'L')
        node.set_node(right, 'R')

    INSTRUCTIONS = cycle(INSTRUCTIONS)

    node = MAP[START]
    end = MAP[END]

    num_steps = 0
    for step in INSTRUCTIONS:
        node = node.get_node(step)
        num_steps += 1
        if node == end:
            break
        
    print(num_steps)

if __name__ == '__main__':
    main()