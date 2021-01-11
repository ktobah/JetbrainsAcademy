import random
# random.seed(42)

rock_paper_scissors = ["paper", "rock", "scissors"]


class Robot:

    def __init__(self, name):
        self.name = name
        self.battery_level = 100
        self.prev_battery_level = 100
        self.overheat_level = 0
        self.prev_overheat_level = 0
        self.skills_level = 0
        self.prev_skills_level = 0
        self.boredom_level = 0
        self.prev_boredom_level = 0
        self.rust_level = 0
        self.prev_rust_level = 0
        self.result_stats = {}
        self.unpleasant_events = ['NA', 'pool', 'puddle', 'sprinkler']

    def play(self):
        self.result_stats = game_play()
        self.prev_overheat_level = self.overheat_level
        self.prev_boredom_level = self.boredom_level
        self.boredom_level = self.boredom_level - 10 if self.boredom_level - 10 >= 0 else 0
        self.overheat_level = self.overheat_level + 10 if self.overheat_level + 10 < 100 else 100
        if self.overheat_level == 100:
            print(f"\nThe level of overheat reached 100, {self.name} has blown up! Game over. Try again?")
            exit()
        elif self.rust_level == 100:
            print(f"\n{self.name} is too rusty! Game over. Try again?")
            exit()
        else:
            print_stats(self.result_stats)
            print(f"\n{self.name}'s level of overheat was {self.prev_overheat_level}. Now it is {self.overheat_level}.")

        if self.boredom_level == 0:
            print(f"{self.name} is in a great mood!")
        elif self.boredom_level != 0 and self.prev_boredom_level == 0:
            print(f"\n{self.name}'s level of boredom was {self.prev_boredom_level}. Now it is {self.boredom_level}.")
        if self.prev_boredom_level != 0:
            print(f"\n{self.name}'s level of boredom was {self.prev_boredom_level}. Now it is {self.boredom_level}.")
        self.unpleasant_event()

    def recharge(self):
        if self.battery_level == 100:
            print(f"\n{self.name} is charged!")
        else:
            self.prev_overheat_level = self.overheat_level
            self.prev_boredom_level = self.boredom_level
            self.prev_battery_level = self.battery_level
            self.battery_level = self.battery_level + 10 if self.battery_level + 10 < 100 else 100
            self.boredom_level = self.boredom_level + 5 if self.boredom_level + 5 < 100 else 100
            self.overheat_level = self.overheat_level - 5 if self.overheat_level - 5 > 0 else 0
            print(f"\n{self.name}'s level of overheat was {self.prev_overheat_level}. Now it is {self.overheat_level}.")
            print(f"{self.name}'s level of the battery was {self.prev_battery_level}. Now it is {self.battery_level}.")
            print(f"{self.name}'s level of boredom was {self.prev_boredom_level}. Now it is {self.boredom_level}.")
            print(f"{self.name} is recharged!")

    def sleep(self):
        if self.overheat_level == 0:
            print(f"\n{self.name} is cool!")
        else:
            self.prev_overheat_level = self.overheat_level
            self.overheat_level = self.overheat_level - 20 if self.overheat_level - 20 > 0 else 0
            print(f"\n{self.name}'s level of overheat was {self.prev_overheat_level}. Now it is {self.overheat_level}.")
            if self.overheat_level == 0:
                print(f"\n{self.name} is cool!")
            else:
                print(f"\n{self.name} cooled off!")

    @staticmethod
    def exit():
        print('\nGame over.')
        exit()

    def info(self):
        print(f"\n{self.name}'s stats are:")
        print(f"battery is {self.battery_level},")
        print(f"overheat is {self.overheat_level},")
        print(f"skill level is {self.skills_level},")
        print(f"boredom is {self.boredom_level},")
        print(f"rust is {self.rust_level}.")

    def learn(self):
        if self.skills_level == 100:
            print(f"\nThere's nothing for {self.name} to learn!")
        else:
            self.prev_skills_level = self.skills_level
            self.prev_overheat_level = self.overheat_level
            self.prev_battery_level = self.battery_level
            self.prev_boredom_level = self.boredom_level
            self.skills_level = self.skills_level + 10 if self.skills_level + 10 <= 100 else 100
            # self.skills_level += 10
            self.overheat_level = self.overheat_level + 10 if self.overheat_level + 10 < 100 else 100
            self.boredom_level = self.boredom_level + 5 if self.boredom_level + 5 < 100 else 100
            self.battery_level = self.battery_level - 10 if self.battery_level - 10 > 0 else 0
            print(f"\n{self.name}'s level of skill was {self.prev_skills_level}. Now it is {self.skills_level}.")
            print(f"{self.name}'s level of overheat was {self.prev_overheat_level}. Now it is {self.overheat_level}.")
            print(f"{self.name}'s level of the battery was {self.prev_battery_level}. Now it is {self.battery_level}.")
            print(f"{self.name}'s level of boredom was {self.prev_boredom_level}. Now it is {self.boredom_level}.")
            print(f"{self.name} has become smarter!")

    def work(self):
        if self.skills_level < 50:
            print(f"{self.name} has got to learn before working!")
        else:
            self.prev_overheat_level = self.overheat_level
            self.prev_battery_level = self.battery_level
            self.prev_boredom_level = self.boredom_level
            self.battery_level = self.battery_level - 10 if self.battery_level - 10 > 0 else 0
            self.overheat_level = self.overheat_level + 10 if self.overheat_level + 10 < 100 else 100
            self.boredom_level = self.boredom_level + 10 if self.boredom_level + 10 < 100 else 100
            print(f"\n{self.name} did well!")
            print(f"\n{self.name}'s level of boredom was {self.prev_boredom_level}. Now it is {self.boredom_level}.")
            print(f"\n{self.name}'s level of overheat was {self.prev_overheat_level}. Now it is {self.overheat_level}.")
            print(f"\n{self.name}'s level of the battery was {self.prev_battery_level}. Now it is {self.battery_level}.")

            self.unpleasant_event()

    def oil(self):
        if self.rust_level == 0:
            print(f"{self.name} is fine, no need to oil!")
        else:
            self.prev_rust_level = self.rust_level
            self.rust_level = self.rust_level - 20 if self.rust_level - 20 > 0 else 0
            print(f"\n{self.name}'s level of rust was {self.prev_rust_level}. Now it is {self.rust_level}. {self.name} is less rusty!")

    def unpleasant_event(self):
        rust_event = self.unpleasant_events[random.randint(0, 3)]
        if rust_event == 'NA':
            return
        else:
            self.prev_rust_level = self.rust_level
            if rust_event == 'puddle':
                self.rust_level = self.rust_level + 10 if self.rust_level + 10 < 100 else 100
                print(f"\nOh no, {self.name} stepped into a puddle!")
            elif rust_event == 'sprinkler':
                self.rust_level = self.rust_level + 30 if self.rust_level + 30 < 100 else 100
                print(f"\nOh, {self.name} encountered a sprinkler!")
            elif rust_event == 'pool':
                self.rust_level = self.rust_level + 50 if self.rust_level + 50 < 100 else 100
                print(f"\nGuess what! {self.name} fell into the pool!")
            print(f"\n{self.name}'s level of rust was {self.prev_rust_level}. Now it is {self.rust_level}.")
        if self.rust_level >= 100:
            print(f"\n{self.name} is too rusty! Game over. Try again?")


class NegativeNumberError(Exception):
    def __str__(self):
        return "\nThe number can't be negative!"


class TextStringError(Exception):
    def __str__(self):
        return "\nA string is not a valid input!"


class NotInBoundError(Exception):
    def __str__(self):
        return "\nInvalid input! The number can't be bigger than 1000000."


class NotValidChoiceError(Exception):
    def __str__(self):
        return "No such option! Try again!"


def print_stats(stats: dict):
    print()
    print(f"You won: {stats['human']},")
    print(f"The robot won: {stats['robot']},")
    print(f"Draws: {stats['draw']}.")


def check_input(user_input, game="numbers"):
    if game == "numbers":
        try:
            user_input = int(user_input)
        except ValueError:
            raise TextStringError

        if user_input < 0:
            raise NegativeNumberError
        if user_input > 1000000:
            raise NotInBoundError
    elif user_input not in ["paper", "rock", "scissors"]:
        raise NotValidChoiceError

    return user_input


def generate_random_choice(game="numbers"):
    if game == "numbers":
        return random.randint(0, 1000000)
    else:
        return rock_paper_scissors[random.randint(0, 2)]


def check_winner_update(user_input, robot_guess, total_results, computer_num=None, game="numbers"):
    if game == "numbers":
        print(f"\nThe robot entered the number {robot_guess}.")
        print(f"The goal number is {computer_num}.")
        user_comp_distance = abs(computer_num - user_input)
        robot_comp_distance = abs(computer_num - robot_guess)

        if robot_comp_distance < user_comp_distance:
            print("The robot won!")
            total_results['robot'] += 1
        elif user_comp_distance < robot_comp_distance:
            print("You won!")
            total_results['human'] += 1
        elif user_comp_distance == robot_comp_distance:
            print("It's a draw!")
            total_results['draw'] += 1
    else:
        print(f"Robot chose {robot_guess}")
        if (user_input == "scissors" and robot_guess == "paper") \
                or (user_input == "rock" and robot_guess == "scissors") \
                or (user_input == "paper" and robot_guess == "rock"):
            print("You won!")
            total_results['human'] += 1
        elif (robot_guess == "scissors" and user_input == "paper") \
                or (robot_guess == "rock" and user_input == "scissors") \
                or (robot_guess == "paper" and user_input == "rock"):
            print("Robot won!")
            total_results['robot'] += 1
        else:
            print("It's a draw!")
            total_results['draw'] += 1


def game_play():
    result = {"human": 0, "robot": 0, "draw": 0}
    while True:
        user_choice = input('\nWhich game would you like to play? ').lower()
        if user_choice in ["numbers", "rock-paper-scissors"]:
            while True:
                if user_choice == "numbers":
                    user_input = input("\nWhat is your number?")
                else:
                    user_input = input("\nWhat is your move? ").lower()
                if user_input == "exit game":
                    return result

                try:
                    user_input = check_input(user_input, game=user_choice)
                except TextStringError as e:
                    print(e)
                    continue
                except NegativeNumberError as e:
                    print(e)
                    continue
                except NotInBoundError as e:
                    print(e)
                    continue
                except NotValidChoiceError as e:
                    print(e)
                    continue

                if user_choice == "numbers":
                    hidden_num = generate_random_choice(game=user_choice)
                    robot_choice = generate_random_choice(game=user_choice)
                    check_winner_update(user_input, robot_choice, result, hidden_num, game=user_choice)
                else:
                    robot_choice = generate_random_choice(game=user_choice)
                    check_winner_update(user_input, robot_choice, result, game=user_choice)
        else:
            print("\nPlease choose a valid option: Numbers or Rock-paper-scissors?\n")


# result_stats = {"human": 0, "robot": 0, "draw": 0}
robot_name = input("How will you call your robot? ")
robot = Robot(robot_name)
while True:
    print(f"\nAvailable interactions with {robot.name}:")
    print("exit – Exit")
    print("info – Check the vitals")
    print("work – Work")
    print("play – Play")
    print("oil – Oil")
    print("recharge – Recharge")
    print("sleep – Sleep mode")
    print("learn – Learn skills\n")
    user_interaction = input('Choose: ')
    if user_interaction not in ["info", "sleep", "play", "recharge", "exit", "learn", "work", "oil"]:
        print("\nInvalid input, try again!")
        continue
    elif robot.boredom_level == 100 and user_interaction != "play":
        print(f"{robot.name} is too bored! {robot.name} needs to have fun!")
        continue
    elif user_interaction in ["info", "sleep", "play", "learn", "work", "oil"] and robot.battery_level == 0:
        print(f"The level of the battery is 0, {robot.name} needs recharging!")
        # continue
    elif user_interaction == "recharge":
        robot.recharge()
    if user_interaction == "exit":
        robot.exit()
    elif user_interaction == "info":
        robot.info()
    elif user_interaction == "sleep":
        robot.sleep()
    elif user_interaction == "play":
        robot.play()
    elif user_interaction == "learn":
        robot.learn()
    elif user_interaction == "work":
        robot.work()
    elif user_interaction == "oil":
        robot.oil()