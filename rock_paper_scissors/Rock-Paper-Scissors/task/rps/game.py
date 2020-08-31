import random


def print_win(result, option=None):
    if result == "lose":
        print(f"Sorry, but the computer chose {option}")
    elif result == "draw":
        print(f"There is a draw ({option})")
    elif result == "win":
        print(f"Well done. The computer chose {option} and failed")
    elif result == "!exit":
        print("Bye!")


with open('rating.txt') as f:
    ratings = {}
    for line in f:
        line = line.split()
        ratings[line[0]] = int(line[1])

user_name = input('Enter your name: ')
print(f'Hello, {user_name}')
if user_name in ratings.keys():
    user_rating = ratings[user_name]
else:
    user_rating = 0

outcomes = input()
if outcomes == '':
    outcomes = ['rock', 'paper', 'scissors']
else:
    outcomes = outcomes.split(',')
print("Okay, let's start")
valid_input = [item for item in outcomes]
valid_input.extend(['!exit', '!rating'])

while True:
    user_choice = input()
    rand_int = random.randint(0, len(outcomes)-1)
    computer_choice = outcomes[rand_int]

    if user_choice not in valid_input:
        print("Invalid input")
    elif user_choice == "!exit":
        print_win("!exit")
        break
    elif user_choice == "!rating":
        print(f"Your rating: {user_rating}")
    else:
        choice_index = outcomes.index(user_choice)
        new_options_list = outcomes[choice_index+1:] + outcomes[:choice_index]
        beating_list = new_options_list[:len(new_options_list)//2]
        defeated_list = new_options_list[len(new_options_list)//2:]
        if user_choice == computer_choice:
            print_win("draw", user_choice)
            user_rating += 50
        elif computer_choice in beating_list:
            print_win("lose", computer_choice)
        elif computer_choice in defeated_list:
            print_win("win", computer_choice)
            user_rating += 100