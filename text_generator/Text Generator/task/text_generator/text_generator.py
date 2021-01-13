# Write your code here
from nltk.tokenize import WhitespaceTokenizer
from nltk.util import bigrams, trigrams
from collections import Counter, defaultdict
import random


def get_corpus_stats(text_content):
    return WhitespaceTokenizer().tokenize(text_content)


def get_grams(tokens, mode="bigrams"):
    if mode == "bigrams":
        return bigrams(tokens)
    if mode == "trigrams":
        return trigrams(tokens)


def build_markov_model(grams, mode='bigrams'):
    markov_dict = defaultdict(list)
    for i in grams:
        if mode == 'bigrams':
            markov_dict[i[0]].append(i[1])
        else:
            markov_dict[i[0] + " " + i[1]].append(i[2])

    for k, v in markov_dict.items():
        markov_dict[k] = Counter(v)

    return markov_dict


def print_corpus_stats(tokens, mode="tokens"):
    if mode == "tokens":
        print('Corpus statistics')
        print(f'All tokens: {len(tokens)}')
        print(f'Unique tokens: {len(set(tokens))}')
    elif mode == 'bigrams':
        print(f'Number of bigrams: {len(tokens) - 1}')


def generate_text(markov_dict, mode='bigrams'):
    if mode == 'bigrams':
        first_word = random.choice(list(markov_dict.keys()))
        while not first_word[0].isupper() or first_word[-1] in [".", "!", "?"]:
            first_word = random.choice(list(markov_dict.keys()))

        for i in range(10):
            sentence = first_word
            next_word = first_word
            complete_sentence = False
            while not complete_sentence:
                if len(sentence.split()) < 5:
                    item = markov_dict[next_word]
                    if list(item.keys()):
                        next_word = random.choices(population=list(item.keys()), weights=list(item.values()))[0]
                        sentence += f' {next_word}'
                elif next_word[-1] not in [".", "!", "?"]:
                    item = markov_dict[next_word]
                    next_word = random.choices(population=list(item.keys()), weights=list(item.values()))[0]
                    sentence += f' {next_word}'
                else:
                    complete_sentence = True
            print(sentence.strip())
            first_word = next_word
            while not first_word[0].isupper() or first_word[-1] in [".", "!", "?"]:
                first_word = random.choice(list(markov_dict.keys()))

    if mode == 'trigrams':
        first_word = random.choice(list(markov_dict.keys()))
        while not first_word[0].isupper() or first_word.split()[0][-1] in [".", "!", "?"]:
            first_word = random.choice(list(markov_dict.keys()))

        for i in range(10):
            sentence = first_word
            next_word = first_word
            complete_sentence = False
            while not complete_sentence:
                if len(sentence.split()) < 5:
                    item = markov_dict[next_word]
                    if list(item.keys()):
                        next_word = random.choices(population=list(item.keys()), weights=list(item.values()))[0]
                        sentence += f' {next_word}'
                        next_word = sentence.split()[-2] + " " + sentence.split()[-1]
                elif next_word[-1] not in [".", "!", "?"]:
                    item = markov_dict[next_word]
                    next_word = random.choices(population=list(item.keys()), weights=list(item.values()))[0]
                    sentence += f' {next_word}'
                    next_word = sentence.split()[-2] + " " + sentence.split()[-1]
                else:
                    complete_sentence = True
            print(sentence.strip())
            first_word = next_word
            while not first_word[0].isupper() or first_word.split()[0][-1] in [".", "!", "?"]:
                first_word = random.choice(list(markov_dict.keys()))


mode = 'generate'
text_file = input('')
data = open(text_file, "r", encoding="utf-8").read()
tokenized_data = get_corpus_stats(data)
# For bigrams
# grams_data = list(get_grams(tokenized_data))
# For trigrams
grams_data = list(get_grams(tokenized_data, mode="trigrams"))

markov_dict = build_markov_model(grams_data, mode="trigrams")
# print_corpus_stats(tokenized_data, mode=mode)

if mode == 'generate':
    generate_text(markov_dict, mode="trigrams")
else:
    while True:
        user_input = input('')
        if user_input == "exit":
            break

        try:
            if mode != "markov":
                user_input = int(user_input)
            try:
                if mode == "bigrams":
                    print(f'Head: {grams_data[user_input][0]} \t Tail: {grams_data[user_input][1]}')
                elif mode == "tokens":
                    print(tokenized_data[user_input])
                elif mode == "markov":
                    print(f"Head: {user_input}")
                    if user_input in markov_dict:
                        for item in markov_dict[user_input].most_common():
                            print(f"Tail: {item[0]} \t Count: {item[1]}")
                        print()
                    else:
                        print("Key Error. The requested word is not in the model. Please input another word.\n")
                elif mode == "generate":
                    generate_text(markov_dict)
            except IndexError:
                print('Index Error. Please input an integer that is in the range of the corpus.')
        except ValueError:
            print('Type Error. Please input an integer.')