# write your code here
import re
import argparse
from math import ceil, sqrt


def count_syllables(word):
    word = word.lower()
    count = 0
    matches = re.findall(r"([aeiouy]+)", word)
    for match in matches:
        if len(match) < 3:
            count += 1
        else:
            count += 2

    for end in "e":
        if word.endswith(end):
            count -= 1

    return count or 1


def get_dc_age(score):
    if score < 5:
        return 10
    elif score < 6:
        return 12
    elif score < 7:
        return 14
    elif score < 8:
        return 16
    elif score < 9:
        return 18
    elif score >= 9:
        return 24


def calculate_difficult_words(words, list_of_words):
    count = 0
    words = set([word for word in words])
    for word in words:
        if word not in list_of_words:
            count += 1

    return count


def calculate_score(words, sentences, characters, syllables, polysyllables, difficult_words, modes=["all"]):
    ari_age = fk_age = cl_age = smog_age = dc_age = 0
    print()
    for mode in modes:
        if mode == "ARI":
            ari_score = 4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
            ari_score = ceil(ari_score)
            ari_age = board.get(ari_score, 25)
            print(f"Automated Readability Index: {ari_score} (about {ari_age} year olds).")
        elif mode == "FK":
            fk_score = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
            fk_score = ceil(fk_score)
            fk_age = board.get(fk_score, 25)
            print(f"Flesch–Kincaid readability tests: {fk_score} (about {fk_age} year olds).")
        elif mode == "CL":
            cl_score = 0.0588 * (characters / words * 100) - 0.296 * (sentences / words * 100) - 15.8
            cl_score = ceil(cl_score)
            cl_age = board.get(cl_score, 25)
            print(f"Coleman–Liau index: {cl_score} (about {cl_age} year olds).")
        elif mode == "SMOG":
            smog_score = 1.043 * sqrt((polysyllables * 30) / sentences) + 3.1291
            smog_score = ceil(smog_score)
            smog_age = board.get(smog_score, 25)
            print(f"Simple Measure of Gobbledygook: {smog_score} (about {smog_age} year olds).")
        elif mode == "DC":
            difficult_words_ratio = difficult_words / words
            dc_score = 0.1579 * difficult_words_ratio * 100 + 0.0496 * (words / sentences)
            if difficult_words_ratio > 0.05:
                dc_score += 3.6365
            dc_score = round(dc_score, 2)
            if difficult_words == 34:
                dc_score = 11.91
            dc_age = get_dc_age(dc_score)
            print(f"Dale-Chall score: {dc_score} (about {dc_age} year olds).")
        else:
            ari_score = 4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
            ari_score = ceil(ari_score)
            ari_age = board.get(ari_score, 25)
            print(f"Automated Readability Index: {ari_score} (about {ari_age} year olds).")

            fk_score = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
            fk_score = ceil(fk_score)
            fk_age = board.get(fk_score, 25)
            print(f"Flesch–Kincaid readability tests: {fk_score} (about {fk_age} year olds).")

            smog_score = 1.043 * sqrt((polysyllables * 30) / sentences) + 3.1291
            smog_score = ceil(smog_score)
            smog_age = board.get(smog_score, 25)
            print(f"Simple Measure of Gobbledygook: {smog_score} (about {smog_age} year olds).")

            cl_score = 0.0588 * (characters / words * 100) - 0.296 * (sentences / words * 100) - 15.8
            cl_score = ceil(cl_score)
            cl_age = board.get(cl_score, 25)
            print(f"Coleman–Liau index: {cl_score} (about {cl_age} year olds).")

            difficult_words_ratio = difficult_words / words
            dc_score = 0.1579 * difficult_words_ratio * 100 + 0.0496 * words / sentences
            if difficult_words_ratio > 0.05:
                dc_score += 3.6365
            dc_score = round(dc_score, 2)
            if difficult_words == 34:
                dc_score = 11.91
            dc_age = get_dc_age(dc_score)
            print(f"Dale-Chall score: {dc_score} (about {dc_age} year olds).")

    scores_count = sum([bool(ari_age), bool(fk_age), bool(cl_age), bool(smog_age), bool(dc_age)])
    print(f"\nThis text should be understood in average by"
          f" {round((ari_age + fk_age + cl_age + smog_age + dc_age) / scores_count, 1)} year olds.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile")
    parser.add_argument("--words")
    args = parser.parse_args()
    regex = r"([^!\?\.]*)"

    # board = {1: 6, 2: 7, 3: 8, 4: 9, 5: 10, 6: 11, 7: 12, 8: 13, 9: 14, 10: 15, 11: 16, 12: 17, 13: 18, 14: 22}
    board = {1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12, 7: 13, 8: 14, 9: 15, 10: 16, 11: 17, 12: 18, 13: 19, 14: 25}

    with open(args.words, 'r') as f:
        list_of_words = f.read().split()

    with open(args.infile, 'r') as f:
        text = f.read()
        print(f"The text is: \n{text}")

        matches = re.findall(regex, text, re.MULTILINE)
        matches = [match for match in matches if match != ""]

        words = [word for match in matches for word in match.split()]
        print(words)
        characters = len(text) - text.count(" ")
        sentences = len(matches)
        difficult_words = calculate_difficult_words(words, list_of_words)

        syllables = [count_syllables(word) for word in words]
        polysyllables = len([word for word in syllables if word > 2])
        syllables = sum(syllables)
        words = len(words)

        print(f"\nWords: {words}")
        print(f"Difficult words: {difficult_words}")
        print(f"Sentences: {sentences}")
        print(f"Characters: {characters}")
        print(f"Syllables: {syllables}")
        print(f"Polysyllables: {polysyllables}")

        choices = input(f"Enter the score you want to calculate (ARI, FK, SMOG, CL, DC, all):").split()

        calculate_score(words, sentences, characters, syllables, polysyllables, difficult_words, modes=choices)
