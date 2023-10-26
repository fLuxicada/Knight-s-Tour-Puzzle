class Board:
    def __init__(self, x, y):
        """Create board of x columns and y rows, based on a cartesian coordinates system"""
        self.x, self.y = x, y
        self.curr_x = None
        self.curr_y = None
        self.move_count = 1
        self.available_moves = None
        # Initiates matrix for the board. Placeholder is used to multiply _ character, so it fits with board size
        if x * y < 100:
            self.board = [["__" for i in range(x)] for j in range(y)]
            self.placeholder = 2
        elif x * y >= 100:
            self.board = [["___" for i in range(x)] for j in range(y)]
            self.placeholder = 3
        # Char space is used to right align cell text
        self.char_space = " " * (self.placeholder - 1)

    def draw(self):
        """Displays the current state of the board"""
        border = "-" * (self.x * (self.placeholder + 1) + 3)
        print(self.char_space + border)
        # Prints the board matrix in reverse order so that the moves correspond to cartesian coordinates
        for i in range(self.y - 1, -1, -1):
            print(f"{i + 1}| {' '.join(self.board[i])} |")
        print(self.char_space + border)
        print("   " + " ".join([" " * (self.placeholder - 1) + str(col + 1) for col in range(self.x)]))

    def clear(self):
        """Completely clears the board of preview moves, leaving only current position and visited positions"""
        for i, row in enumerate(self.board):
            for j, pos in enumerate(row):
                if pos != self.char_space + "X" and pos != self.char_space + "*":
                    self.board[i][j] = "_" * self.placeholder

    def new_move(self, pos):
        """Marks and updates current position on the board"""
        self.board[pos.y][pos.x] = " " * (self.placeholder - 1) + "X"
        self.curr_x = pos.x
        self.curr_y = pos.y

    def mark_visited(self, pos):
        """Marks previously visited square"""
        self.board[pos.y][pos.x] = " " * (self.placeholder - 1) + "*"

    def generate_moves(self, x_pos, y_pos):
        """Takes in a position on the board, checks all possible moves to see if they are on board and if the position
         is empty and returns a list of valid moves coordinates"""
        col, row = self.x, self.y
        x, y = x_pos, y_pos
        moves = [[x + 1, y + 2], [x + 1, y - 2], [x - 1, y + 2], [x - 1, y - 2],
                 [x + 2, y + 1], [x + 2, y - 1], [x - 2, y + 1], [x - 2, y - 1]]
        valid_moves = []
        for move in moves:
            if 0 <= move[0] < col and 0 <= move[1] < row and self.board[move[1]][move[0]] == "_" * self.placeholder:
                valid_moves.append(move)
        return valid_moves

    def next_moves(self, valid_moves):
        """Calls the generate_moves function to look one step ahead. It tells you how many valid moves you will have
        if you move to a certain position. From a given position you pass the valid moves list - this function then
        looks at every valid move and counts how many future moves are valid from that position.
        """
        options = []
        for move in valid_moves:
            count = len(self.generate_moves(move[0], move[1]))
            options.append(count)
        opt = 0
        for move in valid_moves:
            self.board[move[1]][move[0]] = self.char_space + str(options[opt])
            opt += 1

    def check_move(self, str):
        """Checks user input to make sure it fits the 2 integers format; then checks to see if that move is valid
        by generating the list of valid moves"""
        self.clear() # The board is cleared to prevent future moves previews to interfere with empty positions
        try:
            move = list(map(int, str.split(" ")))
            move[0] -= 1
            move[1] -= 1
        except (ValueError, IndexError):
            return "Invalid input!"
        if move not in self.generate_moves(self.curr_x, self.curr_y):
            return False

        return move

    def ask_move(self):
        """Sequence for user input for one move. Updates visited positions, current position and returns current
        available moves to check for game over."""
        user_move = self.check_move(input("Enter your next move: "))
        if user_move:
            self.clear()
            self.mark_visited(knight)
            knight.move(user_move)
            self.new_move(knight)
            self.available_moves = len(self.generate_moves(self.curr_x, self.curr_y))
            self.next_moves(self.generate_moves(self.curr_x, self.curr_y))
            self.draw()
            self.move_count += 1
            return self.available_moves
        else:
            print("Invalid move!")

    # AUTO SOLVE SECTION
    def solve(self, x, y, counter):
        """Backtracking algorithm that generates valid moves from every valid moves and checks for the correct route"""
        if counter >= self.x * self.y + 1:
            return True

        for move in self.generate_moves(x, y):
            new_x = move[0]
            new_y = move[1]
            self.board[new_y][new_x] = self.char_space + str(counter) if counter < 10 else " " * (self.placeholder - 2) + str(counter)

            if self.solve(new_x, new_y, counter + 1):
                return True
            self.board[new_y][new_x] = "_" * self.placeholder

        return False


class Knight:
    def __init__(self, x, y):
        # -1 adjusts value to fit board index (position 1 actually corresponds to index 0)
        self.x = x - 1
        self.y = y - 1

    def move(self, move):
        self.x = move[0]
        self.y = move[1]


def check_start(str):
    """Checks starting position to make sure it is 2 integers and is within board dimensions"""
    try:
        x_i, y_i = list(map(int, str.split(" ")))
    except ValueError:
        return False
    if x_i not in range(1, board.x + 1) or y_i not in range(1, board.y + 1):
        return False
    return [x_i, y_i]


def check_board(str):
    """Validates board dimensions - must be 2 integers separated by space"""
    try:
        col, row = list(map(int, str.split(" ")))
    except ValueError:
        return False
    if col <= 0 or row <= 0:
        return False
    return [col, row]


def check_solution(x, y):
    """Checks if a solution exists for the given board from the given position. Returns solution for printing later"""
    board.board[y][x] = board.char_space + "1"
    board.solve(x, y, 2)
    for i in range(board.y):
        for j in range(board.x):
            if board.board[i][j] == "_" * board.placeholder:
                return False
    solution = board.board
    return solution


def draw_solution(solution):
    """Replicates draw method to display saved solution without having to solve it again"""
    border = "-" * (board.x * (board.placeholder + 1) + 3)
    print(board.char_space + border)
    # Prints the board matrix in reverse order so that the moves correspond to cartesian coordinates
    for i in range(board.y - 1, -1, -1):
        print(f"{i + 1}| {' '.join(solution[i])} |")
    print(board.char_space + border)
    print("   " + " ".join([" " * (board.placeholder - 1) + str(col + 1) for col in range(board.x)]))

# ------------------PROGRAM------------------------

while True:
    dimensions = check_board(input("Enter your board dimensions: "))
    if dimensions:
        board = Board(dimensions[0], dimensions[1])
        break
    else:
        print("Invalid dimensions!")

while True:
    ans = check_start(input("Enter the knight's starting position: "))
    if ans:
        knight = Knight(ans[0], ans[1])
        break
    else:
        print("Invalid dimensions!")

while True:
    choice = input("Do you want to try the puzzle? (y/n): ")
    if choice in ["y", "n"]:
        print("Checking for possible solutions. Please wait...")
        solution = check_solution(knight.x, knight.y)
        if choice == "y":
            if solution:
                board.clear()
                board.new_move(knight)
                board.next_moves(board.generate_moves(board.curr_x, board.curr_y))
                board.draw()
                while True:
                    board.ask_move()
                    if board.move_count == (board.x * board.y):
                        print("What a great tour! Congratulations!")
                        break
                    elif board.available_moves == 0:
                        print(f"No more possible moves!\nYour knight visited {board.move_count} squares!")
                        break
            else:
                print("No solution exists!")
        elif choice == "n":
            if solution:
                print("Here's the solution!")
                draw_solution(solution)
            else:
                print("No solution exists!")
        break
    else:
        print("Invalid input!")