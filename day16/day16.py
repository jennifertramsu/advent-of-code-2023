import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path

TRAVERSED = {} # (x, y) : [dir]
SPLITS = {} # (x, y) : dir
# ANIM = []

def traverse(maze, r, c, dir=None, COP=None):
    el = maze[r][c]
    SPLIT = False

    if (r, c) in TRAVERSED:
        if dir not in TRAVERSED[(r, c)]:
            TRAVERSED[(r, c)].append(dir)
        else:
            return
    else:
        TRAVERSED[(r, c)] = [dir]
        # xs = [x[1] / 110 for x in TRAVERSED.keys()]
        # ys = [y[0] / 110 for y in TRAVERSED.keys()]
        # ANIM.append((xs, ys))

    match el:
        case '.':
            match dir:
                case 'above':
                    new_r = r + 1
                    new_c = c
                case 'below':
                    new_r = r - 1
                    new_c = c
                case 'left':
                    new_c = c + 1
                    new_r = r
                case 'right':
                    new_c = c - 1
                    new_r = r
        case '/':
            match dir:
                case 'above':
                    new_c = c - 1
                    new_r = r
                    dir = 'right'
                case 'below':
                    new_c = c + 1
                    new_r = r
                    dir = 'left'
                case 'left':
                    new_r = r - 1
                    new_c = c
                    dir = 'below'
                case 'right':
                    new_r = r + 1
                    new_c = c
                    dir = 'above'
        case '\\':
            match dir:
                case 'above':
                    new_c = c + 1
                    new_r = r
                    dir = 'left'
                case 'below':
                    new_c = c - 1
                    new_r = r
                    dir = 'right'
                case 'left':
                    new_r = r + 1
                    new_c = c
                    dir = 'above'
                case 'right':
                    new_r = r - 1
                    new_c = c
                    dir = 'below'
        case '|':
            match dir:
                case 'above':
                    new_r = r + 1
                    new_c = c
                case 'below':
                    new_r = r - 1
                    new_c = c
                case 'left':
                    SPLIT = True
                case 'right':
                    SPLIT = True
        case '-':
            match dir:
                case 'above':
                    SPLIT = True
                case 'below':
                    SPLIT = True
                case 'left':
                    new_c = c + 1
                    new_r = r
                case 'right':
                    new_c = c - 1
                    new_r = r

    if SPLIT:
        if el == '|':
            r1 = r - 1
            r2 = r + 1
            c1 = c2 = c
            d1 = 'below'
            d2 = 'above'

            if r2 != len(maze):
                if (r2, c2) in SPLITS:
                    SPLITS[(r2, c2)].append(d2)
                else:
                    SPLITS[(r2, c2)] = [d2]
            if r1 >= 0:
                if (r1, c1) in SPLITS:
                    SPLITS[(r1, c1)].append(d1)
                else:
                    SPLITS[(r1, c1)] = [d1]

        elif el == '-':
            c1 = c - 1
            c2 = c + 1
            r1 = r2 = r
            d1 = 'right'
            d2 = 'left'

            if c2 != len(maze[0]):
                if (r2, c2) in SPLITS:
                    SPLITS[(r2, c2)].append(d2)
                else:
                    SPLITS[(r2, c2)] = [d2]
            if c1 >= 0:
                if (r1, c1) in SPLITS:
                    SPLITS[(r1, c1)].append(d1)
                else:
                    SPLITS[(r1, c1)] = [d1]

    else:
        if new_r == len(maze):
            return
        if new_r < 0:
            return
        if new_c == len(maze[0]):
            return
        if new_c < 0:
            return
        
        traverse(maze, new_r, new_c, dir)

    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file")
    args = parser.parse_args()

    input = Path(args.input)

    with input.open() as f:
        GRID = f.read().splitlines()

    x = y = 0
    dir = 'left'

    traverse(GRID, x, y, dir)

    while SPLITS:
        cur = SPLITS.copy()
        for split, dirs in cur.items():
            x = split[0]
            y = split[1]
            for d in dirs:
                traverse(GRID, x, y, d)
                SPLITS[split].remove(d)
            if len(SPLITS[split]) == 0:
                SPLITS.pop(split)

    print(len(TRAVERSED))

    # Fixed frame size to fit GRID
    fig, ax = plt.subplots()

    # def animate(i):
    #     ax.clear()
    #     ax.plot(ANIM[i][0], ANIM[i][1], 'o')
    #     ax.set_title(f"Frame {i}")
    
    # ani = animation.FuncAnimation(fig, animate, frames=len(ANIM), interval=5)
    # ani.save('progress/animation.gif', fps=60)
    # plt.show()

if __name__ == "__main__":
    main()
