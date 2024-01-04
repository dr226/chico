import random

matadora_placed = False


def initialize_board():
    board = [[None for _ in range(7)] for _ in range(7)]
    # Place the 'Impiedosa' at the center
    board[3][3] = Impiedosa(3, 3)
    return board


def print_board(board):
    print("  1 2 3 4 5 6 7")
    for i, row in enumerate(board):
        row_display = []
        for piece in row:
            if piece is None:
                row_display.append(' ')
            else:
                row_display.append(type(piece).__name__[0])  # First letter of class name
        print(f"{i + 1} {' '.join(row_display)}")


def is_valid_move(board, start_pos, end_pos):
    start_x, start_y = start_pos
    piece = board[start_x][start_y]
    if piece is None or not isinstance(piece, (Mosqueteiros, Matadora)):
        return False

    return piece.move(end_pos[0], end_pos[1], board)


def move_piece(board, start_pos, end_pos):
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    piece = board[start_x][start_y]
    if piece.move(end_x, end_y, board):
        board[end_x][end_y] = piece
        board[start_x][start_y] = None
    else:
        print("Move not allowed.")


def computer_turn(board, computer_pieces):
    """Execute a turn for the computer."""
    print("Computer's turn.")
    # Logic for the computer's turn


def describe_board(board):
    """
    Describes the current state of the board, including the positions of all pieces.
    """
    description = ""
    for row in range(7):
        for col in range(7):
            piece = board[row][col]
            if piece != ' ':  # If there is a piece on the current cell
                row_label = row + 1
                column_label = col + 1
                description += f"{piece} at Row {row_label}, Column {column_label}. "
    return description


def player_turn(board, turn_count, matadora_placed):
    while True:
        # Offer the option to place a Matadora if it's round 4 or later and Matadora hasn't been placed
        if turn_count >= 4 and not matadora_placed:
            action = input(
                "Enter 'm' to place a Matadora, 'r' for a description of the board, or 'move' to move a piece: ").lower()
            if action == 'm':
                place_matadora(board)
                matadora_placed = True  # Set the flag after the Matadora is placed
                return
            elif action == 'r':
                print(describe_board(board))
                continue

        # If the player chooses to move a piece or it's not yet time to place a Matadora
        command = input("Enter your move (e.g., '3 4 to 3 5'): ").lower()
        try:
            # command = "3 4 to 4 5"
            parts = command.split()
            start, to, end = ' '.join(parts[:2]), parts[2], ' '.join(parts[3:])

            if to != "to":
                raise ValueError("Invalid command format. Please use the format 'x y to a b' for moves.")

            start_x, start_y = map(int, start.split())
            end_x, end_y = map(int, end.split())

            start_pos = (start_x - 1, start_y - 1)
            end_pos = (end_x - 1, end_y - 1)

            if is_valid_move(board, start_pos, end_pos):
                move_piece(board, start_pos, end_pos)
                print_board(board)  # Show the board after the move
                break
            else:
                print("Invalid move. Please try again.")

        except ValueError as e:
            print(e)
            print("Please enter a valid move.")


class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Mosqueteiros(Piece):
    def __init__(self, x, y, allegiance):
        super().__init__(x, y)
        self.allegiance = allegiance  # 'player' or 'computer'

    def move(self, new_x, new_y, board):
        if 0 <= new_x < 7 and 0 <= new_y < 7:
            if abs(new_x - self.x) + abs(new_y - self.y) == 1 and board[new_x][new_y] is None:
                self.x, self.y = new_x, new_y
                return True
        return False


class Matadora(Piece):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self, new_x, new_y, board):
        if 0 <= new_x < 7 and 0 <= new_y < 7:
            if max(abs(new_x - self.x), abs(new_y - self.y)) == 1 and board[new_x][new_y] is None:
                self.x, self.y = new_x, new_y
                return True
        return False


class Impiedosa(Piece):
    def __init__(self, x, y):
        super().__init__(x, y)

    def place(self, new_x, new_y, board, turn_count):
        if turn_count >= 5 and 0 <= new_x < 7 and 0 <= new_y < 7 and board[new_x][new_y] is None:
            self.x, self.y = new_x, new_y
            return True
        return False

    def move(self, new_x, new_y, board):
        # The Impiedosa does not move but is placed on the board
        return False


def is_mosqueteiro_surrounded(board, x, y):
    """Check if a Musketeer at position (x, y) is surrounded on all four sides by opposing pieces."""
    if not isinstance(board[x][y], Mosqueteiros):
        return False  # Only Musketeers can be checked for this condition

    # Directions represent up, right, down, left
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # Check if the adjacent square is within the board and occupied by an opposing piece
        if 0 <= nx < len(board) and 0 <= ny < len(board[0]):
            if not isinstance(board[nx][ny], Matadora) and not isinstance(board[nx][ny], Impiedosa):
                return False  # One of the sides is not surrounded by an opposing piece
    return True


# Function to welcome and explain the rules of the game
def welcome_and_explain_rules():
    print("Welcome to the strategic game The Three Musketeers Plus (3Musketeers+).")
    # Here the rules of the game are explained (can be expanded)


# Function to choose the Musketeers
def choose_mosqueteiros():
    choice = input(
        "Which Musketeers do you want to play with? Enter b to play with the Black Musketeers or w for the White "
        "Musketeers: ")
    return choice.lower()


# Function to position the Musketeers on the board
def position_mosqueteiros(board):
    """
    Allows the player to position their musketeers on the board.
    The musketeers are assigned to the player by default.
    :param board: The game board.
    """
    num_mosqueteiros = 3  # Assuming three musketeers need to be placed
    placed = 0

    while placed < num_mosqueteiros:
        try:
            position = input(f"Position your musketeer {placed + 1} (e.g., '3 4'): ").split()
            if len(position) != 2:
                raise ValueError("Invalid input format. Please enter two numbers separated by a space.")

            x, y = int(position[0]) - 1, int(position[1]) - 1

            if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
                raise ValueError("Position out of board boundaries.")

            if board[x][y] is not None:
                raise ValueError("Position is already occupied.")

            # Place a Mosqueteiro at the specified position with 'player' allegiance
            board[x][y] = Mosqueteiros(x, y, 'player')
            placed += 1

        except ValueError as e:
            print(e)

    return board


def place_computer_pieces_randomly(board):
    """
    Randomly places the computer's Mosqueteiros on the board.
    The function assumes the computer needs to place 3 Mosqueteiros.
    :param board: The game board.
    """
    num_mosqueteiros = 3  # Set the number of Mosqueteiros for the computer
    placed = 0
    while placed < num_mosqueteiros:
        x, y = random.randint(0, 6), random.randint(0, 6)
        if board[x][y] is None:
            board[x][y] = Mosqueteiros(x, y, 'computer')
            placed += 1


def update_board_for_captures(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            piece = board[x][y]
            if isinstance(piece, Mosqueteiros) and is_mosqueteiro_surrounded(board, x, y):
                board[x][y] = None  # Remove captured Musketeer


def check_victory(board):
    """
    Check if the game has ended.
    Returns 'player' if the player wins, 'computer' if the computer wins, or None if the game is ongoing.
    """
    player_mosqueteiros_remaining = any(isinstance(piece, Mosqueteiros) and piece.allegiance == 'player'
                                        for row in board for piece in row)
    computer_mosqueteiros_remaining = any(isinstance(piece, Mosqueteiros) and piece.allegiance == 'computer'
                                          for row in board for piece in row)

    if not player_mosqueteiros_remaining:
        return 'computer'
    elif not computer_mosqueteiros_remaining:
        return 'player'
    else:
        return None


def place_matadora(board):
    """
    Allows a player to place a Matadora on the board.
    :param board: The game board.
    """
    while True:
        try:
            position = input("Place your Matadora (e.g., '3 4'): ").split()
            if len(position) != 2:
                raise ValueError("Invalid input format. Please enter two numbers separated by a space.")

            x, y = int(position[0]) - 1, int(position[1]) - 1

            if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
                raise ValueError("Position out of board boundaries.")

            if board[x][y] is not None:
                raise ValueError("Position is already occupied.")

            board[x][y] = Matadora(x, y)
            break
        except ValueError as e:
            print(e)


def main():
    """Execute the main game."""
    board = initialize_board()

    # Welcome the player and explain the rules
    welcome_and_explain_rules()

    # Let the player choose their musketeers
    choose_mosqueteiros()

    # Positioning the musketeers on the board
    position_mosqueteiros(board)  # Player positions their musketeers

    # Computer places its pieces
    place_computer_pieces_randomly(board)

    turn_count = 1  # Initialize the turn count

    # Main game loop
    while True:
        player_turn(board, turn_count, matadora_placed)
        # Update the board for captures after the player's turn
        update_board_for_captures(board)

        # Check if the game has ended after player's turn
        victory_status = check_victory(board)
        if victory_status:
            print(f"Game over. {victory_status.capitalize()} has won.")
            break


def computer_turn(board, computer_pieces):
    # Randomly select a piece from computer_pieces
    selected_piece = random.choice(computer_pieces)

    # Indicate all possible moves for this piece
    # For this step, you would have to implement the method "get_possible_moves" in your piece classes
    possible_moves = selected_piece.get_possible_moves(board)

    # If there are no possible moves, then return from the function
    if not possible_moves:
        return

    # Randomly select a move from possible_moves
    selected_move = random.choice(possible_moves)

    # Apply the selected move
    # This would involve implementing a method "apply_move"
    # in board class that takes a piece and a move, and applies the move for that piece.
    board.apply_move(selected_piece, selected_move)(board, computer_pieces)

    # Update the board for captures after the computer's turn
    update_board_for_captures(board)

    # Check if the game has ended after computer's turn
    victory_status = check_victory(board)
    if victory_status:
        print(f"Game over. {victory_status.capitalize()} has won.")
        exit()


# Execute the game if this file is the main script
if __name__ == "__main__":
    main()
