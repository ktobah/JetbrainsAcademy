import random
from collections import Counter


def determine_start(player, computer):
    max_player = max(player)
    max_computer = max(computer)

    if max_player > max_computer:
        return [max_player], "computer"
    else:
        return [max_computer], "player"


def has_double(pieces):
    for piece in pieces:
        if piece[0] == piece[1]:
            return True
    return False


def distribute_pieces():
    # full set
    domino_full = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
                   [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [2, 2],
                   [2, 3], [2, 4], [2, 5], [2, 6], [3, 3], [3, 4], [3, 5],
                   [3, 6], [4, 4], [4, 5], [4, 6], [5, 5], [5, 6], [6, 6]
                   ]
    # This shuffling might not be needed
    random.shuffle(domino_full)
    player_pieces = random.sample(domino_full, 7)
    for i in player_pieces:
        domino_full.remove(i)

    computer_pieces = random.sample(domino_full, 7)
    for i in computer_pieces:
        domino_full.remove(i)

    stock_pieces = domino_full

    return stock_pieces, player_pieces, computer_pieces


def display_stats(stock_pieces, player_pieces, computer_pieces, domino_snake):
    print('=' * 70)
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_pieces)}\n")
    if len(domino_snake) > 6:
        print('%s...%s\n' % (''.join(map(str, domino_snake[:3])), ''.join(map(str, domino_snake[-3:]))))
    else:
        print('%s\n' % ''.join(map(str, domino_snake)))

    print(f"Your pieces:")
    for idx, piece in enumerate(player_pieces):
        print(f"{idx + 1}:{piece}")
    print()


def apply_move(stock_pieces, player_pieces, computer_pieces, status, domino_snake, move, insert_direction, is_inverted):
    if move == 0 and stock_pieces:
        taken_piece = stock_pieces.pop(0)
        computer_pieces.append(taken_piece) if status == "player" else player_pieces.append(taken_piece)
    elif move != 0:
        if insert_direction == "left":
            domino_snake.insert(0, move)
        else:
            domino_snake.append(move)
        move = move[::-1] if is_inverted else move
        computer_pieces.remove(move) if status == "player" else player_pieces.remove(move)

    display_stats(stock_pieces, player_pieces, computer_pieces, domino_snake)


def is_game_over(player_pieces, computer_pieces, domino_snake):
    if not player_pieces and computer_pieces:
        return True, "player"
    elif player_pieces and not computer_pieces:
        return True, "computer"
    else:
        a = Counter(ele[0] for ele in domino_snake)
        b = Counter(ele[1] for ele in domino_snake)
        counts = a + b
        for k, v in counts.items():
            if v == 8 & domino_snake[0][0] == k & domino_snake[-1][-1] == k:
                return True, "draw"
    return False, False


def generate_ai_score(computer_pieces, domino_snake):
    final_count = {k: 0 for k in range(7)}

    snake_keys = Counter(ele[0] for ele in domino_snake)
    snake_values = Counter(ele[1] for ele in domino_snake)
    snake_counts = snake_keys + snake_values

    computer_keys = Counter(ele[0] for ele in computer_pieces)
    computer_values = Counter(ele[1] for ele in computer_pieces)
    computer_counts = computer_keys + computer_values

    final_count.update(snake_counts + computer_counts)

    final_scores = {str(k): final_count[k[0]] + final_count[k[1]] for k in computer_pieces}
    final_scores = dict(sorted(final_scores.items(), key=lambda item: item[1], reverse=True))

    return [eval(k) for k in final_scores]


def is_input_correct(move, player_pieces):
    try:
        move_int = int(move)
        if abs(move_int) > len(player_pieces):
            print("Invalid input. Please try again.")
            return False
    except ValueError:
        print("Invalid input. Please try again.")
        return False

    return True


def check_legal_move(move, domino_snake):
    snake_left_side = domino_snake[0][0]
    snake_right_side = domino_snake[-1][-1]
    if snake_left_side == move[-1]:
        return True, "left", move, False
    if snake_left_side == move[0]:
        return True, "left", move[::-1], True
    if snake_right_side == move[0]:
        return True, "right", move, False
    if snake_right_side == move[-1]:
        return True, "right", move[::-1], True

    return False, '', move, False


stock_pieces, player_pieces, computer_pieces = distribute_pieces()

while not has_double(player_pieces) and not has_double(computer_pieces):
    stock_pieces, player_pieces, computer_pieces = distribute_pieces()

domino_snake, status = determine_start(player_pieces, computer_pieces)

is_initial = True
game_over = False

while not game_over:

    if is_initial:
        player_pieces.remove(domino_snake[0]) if status == "computer" else computer_pieces.remove(domino_snake[0])
        display_stats(stock_pieces, player_pieces, computer_pieces, domino_snake)
        is_initial = False
    else:
        apply_move(stock_pieces, player_pieces, computer_pieces, status, domino_snake, move, insertion_side, is_inverted)

        # check if the game is over
        game_over, winner = is_game_over(player_pieces, computer_pieces, domino_snake)
        if game_over:
            if winner == "player":
                print('Status: The game is over. You won!')
            elif winner == "computer":
                print('Status: The game is over. The computer won!')
            else:
                print("Status: The game is over. It's a draw!")
            break

    if status == "computer":
        answer = input("Status: Computer is about to make a move. Press Enter to continue...")
        computer_pieces = generate_ai_score(computer_pieces, domino_snake)
        is_move_legal, insertion_side, move, is_inverted = check_legal_move(computer_pieces[0], domino_snake)
        move_idx = 1
        while not is_move_legal and move_idx < len(computer_pieces):
            is_move_legal, insertion_side, move, is_inverted = check_legal_move(computer_pieces[move_idx], domino_snake)
            move_idx += 1

        if not is_move_legal and stock_pieces:
            move = 0
            insertion_side = ''
            is_inverted = False
    else:
        move_idx = input("Status: It's your turn to make a move. Enter your command.")
        while True:
            if not is_input_correct(move_idx, player_pieces):
                move_idx = input("Status: It's your turn to make a move. Enter your command.")
                continue
            move_idx = abs(int(move_idx))
            if move_idx == 0:
                move = 0
                insertion_side = ''
                is_inverted = False
                break
            is_move_legal, insertion_side, move, is_inverted = check_legal_move(player_pieces[move_idx - 1], domino_snake)
            if not is_move_legal:
                move_idx = input("Illegal move. Please try again.")
                continue
            break

    status = "player" if status == "computer" else "computer"
