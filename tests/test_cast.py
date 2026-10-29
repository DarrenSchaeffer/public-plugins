"""Tests for the Inkling cast script. Run: python3 -m unittest discover tests"""

import importlib.util
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/inkling/skills/inkling/scripts/cast.py"
spec = importlib.util.spec_from_file_location("cast", SCRIPT)
cast = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cast)

# Darren's local I Ching engine, used only as a cross-check when present.
ENGINE_ROOT = Path.home() / ".claude/vendor/divination-skills"


class Decks(unittest.TestCase):
    def test_tarot_deck(self):
        self.assertEqual(len(cast.TAROT_DECK), 78)
        self.assertEqual(len(set(cast.TAROT_DECK)), 78)
        self.assertIn("Ace of Wands", cast.TAROT_DECK)
        self.assertIn("King of Pentacles", cast.TAROT_DECK)

    def test_lenormand_deck(self):
        self.assertEqual(len(cast.LENORMAND_DECK), 36)
        self.assertEqual(len(set(cast.LENORMAND_DECK)), 36)

    def test_hexagram_table(self):
        self.assertEqual(len(cast.HEXAGRAMS), 64)
        self.assertEqual(sorted(n for n, _ in cast.HEXAGRAMS.values()), list(range(1, 65)))
        for bits in cast.HEXAGRAMS:
            self.assertRegex(bits, r"^[01]{6}$")

    def test_hexagram_table_self_contained(self):
        # Standard King Wen grid: rows = lower trigram, columns = upper trigram,
        # trigram order Heaven, Thunder, Water, Mountain, Earth, Wind, Fire, Lake.
        trigram_bits = {"heaven": "111", "thunder": "100", "water": "010", "mountain": "001",
                        "earth": "000", "wind": "011", "fire": "101", "lake": "110"}
        order = ["heaven", "thunder", "water", "mountain", "earth", "wind", "fire", "lake"]
        grid = [
            [1, 34, 5, 26, 11, 9, 14, 43],
            [25, 51, 3, 27, 24, 42, 21, 17],
            [6, 40, 29, 4, 7, 59, 64, 47],
            [33, 62, 39, 52, 15, 53, 56, 31],
            [12, 16, 8, 23, 2, 20, 35, 45],
            [44, 32, 48, 18, 46, 57, 50, 28],
            [13, 55, 63, 22, 36, 37, 30, 49],
            [10, 54, 60, 41, 19, 61, 38, 58],
        ]
        for r, lower in enumerate(order):
            for c, upper in enumerate(order):
                bits = trigram_bits[lower] + trigram_bits[upper]
                self.assertEqual(cast.HEXAGRAMS[bits][0], grid[r][c], bits)

    @unittest.skipUnless(ENGINE_ROOT.is_dir(), "local I Ching engine not installed")
    def test_hexagram_names_match_engine(self):
        import json
        data = json.loads((ENGINE_ROOT / "systems/iching/data/hexagrams.json").read_text())
        engine = {h["number"]: h["english"] for h in data}
        for number, name in cast.HEXAGRAMS.values():
            self.assertEqual(engine[number], name, number)

    @unittest.skipUnless(ENGINE_ROOT.is_dir(), "local I Ching engine not installed")
    def test_hexagram_table_matches_engine(self):
        sys.path.insert(0, str(ENGINE_ROOT))
        from systems.iching.engine import PAIR_TO_NUMBER, TRIGRAM_BY_BITS
        for bits, (number, name) in cast.HEXAGRAMS.items():
            b = tuple(int(c) for c in bits)
            lower = TRIGRAM_BY_BITS[b[:3]][0]
            upper = TRIGRAM_BY_BITS[b[3:]][0]
            self.assertEqual(PAIR_TO_NUMBER[(upper, lower)], number, f"{bits} {name}")


class Casts(unittest.TestCase):
    def test_tarot_cast(self):
        cards = cast.cast_tarot().splitlines()[1:]
        self.assertEqual(len(cards), 3)
        names = [line.split(": ", 1)[1].replace(", reversed", "") for line in cards]
        self.assertEqual(len(set(names)), 3)
        for i, position in enumerate(cast.TAROT_POSITIONS):
            self.assertIn(position, cards[i])

    def test_reversals_near_half(self):
        reversed_count = sum(cast.cast_tarot().count(", reversed") for _ in range(6000))
        self.assertTrue(0.47 < reversed_count / 18000 < 0.53, reversed_count)

    def test_tarot_shuffle_uniform_enough(self):
        first = Counter(cast.shuffled(cast.TAROT_DECK)[0] for _ in range(39000))
        self.assertEqual(len(first), 78)  # every card can come up first
        self.assertTrue(all(300 < n < 700 for n in first.values()))

    def test_lenormand_cast(self):
        out = cast.cast_lenormand()
        cards = out.splitlines()[1:]
        self.assertEqual(len(cards), 3)
        names = [line.split(": ", 1)[1] for line in cards]
        self.assertEqual(len(set(names)), 3)
        for i, position in enumerate(cast.LENORMAND_POSITIONS):
            self.assertIn(position, cards[i])
        self.assertNotIn("reversed", out)

    def test_iching_cast(self):
        for _ in range(500):
            out = cast.cast_iching()
            line_rows = [l for l in out.splitlines() if l.startswith("Line ")]
            self.assertEqual(len(line_rows), 6)
            totals = [int(l.split(" = ")[1].split(",")[0]) for l in line_rows]
            self.assertTrue(all(t in (6, 7, 8, 9) for t in totals))
            changing = [i + 1 for i, t in enumerate(totals) if t in (6, 9)]
            if changing:
                self.assertIn("Becomes:", out)
            else:
                self.assertIn("Changing lines: none", out)
                self.assertNotIn("Becomes:", out)

    def test_iching_known_cast(self):
        # Lines bottom to top: 8, 8, 7, 9, 8, 9 -> 001101 (56 Wanderer),
        # lines 4 and 6 change -> 001000 (15 Modesty).
        from unittest import mock
        totals = iter([8, 8, 7, 9, 8, 9])
        with mock.patch.object(cast, "toss_line", lambda: ([], next(totals))):
            out = cast.cast_iching()
        self.assertIn("Hexagram: 56 Wanderer (001101", out)
        self.assertIn("Changing lines: 4, 6", out)
        self.assertIn("Becomes: 15 Modesty (001000", out)

    def test_iching_all_casts(self):
        # Every one of the 4,096 possible casts gives the right second hexagram.
        import itertools
        from unittest import mock
        for combo in itertools.product([6, 7, 8, 9], repeat=6):
            totals = iter(combo)
            with mock.patch.object(cast, "toss_line", lambda: ([], next(totals))):
                out = cast.cast_iching()
            first = "".join("1" if t in (7, 9) else "0" for t in combo)
            second = "".join("1" if t in (7, 6) else "0" for t in combo)
            self.assertIn(f"Hexagram: {cast.HEXAGRAMS[first][0]} ", out)
            if first != second:
                self.assertIn(f"Becomes: {cast.HEXAGRAMS[second][0]} ", out)
            else:
                self.assertNotIn("Becomes:", out)

    def test_iching_line_odds(self):
        # Three coins: 6 and 9 each 1/8, 7 and 8 each 3/8.
        totals = Counter(cast.toss_line()[1] for _ in range(40000))
        self.assertTrue(4400 < totals[6] < 5600, totals)
        self.assertTrue(4400 < totals[9] < 5600, totals)
        self.assertTrue(14000 < totals[7] < 16000, totals)

    def test_cli_rejects_unknown(self):
        self.assertEqual(cast.main(["cast.py", "runes"]), 2)

    def test_offline_and_stateless(self):
        # README promise: only random and sys; no network, no file reads, nothing saved.
        import ast
        tree = ast.parse(SCRIPT.read_text())
        modules = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        modules |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
        self.assertEqual(modules, {"random", "sys"})
        builtins_called = {n.func.id for n in ast.walk(tree)
                           if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        self.assertFalse(builtins_called & {"open", "eval", "exec", "__import__", "compile", "input"})

    def test_license_copies_match(self):
        self.assertEqual((ROOT / "LICENSE").read_text(), (ROOT / "plugins/inkling/LICENSE").read_text())

    def test_never_seeded(self):
        self.assertNotIn(".seed(", SCRIPT.read_text())


if __name__ == "__main__":
    unittest.main()
