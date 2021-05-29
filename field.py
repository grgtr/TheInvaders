"""Модуль игрового поля"""
import random
import os
import pygame as pg


class Field:
    """Класс игрового поля"""
    # Конструктор
    def __init__(self, screen_size, field_size):
        self.hexes = {  # Массив с картинками гексов
            'dirt': [],  # Типы гексов
            'grass': [],
            'mars': [],
            'medieval': [],
            'sand': [],
            'stone': [],
            'water': [],
        }
        self.field = [[('grass', random.randint(0, 6)) for _ in range(field_size[0] - 1)] for _ in
                      range(field_size[1])]  # Массив поля
        for i in range(field_size[1] // 2):  # В нечетных строчках на 1 гекс больше
            self.field[i * 2].append(('grass', 0))
        self.field_size = field_size  # Размер поля
        files = os.listdir('gameHexPallet')  # Имена картинок
        self.hex_size = (screen_size[0] // field_size[0],  # Размер гекса (120, 140)
                         screen_size[1] // field_size[1])
        for key in self.hexes:  # Перебор по типам гексов
            # Количество имен файлов, где встречается название типа гекса
            count = sum((key in name) for name in files)
            for i in range(count):  # Перебор по номерам
                self.hexes[key].append(  # Загрузка картинок
                    pg.image.load(f'gameHexPallet/{key}_{self.int_format(i)}.png'))
                self.hexes[key][-1] = pg.transform.scale(self.hexes[key][-1], self.hex_size)

    def gen_building(self, x_range, y_range, title, index, val) -> None:
        """
        Создание постройки на заданном поле
        :param x_range: вертикальные границы
        :param y_range: горизонтальные границы
        :param title: подпись
        :param index:
        :param val:
        :return:
        """
        for _ in range(val):
            yes = False
            while not yes:
                i = random.randint(y_range[0], y_range[1])
                j = random.randint(x_range[0], x_range[1])
                name = self.field[j][i][0]
                if name != 'medieval':
                    yes = True
                    self.field[j][i] = title, index
                    if j % 2 == 0:
                        self.field[j][self.field_size[0] - 1 - i] = title, index
                    else:
                        self.field[j][self.field_size[0] - 2 - i] = title, index

    def draw(self, screen) -> None:
        """Отрисовка поля"""
        width, height = self.hex_size  # Координаты гекса
        line = 0  # Номер линии
        for i in range(len(self.field)):  # Перебор по типам гексов
            for j in range(len(self.field[i])):  # Перебор по номерам
                img = self.hexes[self.field[i][j][0]][self.field[i][j][1]]
                screen.blit(img, img.get_rect(bottomright=(width, height)))  # Отрисовка
                width += self.hex_size[0]  # Сдвиг координат на 1 гекс
            # Сдвиг координат на следующую строку
            if line % 2 == 1:
                width = self.hex_size[0]
            else:
                width = 3 * self.hex_size[0] // 2
            height += 3 * self.hex_size[1] // 4
            line += 1

    def gen_given_field(self) -> None:
        """Генерация поля"""
        # Погексовая генерация
        if self.chet_hex(self.field_size[1] - 1):
            x_size = self.field_size[0]
        else:
            x_size = self.field_size[0] - 1

        for j in range(0, x_size):
            self.field[self.field_size[1] - 1][j] = 'dirt', random.randint(0, 7)

        if self.chet_hex(self.field_size[1] - 2):
            x_size = self.field_size[0]
        else:
            x_size = self.field_size[0] - 1

        for j in range(0, x_size):
            self.field[self.field_size[1] - 2][j] = 'dirt', random.randint(0, 5)

        if self.chet_hex(self.field_size[1] - 3):
            x_size = self.field_size[0]
        else:
            x_size = self.field_size[0] - 1

        for j in range(0, x_size):
            self.field[self.field_size[1] - 3][j] = 'dirt', random.randint(0, 5)

        for j in range(0, self.field_size[1]):
            self.field[j][0] = 'water', 0

        for j in range(0, self.field_size[1]):
            if j % 2 == 0:
                self.field[j][self.field_size[0] - 1] = 'water', 0
            else:
                self.field[j][self.field_size[0] - 2] = 'water', 0

        # Создание уникального гекса(домика)
        # с границами по вертикали и горизонтали, названием гекса, его индексом и количеством
        self.gen_building((1, 5), (2, 6), 'medieval', 0, 1)
        self.gen_building((6, 10), (2, 6), 'medieval', 0, 1)
        self.gen_building((1, 5), (2, 6), 'medieval', 1, 1)
        self.gen_building((1, 5), (2, 6), 'medieval', 2, 1)
        self.gen_building((6, 10), (2, 6), 'medieval', 2, 1)
        self.gen_building((1, 10), (2, 11), 'medieval', 3, 1)
        self.gen_building((1, 10), (2, 11), 'medieval', 4, 1)
        self.gen_building((1, 5), (2, 6), 'medieval', 5, 1)
        self.gen_building((6, 10), (2, 6), 'medieval', 5, 1)
        self.gen_building((1, 10), (2, 11), 'medieval', 6, 1)
        self.gen_building((1, 5), (9, 13), 'medieval', 7, 1)
        self.gen_building((6, 10), (9, 13), 'medieval', 7, 1)
        self.gen_building((1, 10), (2, 11), 'medieval', 8, 1)
        self.gen_building((1, 5), (5, 9), 'medieval', 9, 1)
        self.gen_building((6, 10), (5, 9), 'medieval', 9, 1)
        self.gen_building((1, 5), (2, 6), 'medieval', 10, 1)
        self.gen_building((6, 10), (2, 6), 'medieval', 10, 1)
        self.gen_building((1, 10), (2, 13), 'medieval', 11, 2)
        self.gen_building((11, 13), (2, 12), 'medieval', 12, 1)
        self.gen_building((11, 13), (2, 12), 'medieval', 12, 1)
        self.gen_building((12, 13), (2, 12), 'medieval', 13, 1)
        self.gen_building((12, 13), (2, 12), 'medieval', 13, 1)
        self.gen_building((12, 13), (2, 12), 'medieval', 14, 1)
        self.gen_building((12, 13), (2, 12), 'medieval', 14, 1)

    def generate(self) -> None:
        """Генерация поля"""
        # Количество гексов каждого типа
        hexes_count = self.field_size[0] * self.field_size[1] - self.field_size[1] // 2
        count = {
            'mars': hexes_count // 20,  # Типы гексов
            'medieval': hexes_count // 20,
            'sand': hexes_count // 10,
            'stone': hexes_count // 10,
            'water': hexes_count // 3,
            'dirt': hexes_count // 8,
            'grass': hexes_count,
        }
        for i in count:  # Остальные - трава
            if i != 'grass':
                count['grass'] -= count[i]

        for i in range(len(self.field)):  # Погексовая генерация
            for j in range(len(self.field[i])):
                rand_choice = random.choice(list(self.hexes.keys()))
                if count[rand_choice] > 0:
                    self.field[i][j] = rand_choice,\
                                       random.randint(0, len(self.hexes[rand_choice]) - 1)
                    count[rand_choice] -= 1

    @staticmethod
    def int_format(number: int, decimals=2) -> str:
        """
        Приведение числа к нужному формату
        :param number: число
        :param decimals: количество знаков после запятой
        :return: отформатированная строка
        """
        res = str(number)[::-1]
        while len(res) < decimals:
            res += '0'
        return res[::-1]

    @staticmethod
    def chet_hex(number) -> bool:
        """
        Проверка числа на четность
        :param number: число
        :return: bool
        """
        if number % 2 == 0:
            return True
        return False
