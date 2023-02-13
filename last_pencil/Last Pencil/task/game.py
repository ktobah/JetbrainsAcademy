import random

take_3_pencils = range(4, 200, 4)
take_2_pencils = range(3, 200, 4)
take_1_3_pencils = range(5, 200, 4)


def generate_bot_move(pencils):
    if pencils in take_3_pencils:
        return 3
    elif pencils in take_2_pencils:
        return 2
    elif pencils in take_1_3_pencils:
        return random.choice([1, 2, 3])
    else:
        return 1


while True:
    pencils = input("How many pencils would you like to use:")
    if not pencils.isdigit():
        print("The number of pencils should be numeric")
        continue
    pencils = int(pencils)
    if pencils <= 0:
        print("The number of pencils should be positive")
        continue
    break

while True:
    next_player = input("Who will be the first (Ahmed, Bouchra)").strip()
    if next_player not in ["Ahmed", "Bouchra"]:
        print("Choose between Ahmed and Bouchra")
        continue
    break

while pencils:
    print("|" * pencils)
    print(f"{next_player}'s turn:")
    if next_player == 'Bouchra':
        to_remove = generate_bot_move(pencils)
        print(to_remove)
    else:
        while True:
            to_remove = input()
            if not to_remove.isdigit():
                print("Possible values: '1', '2' or '3'")
                continue
            to_remove = int(to_remove)
            if to_remove < 1 or to_remove > 3:
                print("Possible values: '1', '2' or '3'")
                continue
            if to_remove > pencils:
                print("Too many pencils were taken")
                continue
            break
    pencils -= to_remove
    next_player = 'Ahmed' if next_player == 'Bouchra' else 'Bouchra'

print(f"{next_player} won!")
