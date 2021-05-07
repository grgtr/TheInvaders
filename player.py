import building
import unit
import pygame as pg


class Player:
    def __init__(self, money: int, units, buildings):
        self.money = money
        self.units = units
        self.buildings = buildings
        self.power = 0
        self.step_tavern = 0
        self.step_forge = 0
        self.chet_step = 0
        self.now_step = 0
        self.treasure_map = 0
        self.income = 0
        self.big_treasure = 0

    def add_unit(self, unit):
        self.units.append(unit)
        # power++

    def add_building(self, building):
        self.buildings.append(building)
        self.revenue()
        # power++

    def revenue(self):
        for i in range(len(self.buildings)):
            if self.buildings[i].index == 0:
                self.income += 5
            elif self.buildings[i].index == 5:
                self.income += 10
            elif self.buildings[i].index == 8:
                self.income += 10
            elif self.buildings[i].index == 9:
                self.income += 15
            elif self.buildings[i].index == 10:
                self.income += 15
            elif self.buildings[i].index == 12:
                self.income += 20

    def refresh(self):
        self.money += self.income
