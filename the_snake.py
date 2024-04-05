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

# Цвет фона - желтый:
APPLE_CONTUR_COLOR = (255, 255, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 7

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption(f'Змейкa Скорость: {SPEED} Длина змеи: {1}')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родителький класс для игровых объектов."""

    def __init__(self,
                 position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод."""
        pass


class Apple(GameObject):
    """Дочерний класс игрового объекта - Яблоко."""

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

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.body_color = SNAKE_COLOR
        self.next_direction = None
        self.last = None

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
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self) -> tuple:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Начальное состояние змейки, после столкновения с собой."""
        self.__init__()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, чтобы изменить направление движения змеи"""
    global SPEED  # знаю что не желательно, но первый раз хочу попробовать

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
            elif event.key == pygame.K_EQUALS and SPEED < 20:
                SPEED += 1
            elif event.key == pygame.K_MINUS and SPEED > 1:
                SPEED -= 1
            # elif event.key == pygame.K_ESCAPE:
            #     pygame.quit()


def erase_the_unnecessary(coordinates: list) -> None:
    """Затираем не нужное"""
    for coordinate in coordinates:
        last_rect = pygame.Rect(coordinate, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def main():
    """Главная функция."""
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    apple.draw()
    snake.draw()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверяем есть ли яблоко
        if apple.position in snake.positions:
            apple.__init__()
            apple.draw()
            snake.positions.append(snake.last)
        else:
            # Затирание последнего сегмента
            if snake.last:
                erase_the_unnecessary([snake.last])
        if snake.get_head_position() in snake.positions[1:]:
            erase_the_unnecessary(snake.positions + [snake.last])
            snake.reset()

        snake.draw()
        pygame.display.set_caption(f'Змейкa Скорость: {SPEED} '
                                   f'Длина змеи: {len(snake.positions)}')
        pygame.display.update()


if __name__ == '__main__':
    main()
