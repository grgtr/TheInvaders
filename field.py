import pygame as pg
import os
import random

def chet_hex(y):
    if y % 2 == 0:
        return True
    return False


# Класс игрового поля
class Field:
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
        self.field = [[('grass', random.randint(0,7)) for _ in range(field_size[0] - 1)] for _ in range(field_size[1])]  # Массив поля
        for i in range(field_size[1] // 2):  # В нечетных строчках на 1 гекс больше
            self.field[i * 2].append(('grass', 0))
        self.field_size = field_size  # Размер поля
        files = os.listdir('gameHexPallet')  # Имена картинок
        self.hex_size = (screen_size[0] // field_size[0], screen_size[1] // field_size[1])  # Размер гекса (120, 140)
        for key in self.hexes:  # Перебор по типам гексов
            count = sum((key in name) for name in files)  # Количество имен файлов, где встречается название типа гекса
            for i in range(count):  # Перебор по номерам
                self.hexes[key].append(
                    pg.image.load(f'gameHexPallet/{key}_{self.int_format(i)}.png'))  # Загрузка картинок
                self.hexes[key][-1] = pg.transform.scale(self.hexes[key][-1], self.hex_size)

    # Отрисовка поля
    def draw(self, screen):
        w, h = self.hex_size  # Координаты гекса
        line = 0  # Номер линии
        for i in range(len(self.field)):  # Перебор по типам гексов
            for j in range(len(self.field[i])):  # Перебор по номерам
                img = self.hexes[self.field[i][j][0]][self.field[i][j][1]]
                screen.blit(img, img.get_rect(bottomright=(w, h)))  # Отрисовка
                w += self.hex_size[0]  # Сдвиг координат на 1 гекс
            # Сдвиг координат на следующую строку
            if line % 2 == 1:
                w = self.hex_size[0]
            else:
                w = 3 * self.hex_size[0] // 2
            h += 3 * self.hex_size[1] // 4
            line += 1

    # Генерация поля
    def gen_given_field(self):
          # Погексовая генерация
        for j in range(0,self.field_size[0]):
            self.field[0][j] = 'grass', 5
        #for j in range(0,self.field_size[0]-1):
        #    self.field[1][j] = 'water', 0

        for j in range(0,self.field_size[0] - 1):
            self.field[self.field_size[1] - 1][j] = 'mars', 6

        if chet_hex(self.field_size[1] - 2):
            n = self.field_size[0]
        else:
            n = self.field_size[0] - 1

        for j in range(0, n):
            self.field[self.field_size[1] - 2][j] = 'mars', random.randint(0, 7)

        if chet_hex(self.field_size[1] - 3):
            n = self.field_size[0]
        else:
            n = self.field_size[0] - 1

        for j in range(0, n):
            self.field[self.field_size[1] - 3][j] = 'mars', random.randint(0, 5)

        for j in range(0,self.field_size[1]):
            self.field[j][0] = 'water', 0

        for j in range(0,self.field_size[1]-1):
            if j % 2 == 0:
                self.field[j][self.field_size[0]-1] = 'water', 0
            else:
                self.field[j][self.field_size[0]-2] = 'water', 0



    def generate(self):
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
                r = random.choice(list(self.hexes.keys()))
                if count[r] > 0:
                    self.field[i][j] = r, random.randint(0, len(self.hexes[r]) - 1)
                    count[r] -= 1

    @staticmethod
    def int_format(n: int, zn=2):
        res = str(n)[::-1]
        while len(res) < zn:
            res += '0'
        return res[::-1]
