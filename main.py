"""One Word for the Boss — make.fun bounty u-swift-badger-44-one-word-for-the-boss-6b48c735.

The brief asks for exactly one word that describes a boss: no phrase, no
sentence, no explanation. A judge model then pairs words off against each
other on five things, in this order — a word a person would really use about
the boss they report to; funny on its own; true about a real boss habit;
fresh rather than the first word anyone reaches for; and able to travel
between a kitchen, a warehouse and an office.

Thirteen words were drafted by hand and marked 0-10 on each of those five
points. The entry is the highest total; a tie goes to the shorter word, so
the pick is the same on every run. The chosen word is written to
/output/entry.txt as plain UTF-8 bytes, read straight back, and only
accepted when the bytes round-trip exactly.
"""

import re
import sys
from pathlib import Path

ENTRY_PATH = Path("/output/entry.txt")

# A single word, 1 to 30 letters, nothing else: no spaces, no digits, no
# punctuation. The gate scores the file, not the program, so the check here
# mirrors it exactly. fullmatch pins both ends, so no anchors are needed.
WORD_PATTERN = re.compile(r"[A-Za-z]{1,30}")

# Marks are (boss-word, funny, true, fresh, travels), each 0-10, in the
# judge's own order of importance.
CANDIDATE_MARKS = {
    # The boss who presents your work as theirs in the meeting and forgets
    # your name in the credits. Blunt, understood in a second, and true in
    # every workplace on earth; the unhyphenated compound reads as a coined
    # label, not a stock phrase.
    "Credittaker": (10, 9, 10, 9, 10),
    # The boss who vanishes for weeks, then reappears at 4:59pm on a Friday
    # with an urgent task. A very funny coinage, but ghosting is a habit
    # anyone can have, not a boss-specific sin, and kitchens and warehouses
    # feel it less than offices do.
    "Ghostboss": (9, 10, 8, 10, 8),
    # The boss who claps loudest for other people's work and somehow ends
    # up holding the trophy. Close cousin of the winner, but softer: it
    # accuses the boss of enjoying applause, not of taking what is yours.
    "Applausethief": (9, 9, 9, 9, 8),
    # Same charge as the winner, clumsier word. It grabs where the winner
    # takes, and "grabber" sounds like a playground insult rather than a
    # job title the boss has quietly earned.
    "Creditgrabber": (9, 8, 9, 8, 9),
    # Promises the promotion, the raise, the headcount — and delivers none
    # of it. True everywhere, but the word itself is a little flat; it
    # describes a disappointment more than a joke.
    "Overpromiser": (8, 8, 9, 7, 9),
    # The boss who keeps every compliment for themselves and hands the team
    # the blame. Sharp and specific, but it needs a beat of explaining
    # before it lands, where the winner lands on sight.
    "Praisehoarder": (8, 8, 8, 9, 8),
    # When a project fails, this boss is never in the room where the fault
    # is handed out — someone else always is. True and boss-shaped, but the
    # word is a mouthful and the joke is in the shifting, not the word.
    "Blameshifter": (9, 7, 9, 7, 8),
    # The boss whose calendar is a wall of meetings about meetings. Lands
    # well in offices, but a kitchen or warehouse boss rarely makes
    # meetings at all, so it does not travel.
    "Meetingmaker": (9, 8, 8, 8, 7),
    # Counts every keystroke, reads every draft twice, and still asks for
    # a status update. The truest word on the list and the most boss-shaped
    # — and also the first word anyone reaches for, so it earns no laugh
    # for surprise.
    "Micromanager": (10, 6, 10, 4, 9),
    # The boss who is never around when the hard part starts. A funny
    # picture, but it fits any absent person, not a boss in particular,
    # and it never says what the boss took from you.
    "Vanisher": (8, 8, 7, 8, 8),
    # Hands out five urgent jobs before lunch, then asks at 5pm why none
    # of them is done. A vivid picture of a real boss, but the word leans
    # on the tornado metaphor instead of standing on its own.
    "Tasktornado": (8, 8, 7, 8, 7),
    # Everything is someone else's job, including the job of deciding
    # whose job it is. Accurate, and every office knows one — but as a
    # joke it reads like a job description, not a punchline.
    "Delegator": (9, 6, 8, 6, 9),
    # Drawn to every meeting in the building, whether invited or not.
    # Amusing, and true of a certain kind of boss, but it is a habit of
    # the calendar, not a sin against the people who work for them.
    "Meetingmagnet": (8, 7, 8, 7, 7),
}


def total(word):
    """Add up one candidate's five marks."""
    return sum(CANDIDATE_MARKS[word])


def acceptable(word):
    """One word only: a string of 1 to 30 letters, nothing else."""
    return isinstance(word, str) and WORD_PATTERN.fullmatch(word) is not None


def ranking():
    """Candidates best first: highest total, then shortest word."""
    return sorted(CANDIDATE_MARKS, key=lambda w: (-total(w), len(w)))


def store(word):
    """Write the word as UTF-8 bytes and prove the round-trip is exact."""
    raw = word.encode("utf-8")
    ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENTRY_PATH.write_bytes(raw)
    back = ENTRY_PATH.read_bytes()
    if back != raw or not acceptable(back.decode("utf-8")):
        raise ValueError("round-trip check failed for %r" % (word,))
    return back.decode("utf-8")


def attempt(word):
    """Store one word, or None when it cannot be stored."""
    try:
        return store(word)
    except (OSError, ValueError, UnicodeDecodeError):
        return None


def run():
    for word in ranking():
        if acceptable(word) and attempt(word) is not None:
            sys.stdout.write(word + "\n")
            break
    else:
        raise RuntimeError("no candidate produced a valid entry")


if __name__ == "__main__":
    run()
