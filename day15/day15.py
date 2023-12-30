import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file")
    args = parser.parse_args()

    input = Path(args.input)

    with input.open() as f:
        SEQUENCE = f.readline().strip().split(",")
    
    sum = 0

    for seq in SEQUENCE:
        cur = 0
        for char in seq[:2]:
            cur += ord(char)
            cur *= 17
            cur %= 256
        sum += cur
    
    print(sum)

if __name__ == "__main__":
    main()
