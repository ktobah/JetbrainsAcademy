import re
import random

MIN_LENGTH: int = 100
money = 1000
main_text = ""


def generate_predictions(test_str, triads):
    all_matches = list(re.findall(r"(?=(.{3}))", test_str, re.MULTILINE))[:-1]
    predictions = ""
    for match in all_matches:
        if triads[match][0] > triads[match][1]:
            predictions += "0"
        elif triads[match][0] < triads[match][1]:
            predictions += "1"
        else:
            predictions += random.choice(["0", "1"])

    return predictions


def calculate_accuracy(test_str, predictions):
    test_str = test_str[3:]
    accuracy = 0
    for i, j in zip(test_str, predictions):
        if i == j:
            accuracy += 1
    return accuracy


print('Please provide AI some data to learn...')
while len(main_text) < 100:
    print(f"The current data length is {len(main_text)}, {MIN_LENGTH - len(main_text)} symbols left")
    in_string = input('Print a random string containing 0 or 1:\n')
    in_string = re.sub(r"[^01]", "", in_string, 0, re.MULTILINE)
    main_text += in_string

print("\nFinal data string:\n", main_text, "\n")

triads_counts = {}
for i in ['000', '001', '010', '011', '100', '101', '110', '111']:
    matches_zero = re.findall(f"((?={i}0))", main_text, re.MULTILINE)
    matches_one = re.findall(f"((?={i}1))", main_text, re.MULTILINE)
    triads_counts[i] = [len(matches_zero), len(matches_one)]

print('You have $1000. Every time the system successfully predicts your next press, you lose $1. \n'
      'Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!')


while True:
    print('\nPrint a random string containing 0 or 1:\n')
    test_string = input()
    if test_string.lower() == 'enough':
        break
    test_string = re.sub(r"[^01]", "", test_string, 0, re.MULTILINE)
    while len(test_string) < 4:
        print('\nPrint a random string containing 0 or 1:\n')
        test_string = input()
        if test_string.lower() == 'enough':
            break
        test_string = re.sub(r"[^01]", "", test_string, 0, re.MULTILINE)
    if test_string.lower() == 'enough':
        break

    predictions = generate_predictions(test_string, triads_counts)
    print("predictions:\n", predictions, "\n")

    if not predictions:
        accuracy = 0
        print(f"Computer guessed right 0 out of {len(predictions)} symbols right (0 %)")
    else:
        accuracy = calculate_accuracy(test_string, predictions)
        print(f"Computer guessed right {accuracy} out of {len(predictions)} symbols right"
              f" ({round((accuracy * 100) / len(predictions), 2)} %)")

    money_lost = accuracy
    money_gained = len(predictions) - accuracy
    if money_lost > money_gained:
        money -= money_lost - money_gained
    else:
        money += money_gained - money_lost
    print(f"Your balance is now ${money}")

print("Game over!")
