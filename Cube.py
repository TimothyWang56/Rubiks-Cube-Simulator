import math
from Cubie import Cubie
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (glBegin, GL_QUADS, glColor3fv, glVertex3fv,
                       GL_COLOR_BUFFER_BIT, glEnd, glClear,
                       GL_DEPTH_BUFFER_BIT, glTranslate, glRotate,
                       glEnable, GL_DEPTH_TEST)
from OpenGL.GLU import gluPerspective

side_length = 4
positions = [i for i in range(-1, 2)]
cubies = [Cubie(x, y, z, side_length) for x in positions for y in positions
          for z in positions]

for cubie in cubies:
    # the following if statements sets appropriate
    # surfaces to their respective colors
    if cubie.position[0] == 1:
        cubie.surfaces[0][1] = "blue"
    elif cubie.position[0] == -1:
        cubie.surfaces[1][1] = "green"

    if cubie.position[1] == 1:
        cubie.surfaces[2][1] = "white"
    elif cubie.position[1] == -1:
        cubie.surfaces[3][1] = "yellow"

    if cubie.position[2] == 1:
        cubie.surfaces[4][1] = "red"
    elif cubie.position[2] == -1:
        cubie.surfaces[5][1] = "orange"

edges = [
    (0, 1), (0, 2), (0, 4), (1, 3),
    (1, 5), (2, 3), (2, 6), (3, 7),
    (4, 5), (4, 6), (5, 7), (6, 7)
]

# dictionary used for colors
colors = {
    "white": (1, 1, 1),
    "yellow": (1, 1, 0),
    "blue": (0, 0, 1),
    "green": (0, 1, 0),
    "red": (1, 0, 0),
    "orange": (1, 0.5, 0),
    "black": (0, 0, 0),
}

turn_radians = {
    "CW": -math.pi/10,
    "CCW": math.pi/10
}


# function to draw the entire cube
def Cube():
    glBegin(GL_QUADS)
    for cubie in cubies:
        vertices = cubie.vertices
        for surface, color in cubie.surfaces:
            glColor3fv(colors[color])
            for vertex in surface:
                glVertex3fv(vertices[vertex])
    glEnd()
    # glBegin(GL_LINES)
    # glColor3fv(colors["white"])
    # for cubie in cubies:
    #     vertices = cubie.vertices
    #     for edge in edges:
    #         for vertex in edge:
    #             glVertex3fv(vertices[vertex])
    # glEnd()


# function to re-render the graphics
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Cube()
    pygame.display.flip()
    pygame.time.wait(10)


def rotate(side, direction):
    if side == "front" or side == "back":
        axis = "x"
        position_dim = 0
    elif side == "up" or side == "down":
        axis = "y"
        position_dim = 1
    elif side == "left" or side == "right":
        axis = "z"
        position_dim = 2
    if side == "back" or side == "up" or side == "right":
        layer = 1
    elif side == "front" or side == "down" or side == "left":
        layer = -1
    for _ in range(5):
        for cubie in cubies:
            if abs(cubie.position[position_dim] - layer) < 0.001:
                cubie.rotate(turn_radians[direction], axis)
        render()


# function that performs a full-cube rotation
def full_rotate(axis, direction):
    for _ in range(5):
        for cubie in cubies:
            cubie.rotate(turn_radians[direction], axis)
        render()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Rubik's Cube Simulator")
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslate(0, 0, -40)
    glRotate(45, 0, 1, 0)
    glRotate(30, 1, 0, 1)
    glEnable(GL_DEPTH_TEST)
    render()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if keys[pygame.K_f]:
                rotate("front", "CW")
            elif keys[pygame.K_b]:
                rotate("back", "CCW")
            elif keys[pygame.K_l]:
                rotate("left", "CW")
            elif keys[pygame.K_r]:
                rotate("right", "CCW")
            elif keys[pygame.K_u]:
                rotate("up", "CW")
            elif keys[pygame.K_d]:
                rotate("down", "CCW")
        else:
            if keys[pygame.K_f]:
                rotate("front", "CCW")
            elif keys[pygame.K_b]:
                rotate("back", "CW")
            elif keys[pygame.K_l]:
                rotate("left", "CCW")
            elif keys[pygame.K_r]:
                rotate("right", "CW")
            elif keys[pygame.K_u]:
                rotate("up", "CCW")
            elif keys[pygame.K_d]:
                rotate("down", "CW")
            elif keys[pygame.K_LEFT]:
                full_rotate("y", "CW")
            elif keys[pygame.K_RIGHT]:
                full_rotate("y", "CCW")
            elif keys[pygame.K_UP]:
                full_rotate("x", "CCW")
            elif keys[pygame.K_DOWN]:
                full_rotate("x", "CW")
            elif keys[pygame.K_x]:
                full_rotate("z", "CCW")
            elif keys[pygame.K_z]:
                full_rotate("z", "CW")


main()
