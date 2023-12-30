import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file")
    args = parser.parse_args()

    input = Path(args.input)

    with input.open() as f:
        SEQUENCE = f.readline().strip().split(",")

    BOXES = {i: {} for i in range(256)}
    
    for seq in SEQUENCE:
        cur = 0
        if '=' in seq:
            seq = seq.split('=')
            op = '='
        elif '-' in seq:
            seq = seq.split('-')
            op = '-'
        label = seq[0]
        for char in label:
            cur += ord(char)
            cur *= 17
            cur %= 256

        if op == '=':
            lens = int(seq[1])
            BOXES[cur][label] = lens
        elif op == '-':
            BOXES[cur].pop(label, None)

    BOXES = {k: v for k, v in BOXES.items() if v}

    power = 0

    for box in BOXES:
        for i, lens in enumerate(BOXES[box]):
            power += (box + 1) * (i + 1) * BOXES[box][lens]

    print(power)

if __name__ == "__main__":
    main()
