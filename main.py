# Tested on Python36

from collections import Counter, defaultdict
from re import split
from string import punctuation
import os
import sys


def trim_punctuation(s):
    excluded = set(punctuation)
    return ''.join(c for c in s if c not in excluded)


dir = os.path.dirname(__file__)
relative_path = sys.argv[1] if len(sys.argv) > 1 \
    else (input('Input file name (relative)? ') or 'q1.in')
filename = os.path.join(dir, relative_path)

with open(filename) as f:
    sentences = []
    sentence_count = 0
    word_count = 0
    words_seen = Counter()
    common_phrases = defaultdict(int)

    for line in f:
        lines_processed = split(r'[\.?!] ', line.strip().lower())

        if lines_processed != ['']:
            # if actual sentences needed in future
            #sentences.extend(lines_processed)
            sentence_count += len(lines_processed)

            # process each sentence to omit punctuation, non-words
            for sentence in lines_processed:
                words = [trim_punctuation(w) for w in sentence.split()]
                words = list(filter(lambda w: w.isalpha(), words))
                word_count += len(words)
                words_seen += Counter(words)

                # find all phrases of length >= 3 in each sentence
                for start in range(len(words)):
                    for phrase_length in range(3, len(words) + 1):
                        phrase = words[start: start + phrase_length]
                        if len(phrase) == phrase_length:
                            common_phrases[' '.join(phrase)] += 1

    most_common_words = sorted(words_seen.items(), key=lambda pair: -pair[1])
    most_common_phrases = sorted(common_phrases.items(), key=lambda pair: -pair[1])

    print(f'Total word count: {word_count}')
    print(f'Unique words: {len(words_seen)}')
    print(f'Sentences: {sentence_count}')
    print(f'Average sentence length (in words): {round(word_count / sentence_count, 2)}')
    print(f'Common phrases: ')
    print(*(phrase for phrase in most_common_phrases if phrase[1] >= 3))
    print(f'Word Frequencies: ')
    print(*most_common_words)
