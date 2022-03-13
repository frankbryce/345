#!/usr/bin/python3

import itertools
import random
from tqdm import tqdm

#N = {3: 50, 4: 50, 5: 50}
N = {4: 100}
L = N.keys()

# returns alphabetized list of chars in all words given to function
def chars_in(words: list[str]) -> str:
    chars = ''
    for word in words:
        chars += word
    return ''.join(sorted(chars))

def main():
    all_words: dict[int,list[str]] = dict()
    common_words: dict[int,list[str]] = dict()
    word_list: list[str] = list()
    with open('words.txt', 'r') as f:
        prog = tqdm(f.readlines())
        prog.set_description("Reading Dictionary...")
        for word in prog:
            word = word.rstrip('\n')
            if len(word) in L:
                word_list.append(word)

    for l in L:
        all_words[l] = list()
        common_words[l] = list()
    prog = tqdm(word_list)
    prog.set_description('Finding Most Common Words...')
    for word in prog:
        if len(word) not in N:
            print("Houston, we have a problem")
        if len(all_words[len(word)]) < 200:
            all_words[len(word)].append(word)
        if len(common_words[len(word)]) < N[len(word)]:
            common_words[len(word)].append(word)

    # build dict of {chars: list[(words,)]}
    puzzles: dict[str, tuple[...]] = dict()
    prog = tqdm(itertools.product(*common_words.values()))
    prog.set_description("Getting Common Word Combinations...")
    for words in prog:
        chars = chars_in(words)
        if chars not in puzzles:
            puzzles[chars] = list()
        puzzles[chars].append(tuple(words))

    # make sure all words don't have other solutions
    uniq_checker: dict[str, tuple[...]] = dict()
    prog = tqdm(itertools.product(*all_words.values()))
    prog.set_description("Getting All Word Combinations...")
    for words in prog:
        chars = chars_in(words)
        if chars not in uniq_checker:
            uniq_checker[chars] = list()
        uniq_checker[chars].append(tuple(words))

    found: list[tuple[...]] = list()
    prog = tqdm(puzzles.items())
    prog.set_description("Getting Puzzles w/ Unique Solution...")
    for chars, words in prog:
        if len(uniq_checker[chars]) == 1:
            found.append(words[0])

    print(f'found {len(found)} puzzles')

    random.shuffle(found)
    for choice in found:
        print(chars_in(list(choice)))
        input()
        print(choice)

if __name__ == '__main__':
    main()
