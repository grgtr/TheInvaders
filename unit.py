import pygame as pg
import os

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 180)
red = (255, 0, 0)


# Класс игровых юнитов
class Unit:
    def __init__(self, hp: int, mana: int, dmg: int, moves: int, regen: int, x: int, y: int):
        self.max_hp = hp  # Максимальное количество здоровья
        self.hp = hp  # Здоровье
        self.regen = regen
        self.lvl = 0  # Уровень
        self.exp = 0  # Опыт
        self.max_mana = mana  # Максимальное количество маны
        self.mana = 0  # Количество маны
        self.dmg = dmg  # Урон
        self.max_moves = moves  # Максимальное количество очков перемещения
        self.moves = moves  # Количество очков перемещения
        self.x = x
        self.y = y
        # TODO
        # Сделать подгрузку и отображение

    # Отрисовка юнита
    def draw(self, screen):
        pg.draw.circle(screen, blue, (30, 35), 15, 0)

    # Обновление перед ходом
    def refresh(self):
        self.hp += self.regen  # Регенерация
        self.mana = self.max_mana  # Восстановление маны
        self.moves = self.max_moves  # Восстановление очков перемещения

    # Атака
    def attack(self, enemy):
        enemy: Unit
        enemy.hp -= self.dmg  # Нанесение урона
        self.moves = 0  # Обнуление очков перемещения
        if not enemy.is_alive():  # Если противник побежден
            self.exp += 50 // self.lvl ** 0.5  # получение опыта
            self.check()  # Проверка на новый уровень
        else:  # Если противник не побежден
            self.hp -= enemy.dmg // 2  # Нанесение ответного урона
            if not self.is_alive():  # Если юнит погиб
                enemy.exp += 50 // enemy.lvl ** 0.5  # Получение противником опыта
                enemy.check()  # Проверка на новый уровень

    # Проверка на вшивость
    def check(self):
        # Получен ли уровень
        if self.exp >= 100:
            self.lvl += 1
            self.exp = 0

    # Жив ли юнит
    def is_alive(self):
        return self.hp > 0

    def movement(self):
        return self.moves > 0