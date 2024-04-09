from random import randint

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

# Цвет контура яблока
APPLE_CONTUR_COLOR = (255, 255, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет камня = серый
GREY = (128, 128, 128)

# Скорость движения змейки:
# SPEED = 7

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс игровых объектов."""

    def __init__(self,
                 body_color=None,
                 position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод, отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """Игровой объект - яблока."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Рандомное местоположение яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка яблока"""
        x, y = self.position
        radius = GRID_SIZE // 2
        xy = (x + radius, y + radius)
        pygame.draw.circle(screen, self.body_color, xy, radius, radius)
        pygame.draw.circle(screen, APPLE_CONTUR_COLOR, xy, radius, 1)


class Snake(GameObject):
    """Дочерний класс игрового объекта - змейка."""

    def __init__(self, speed=4):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.body_color = SNAKE_COLOR
        self.next_direction = None
        self.last = None
        self.speed = speed

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""

        def go_right_through(number: int, screen_wh: int) -> int:
            """Змейка проходит стены насквозь."""
            if number < 0:
                number += screen_wh
            if number >= screen_wh:
                number %= screen_wh
            return number

        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        x = go_right_through(head_x + (direction_x * GRID_SIZE), SCREEN_WIDTH)
        y = go_right_through(head_y + (direction_y * GRID_SIZE), SCREEN_HEIGHT)
        self.positions.insert(0, (x, y))
        self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions[:-1]:
            draw(position=position, color=self.body_color)

        # Отрисовка головы змейки
        draw(position=self.get_head_position(), color=self.body_color)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Начальное состояние змейки, после столкновения с собой."""
        self.__init__()


class Stone(GameObject):
    """Игровой объект - камень, уменьшает длину змейки на 1."""

    def __init__(self):
        super().__init__(body_color=GREY)
        self.randomize_position()

    def randomize_position(self):
        """Рандомное местоположение яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка камня."""
        draw(position=self.position, color=self.body_color)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, чтобы изменить направление движения змеи"""
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
            # elif event.key == pygame.K_ESCAPE:
            #     pygame.quit()


def erase_the_unnecessary(coordinates: list) -> None:
    """Затираем не нужное"""
    for coordinate in coordinates:
        last_rect = pygame.Rect(coordinate, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def draw(position, color):
    """Отрисовка."""
    rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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
        snake.move()
        snake.draw()
        apple.draw()
        stone.draw()

        # Проверяем есть ли яблоко
        if apple.position in snake.positions:
            apple.__init__()
            snake.positions.append(snake.last)
            snake.draw()
            snake.length += 1
        else:
            # Затирание последнего сегмента
            if snake.last:
                erase_the_unnecessary([snake.last])
        if snake.get_head_position() in snake.positions[1:]:
            erase_the_unnecessary(snake.positions + [snake.last])
            snake.reset()
        if stone.position in snake.positions:
            if snake.length == 1:
                pygame.quit()
            erase_the_unnecessary([snake.positions.pop()])
            snake.draw()
            stone.__init__()
            # stone.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
