# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 14:07:18 2022

@author: richa
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List
from typing import Tuple

import pygame


@dataclass
class HexagonTile:
    """Hexagon class"""

    radius: float
    position: Tuple[float, float]
    colour: Tuple[int, ...]
    highlight_offset: int = 3
    max_highlight_ticks: int = 15

    colours_array = [(255, 153, 153), (255, 204, 153), (255, 255, 153), (204, 255, 153), (153, 255, 255), (153, 153, 255), (0, 0, 255), (153, 51, 255), (255, 51, 255), (96, 96, 96)]

    def __post_init__(self):
        self.vertices = self.compute_vertices()
        self.highlight_tick = 0
        self.alpha = 0.3
        self.beta = 0.2
        self.gama = 0.1
        self.isColourValid=0
        self.cluster = []

    def update(self):
        """Updates tile highlights"""
        if self.highlight_tick > 0:
            self.highlight_tick -= 1

    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - minimal_radius, y + half_radius),
            (x - minimal_radius, y + 3 * half_radius),
            (x, y + 2 * self.radius),
            (x + minimal_radius, y + 3 * half_radius),
            (x + minimal_radius, y + half_radius),
        ]

    def compute_neighbours(self, hexagons: List[HexagonTile]) -> List[HexagonTile]:
        """Returns hexagons whose centres are two minimal radiuses away from self.centre"""
        # could cache results for performance
        return [hexagon for hexagon in hexagons if self.is_neighbour(hexagon)]

    def compute_neighbours_second_row(self, hexagons: List[HexagonTile]) -> List[HexagonTile]:
        """Returns hexagons whose centres are two minimal radiuses away from self.centre"""
        # could cache results for performance
        return [hexagon for hexagon in hexagons if self.is_neighbour_second_row(hexagon)]

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < self.minimal_radius

    def is_neighbour(self, hexagon: HexagonTile) -> bool:
        """Returns True if hexagon centre is approximately
        2 minimal radiuses away from own centre
        """
        distance = math.dist(hexagon.centre, self.centre)
        return math.isclose(distance, 2 * self.minimal_radius, rel_tol=0.05)

    def is_neighbour_second_row(self, hexagon: HexagonTile) -> bool:
        """Returns True if hexagon centre is approximately
        2 minimal radiuses away from own centre
        """
        distance = math.dist(hexagon.centre, self.centre)
        return math.isclose(distance, 4 * self.minimal_radius, rel_tol=0.05)

    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, self.highlight_colour, self.vertices)

    def render_highlight(self, screen, border_colour) -> None:
        """Draws a border around the hexagon with the specified colour"""
        self.highlight_tick = self.max_highlight_ticks
        # pygame.draw.polygon(screen, self.highlight_colour, self.vertices)
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return (x, y + self.radius)

    @property
    def minimal_radius(self) -> float:
        """Horizontal length of the hexagon"""
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius * math.cos(math.radians(30))

    @property
    def highlight_colour(self) -> Tuple[int, ...]:
        """Colour of the hexagon tile when rendering highlight"""
        offset = self.highlight_offset * self.highlight_tick
        brighten = lambda x, y: x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.colour)

    def addRepresentedVector(self,v):
        self.representedVector =v

    def digit_2_colour(self, digit) -> Tuple[int, ...]:
        """Returns a random RGB colour with each component between min_ and max_"""
        return self.colours_array[digit - 1]

    def goTowardsVector(self, v, factor):
        for i, field in enumerate(v):
            self.representedVector[i] += factor * (v[i] - self.representedVector[i])

    def updateHexagonVector(self, v,hexagons):
        self.isColourValid=1
        neighbours_first_row = self.compute_neighbours(hexagons)
        neighbours_second_row = []
        for neighbour in neighbours_first_row:
            neighbours_of_neighbour = neighbour.compute_neighbours(hexagons)
            for n in neighbours_of_neighbour:
                if ((not self.is_neighbour(n)) and (n not in neighbours_second_row) and n !=self):
                    neighbours_second_row.append(n)
        self.goTowardsVector(v, self.alpha)
        for neighbour in neighbours_first_row:
            neighbour.goTowardsVector(v, self.beta)
        for neighbour in neighbours_second_row:
            neighbour.goTowardsVector(v, self.gama)

    def getClusterAvgEconomics(self):
        sum=0
        for v in self.cluster:
            sum+=v[0]
        return sum/len(self.cluster)
    def updateColour(self):
        if (self.isColourValid==1):
            self.colour=self.digit_2_colour(int(round(self.getClusterAvgEconomics())))
        else:
            self.colour=(255,255,255)


class FlatTopHexagonTile(HexagonTile):
    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + self.radius, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + self.radius, y),
        ]

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return (x, y + self.minimal_radius)
