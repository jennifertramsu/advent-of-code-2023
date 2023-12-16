#! /bin/bash

# Usage function
function usage() {
    echo "Usage: $0 <day>"
    echo "  day: day of the AOC challenge to generate"
    exit 1
}

# If no arguments are given, print usage
if [ $# -ne 1 ]; then
    usage
fi

# Create the directory for the day
DAY=$1
DIR="day$DAY"

# Check if the directory already exists
if [ -d $DIR ]; then
    echo "Directory $DIR already exists"
    exit 1
fi

mkdir $DIR

# Generate python file and inputs files
touch $DIR/example.txt
touch $DIR/input.txt
touch $DIR/day$DAY.py

# Write the python file
echo "import argparse" >>$DIR/day$DAY.py
echo "from pathlib import Path" >>$DIR/day$DAY.py
echo "" >>$DIR/day$DAY.py
echo "def main():" >>$DIR/day$DAY.py
echo "    parser = argparse.ArgumentParser()" >>$DIR/day$DAY.py
echo "    parser.add_argument(\"-i\", \"--input\", help=\"Input file\")" >>$DIR/day$DAY.py
echo "    args = parser.parse_args()" >>$DIR/day$DAY.py
echo "" >>$DIR/day$DAY.py
echo "    input = Path(args.input)" >>$DIR/day$DAY.py
echo "" >>$DIR/day$DAY.py
echo "if __name__ == \"__main__\":" >>$DIR/day$DAY.py
echo "    main()" >>$DIR/day$DAY.py
