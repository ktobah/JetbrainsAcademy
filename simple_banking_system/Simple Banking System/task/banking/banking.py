# Write your code here
import sqlite3
import random
import sys


def read_input():
    print("1. Create an account\n2. Log into account\n0. Exit")
    input_value = int(input())
    return input_value


def login(conn, cursor):
    card_id = input("\nEnter your card number:")
    pin = input("Enter your PIN:")
    query = f"SELECT * FROM card WHERE number = {card_id} AND pin = {pin}"
    if cursor.execute(query).fetchone() is not None:
        print("\nYou have successfully logged in!\n")
        account_actions(card_id, conn, cursor)
    else:
        print("\nWrong card number or PIN!")


def account_actions(card_id, conn, cursor):
    while True:
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        action = int(input())
        if action == 1:
            query = f"SELECT balance FROM card WHERE number = {card_id}"
            print(f'Balance: {cursor.execute(query).fetchone()[0]}')
        elif action == 2:
            income = int(input('Enter income:'))
            query = f"UPDATE card SET balance = balance + {income} WHERE number = {card_id}"
            cursor.execute(query)
            conn.commit()
            print('Income was added!\n')
        elif action == 3:
            print("\nTransfer")
            transfer_card = input('Enter card number:')
            card_exists = cursor.execute(f"SELECT * FROM card WHERE number = {transfer_card}").fetchall()
            if not check_card_id(transfer_card):
                print('Probably you made mistake in the card number. Please try again!\n')
            elif len(card_exists) == 0:
                print("Such a card does not exist.\n")
            elif transfer_card == card_id:
                print("You can't transfer money to the same account!\n")
            else:
                transfer_amount = int(input('Enter how much money you want to transfer:'))
                query = f"SELECT * FROM card WHERE number = {card_id} AND balance >= {transfer_amount}"
                if len(cursor.execute(query).fetchall()) == 0:
                    print("Not enough money!\n")
                else:
                    query = f"UPDATE card SET balance = balance + {transfer_amount} WHERE number = {transfer_card}"
                    cursor.execute(query)
                    query = f"UPDATE card SET balance = balance - {transfer_amount} WHERE number = {card_id}"
                    cursor.execute(query)
                    conn.commit()
                    print('Success!\n')
        elif action == 4:
            query = f"DELETE FROM card WHERE number = {card_id}"
            cursor.execute(query)
            conn.commit()
            print('The account has been closed!\n')
        elif action == 5:
            break
        elif action == 0:
            print("\nBye!")
            sys.exit()


def check_card_id(card_id):
    card_id_sum = 0
    checksum = int(card_id[-1])
    card_id_check = "".join([str(int(x) * 2) if idx % 2 == 0 else x for idx, x in enumerate(card_id[:-1])])
    card_id_check = "".join([str(int(x) - 9) if int(x) > 9 else x for x in card_id_check])
    for i in card_id_check:
        card_id_sum += int(i)
    if (card_id_sum + checksum) % 10 == 0:
        return True
    else:
        return False


def generate_card_id():
    card_id = "400000" + "".join([str(random.randint(0, 9)) for x in range(9)])
    card_id_check = "".join([str(int(x) * 2) if idx % 2 == 0 else x for idx, x in enumerate(card_id)])
    card_id_check = "".join([str(int(x) - 9) if int(x) > 9 else x for x in card_id_check])
    card_id_sum = 0
    for i in card_id_check:
        card_id_sum += int(i)
    checksum = 0
    while (card_id_sum + checksum) % 10 != 0:
        checksum += 1
    return card_id + str(checksum)


def create_account(conn, cursor):
    card_id = generate_card_id()
    pin = "".join([str(random.randint(0, 9)) for x in range(4)])
    print("\nYour card has been created\nYour card number:")
    print(card_id)
    print("Your card PIN:")
    print(pin)
    print()
    query = f"INSERT INTO card (number, pin) VALUES ({card_id}, {pin})"
    cursor.execute(query)
    conn.commit()


conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS card")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS card (
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0);""")
conn.commit()

while True:
    user_input = read_input()
    if user_input == 0:
        print()
        print("Bye!")
        break
    elif user_input == 1:
        create_account(conn, cur)
    elif user_input == 2:
        login(conn, cur)
