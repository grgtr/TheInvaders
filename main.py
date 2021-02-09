import pygame
import sys

size = width, height = 1000, 800


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    is_run = True

    while is_run:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_run = False

        # Логика работы

        # Отрисовка кадра
        screen.fill((255, 255, 255))  # Белый фон, рисуется первым!

        # Подтверждение отрисовки и ожидание
        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit()


if __name__ == '__main__':
    main()
