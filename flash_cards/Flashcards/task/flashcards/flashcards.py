# Write your code here
import random
import io
import argparse


class FlashCards:

    def __init__(self):
        self.cards = {}
        self.cards_stats = {}
        self.output = io.StringIO()

    def create_card(self):
        cards_finished = False
        term_exists = False
        definition_exists = False
        cards_number = len(self.cards)
        while not cards_finished:
            if not definition_exists:
                if not term_exists:
                    print('The card:')
                    self.output.write('The card:\n')
                term = input()
                self.output.write(f'{term}\n')
                if term in self.cards.keys():
                    term_exists = True
                    print(f'The card "{term}" already exists.')
                    self.output.write(f'The card "{term}" already exists.\n')
                    continue
            if not definition_exists:
                print(f'The definition of the card:')
                self.output.write(f'The definition of the card:\n')
            definition = input()
            self.output.write(f'{definition}\n')
            if definition in self.cards.values():
                definition_exists = True
                print(f'The definition "{definition}" already exists.')
                self.output.write(f'The definition "{definition}" already exists.\n')
                continue
            self.cards[term] = definition
            self.cards_stats[term] = 0
            print(f'The pair ("{term}":"{definition}") has been added.\n')
            self.output.write(f'The pair ("{term}":"{definition}") has been added.\n')
            if len(self.cards.keys()) == cards_number + 1:
                cards_finished = True

    def remove_card(self):
        print("Which card?")
        self.output.write("Which card?\n")
        card_term = input()
        self.output.write(f'{card_term}\n')
        if self.cards.pop(card_term, -1) == -1:
            print(f'Can\'t remove "{card_term}": there is no such card.\n')
            self.output.write(f'Can\'t remove "{card_term}": there is no such card.\n')
        else:
            self.cards_stats.pop(card_term)
            print("The card has been removed.\n")
            self.output.write("The card has been removed.\n")

    def export_cards(self, export_path=None):
        if export_path:
            file_name = export_path
        else:
            print("File name:")
            self.output.write("File name:\n")
            file_name = input()
            self.output.write(f'{file_name}\n')
        with open(file_name, "w") as f:
            for key, val in self.cards.items():
                f.write(f"{key}:{val}:{self.cards_stats[key]}\n")
            f.close()
        print(f"{len(self.cards)} cards have been saved.\n")
        self.output.write(f"{len(self.cards)} cards have been saved.\n")

    def log(self):
        print("File name:")
        self.output.write("File name:\n")
        file_name = input()
        self.output.write(f'{file_name}\n')
        with open(file_name, "w") as f:
            f.write(self.output.getvalue())
        f.close()
        print("The log has been saved.")
        self.output.write("The log has been saved.\n")

    def import_cards(self, import_path=None):
        if import_path:
            file_name = import_path
        else:
            print("File name:")
            self.output.write("File name:\n")
            file_name = input()
            self.output.write(f'{file_name}\n')
        try:
            f = open(file_name, 'r')
            i = 0
            for line in f.readlines():
                term, definition, stats = line.strip().split(':')
                self.cards[term] = definition
                self.cards_stats[term] = int(stats)
                i += 1
            f.close()
            print(f"{i} cards have been loaded.\n")
            self.output.write(f"{i} cards have been loaded.\n")
        except FileNotFoundError:
            print("File not found.\n")
            self.output.write("File not found.\n")

    def ask(self):
        print("How many times to ask?")
        self.output.write("How many times to ask?\n")
        ask_times = int(input())
        self.output.write(f'{ask_times}\n')
        for i in range(ask_times):
            term = random.choice(list(self.cards.keys()))
            print(f'Print the definition of "{term}":')
            self.output.write(f'Print the definition of "{term}":\n')
            answer = input()
            self.output.write(f'{answer}\n')
            if self.check_answer(self.cards[term], answer):
                print('Correct!')
                self.output.write('Correct!\n')
            else:
                self.cards_stats[term] += 1
                if answer in self.cards.values():
                    answer_pos = list(self.cards.values()).index(answer)
                    print(f'Wrong. The right answer is "{self.cards[term]}", '
                          f'but your definition is correct for {list(self.cards.keys())[answer_pos]}.')
                    self.output.write(f'Wrong. The right answer is "{self.cards[term]}", '
                          f'but your definition is correct for {list(self.cards.keys())[answer_pos]}.\n')
                else:
                    print(f'Wrong. The right answer is "{self.cards[term]}".')
                    self.output.write(f'Wrong. The right answer is "{self.cards[term]}".\n')
        print()
        self.output.write("\n")

    @staticmethod
    def check_answer(definition, answer):
        return definition.lower() == answer.lower()

    def hard_cards(self):
        if sum(self.cards_stats.values()) == 0:
            print("There are no cards with errors.")
            self.output.write("There are no cards with errors.\n")
        else:
            stats_sorted = dict(sorted(self.cards_stats.items(), reverse=True, key=lambda item: item[1]))
            if stats_sorted[list(stats_sorted)[0]] > stats_sorted[list(stats_sorted)[1]]:
                print(f'The hardest card is "{list(stats_sorted)[0]}". '
                      f'You have {stats_sorted[list(stats_sorted)[0]]} errors answering it.\n')
                self.output.write(f'The hardest card is "{list(stats_sorted)[0]}". '
                                  f'You have {stats_sorted[list(stats_sorted)[0]]} errors answering it.\n')
            else:
                stats_values = list(stats_sorted.values())
                wrong_terms = [list(stats_sorted)[0]]
                max_val = stats_values[0]
                i = 1
                while max_val == stats_values[i]:
                    wrong_terms.append(list(stats_sorted)[i])
                    i += 1
                print(f'The hardest cards are "{" ".join(wrong_terms)}".')
                self.output.write(f'The hardest cards are "{" ".join(wrong_terms)}".\n')

    def reset_stats(self):
        for term in self.cards_stats.keys():
            self.cards_stats[term] = 0
        print("Card statistics have been reset.")
        self.output.write("Card statistics have been reset.\n")

    def write_actions(self, action):
        self.output.write(f'{action}\n')


def parse_args():
    parser = argparse.ArgumentParser(description="This is a Falshcards app.")
    parser.add_argument("--import_from", help="Import flashcards info from a file")
    parser.add_argument("--export_to", help="Write all flashcards info to a file")
    return parser.parse_args()


def main(args):
    flashcards = FlashCards()

    if args.import_from:
        flashcards.import_cards(args.import_from)

    while True:
        print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        flashcards.write_actions(
            "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        user_action = input()
        flashcards.write_actions(user_action)

        if user_action == "exit":
            if args.export_to:
                flashcards.export_cards(args.export_to)
            print("Bye bye!")
            flashcards.write_actions("Bye bye!")
            break
        elif user_action == "add":
            flashcards.create_card()
        elif user_action == "remove":
            flashcards.remove_card()
        elif user_action == "import":
            flashcards.import_cards()
        elif user_action == "export":
            flashcards.export_cards()
        elif user_action == "ask":
            flashcards.ask()
        elif user_action == "log":
            flashcards.log()
        elif user_action == "hardest card":
            flashcards.hard_cards()
        elif user_action == "reset stats":
            flashcards.reset_stats()


if __name__ == '__main__':
    args = parse_args()
    main(args)