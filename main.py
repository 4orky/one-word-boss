# One Word for the Boss — make.fun bounty
# u-swift-badger-44-one-word-for-the-boss-6b48c735
#
# The program writes exactly one word describing the boss to
# /output/entry.txt (1-30 characters, no spaces, no explanation).
#
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a single word a person would actually use about their boss
#   2. funny on its own — the kind of word a colleague repeats at lunch
#   3. rings true, catching a real habit of bosses
#   4. fresh, not the first word anyone would reach for
#   5. travels — works for a boss in a kitchen, a warehouse or an office
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter word. The output is byte-identical on every run.

CANDIDATES = [
    # score: boss-word 10, funny 9, true 10, fresh 9, travels 10 = 48.
    # The boss who presents your work as theirs in the meeting and
    # forgets your name in the credits. Blunt, instantly understood,
    # and true in every workplace on earth. The unhyphenated compound
    # reads as a coined label rather than a stock phrase.
    ("Credittaker", 48),
    # score: boss-word 9, funny 10, true 8, fresh 10, travels 8 = 45.
    # The boss who vanishes for weeks, then reappears at 4:59pm on a
    # Friday with an urgent task. Very funny coinage, but ghosting is
    # a habit anyone can have, not a boss-specific sin, and kitchens
    # and warehouses feel it less than offices do.
    ("Ghostboss", 45),
    # score: boss-word 9, funny 8, true 8, fresh 8, travels 7 = 40.
    # The boss whose calendar is a wall of meetings about meetings.
    # Lands well in offices, but a kitchen or warehouse boss rarely
    # makes meetings at all, so it does not travel.
    ("Meetingmaker", 40),
    # score: boss-word 8, funny 8, true 9, fresh 7, travels 9 = 41.
    # Promises the promotion, the raise, the headcount — and delivers
    # none of it. True everywhere, but the word itself is a little
    # flat; it describes a disappointment more than a joke.
    ("Overpromiser", 41),
    # score: boss-word 8, funny 8, true 7, fresh 8, travels 8 = 39.
    # The boss who disappears the moment real work needs doing. Funny
    # image, but too generic: it could describe anyone, and it says
    # nothing about what a boss does to you.
    ("Vanisher", 39),
]


def is_valid(word):
    """Gate check, mirroring the sealed scorer: UTF-8 text of 1 to 30
    characters, not only whitespace — plus the judge's first criterion:
    exactly one word, no spaces, no punctuation, letters only."""
    if not isinstance(word, str):
        return False
    if not 1 <= len(word) <= 30:
        return False
    if word != word.strip() or any(ch.isspace() for ch in word):
        return False
    return word.isalpha()


def write_entry(word, path="/output/entry.txt"):
    """Write one word, then read it back and verify byte-for-byte."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(word)
    with open(path, "r", encoding="utf-8") as f:
        back = f.read()
    if back != word or not is_valid(back):
        raise ValueError("verification failed for %r (read back %r)" % (word, back))
    return back


def main():
    ranked = sorted(CANDIDATES, key=lambda c: (-c[1], len(c[0])))
    last_error = None
    for word, _score in ranked:
        if not is_valid(word):
            continue
        try:
            write_entry(word)
        except (OSError, ValueError) as e:
            last_error = e
            continue
        print(word)
        return
    raise RuntimeError("no candidate produced a valid entry: %r" % (last_error,))


if __name__ == "__main__":
    main()
