import random

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центральная позиция поля.
CENTER_BOARD = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Ячейки поля, все варианты.
CELLS = {(i, j) for i in range(0, SCREEN_WIDTH, GRID_SIZE)
         for j in range(0, SCREEN_HEIGHT, GRID_SIZE)}

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

# Цвет контура яблока
APPLE_CONTUR_COLOR = (255, 255, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет камня = серый
GREY = (128, 128, 128)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс игровых объектов."""

    def __init__(self,
                 body_color=None):
        self.body_color = body_color
        self.position = None
        self.reset()

    def draw(self, pos):
        """Отрисовка игрового объекта."""
        rect = (pygame.Rect(pos, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, pos=[CENTER_BOARD]) -> None:
        """Рандомное местоположение яблока."""
        pos = set(pos)
        self.position = random.choice(list(CELLS - pos))

    def reset(self, occupied_cells=None):
        """Перезагрузка игрового объекта."""
        if occupied_cells is None:
            occupied_cells = set()  # Пустой список по умолчанию
        self.randomize_position(occupied_cells)


class Apple(GameObject):
    """Игровой объект - яблока."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def draw(self, pos):
        """Отрисовка яблока."""
        x, y = pos
        radius = GRID_SIZE // 2
        xy = (x + radius, y + radius)
        pygame.draw.circle(screen, self.body_color, xy, radius, radius)
        pygame.draw.circle(screen, APPLE_CONTUR_COLOR, xy, radius, 1)


class Snake(GameObject):
    """Дочерний класс игрового объекта - змейка."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.last = None
        self.speed = None
        self.next_direction = None
        self.direction = None
        self.positions = None
        self.length = None
        self.reset()

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple, stone):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head_position = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        if apple.position != new_head_position:
            self.last = self.positions.pop()
        else:
            occupied_cells = set(self.positions + [stone.position])
            apple.reset(occupied_cells)
            self.length += 1
        if new_head_position in self.positions:
            screen.fill(BOARD_BACKGROUND_COLOR)
            self.reset()
            return
        self.positions.insert(0, new_head_position)

        last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        if stone.position == new_head_position:
            if self.length == 1:
                pygame.quit()
            occupied_cells = set(self.positions + [apple.position])
            stone.reset(occupied_cells)
            self.length -= 1
            self.last = self.positions.pop()
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self, speed=4):
        """Начальное состояние змейки, после столкновения с собой."""
        self.length = 1
        self.position = CENTER_BOARD
        self.positions = [self.position]
        self.direction = RIGHT
        self.body_color = SNAKE_COLOR
        self.next_direction = None
        self.last = None
        self.speed = speed


class Stone(GameObject):
    """Игровой объект - камень, уменьшает длину змейки на 1."""

    def __init__(self):
        super().__init__(body_color=GREY)
        self.reset()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, изменяет направление движения змеи."""
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
            elif event.key == pygame.K_EQUALS and game_object.speed < 20:
                game_object.speed += 1
            elif event.key == pygame.K_MINUS and game_object.speed > 1:
                game_object.speed -= 1


def main():
    """Главная функция."""
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    stone = Stone()

    while True:
        clock.tick(snake.speed)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple, stone)
        snake.draw(snake.get_head_position())
        apple.draw(apple.position)
        stone.draw(stone.position)
        pygame.display.update()


if __name__ == '__main__':
    main()
