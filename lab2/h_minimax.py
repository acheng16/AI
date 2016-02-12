__author__ = 'Andrew-Cheng'


# Class for our tic tac toe game
class Game:
    def __init__(self):
        """

        :type self: object
        """
        self.board = ['.' for i in range(9)]  # our game board
        self.last_moves = []  # list of moves we have made used for reverting
        self.winner = None  # player that wins the game

    # prints the board
    def print_board(self):
        for j in range(0, 9, 3):
            for i in range(3):
                print("%s " % self.board[j + i], end="")
            print('\n')

    # if the position has not been filled with 'O' or 'X' then append that position to the moves list
    def get_free_positions(self):
        moves = []
        for i, v in enumerate(self.board):
            if v == '.':
                moves.append(i);
        return moves

    # mark the spot with the given marker
    def mark_spot(self, marker, pos):
        self.board[pos] = marker
        self.last_moves.append(pos)

    # revert back the start of the board
    def revert(self):
        self.board[self.last_moves.pop()] = "."
        self.winner = None

    # runs the game to find the best minimax solution
    def run_game(self: object, p1, p2):
        """

        :type self: object
        """
        self.p1 = p1;
        self.p2 = p2;

        depth = 0

        # we are making a total of 9 moves or until we hit the goal_state
        for i in range(9):
            if self.goal_test() is False:
                if i % 2 == 0:
                    self.p1.move(self, depth)
                    depth += 1
                else:
                    self.p2.move(self, depth)
                    depth += 1
            self.print_board()

        # prints the winner or draw
        if self.goal_test():
            if self.winner == ".":
                print("The game ended with a draw.")
            else:
                print("Winning player is: %s" % self.winner)
            return

    # checks the current board against all winning combination and returns True if one matches else return False
    def goal_test(self):
        horizontal = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
        vertical = [(0, 3, 6), (1, 4, 7), (2, 5, 8)]
        diagonal = [(0, 4, 8), (2, 4, 6)]
        win_combinations = horizontal + vertical + diagonal
        for i, j, k in win_combinations:
            if self.board[i] == self.board[j] == self.board[k] and self.board[i] != ".":
                self.winner = self.board[i]
                return True

        if "." not in self.board:
            self.winner = "."
            return True
        return False


# Class for our plyears playing in the tic tac toe
class Player:
    # two options either you are playing as 'X' or 'O'
    def __init__(self, marker):
        self.marker = marker
        if self.marker == "X":
            self.opponent_marker = 'O'
        else:
            self.opponent_marker = 'X'

    # move the player makes, fills board with that marker
    def move(self, game, depth):
        cutoff_depth = depth+4
        move_position, score = self.maximized_move(game, depth, cutoff_depth)
        game.mark_spot(self.marker, move_position)

    # max part of min max
    def maximized_move(self, game, depth, cutoff_depth):
        best_score = None
        best_move = None
        count = 0

        # attempts for all open positions
        for m in game.get_free_positions():
            game.mark_spot(self.marker, m)

            # when at goal_state it can be evaluated
            if game.goal_test():
                score = self.utility(game)
            # if at cutoff depth use cutoff_utility
            elif depth > cutoff_depth:
                score = self.cutoff_utility(game)
            else:
                # if we aren't at goal_state there is another move to be made, so we find min move.
                move_position, score = self.minimized_move(game, depth+1, cutoff_depth)
                # printing out the first Minimax values for first move
                if len(game.get_free_positions()) == 8:
                    print("%d " % score, end="")
                    count += 1
                    if count % 3 == 0:
                        print("\n")
            game.revert()   # revert game to original state

            # store the best_score (highest) and its move
            if best_score is None or score > best_score:
                assert isinstance(score, object)
                best_score = score
                best_move = m

        return best_move, best_score

    # The min part of Minimax
    def minimized_move(self, game, depth, cutoff_depth):

        best_score = None
        best_move = None

        # attempts for all open positions
        for m in game.get_free_positions():
            game.mark_spot(self.opponent_marker, m)

            # when at goal_state it can be evaluated
            if game.goal_test():
                score = self.utility(game)
            # if at cutoff depth use cutoff_utility
            elif depth> cutoff_depth:
                score = self.cutoff_utility(game)
            else:
                # if we aren't at goal_state there is another move to be made, so we find max move.
                move_position, score = self.maximized_move(game, depth+1, cutoff_depth)

            game.revert() # revert the board

            # store the best_score (lowest) and its move
            if best_score is None or score < best_score:
                assert isinstance(score, object)
                best_score = score
                best_move = m

        return best_move, best_score

    # +10 for X win, -10 for O win, and 0 if tie
    def utility(self, game):
        if game.goal_test:
            if game.winner == self.marker:
                return 10
            elif game.winner == self.opponent_marker:
                return -10
            else:
                return 0

    # calculate utility at non terminal states
    def cutoff_utility(self, game):
        horizontal = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
        vertical = [(0, 3, 6), (1, 4, 7), (2, 5, 8)]
        diagonal = [(0, 4, 8), (2, 4, 6)]
        combinations = horizontal + vertical + diagonal
        utility = 0
        for i, j, k in combinations:
            # start 2x or o condition
            if game.board[i] == game.board[j] and game.board[i] != '.' and game.board[k] != self.opponent_marker:
                if game.board[i] == 'X':
                    utility += 3
                else:
                    utility -= 3

            if game.board[i] == game.board[k] and game.board[i] != '.' and game.board[j] != self.opponent_marker:
                if game.board[i] == 'X':
                    utility += 3
                else:
                    utility -= 3

            if game.board[j] == game.board[k] and game.board[j] != '.' and game.board[i] != self.opponent_marker:
                if game.board[j] == 'X':
                    utility += 3
                else:
                    utility -= 3
            # end 2 x or O condition

            # start 1 x or o condition
            if game.board[i] != '.' and game.board[j] == game.board[k] and game.board[j] == '.':
                if game.board[i] == 'X':
                    utility += 1
                else:
                    utility -= 1

            if game.board[k] != '.' and game.board[j] == game.board[i] and game.board[i] == '.':
                if game.board[k] == 'X':
                    utility += 1
                else:
                    utility -= 1

            if game.board[j] != '.' and game.board[i] == game.board[k] and game.board[i] == '.':
                if game.board[j] == 'X':
                    utility += 1
                else:
                    utility -= 1
            # end 1 x or o condition
        return utility

game = Game()
player1 = Player("X")
player2 = Player("O")
game.run_game(player1, player2)
