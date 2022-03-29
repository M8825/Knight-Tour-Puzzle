import sys
board = []
curr_pos = []
state = None
cell_size = 0
move_y = [2, 1, -1, -2, -2, -1, 1, 2]
move_x = [1, 2, 2, 1, -1, -2, -2, -1]
visited_pos = []


def clear_board():
    """Clear stats from previous position

    Deletes 'next move' counts for previous position
    """
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col][-1].isdigit():
                board[row][col] = cell_size * "_"


def update_visited():
    for pos in visited_pos:
        y, x = pos[0], pos[1]
        board[y][x] = "*".rjust(cell_size)


def validateMove(row, col):
    if len(board) > row >= 0 and len(board[0]) > col >= 0 and board[row][col] == cell_size * "_":
        return True


def solve(row, col, width, height, counter):
    for i in range(8):
        if counter >= width * height:
            return True

        new_y = row + move_y[i]
        new_x = col + move_x[i]
        if validateMove(new_y, new_x):
            board[new_y][new_x] = str(counter).rjust(cell_size)
            if solve(new_y, new_x, width, height, counter + 1):
                return True
            board[new_y][new_x] = cell_size * "_"
    return False


def possible_moves(p_row, p_col, c=2):
    """Recursive function

    Check for available moves from current position with check_next()
    function. After function reaches depth level(default 2) clear previous
    position statistics from board and updates new stats.
    """

    if c == 0:  # Base case
        update_visited()
        return

    for i in range(8):
        y, x = p_row + move_y[i], p_col + move_x[i]

        if validateMove(y, x):
            if [y, x] == curr_pos:
                continue
            if not board[p_row][p_col][-1].isdigit():
                board[p_row][p_col] = "1".rjust(cell_size)
            else:
                board[p_row][p_col] = str(int(board[p_row][p_col][-1]) + 1).rjust(cell_size)
            possible_moves(y, x, c - 1)  # Recursion

        if not board[p_row][p_col][-1].isdigit():  # If next position doesn't have additional moves
            board[p_row][p_col] = "0".rjust(cell_size)
            update_visited()


def border_formula(width):
    """Board border - Top; Bottom -

    Based on a formula
    """
    border = (width * (cell_size + 1) + 3) * "-"  # Border based on formula

    return border.rjust(cell_size + len(border) - 1)  # Add spaces as prefix


def print_board(height, width):
    border = border_formula(width)
    print(border)
    for i in range(height, 0, -1):
        i = str(i).rjust(cell_size - 1)  # Add spaces to row numbers when necessary
        print(f"{i}|", " ".join(board[int(i) - 1]), "|")
    print(border)
    # Column numbers
    footer = [str(i).rjust(cell_size) for i in range(1, width + 1)]
    print("  ", " ".join(footer))


def draw_board(row, col, width, height):
    global state

    visited_pos.append([row, col])
    possible_moves(row, col)  # Next available moves based on initial coordinates
    board[row][col] = "X".rjust(cell_size)  # X initial position

    print_board(height, width)

    # Game over in case there are no "next positions"
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col][-1].isdigit():
                state = False
                return
            else:
                state = True


def main():
    global board
    global curr_pos
    global cell_size

    while True:
        try:
            d_col, d_row = map(
                int, input("Enter your board dimensions: ").split()
            )
            assert 0 < d_row and 0 < d_col
            cell_size = len(str(d_row * d_col))
            board = [d_col * (cell_size * "_").split() for _ in range(0, d_row)]
        except (ValueError, AssertionError):
            print("Invalid dimensions!")
        else:
            while True:
                try:
                    col, row = map(
                        int, input("Enter the knight's starting position: ").split()
                    )
                    col, row = col - 1, row - 1  # Change values to match indexing
                    assert 0 <= row < d_row and 0 <= col < d_col
                    curr_pos = [row, col]
                except (ValueError, AssertionError):
                    print("Invalid position!")
                else:
                    try:
                        try_puzzle = input("Do you want to try the puzzle? (y/n):")

                        if try_puzzle == "n":
                            board[col][row] = "0".rjust(cell_size)
                            if solve(row, col, d_row, d_col, 1):
                                print("\nHere's the solution!")
                                print_board(d_row, d_col)
                            else:
                                print("No solution exists!")
                                break
                        elif try_puzzle == "y":
                            board[col][row] = "X"
                            if solve(row, col, d_col, d_row, 1):
                                clear_board()
                                draw_board(row, col, d_col, d_row)
                                while True:
                                    if d_row * d_col == len(visited_pos):  # Player visited every square
                                        print("What a great tour! Congratulations!")
                                        break
                                    elif state:  # Game over
                                        print("No more possible moves!")
                                        print(f"Your knight visited {len(visited_pos)} squares!")
                                        break
                                    try:
                                        col, row = map(
                                            int, input("Enter your next move: ").split()
                                        )
                                        col, row = col - 1, row - 1  # Change values to match indexing
                                        assert 0 <= row < d_row and 0 <= col < d_col
                                        curr_pos = [row, col]
                                        if board[row][col][-1] == "_" \
                                                or curr_pos in visited_pos:
                                            raise AssertionError
                                    except (ValueError, AssertionError):
                                        print("Invalid Move!", end=" ")
                                        continue
                                    else:
                                        clear_board()
                                        draw_board(row, col, d_col, d_row)
                            else:
                                print("No solution exists!")
                                break
                        else:
                            raise AssertionError
                    except AssertionError:
                        print("Invalid input!")
                        continue
                    break
            break


if __name__ == "__main__":
    main()