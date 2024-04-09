"""Крестики нолики."""


# Объявить класс.
class Board:
    """Класс, который описывает игровое поле."""
    field_size = 3

    # Инициализировать игровое поле - список списков с пробелами.
    # Пробелы - это пустые клетки.
    def __init__(self):
        self.board = [[' ' for _ in range(self.field_size)] for _ in range(self.field_size)]

    # Метод, который обрабатывает ходы игроков.
    def make_move(self, row, col, player):
        """ Метод, который обрабатывает ходы игроков. """
        self.board[row][col] = player

    # Метод, который отрисовывает игровое поле.
    def display(self):
        """ Создание поля """
        for row in self.board:
            print(' | '.join(row))
            print('-' * 9)

    def is_board_full(self):
        """ Проверка есть ли пусты яейки """
        # Цикл проходится по всем столбцам игрового поля.
        for i in range(self.field_size):
            # А потом по всем строчкам.
            for j in range(self.field_size):
                # Если находит свободную ячейку...
                if self.board[i][j] == ' ':
                    # ...игра продолжается.
                    return False
        # Иначе - ничья!
        return True

    def check_win(self, player):
        """ Определяем победителя """
        # Тут реализована проверка по вертикали и горизонтали.
        for i in range(3):
            if (
                    all([self.board[i][j] == player for j in range(3)])
                    or
                    all([self.board[j][i] == player for j in range(3)])
            ):
                return True
        # Тут реализована проверка по диагонали.
        if (
            self.board[0][0] == self.board[1][1] == self.board[2][2] == player
            or
            self.board[0][2] == self.board[1][1] == self.board[2][0] == player
        ):
            return True
        return False

    def __str__(self):
        """Переопределяем метод __str__."""
        return (
            '{ Объект игрового поля размером '
            f'{self.field_size}x{self.field_size} '
            '}'
        )