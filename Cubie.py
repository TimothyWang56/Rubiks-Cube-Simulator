import math


class Cubie:
    def __init__(self, x, y, z, side_length):
        self.position = [x, y, z]
        self.vertices = self.generate_vertices(x, y, z, side_length)
        self.surfaces = [
            [(4, 6, 7, 5), "black"],
            [(0, 1, 3, 2), "black"],
            [(2, 3, 7, 6), "black"],
            [(0, 4, 5, 1), "black"],
            [(1, 5, 7, 3), "black"],
            [(0, 4, 6, 2), "black"]
        ]

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
