"""Змейка."""
from random import choice
import pygame

pygame.init()  # Инициализация PyGame: # pylint: disable=no-member

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

ALL_CELLS = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)
)  # Ячейки поля

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона - черный:
BORDER_COLOR = (93, 216, 228)  # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)  # Цвет яблока
SNAKE_COLOR = (0, 255, 0)  # Цвет змейки
SPEED = 15  # Скорость движения змейки:

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс."""

    def __init__(self, color=BOARD_BACKGROUND_COLOR):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = color

    def draw(self):
        """Абстрактный метод."""

    def create_cell(self, position, color=BORDER_COLOR):
        """Отрисовка обектов"""
        if color != BORDER_COLOR:
            last_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, color, last_rect)
        else:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, color, rect, 1)


class Snake(GameObject):
    """Описывает змейку и её поведение."""

    def __init__(self, color=BOARD_BACKGROUND_COLOR):
        """Описывает змейку и действия с ним."""
        super().__init__(color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None
        # self.length = len(self.positions)
        self.reset()

    def move(self):
        """Обновление положения змейки в игре."""
        head_x, head_y = self.get_head_position()
        self.last = self.positions[-1]  # Последний елемент
        self.positions = [self.get_head_position()] + self.positions[:-1]
        # Вычисление границы поля
        head_x = (head_x + (self.direction[0] * GRID_SIZE)) % SCREEN_WIDTH
        head_y = (head_y + (self.direction[1] * GRID_SIZE)) % SCREEN_HEIGHT
        list.pop(self.positions, 0)
        list.insert(self.positions, 0, (head_x, head_y))  # Сохроняем всЁ

    def reset(self):
        """Сброс игры"""
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Текущее положение головы змейки (первый элемент в списке)"""
        return self.positions[0]

    def update_direction(self, next_direction):
        """Метод обновления направления после нажатия на кнопку"""
        self.direction = next_direction

    def draw(self):
        """Отрисовка на поле"""
        self.create_cell(self.get_head_position())  # Отрисовка головы змеи
        if self.last:  # Затирание последнего сегмента
            self.create_cell(self.last, BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Описывает яблоко и действия с ним."""

    def __init__(self, occupied_cell, color=BOARD_BACKGROUND_COLOR):
        super().__init__(color)
        self.occupied_cell = occupied_cell
        self.position = self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        random_cell = ALL_CELLS - set(self.occupied_cell)
        random_pos = choice(tuple(random_cell))
        return random_pos

    def draw(self):
        """Отрисовка на поле"""
        self.create_cell(self.position)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    key_map = {
        (RIGHT, pygame.K_UP): UP,  # pylint: disable=no-member
        (RIGHT, pygame.K_DOWN): DOWN,  # pylint: disable=no-member
        (LEFT, pygame.K_UP): UP,  # pylint: disable=no-member
        (LEFT, pygame.K_DOWN): DOWN,  # pylint: disable=no-member
        (UP, pygame.K_LEFT): LEFT,  # pylint: disable=no-member
        (UP, pygame.K_RIGHT): RIGHT,  # pylint: disable=no-member
        (DOWN, pygame.K_LEFT): LEFT,  # pylint: disable=no-member
        (DOWN, pygame.K_RIGHT): RIGHT,  # pylint: disable=no-member
    }
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            direction = key_map.get((game_object.direction, event.key))
            if direction is not None:
                game_object.update_direction(direction)
        elif event.type == pygame.QUIT:  # pylint: disable=no-member
            pygame.quit()  # pylint: disable=no-member
            raise SystemExit


def main():
    """Тело игры"""
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    aple = Apple(snake.positions, APPLE_COLOR)

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        aple.draw()  # Отображает яблоко на поле.
        snake.draw()  # Отображает змейку на поле.
        handle_keys(snake)  # события клавиш.
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()  # Сбрасывает игры
        elif snake.get_head_position() == aple.position:  # Съел яблоко.
            list.insert(snake.positions, 0, aple.position)
            aple.occupied_cell = snake.positions  # Занятые ячеки
            aple.position = aple.randomize_position()
        pygame.display.update()  # обновление поля.


if __name__ == '__main__':
    main()
