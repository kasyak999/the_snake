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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

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

    def __init__(self, color):
        """Описывает змейку и действия с ним."""
        super().__init__(color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.length = 1

    def move(self):
        """Обновление положения змейки в игре."""
        golova = self.get_head_position()

        if self.length > 1:
            for i in range(1, self.length):
                list.pop(self.positions, i)
                i_add = i - 1
                list.insert(self.positions, i, self.positions[i_add])
            
        if self.direction == RIGHT:
            golova[0] += self.direction[0] * 20
        elif self.direction == LEFT:
            golova[0] += self.direction[0] * 20
        elif self.direction == UP:
            golova[1] += self.direction[1] * 20
        elif self.direction == DOWN:
            golova[1] += self.direction[1] * 20  

        if golova[0] >= SCREEN_WIDTH:  # если змейка идет вправо
            self.direction = RIGHT
            golova = (0, golova[1])
        elif golova[0] < 0:  # Если змейка идет влево
            self.direction = LEFT
            golova = (SCREEN_WIDTH, golova[1])
        elif golova[1] >= SCREEN_HEIGHT:
            self.direction = DOWN
            golova = (golova[0], 0)
        elif golova[1] < 0:
            self.direction = UP
            golova = (golova[0], SCREEN_HEIGHT)

        list.insert(self.positions, 0, tuple(golova))  # Сохроняем всЁ

    def reset(self):
        """Сброс игры"""
        pass

    def get_head_position(self):
        """Текущее положение головы змейки (первый элемент в списке)"""
        self.last = self.positions[-1]
        pos = list.pop(self.positions, 0)
        return list(pos)

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
        pygame.display.update()  # обновление поля.
        aple.draw()  # Отображает яблоко на поле.
        snake.draw()  # Отображает змейку на поле.
        handle_keys(snake)  # события клавиш.
        snake.move()
        if snake.positions[0] == aple.position:  # Если съел яблоко.
            snake.length += 1
            list.insert(snake.positions, 0, aple.position)
            aple = Apple(APPLE_COLOR)
        snake.update_direction()
        print(snake.positions)


if __name__ == '__main__':
    main()
