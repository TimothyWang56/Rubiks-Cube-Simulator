import math
import collections


class Color():
    white = (1, 1, 1)
    yellow = (1, 1, 0)
    blue = (0, 0, 1)
    green = (0, 1, 0)
    red = (1, 0, 0)
    orange = (1, 0.5, 0)
    black = (0, 0, 0)


class Radians():
    CW = -math.pi/10
    CCW = math.pi/10


FaceInfo = collections.namedtuple("FaceInfo", "axis position_dim layer")


class Face():
    front = FaceInfo(axis="x", position_dim=0, layer=-1)
    back = FaceInfo(axis="x", position_dim=0, layer=1)
    up = FaceInfo(axis="y", position_dim=1, layer=1)
    down = FaceInfo(axis="y", position_dim=1, layer=-1)
    left = FaceInfo(axis="z", position_dim=2, layer=-1)
    right = FaceInfo(axis="z", position_dim=2, layer=1)
