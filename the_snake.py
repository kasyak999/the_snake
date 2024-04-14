"""Змейка."""
from random import choice, randint
import pygame


pygame.init()  # Инициализация PyGame:

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона - черный:
BORDER_COLOR = (93, 216, 228)  # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)  # Цвет яблока
SNAKE_COLOR = (0, 255, 0)  # Цвет змейки
SPEED = 5  # Скорость движения змейки:

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс."""

    cells: list[int] = []

    def __init__(self, color=BOARD_BACKGROUND_COLOR):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = color

    def draw(self):
        """Абстрактный метод."""

    def create_cell(self, value):
        """Занятые ячейки"""
        GameObject.cells = value


class Snake(GameObject):
    """Описывает змейку и её поведение."""

    def __init__(self, color=BOARD_BACKGROUND_COLOR):
        """Описывает змейку и действия с ним."""
        super().__init__(color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None
        self.length = len(self.positions)

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
        for position in self.positions:  # [:-1]
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Описывает яблоко и действия с ним."""

    def __init__(self, color=BOARD_BACKGROUND_COLOR):
        super().__init__(color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:  # Проверяем ячейки.
            rand1 = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            rand2 = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (rand1, rand2) not in self.cells:
                break
            else:
                print('попала на змейку')
        return rand1, rand2

    def draw(self):
        """Отрисовка на поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Тело игры"""
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    aple = Apple(APPLE_COLOR)

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
            list.insert(snake.positions, snake.length, aple.position)
            snake.length += 1
            aple.create_cell(snake.positions)  # Занятые ячеки
            # print(aple.cells)
            aple = Apple(APPLE_COLOR)
        pygame.display.update()  # обновление поля.


if __name__ == '__main__':
    main()
