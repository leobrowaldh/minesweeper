import random


# Creating a board object to represent the minesweeper board
# This is so that when we code up the game, we can just say "create a new board object"
# and dig on that board, etc.
class Board:
    def __init__(self, dim_size, num_bombs):
        # keep track of these parameters because we might find them helpful later on
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # get the board
        self.board = self.make_new_board()
        self.assign_values_to_board()

        # initialize a set to keep track of which locations we've uncovered
        # we will put (row,col) tuples into these sets
        self.dug = set()

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
        board = [[0 for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_to_plant = self.num_bombs
        while bombs_to_plant > 0:
            a = random.randrange(0, self.dim_size, 1)
            b = random.randrange(0, self.dim_size, 1)
            if board[a][b] != '*':
                board[a][b] = '*'
                bombs_to_plant -= 1
        return board

    def assign_values_to_board(self):
        # now that we have the bombs planted, let's assign a number 0-8 for all the empty spaces, which
        # represents how many neighboring bombs there are. we can precompute these, and it'll save us some
        # effort checking what's around the board later on :)
        for row_index, row in enumerate(self.board):
            for column_index, column in enumerate(self.board[row_index]):
                if column != '*':
                    self.board[row_index][column_index] = self.get_num_neighboring_bombs(row_index, column_index)

    def get_num_neighboring_bombs(self, row, col):
        # let's iterate through each of the neighboring positions and sum number of bombs
        neighbours = 0
        for ro in range(row - 1, row + 2):
            for co in range(col - 1, col + 2):
                if ro == row and co == col:  # we don't want to check current position for bombs.
                    continue
                # let's make sure we don't get out of the board, and that we have a neighbouring bomb:
                if 0 <= ro < self.dim_size and 0 <= co < self.dim_size:
                    if self.board[ro][co] == '*':
                        neighbours += 1
        return neighbours

    def dig(self, row, col):
        # dig at that location!
        # return True if successful dig, False if bomb dug

        # a couple of scenarios to consider:
        # hit a bomb -> game over
        # dig at a location with neighboring bombs -> finish dig.
        # dig at a location with no neighboring bombs -> recursively dig neighbors!

        # mark the position as dug:
        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False  # means game over.
        if self.board[row][col] > 0:
            return True  # means we reached a bomb-neighbouring location. this is our recursive base case.
        # If the position is a 0:
        for ro in range(row - 1, row + 2):
            for co in range(col - 1, col + 2):
                if 0 <= ro < self.dim_size and 0 <= co < self.dim_size:
                    if (ro, co) not in self.dug:
                        self.dig(ro, co)
        return True

    def print_player_board(self):
        # return a string that shows the board to the player
        visible_board = [[' ' for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if (r, c) in self.dug:
                    visible_board[r][c] = str(self.board[r][c])
        # printing column indexing:
        co_index = [str(i) for i in range(self.dim_size)]
        print('    ' + '   '.join(co_index) + '  ')
        # printing board with added list indexing:
        for i in range(self.dim_size):
            print(f'{i} | ' + ' | '.join(visible_board[i]) + ' |')


def play(dim_size=10, num_bombs=10):
    # Step 1: create the board and plant the bombs
    minesweeper = Board(dim_size, num_bombs)
    alive = True
    # Step 2: show the user the board and ask for where they want to dig
    total_squares = dim_size**2
    dug_locations = len(minesweeper.dug)
    while dug_locations < (total_squares - num_bombs):
        minesweeper.print_player_board()
        player_move = input('Where do you want to dig? please choose a position row,column')
        player_move = player_move.strip().split(',')
        p_row = int(player_move[0])
        p_col = int(player_move[1])
    # Step 3a: if the location is a bomb, then show game over message
    # Step 3b: if the location is not a bomb, dig recursively until one of the squares is next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig, then show victory
        if 0 <= p_row <= dim_size and 0 <= p_col <= dim_size:
            alive = minesweeper.dig(p_row, p_col)
            if not alive:
                break  # a mine, dead!

    if alive:
        print('VICTORY!!!! YOU MADE IT!!')
    else:
        # Reveal the board:
        minesweeper.dug = set()
        for i in range(dim_size):
            for j in range(dim_size):
                minesweeper.dug.add((i, j))
        minesweeper.print_player_board()
        print('You hit a mine and blew up, YOU ARE DEAD!')


if __name__ == '__main__':
    play()
