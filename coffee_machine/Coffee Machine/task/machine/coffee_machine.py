class CoffeeMachine:
    # current supply
    current_money = 550
    current_water = 400
    current_milk = 540
    current_beans = 120
    current_cups = 9
    state = "resting"

    def change_state(self, action=None):
        if action == "buy":
            self.state = "buying"
        elif action == "fill":
            self.state = "filling"
        elif action == "take":
            self.state = "taking"
        elif action == "remain":
            self.state = "remaining"
        else:
            self.state = "resting"

    def process(self, user_input=None):
        if self.state == "buying":
            self.buy(user_input[0])
        elif self.state == "filling":
            self.fill(user_input[0], user_input[1], user_input[2], user_input[3])
        elif self.state == "taking":
            self.take()
        elif self.state == "remaining":
            self.remaining()
        self.change_state()

    def fill(self, extra_water, extra_milk, extra_beans, extra_cups):
        # global current_water, current_milk, current_beans, current_cups
        print()
        self.current_water += extra_water
        self.current_milk += extra_milk
        self.current_beans += extra_beans
        self.current_cups += extra_cups
        print()

    def buy(self, coffee_type):
        # global current_water, current_milk, current_beans, current_cups, current_money
        if coffee_type == "back":
            return
        else:
            if int(coffee_type) == 1:
                water_needed = 250
                milk_needed = 0
                beans_needed = 16
                cost = 4
            elif int(coffee_type) == 2:
                water_needed = 350
                milk_needed = 75
                beans_needed = 20
                cost = 7
            elif int(coffee_type) == 3:
                water_needed = 200
                milk_needed = 100
                beans_needed = 12
                cost = 6

            if (self.current_water >= water_needed) & (self.current_milk >= milk_needed) & (self.current_beans >= beans_needed):
                print("I have enough resources, making you a coffee!")
                self.current_water -= water_needed
                self.current_milk -= milk_needed
                self.current_beans -= beans_needed
                self.current_cups -= 1
                self.current_money += cost
            elif self.current_water < water_needed:
                print('Sorry, not enough water!')
            elif self.current_milk < milk_needed:
                print('Sorry, not enough milk!')
            elif self.current_beans < beans_needed:
                print('Sorry, not enough beans!')
            print()

    def take(self):
        # self.current_money
        print()
        print(f'I gave you {self.current_money}')
        self.current_money = 0
        print()

    def remaining(self):
        print()
        print('The coffee machine has:')
        print(f'{self.current_water} of water')
        print(f'{self.current_milk} of milk')
        print(f'{self.current_beans} coffee beans')
        print(f'{self.current_cups} of disposable cups')
        print(f'{self.current_money} of money')
        print()


coffee_machine = CoffeeMachine()

while True:
    action = input('Write action (buy, fill, take, remaining, exit): ')

    if action == "buy":
        coffee_machine.change_state("buy")
        print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu: ")
        coffee_type = input()
        coffee_machine.process([coffee_type])
    elif action == "fill":
        coffee_machine.change_state("fill")
        extra_water = int(input("Write how many ml of water do you want to add: "))
        extra_milk = int(input("Write how many ml of milk do you want to add: "))
        extra_beans = int(input("Write how many grams of coffee beans do you want to add: "))
        extra_cups = int(input("Write how many disposable cups of coffee do you want to add: "))
        coffee_machine.process([extra_water, extra_milk, extra_beans, extra_cups])
    elif action == "take":
        coffee_machine.change_state("take")
        coffee_machine.process()
    elif action == "remaining":
        coffee_machine.change_state("remain")
        coffee_machine.process()
    elif action == "exit":
        break
