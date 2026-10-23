#!/usr/bin/env python3
"""Inkling: cast a reading: tarot (Celtic Cross), Lenormand (3x3 grid), or I Ching (one hexagram).

Usage:
    python3 cast.py tarot
    python3 cast.py lenormand
    python3 cast.py iching

Randomness comes from random.SystemRandom (the operating system's random source).
It is never seeded, so no cast can be repeated or predicted.

By Darren Schaeffer. CC BY-NC-SA 4.0.
"""

import random
import sys

RNG = random.SystemRandom()

MAJOR_ARCANA = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World",
]
RANKS = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
         "Page", "Knight", "Queen", "King"]
SUITS = ["Wands", "Cups", "Swords", "Pentacles"]
TAROT_DECK = MAJOR_ARCANA + [f"{rank} of {suit}" for suit in SUITS for rank in RANKS]

CELTIC_CROSS = [
    "The heart of the matter",
    "What crosses it",
    "The root (below)",
    "The recent past (behind)",
    "The crown (above)",
    "The near future (ahead)",
    "You",
    "Your surroundings",
    "Hopes and fears",
    "The outcome",
]

LENORMAND_DECK = [
    "Rider", "Clover", "Ship", "House", "Tree", "Clouds", "Snake", "Coffin", "Bouquet",
    "Scythe", "Whip", "Birds", "Child", "Fox", "Bear", "Stars", "Stork", "Dog", "Tower",
    "Garden", "Mountain", "Crossroads", "Mice", "Heart", "Ring", "Book", "Letter", "Man",
    "Woman", "Lily", "Sun", "Moon", "Key", "Fish", "Anchor", "Cross",
]
GRID_COLUMNS = ["past", "present", "future"]
GRID_ROWS = ["Top (above the situation)", "Middle (what is happening)", "Bottom (underneath)"]

# Hexagrams by their lines, bottom to top (1 = yang, 0 = yin), King Wen order.
HEXAGRAMS = {
    "111111": (1, "Creative"), "000000": (2, "Receptive"),
    "100010": (3, "Difficulty at the Beginning"), "010001": (4, "Youthful Folly"),
    "111010": (5, "Waiting"), "010111": (6, "Conflict"), "010000": (7, "Army"),
    "000010": (8, "Holding Together"), "111011": (9, "Small Taming"),
    "110111": (10, "Treading"), "111000": (11, "Peace"), "000111": (12, "Standstill"),
    "101111": (13, "Fellowship"), "111101": (14, "Great Possession"),
    "001000": (15, "Modesty"), "000100": (16, "Enthusiasm"), "100110": (17, "Following"),
    "011001": (18, "Repairing What Was Spoiled"), "110000": (19, "Approach"),
    "000011": (20, "Contemplation"), "100101": (21, "Biting Through"),
    "101001": (22, "Grace"), "000001": (23, "Splitting Apart"), "100000": (24, "Return"),
    "100111": (25, "Innocence"), "111001": (26, "Great Taming"),
    "100001": (27, "Nourishment"), "011110": (28, "Great Exceeding"),
    "010010": (29, "Abysmal Water"), "101101": (30, "Clinging Fire"),
    "001110": (31, "Influence"), "011100": (32, "Duration"), "001111": (33, "Retreat"),
    "111100": (34, "Great Power"), "000101": (35, "Progress"),
    "101000": (36, "Darkening of Light"), "101011": (37, "Family"),
    "110101": (38, "Opposition"), "001010": (39, "Obstruction"),
    "010100": (40, "Deliverance"), "110001": (41, "Decrease"), "100011": (42, "Increase"),
    "111110": (43, "Breakthrough"), "011111": (44, "Coming to Meet"),
    "000110": (45, "Gathering Together"), "011000": (46, "Pushing Upward"),
    "010110": (47, "Oppression"), "011010": (48, "Well"), "101110": (49, "Revolution"),
    "011101": (50, "Cauldron"), "100100": (51, "Arousing Thunder"),
    "001001": (52, "Keeping Still"), "001011": (53, "Development"),
    "110100": (54, "Marrying Maiden"), "101100": (55, "Abundance"),
    "001101": (56, "Wanderer"), "011011": (57, "Gentle Wind"),
    "110110": (58, "Joyous Lake"), "010011": (59, "Dispersion"),
    "110010": (60, "Limitation"), "110011": (61, "Inner Truth"),
    "001100": (62, "Small Exceeding"), "101010": (63, "After Completion"),
    "010101": (64, "Before Completion"),
}

LINE_KIND = {6: "changing yin", 7: "yang", 8: "yin", 9: "changing yang"}


def shuffled(deck):
    """Return a shuffled copy. SystemRandom.shuffle is a Fisher-Yates shuffle."""
    cards = list(deck)
    RNG.shuffle(cards)
    return cards


def cast_tarot():
    cards = shuffled(TAROT_DECK)[: len(CELTIC_CROSS)]
    lines = ["TAROT: Celtic Cross, 10 cards from a shuffled 78-card deck"]
    for number, (position, card) in enumerate(zip(CELTIC_CROSS, cards), start=1):
        reversed_ = RNG.random() < 0.5
        lines.append(f"{number:>2}. {position}: {card}{', reversed' if reversed_ else ''}")
    return "\n".join(lines)


def cast_lenormand():
    cards = shuffled(LENORMAND_DECK)[:9]
    lines = ["LENORMAND: 3x3 grid, 9 cards from a shuffled 36-card deck",
             "Columns run " + ", ".join(GRID_COLUMNS) + ", left to right. The center card is the heart of the matter."]
    for row, name in enumerate(GRID_ROWS):
        row_cards = cards[row * 3: row * 3 + 3]
        lines.append(f"{name}: " + " | ".join(row_cards))
    lines.append(f"Center: {cards[4]}")
    return "\n".join(lines)


def toss_line():
    coins = [RNG.choice([3, 2]) for _ in range(3)]  # heads 3, tails 2
    return coins, sum(coins)


def hexagram(bits):
    number, name = HEXAGRAMS[bits]
    return f"{number} {name} ({bits}, bottom to top)"


def cast_iching():
    lines = ["I CHING: one hexagram (plus a second when lines change), three coins per line (heads 3, tails 2), cast bottom to top"]
    totals = []
    for position in range(1, 7):
        coins, total = toss_line()
        totals.append(total)
        faces = ", ".join("heads" if c == 3 else "tails" for c in coins)
        lines.append(f"Line {position}: {faces} = {total}, {LINE_KIND[total]}")
    first = "".join("1" if t in (7, 9) else "0" for t in totals)
    changing = [i + 1 for i, t in enumerate(totals) if t in (6, 9)]
    lines.append(f"Hexagram: {hexagram(first)}")
    if changing:
        second = "".join(
            ("0" if b == "1" else "1") if totals[i] in (6, 9) else b for i, b in enumerate(first)
        )
        lines.append("Changing lines: " + ", ".join(str(n) for n in changing))
        lines.append(f"Becomes: {hexagram(second)}")
    else:
        lines.append("Changing lines: none")
    return "\n".join(lines)


CASTS = {"tarot": cast_tarot, "lenormand": cast_lenormand, "iching": cast_iching}


def main(argv):
    if len(argv) != 2 or argv[1].lower() not in CASTS:
        print("Usage: python3 cast.py tarot|lenormand|iching", file=sys.stderr)
        return 2
    print(CASTS[argv[1].lower()]())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
