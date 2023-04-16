from board import *
from car import *
import helper
import sys


class Game:
    """
    Add class description here
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        error_msg = "Invalid move, try again"
        line = '* ' * 15 + '\n'

        print(line, self.__board, line)

        user_move = input("CAR, move: ")
        if user_move == '!':
            return False
        user_move = user_move.split(',')
        num_of_moves = len(user_move)

        if num_of_moves > 2:
            if num_of_moves == 3 and user_move[2] == '!':
                print(line, self.__board, line)
                return False
            print(error_msg)
            return True

        if user_move[0] not in ['R', 'G', 'W', 'O', 'B', 'Y'] or user_move[1] not in ['u', 'd', 'l', 'r']:
            print(error_msg)
            return True
        is_succeed = self.__board.move_car(user_move[0], user_move[1])
        if not is_succeed:
            print(error_msg)
            return True

        if self.__board.cell_content((3, 7)) == user_move[0]:
            print("You won!")
            print(board)
            return False
        return True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        game_round = self.__single_turn()
        while game_round:
            game_round = self.__single_turn()


if __name__ == "__main__":
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    car_config = sys.argv[1]
    car_dict = helper.load_json(car_config)
    board = Board()
    for car_name in car_dict:
        properties = car_dict[car_name]

        valid_name = car_name in ['R', 'G', 'W', 'O', 'B', 'Y']

        length = properties[0]
        valid_len = 2 <= length <= 4

        location = properties[1]
        valid_location = len(location) == 2

        orientation = properties[2]
        valid_orientation = orientation in [0, 1]
        location = (location[0], location[1])

        if not (valid_name and valid_len and valid_location and valid_orientation):
            continue
        car = Car(car_name, length, location, orientation)
        board.add_car(car)
    game = Game(board)
    game.play()
