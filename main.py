from cube import Cube
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GLU import gluPerspective
from OpenGL.GL import (glTranslate, glRotate,
                       glEnable, GL_DEPTH_TEST)
from cube_properties import Face, Radians


def main():
    pygame.init()
    dimensions = (800, 600)
    display = pygame.display.set_mode(dimensions, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Rubik's Cube Simulator")
    gluPerspective(45, (dimensions[0]/dimensions[1]), 0.1, 50.0)
    glTranslate(0, 0, -40)
    glRotate(45, 0, 1, 0)
    glRotate(30, 1, 0, 1)
    glEnable(GL_DEPTH_TEST)
    cube = Cube()
    cube.render()
    scramble_button = pygame.Rect(300, 300, 50, 50)
    while True:
        pygame.draw.rect(display, (0, 0, 255), scramble_button)

        # pygame.display.flip()
        cube.render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # mouse_pos == event.pos
                if scramble_button.collidepoint(event.pos):
                    print("hi")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if keys[pygame.K_f]:
                cube.rotate(Face.front, Radians.CW)
            elif keys[pygame.K_b]:
                cube.rotate(Face.back, Radians.CCW)
            elif keys[pygame.K_l]:
                cube.rotate(Face.left, Radians.CW)
            elif keys[pygame.K_r]:
                cube.rotate(Face.right, Radians.CCW)
            elif keys[pygame.K_u]:
                cube.rotate(Face.up, Radians.CW)
            elif keys[pygame.K_d]:
                cube.rotate(Face.down, Radians.CCW)
        else:
            if keys[pygame.K_f]:
                cube.rotate(Face.front, Radians.CCW)
            elif keys[pygame.K_b]:
                cube.rotate(Face.back, Radians.CW)
            elif keys[pygame.K_l]:
                cube.rotate(Face.left, Radians.CCW)
            elif keys[pygame.K_r]:
                cube.rotate(Face.right, Radians.CW)
            elif keys[pygame.K_u]:
                cube.rotate(Face.up, Radians.CCW)
            elif keys[pygame.K_d]:
                cube.rotate(Face.down, Radians.CW)
            elif keys[pygame.K_LEFT]:
                cube.full_rotate("y", Radians.CW)
            elif keys[pygame.K_RIGHT]:
                cube.full_rotate("y", Radians.CCW)
            elif keys[pygame.K_UP]:
                cube.full_rotate("x", Radians.CCW)
            elif keys[pygame.K_DOWN]:
                cube.full_rotate("x", Radians.CW)
            elif keys[pygame.K_x]:
                cube.full_rotate("z", Radians.CCW)
            elif keys[pygame.K_z]:
                cube.full_rotate("z", Radians.CW)
            elif keys[pygame.K_s]:
                cube.scramble()


main()
