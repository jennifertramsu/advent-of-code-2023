import argparse
from pathlib import Path

PIPES = ['|', '-', 'L', 'J', '7', 'F']
ANIMAL = 'S'
MAP = {
    'S': {
        'below': ['|', 'L', 'J'],
        'above': ['|', '7', 'F'],
        'left': ['-', 'L', 'F'],
        'right': ['-', 'J', '7']
    },
    '|': {
        'below': ['L', 'J', 'S', '|'],
        'above': ['7', 'F', 'S', '|']
    },
    '-': {
        'left': ['L', 'F', 'S', '-'],
        'right': ['J', '7', 'S', '-']
    },
    'L': {
        'above': ['|', '7', 'F', 'S'],
        'right': ['-', 'J', '7', 'S']
    },
    'J': {
        'above': ['|', '7', 'F', 'S'],
        'left': ['-', 'L', 'F', 'S']
    },
    '7': {
        'below': ['|', 'L', 'J', 'S'],
        'left': ['-', 'L', 'F', 'S']
    },
    'F': {
        'below': ['|', 'L', 'J', 'S'],
        'right': ['-', 'J', '7', 'S']
    }
}

def search_adjacent(maze, element, r, c, dir=None):
    match element:
        case '|':
            if dir == 'above':
                if r + 1 < len(maze):
                    el = maze[r + 1][c]
                    if el in MAP[element]['below']:
                        new_r = r + 1
                        new_c = c
                        new_dir = 'above'
            elif dir == 'below':
                if r - 1 >= 0:
                    el = maze[r - 1][c]
                    if el in MAP[element]['above']:
                        new_r = r - 1
                        new_c = c
                        new_dir = 'below'
        case '-':
            if dir == 'left':
                if c + 1 < len(maze[0]):
                    el = maze[r][c + 1]
                    if el in MAP[element]['right']:
                        new_r = r
                        new_c = c + 1
                        new_dir = 'left'
            elif dir == 'right':
                if c - 1 >= 0:
                    el = maze[r][c - 1]
                    if el in MAP[element]['left']:
                        new_r = r
                        new_c = c - 1
                        new_dir = 'right'
        case 'L':
            if dir == 'above':
                if c + 1 < len(maze[0]):
                    el = maze[r][c + 1]
                    if el in MAP[element]['right']:
                        new_r = r
                        new_c = c + 1
                        new_dir = 'left'
            elif dir == 'right':
                if r - 1 >= 0:
                    el = maze[r - 1][c]
                    if el in MAP[element]['above']:
                        new_r = r - 1
                        new_c = c
                        new_dir = 'below'
        case 'J':
            if dir == 'above':
                if c - 1 >= 0:
                    el = maze[r][c - 1]
                    if el in MAP[element]['left']:
                        new_r = r
                        new_c = c - 1
                        new_dir = 'right'
            elif dir == 'left':
                if r - 1 >= 0:
                    el = maze[r - 1][c]
                    if el in MAP[element]['above']:
                        new_r = r - 1
                        new_c = c
                        new_dir = 'below'
        case '7':
            if dir == 'below':
                if c - 1 >= 0:
                    el = maze[r][c - 1]
                    if el in MAP[element]['left']:
                        new_r = r
                        new_c = c - 1
                        new_dir = 'right'
            elif dir == 'left':
                if r + 1 < len(maze):
                    el = maze[r + 1][c]
                    if el in MAP[element]['below']:
                        new_r = r + 1
                        new_c = c
                        new_dir = 'above'
        case 'F':
            if dir == 'below':
                if c + 1 < len(maze[0]):
                    el = maze[r][c + 1]
                    if el in MAP[element]['right']:
                        new_r = r
                        new_c = c + 1
                        new_dir = 'left'
            elif dir == 'right':
                if r + 1 < len(maze):
                    el = maze[r + 1][c]
                    if el in MAP[element]['below']:
                        new_r = r + 1
                        new_c = c
                        new_dir = 'above'
        case ANIMAL:
            # Below
            if r + 1 < len(maze):
                el = maze[r + 1][c]
                if el in MAP[element]['below']:
                    new_r = r + 1
                    new_c = c
                    new_dir = 'above'
            # Above
            if r - 1 >= 0:
                el = maze[r - 1][c]
                if el in MAP[element]['above']:
                    new_r = r - 1
                    new_c = c
                    new_dir = 'below'
            # Left
            if c - 1 >= 0:
                el = maze[r][c - 1]
                if el in MAP[element]['left']:
                    new_r = r
                    new_c = c - 1
                    new_dir = 'right'
            # Right
            if c + 1 < len(maze[0]):
                el = maze[r][c + 1]
                if el in MAP[element]['right']:
                    new_r = r
                    new_c = c + 1
                    new_dir = 'left'

    # Return coordinate of next pipe
    return new_r, new_c, new_dir

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file")

    args = parser.parse_args()
    input = Path(args.input)

    with input.open() as f:
        MAZE = f.readlines()
        MAZE = [l.strip() for l in MAZE]

    # Find animal
    for i, row in enumerate(MAZE):
        S = row.find(ANIMAL)
        if S != -1:
            r, c = i, S

    # Determine length of pipe
    len_pipe = 1
    cur_r, cur_c, dir = search_adjacent(MAZE, ANIMAL, r, c)

    while cur_r != r or cur_c != c:
        element = MAZE[cur_r][cur_c]
        len_pipe += 1
        cur_r, cur_c, dir = search_adjacent(MAZE, element, cur_r, cur_c, dir)
        
    print(int(len_pipe / 2))
if __name__ == '__main__':
    main()