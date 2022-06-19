# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:50:07 2022

@author: richa
"""
import random
from typing import List
from typing import Tuple

import pygame
import matplotlib.pyplot as plt
from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile
import tools


# pylint: disable=no-member
'''
These functions (except main) are part of HexagonTile which is an open source code we used.
'''

def create_hexagon(position, radius=30, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(radius, position, colour=get_random_colour())


def get_random_colour(min_=150, max_=255) -> Tuple[int, ...]:
    """Returns a random RGB colour with each component between min_ and max_"""
    return tuple(random.choices(list(range(min_, max_)), k=3))


def init_hexagons(num_x=4, num_y=9, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    leftmost_hexagon = create_hexagon(position=(200, 30), flat_top=flat_top)
    hexagons = [leftmost_hexagon]
    row = -1

    for x in range(num_y):
        if x < 5:
            row += 1
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x < 5 else 4
            if x >= 5:
                row -= 1
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        for i in range(num_x + row):
            x, y = hexagon.position  # type: ignore
            if flat_top:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(hexagon)

    return hexagons


def render(screen, hexagons):
    """Renders hexagons on the screen"""
    screen.fill((0, 0, 0))
    for hexagon in hexagons:
        hexagon.render(screen)
    pygame.display.flip()

'''
Main function of the algorithm.
first the data is being extracted from the csv to two dim array which is called inputsArr.
later on, inputsArr is normalized with norm_zero_to_one and z_score functions.
then the SOM alg will be running for 10 iterations, each iteration's quantization error and alg state are being kept
for later comparison with other iterations.
Each iteration runs for 30 epochs which are being displayed in pygame screen.
After the 10th iteration the qunatization errors are being displaye with plot graph. 
'''
def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    #
    csvName = "Elec_24.csv"
    inputsArr = tools.getArrOfVectorByCSVName(csvName)
    tools.norm_zero_to_one(inputsArr)
    tools.Z_ScoreNormalization(inputsArr)
    solutions_and_scores = []
    for iter in range(10):
        hexagons = init_hexagons(flat_top=False)
        #inputsArr = tools.shuffleRows(inputsArr)
        tools.createAndAddRandomVectorToEachHexagon(hexagons,inputsArr)
        #
        epochs=30
        counter=0
        terminated = False
        while not terminated:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminated = True
            if (counter<epochs):
                tools.doEpoch(hexagons,inputsArr)
                counter+=1
                if counter == epochs:
                    score_quant = tools.calcQuantErrorScore(hexagons)
                    solutions_and_scores.append([hexagons, score_quant])
                    print("Quantization Error:",score_quant)
                    terminated = True

            for hexagon in hexagons:
                hexagon.update()

            render(screen, hexagons)
            clock.tick(50)
    max_sol = solutions_and_scores[0]
    for sol_and_score in solutions_and_scores:
        if sol_and_score[1] > max_sol[1]:
            max_sol = sol_and_score
    solutions_for_plot = [sol_and_score_i[1] for sol_and_score_i in solutions_and_scores ]
    plt.plot([i+1 for i in range(10)], solutions_for_plot, color='r')
    plt.show()
    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
        render(screen, max_sol[0])
    pygame.display.quit()


if __name__ == "__main__":
    main()
