import logging
import datetime
from collections import Counter, defaultdict
import math

DATEFORMAT = "%y%m%d"
# DAYS   30  14  7
# MIN    6   4   4
DAYSRECENT = 30  # Anzahl Tage für "aktuell"
MINCOUNT = DAYSRECENT // 5  # Minimale Häufigkeit für Berücksichtigung
MINSCORE = 10.0  # Minimale Signifikanz für Ausgabe


def parse_line(line):
    datestr, headline = line.strip().split(";", 1)
    date = datetime.datetime.strptime(datestr, DATEFORMAT).date()
    words = headline.lower().split()
    return date, words


def get_ngrams(words, n=1):
    return [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]


def analyze(file_path):
    today = datetime.date.today()
    recentcutoff = today - datetime.timedelta(days=DAYSRECENT)

    recentcounts = Counter()
    pastcounts = Counter()
    totalrecent = 0
    totalpast = 0

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            date, words = parse_line(line)
            for n in [1, 2, 3]:  # Unigrams und Bigrams
                ngrams = get_ngrams(words, n)
                if date >= recentcutoff:
                    recentcounts.update(ngrams)
                    totalrecent += len(ngrams)
                else:
                    pastcounts.update(ngrams)
                    totalpast += len(ngrams)

    # Signifikanzbewertung (Log-Likelihood-Ratio)
    def llr(krecent, kpast, nrecent, npast):
        def safelog(x):
            return math.log(x) if x > 0 else 0

        ktotal = krecent + kpast
        ntotal = nrecent + npast
        p = ktotal / ntotal
        p1 = krecent / nrecent if nrecent else 0
        p2 = kpast / npast if npast else 0
        ll = 0
        if krecent > 0:
            ll += krecent * safelog(p1 / p)
        if kpast > 0:
            ll += kpast * safelog(p2 / p)
        return 2 * ll

    results = []
    allkeys = set(recentcounts.keys()) | set(pastcounts.keys())
    for key in allkeys:
        score = llr(recentcounts[key], pastcounts[key], totalrecent, totalpast)
        if score > MINSCORE and recentcounts[key] >= MINCOUNT:  # Schwellenwert
            results.append((key, score, recentcounts[key]))

    results.sort(key=lambda x: -x[1])
    print(f"\n{DAYSRECENT} recent days, cutoff date: {recentcutoff}")
    print(f"Total recent ngrams: {totalrecent}, Total past ngrams: {totalpast}")
    print(
        f"Considered {len(allkeys)} unique ngrams, found {len(results)} significant ones."
    )
    print(f"Top ngrams (count > {MINCOUNT}, score > {MINSCORE}):")
    return results
