from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

running = True


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс."""

    def __init__(self, color):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = color

    def draw(self):
        """Абстрактный метод."""
        pass


class Snake(GameObject):
    """Описывает змейку и её поведение."""
    length = 1

    def __init__(self, color):
        """Описывает змейку и действия с ним."""
        super().__init__(color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def move(self):
        """Обновление положения змейки в игре."""
        self.get_head_position()
        print('-----------', self.direction)
        #self.last = self.positions[-1]
        if self.direction == RIGHT:
            print(self.get_head_position())
            new = self.positions[0][0] + (self.direction[0 * 20])
            y1 = self.positions[0][1]
            list.insert(self.positions, 0, (new, y1))

    def get_head_position(self):
        """текущее положение головы змейки (первый элемент в списке"""
        # x1 = self.positions[0][0] - GRID_SIZE
        # y1 = self.positions[0][1]
        # list.insert(self.positions, 0, (x1, y1))
        return self.positions[0]

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовка на поле"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Описывает яблоко и действия с ним."""

    def __init__(self, color):
        super().__init__(color)
        self.position = self.randomize_position()

    @staticmethod
    def randomize_position():
        """Устанавливает случайное положение яблока на игровом поле."""
        rand1 = randint(0, GRID_WIDTH) * GRID_SIZE
        rand2 = randint(0, GRID_HEIGHT) * GRID_SIZE
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
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Тело игры"""
    # Тут нужно создать экземпляры классов.
    running = True
    aple = Apple(APPLE_COLOR)
    snake = Snake(SNAKE_COLOR)

    while running:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        pygame.display.update()  # обновление поля
        aple.draw()  # Отображает яблоко на поле
        snake.draw()  # Отображает змейку на поле
        handle_keys(snake)  # события клавиш
        snake.move()
        print(snake.positions)


if __name__ == '__main__':
    main()
    pygame.quit()


# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None