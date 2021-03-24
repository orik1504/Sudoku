import random


class SudokuTable:

    def __init__(self,
                 block_size: int,
                 row_seperator: str = '-',
                 col_seperator: str = '| '
                 ):

        self._block_size = block_size
        self._size = block_size ** 2

        self._table = self.__build_table()

        self._row_seperator = row_seperator
        self._col_seperator = col_seperator

    def __build_table(self,):

        table = list()
        for _ in range(self._size):
            table.append([None] * self._size)

        return table

    def reset(self,):
        self._table = self.__build_table()

    def __str__(self,) -> str:

        string = str()

        for row_index, row in enumerate(self._table):
            if row_index % self._block_size == 0:
                string += self.__empty_line()
                string += '\n'

            string += self.__generate_row(row)
            string += '\n'

        return string

    def __generate_row(self, row):

        string = str()

        for char_index, char in enumerate(row):
            if char_index % self._block_size == 0:
                string += self._col_seperator

            if char is None:
                padding_amount = len(str(self._size))
                string += " " * (padding_amount + 1)

            else:
                padding_amount = 1 + len(str(self._size)) - len(str(char))
                string += str(char) + (" " * padding_amount)

        return string

    def __empty_line(self,):
        length = 0

        length += len(self._col_seperator) * self._block_size
        length += self._size * (len(str(self._size)) + 1)

        return self._row_seperator * length

    def set(self, row: int, col: int, value: int):
        """ Recives a Sudoku cell, and sets its value. """

        if not isinstance(value, int):
            raise TypeError("Value must be an integer")

        if value < 1 or value > self._size:
            raise ValueError(
                f"Value must be between 1 and {self._size} (not {value})")

        self._table[row - 1][col - 1] = value

    def get(self, row: int, col: int):
        """ Returns the value of the given Sudoku cell. """
        return self._table[row][col]

    def fill_randomly(self,):
        """ Fills the board completly and randomly. It doesn't guarantee that
        the board is a valid result. """

        for row in range(1, self._size + 1):
            for col in range(1, self._size + 1):
                self.set(row, col, random.randint(1, self._size))

    @staticmethod
    def __check_unique_list(to_check: list) -> bool:
        """ Checks if all values in the list are different and unique. """
        return len(set(to_check)) == len(to_check)

    def check_row(self, row: int) -> bool:
        self.__check_unique_list(self._table[row-1])

    def check_col(self, col: int) -> bool:
        self.__check_unique_list([
            row[col]
            for row in self._table
        ])

    def check_block(self, block_row: int, block_col: int) -> bool:

        start_row = ((block_row - 1) * self._block_size) + 1
        start_col = ((block_col - 1) * self._block_size) + 1

        finish_row = start_row + self._block_size
        finish_col = start_col + self._block_size

        values = list()

        for row in range(start_row, finish_row):
            for col in range(start_col, finish_col):
                values.append(self._table[row-1][col-1])

        return self.__check_unique_list(values)

    def check_rows(self,) -> bool:
        for row in range(1, self._size + 1):
            if not self.check_row(row):
                return False

        return True

    def check_cols(self,) -> bool:
        for col in range(1, self._size + 1):
            if not self.check_col(col):
                return False

        return True

    def check_blocks(self,) -> bool:
        for row in range(self._block_size):
            for col in range(self._block_size):
                if not self.check_block(row, col):
                    return False

        return True

    def check(self,) -> bool:
        return self.check_rows() and self.check_cols() and self.check_blocks()

    def check_cell(self, row: int, col: int) -> bool:
        """ Makes only three check operations, to check if the given cell
        is valid or not. """

        block_row = ((row - 1) // self._block_size) + 1
        block_col = ((col - 1) // self._block_size) + 1

        return (
            self.check_row(row) and
            self.check_col(col) and
            self.check_block(block_row, block_col)
        )


if __name__ == "__main__":
    table = SudokuTable(3)
    table.fill_randomly()
    print(table)


"""

row = 4
(4, 4)
(4, 5)
(4, 6)
row = 5
(5, 4)
(5, 5)



given: block_x, block_y

x = ((block_x - 1) * block_size) + 1
y = ((block_y - 1) * block_size) + 1

x + block_size - 1
y + block_size - 1

              x    ?
    ------------------------
    | 5 5 6 | 7 2 5 | 1 9 2
    | 8 5 7 | 2 4 1 | 1 3 4
    | 9 6 9 | 3 6 9 | 6 9 5
    ------------------------
y   | 9 1 5 | 2 6 6 | 3 2 2
    | 1 6 2 | 6 5 5 | 2 4 9
?   | 5 5 6 | 3 9 5 | 7 8 8
    ------------------------
    | 3 3 8 | 4 9 2 | 6 3 7
    | 7 1 3 | 2 6 2 | 6 7 8
    | 2 4 7 | 8 4 8 | 2 4 1
"""
