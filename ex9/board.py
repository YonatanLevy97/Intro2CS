class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """
    __SIZE = 7

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.__board = [['_'] * self.__SIZE for _ in range(self.__SIZE)]
        self.__board[3].append('_')
        self.__cars = list()

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
        board = ""
        for i in range(len(self.__board)):
            for j in range(len(self.__board[i])):
                board += self.__board[i][j] + ' '
            board += '\n'
        return board

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        board = list()
        for i in range(self.__SIZE):
            for j in range(self.__SIZE):
                board.append((i, j))
        return board + [(3, 7)]

    def __possible_moves_helper(self, need_for_x):
        if need_for_x is None:
            return False
        return (need_for_x[0] in self.cell_list()) and (self.cell_content(need_for_x[0]) is None)

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]

        all_moves = list()
        for car in self.__cars:
            car_pos_moves = car.possible_moves()
            for move in car_pos_moves:
                for direction in ['u', 'd', 'l', 'r']:
                    move_req = car.movement_requirements(direction)
                    if direction == move and self.__possible_moves_helper(move_req):
                        to_moves_array = (car.get_name(), direction, car_pos_moves[direction])
                        all_moves.append(to_moves_array)
        return all_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return 3, 7

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        cell = self.__board[coordinate[0]][coordinate[1]]
        is_empty = cell == '_'
        if is_empty:
            return None
        return cell

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        name = car.get_name()
        cord = car.car_coordinates()
        first_cord = cord[0]
        last_cord = cord[-1]

        if name in [in_use_car.get_name() for in_use_car in self.__cars]:
            return False

        for in_use_car in self.__cars:
            in_use_car_cords = in_use_car.car_coordinates()
            for new_cord in cord:
                if in_use_car_cords.count(new_cord) > 0:
                    return False
        all_cell_list = self.cell_list()
        if not (first_cord in all_cell_list and last_cord in all_cell_list):
            return False

        self.__cars.append(car)

        for i in range(len(cord)):
            row = cord[i][0]
            col = cord[i][1]
            self.__board[row][col] = name

        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        for car in self.__cars:
            if name != car.get_name():
                continue

            for move in self.possible_moves():
                if move[0] != name or move[1] != movekey:
                    continue

                remove_cord = car.car_coordinates()

                if movekey in ['u', 'l']:
                    remove_cord = remove_cord[-1]

                elif movekey in ['d', 'r']:
                    remove_cord = remove_cord[0]

                can_move = car.move(movekey)
                if not can_move:
                    return False

                target_cords = car.car_coordinates()
                for cord in target_cords:
                    outside_board = cord not in self.cell_list()
                    cell = self.cell_content(cord)
                    cell_is_not_empty = (cell is not None) and (cell != car.get_name())
                    if outside_board or cell_is_not_empty:
                        return False

                for cord in target_cords:
                    self.__board[cord[0]][cord[1]] = car.get_name()

                self.__board[remove_cord[0]][remove_cord[1]] = '_'
                return True

        return False
