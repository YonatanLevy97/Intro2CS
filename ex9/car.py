class Car:
    """
    Add class description here
    """
    __LEGAL_NAMES = ["R", "G", "W", "O", "B", "Y"]
    __VERTICAL = False
    __HORIZONTAL = False

    def __init__(self, name: str, length: int, location: tuple[int, int], orientation: int):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

        if orientation == 0:
            self.__VERTICAL = True

        elif orientation == 1:
            self.__HORIZONTAL = True

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        cord = list()
        row = self.__location[0]
        col = self.__location[1]

        for i in range(self.__length):

            if self.__VERTICAL:
                cord.append((row + i, col))

            else:
                cord.append((row, col + i))

        return cord

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.

        result = dict()
        if self.__VERTICAL:
            result["u"] = "cause the car to move up one cell"
            result["d"] = "cause the car to move down one cell"

        elif self.__HORIZONTAL:
            result["l"] = "cause the car to move left one cell"
            result["r"] = "cause the car to move right one cell"

        return result

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        ver_option = ['u', 'd']
        hor_option = ['l', 'r']
        if movekey not in (ver_option + hor_option) or \
                (movekey in ver_option and self.__HORIZONTAL) or \
                (movekey in hor_option and self.__VERTICAL):
            return
        cord = self.car_coordinates()

        if movekey in ['u', 'l']:
            cord = cord[0]
        else:
            cord = cord[-1]

        row = cord[0]
        col = cord[1]

        if movekey == 'u':
            return [(row - 1, col)]

        elif movekey == 'd':
            return [(row + 1, col)]

        elif movekey == 'l':
            return [(row, col - 1)]

        elif movekey == 'r':
            return [(row, col + 1)]

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey not in ['u', 'd', 'l', 'r']:
            return False
        row = self.__location[0]
        col = self.__location[1]

        if self.__VERTICAL:
            if movekey in ['u', 'd']:
                if movekey == 'u':
                    self.__location = (row - 1, col)
                    return True
                else:
                    self.__location = (row + 1, col)
                    return True
        elif self.__HORIZONTAL:
            if movekey in ['l', 'r']:
                if movekey == 'l':
                    self.__location = (row, col - 1)
                    return True
                else:
                    self.__location = (row, col + 1)
                    return True
        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name

    def get_orientation(self):
        """
        :return: The orientation of this car.
        """
        return self.__orientation