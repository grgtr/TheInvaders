import unit
import pygame as pg


class Player:
    def __init__(self, money: int, units: [unit.Unit]):
        self.money = money
        self.units = units
        self.power = 0

    def add_unit(self, appended_unit):
        self.units.append(appended_unit)
        # power++

