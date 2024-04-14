import colorsys
import logging
import math
import numpy as np
import pygame as pg
import moderngl as mgl
import glm
from math import floor, ceil

from generation import basic_map, map_from_pooled_noise

# range and value
colors = (
    (-8, (0.6, 0.6, 0.7)),  # deep water
    (0, (0.5, 0.8, 0.8)),  # shallow water
    (2, (0.15, 0.6, 0.8)),  # sand
    (5, (0.27, 0.6, 0.8)),  # grass
    (10, (0.22, 0.5, 0.45)),  # forest
    (25, (0.5, 0.1, 0.3)),  # mountain
    (float("inf"), (0.5, 0.05, 0.9)),  # snow
)


class Map:
    def __init__(self, width, height, block_size=20, pixel_size=20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.full_width = width * block_size
        self.full_height = height * block_size
        self.map = np.zeros((width, height))
        self.pre_colors = []
        self.pixel_size = pixel_size
        assert self.block_size % self.pixel_size == 0

        self.logger = logging.getLogger(__name__)

        self.generate()
        self.generate_sun_path()
        self.max_height = self.map.max()
        self.sun = [0, 0, 0]

    def generate(self):
        map_from_pooled_noise(self.map)
        # print(self.map)
        for x in range(self.width):
            self.pre_colors.append([])
            for y in range(self.height):
                height = self.map[x, y]
                # get color at block
                for j in range(len(colors)):
                    if height < colors[j][0]:
                        pre_color = colors[j][1]
                        break
                self.pre_colors[x].append(pre_color)

    def generate_sun_path(self):
        def f(x, y, r, angle):
            angle = angle / (np.pi * 18)
            return x + r * np.cos(angle), y + r * np.sin(angle)

        self.sun_xs = []
        self.sun_ys = []
        self.sun_pos = 0
        for i in range(0, 360, 10):
            x, y = f(self.width / 2, self.height / 2, 10, i)
            self.sun_xs.append(x)
            self.sun_ys.append(y)

        self.sun_zs = 50 + np.sin(np.linspace(0, np.pi * 2, len(self.sun_xs))) * 55

    def draw(self, screen):
        pixels_per_block = self.block_size // self.pixel_size

        for x in range(self.width * pixels_per_block):
            for y in range(self.height * pixels_per_block):
                pg.draw.rect(
                    screen,
                    self.get_color(
                        x / pixels_per_block + 1 / (pixels_per_block * 2),
                        y / pixels_per_block + 1 / (pixels_per_block * 2),
                    ),
                    (
                        x * self.pixel_size,
                        y * self.pixel_size,
                        self.pixel_size,
                        self.pixel_size,
                    ),
                )

    def draw_sun(self, screen):
        pg.draw.circle(
            screen,
            (255, 255, 0),
            (self.sun[0] * self.block_size, self.sun[1] * self.block_size),
            10,
        )

    def get_color(self, x, y):
        block_x = floor(x)
        block_y = floor(y)

        blocked = False

        height = max(self.map[block_x, block_y], 0)
        start_point = (x, y, height)

        # sun below "horizon"
        if self.sun[2] < height:
            blocked = True

        line = np.linspace(start_point, self.sun, 100)
        rounded_line = np.floor(line[:, :2])
        unique_xs = np.unique(rounded_line[:, 0], 1)[1]
        unqiue_ys = np.unique(rounded_line[:, 1], 1)[1]
        unique = np.unique(np.hstack((unique_xs, unqiue_ys)))
        points = line[unique]

        # points on form (x, y, ray_z)
        if not blocked:
            for point in points.tolist():
                block_x_ = floor(point[0])
                block_y_ = floor(point[1])
                curr_height = point[2]
                if curr_height > self.max_height:
                    break
                # break if outside of map
                if (
                    block_x_ < 0
                    or block_x_ >= self.width
                    or block_y_ < 0
                    or block_y_ >= self.height
                ):
                    break
                block_height = self.map[block_x_, block_y_]
                # water height during shading is 0
                if curr_height < 0:
                    curr_height = 0
                if curr_height < block_height:
                    blocked = True
                    break

        # shade color
        pre_color = self.pre_colors[block_x][block_y]
        color = (
            pre_color[0],
            pre_color[1],
            pre_color[2] - 0.1 if blocked else pre_color[2],
        )
        # convert to 0-255 and rgb
        color = tuple(round(v * 255) for v in colorsys.hsv_to_rgb(*color))
        return color

    def move_sun(self):
        # direction centre
        self.sun_pos += 1
        if self.sun_pos >= len(self.sun_xs):
            self.sun_pos = 0
        # move sun
        self.sun[0] = self.sun_xs[self.sun_pos]
        self.sun[1] = self.sun_ys[self.sun_pos]
        self.sun[2] = self.sun_zs[self.sun_pos]
