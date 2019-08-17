import pygame
from OpenGL.GL import (glBegin, GL_QUADS, glColor3fv, glVertex3fv,
                       GL_COLOR_BUFFER_BIT, glEnd, glClear,
                       GL_DEPTH_BUFFER_BIT)
from cube_properties import Color, Face, Radians
import math
import random


# class that represents a single cubie of a Rubik's Cube (there are 27 in
# total in a 3x3x3)
class Cubie:
    def __init__(self, x, y, z, side_length):
        self.position = [x, y, z]
        self.vertices = self.generate_vertices(x, y, z, side_length)
        self.surfaces = [
            [(4, 6, 7, 5), Color.black],
            [(0, 1, 3, 2), Color.black],
            [(2, 3, 7, 6), Color.black],
            [(0, 4, 5, 1), Color.black],
            [(1, 5, 7, 3), Color.black],
            [(0, 4, 6, 2), Color.black]
        ]

    # method that generates the vertices given a Cubie's position in 3D space
    # and the side length
    def generate_vertices(self, x, y, z, side_length):
        scaled_position = (side_length * x,
                           side_length * y,
                           side_length * z)
        offsets = [-side_length/2, side_length/2]
        vertices = []
        for i in offsets:
            for j in offsets:
                for k in offsets:
                    vertex = (scaled_position[0] + i,
                              scaled_position[1] + j,
                              scaled_position[2] + k)
                    vertices.append(vertex)
        return vertices

    # method that rotates the cubie by given radians along a specified axis
    def rotate(self, radians, axis):
        old_x = self.position[0]
        old_y = self.position[1]
        old_z = self.position[2]
        new_vertices = []
        if axis == "x":
            self.position = [
                self.position[0],
                old_y * math.cos(radians) - old_z * math.sin(radians),
                old_y * math.sin(radians) + old_z * math.cos(radians)
            ]
            for x, y, z in self.vertices:
                new_y = (y * math.cos(radians)) - (z * math.sin(radians))
                new_z = (y * math.sin(radians)) + (z * math.cos(radians))
                new_vertices.append((x, new_y, new_z))
            self.vertices = new_vertices
        elif axis == "y":
            self.position = [
                old_x * math.cos(radians) - old_z * math.sin(radians),
                self.position[1],
                old_x * math.sin(radians) + old_z * math.cos(radians)
            ]
            for x, y, z in self.vertices:
                new_x = (x * math.cos(radians)) - (z * math.sin(radians))
                new_z = (x * math.sin(radians)) + (z * math.cos(radians))
                new_vertices.append((new_x, y, new_z))
            self.vertices = new_vertices
        elif axis == "z":
            self.position = [
                old_x * math.cos(radians) - old_y * math.sin(radians),
                old_x * math.sin(radians) + old_y * math.cos(radians),
                self.position[2]
            ]
            for x, y, z in self.vertices:
                new_x = (x * math.cos(radians)) - (y * math.sin(radians))
                new_y = (x * math.sin(radians)) + (y * math.cos(radians))
                new_vertices.append((new_x, new_y, z))
            self.vertices = new_vertices


# class representing a whole Rubik's cube, consisting of 27 cubies
class Cube():
    def __init__(self):
        side_length = 4
        positions = [-1, 0, 1]
        self.cubies = [Cubie(x, y, z, side_length) for x in positions
                       for y in positions for z in positions]

        for cubie in self.cubies:
            # the following if statements sets appropriate
            # surfaces to their respective colors
            if cubie.position[0] == 1:
                cubie.surfaces[0][1] = Color.blue
            elif cubie.position[0] == -1:
                cubie.surfaces[1][1] = Color.green

            if cubie.position[1] == 1:
                cubie.surfaces[2][1] = Color.white
            elif cubie.position[1] == -1:
                cubie.surfaces[3][1] = Color.yellow

            if cubie.position[2] == 1:
                cubie.surfaces[4][1] = Color.red
            elif cubie.position[2] == -1:
                cubie.surfaces[5][1] = Color.orange

    # method to draw the entire cube
    def construct_cube(self):
        glBegin(GL_QUADS)
        for cubie in self.cubies:
            vertices = cubie.vertices
            for surface, color in cubie.surfaces:
                glColor3fv(color)
                for vertex in surface:
                    glVertex3fv(vertices[vertex])
        glEnd()

    # method to re-render the graphics
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.construct_cube()
        pygame.display.flip()
        pygame.time.wait(15)

    # method that performs a rotation on a single face
    def rotate(self, face, radians):
        for _ in range(5):
            for cubie in self.cubies:
                if abs(cubie.position[face.position_dim] - face.layer) < 0.001:
                    cubie.rotate(radians, face.axis)
            self.render()

    # method that performs a full-cube rotation
    def full_rotate(self, axis, radians):
        for _ in range(5):
            for cubie in self.cubies:
                cubie.rotate(radians, axis)
            self.render()

    # method that scrambles the cube randomly
    def scramble(self):
        faces = [Face.up, Face.down, Face.left, Face.right, Face.back,
                 Face.front]
        radians = [Radians.CCW, Radians.CW]
        previous_face = None
        for _ in range(25):
            possible_faces = [face for face in faces if face != previous_face]
            face_to_turn = random.choice(possible_faces)
            self.rotate(face_to_turn, random.choice(radians))
            previous_face = face_to_turn
