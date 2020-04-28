# Write your code here
from random import choice
from string import ascii_lowercase


def print_masked_word(masked_word, empty_line="none"):
    printed_word = ""
    if empty_line == "before":
        print()
        for i in masked_word:
            printed_word = printed_word + i
        print(printed_word)
    elif empty_line == "middle":
        for i in masked_word:
            printed_word = printed_word + i
        print()
        print(printed_word)
    else:
        for i in masked_word:
            printed_word = printed_word + i
        print(printed_word)


def play(lives):
    print()
    print_masked_word(masked_word)
    while lives != 0:
        guessed_letter = input(f'Input a letter: ')
        if len(guessed_letter) != 1:
            print('You should print a single letter')
            print_masked_word(masked_word, empty_line="before")
        elif guessed_letter not in ascii_lowercase:
            print('It is not an ASCII lowercase letter')
            print_masked_word(masked_word, empty_line="before")
        else:
            if guessed_letter in already_guessed:
                print("You already typed this letter")
                print_masked_word(masked_word, empty_line="before")
            else:
                already_guessed.add(guessed_letter)
                if guessed_letter in word_letters:
                    for idx, i in enumerate(secret_word):
                        if i == guessed_letter:
                            masked_word[idx] = guessed_letter
                    print_masked_word(masked_word, empty_line="middle")
                else:
                    print("No such letter in the word")
                    if lives != 1:
                        print_masked_word(masked_word, empty_line="before")
                    lives -= 1

        if already_guessed == word_letters:
            print('You guessed the word!')
            print('You survived!')
            break

    if already_guessed != word_letters:
        print('You are hanged!')
    print()


words_list = ['python', 'java', 'kotlin', 'javascript']
secret_word = choice(words_list)
tries = 8
masked_word = ['-'] * len(secret_word)
word_letters = set(secret_word)
already_guessed = set()

print('H A N G M A N')
while True:
    choice = input('Type "play" to play the game, "exit" to quit: ')
    if choice == "play":
        play(tries)
    elif choice == "exit":
        break
