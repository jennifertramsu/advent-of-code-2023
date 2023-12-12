import argparse
import re
import numpy as np
from pathlib import Path

CARDS = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'T': 9,
    '9': 8,
    '8': 7,
    '7': 6,
    '6': 5,
    '5': 4,
    '4': 3,
    '3': 2,
    '2': 1,
    'J': 0
}
J = re.compile('J')

def sort_hands(hands, bids):
    global CARDS

    hands = list(map(lambda x: [CARDS[i] for i in x], hands))
    sorted_hands = sorted(zip(hands, bids), key=lambda x: x[0])
    if len(sorted_hands) > 0:
        hands, bids = zip(*sorted_hands)
        return hands, bids
    return [], []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file")

    args = parser.parse_args()
    input = Path(args.input)

    ONE_OR_FIVE = {
        1: {
            'label': 'five',
            'hands': [],
            'bids': []
        },
        4: {
            'label': 'one',
            'hands': [],
            'bids': []
        },
        5: {
            'label': 'high',
            'hands': [],
            'bids': []
        }
    }
    FOUR_OR_FULL = {
        4: {
            'label': 'four',
            'hands': [],
            'bids': []
        },
        'f': {
            'label': 'full',
            'hands': [],
            'bids': []
        }
    }
    TWO_OR_THREE = {
        2: {
            'label': 'two',
            'hands': [],
            'bids': []
        },
        3: {
            'label': 'three',
            'hands': [],
            'bids': []
        }
    }

    with input.open() as f:
        lines = f.readlines()
        HANDS = [l.strip().split()[0] for l in lines]
        BIDS = np.array([l.strip().split()[1] for l in lines]).astype(int)
        num_hands = len(HANDS)

    for i, hand in enumerate(HANDS):
        matches = set(hand)
        if len(matches) != 3 and len(matches) != 2:
            if 'J' in hand:
                if len(matches) == 1: # all Js
                    ONE_OR_FIVE[1]['hands'].append(hand)
                    ONE_OR_FIVE[1]['bids'].append(BIDS[i])
                elif len(matches) == 4:
                    TWO_OR_THREE[3]['hands'].append(hand)
                    TWO_OR_THREE[3]['bids'].append(BIDS[i])
                elif len(matches) == 5:
                    ONE_OR_FIVE[4]['hands'].append(hand)
                    ONE_OR_FIVE[4]['bids'].append(BIDS[i])
            else:
                ONE_OR_FIVE[len(matches)]['hands'].append(hand)
                ONE_OR_FIVE[len(matches)]['bids'].append(BIDS[i])
        elif len(matches) == 3:
            TWO = True
            for char in matches:
                label = re.compile(char)
                rematch = [match.group() for match in label.finditer(hand)]
                if len(rematch) == 3:
                    TWO = False
                    break
            if TWO:
                if 'J' in hand:
                    jokers = len(re.findall(J, hand))
                    if jokers == 1:
                        FOUR_OR_FULL['f']['hands'].append(hand)
                        FOUR_OR_FULL['f']['bids'].append(BIDS[i]) 
                    elif jokers == 2:
                        FOUR_OR_FULL[4]['hands'].append(hand)
                        FOUR_OR_FULL[4]['bids'].append(BIDS[i])    
                else:
                    TWO_OR_THREE[2]['hands'].append(hand)
                    TWO_OR_THREE[2]['bids'].append(BIDS[i])
            else:
                if 'J' in hand:
                    FOUR_OR_FULL[4]['hands'].append(hand)
                    FOUR_OR_FULL[4]['bids'].append(BIDS[i])
                else:
                    TWO_OR_THREE[3]['hands'].append(hand)
                    TWO_OR_THREE[3]['bids'].append(BIDS[i])
        elif len(matches) == 2:
            if 'J' in hand:
                ONE_OR_FIVE[1]['hands'].append(hand)
                ONE_OR_FIVE[1]['bids'].append(BIDS[i])
            else:
                FULL = True
                for char in matches:
                    label = re.compile(char)
                    rematch = [match.group() for match in label.finditer(hand)]
                    if len(rematch) == 4:
                        FULL = False
                        break
                if FULL:
                    FOUR_OR_FULL['f']['hands'].append(hand)
                    FOUR_OR_FULL['f']['bids'].append(BIDS[i])
                else:
                    FOUR_OR_FULL[4]['hands'].append(hand)
                    FOUR_OR_FULL[4]['bids'].append(BIDS[i])

    # Sorting hands
    HANDS = {
        'high': {
            'cards': ONE_OR_FIVE[5]['hands'],
            'bids': ONE_OR_FIVE[5]['bids']
        },
        'one': {
            'cards': ONE_OR_FIVE[4]['hands'],
            'bids': ONE_OR_FIVE[4]['bids']
        },
        'two': {
            'cards': TWO_OR_THREE[2]['hands'],
            'bids': TWO_OR_THREE[2]['bids']
        },
        'three': {
            'cards': TWO_OR_THREE[3]['hands'],
            'bids': TWO_OR_THREE[3]['bids']
        },
        'full': {
            'cards': FOUR_OR_FULL['f']['hands'],
            'bids': FOUR_OR_FULL['f']['bids']
        },
        'four': {
            'cards': FOUR_OR_FULL[4]['hands'],
            'bids': FOUR_OR_FULL[4]['bids']
        },
        'five': {
            'cards': ONE_OR_FIVE[1]['hands'],
            'bids': ONE_OR_FIVE[1]['bids']
        }
    }
    
    ORDERED_BIDS = []
    for hand in HANDS:
        hands = HANDS[hand]['cards']
        bids = HANDS[hand]['bids']
        hands, bids = sort_hands(hands, bids)
        ORDERED_BIDS.extend(bids)

    ORDERED_BIDS = np.array(ORDERED_BIDS)
    IDXS = np.arange(1, num_hands + 1)
    print(np.dot(IDXS, ORDERED_BIDS))

if __name__ == '__main__':
    main()