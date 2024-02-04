import colorsys
import logging
import math
import time
import numpy as np
import pygame as pygame

# range and value
colors = (
    (-10, (0.6, 0.8, 0.8)),  # deep water
    (0, (0.5, 0.8, 0.8)),  # shallow water
    (1, (0.15, 0.6, 0.8)),  # sand
    (3, (0.27, 0.6, 0.8)),  # grass
    (6, (0.22, 0.6, 0.5)),  # forest
    (15, (0.5, 0.1, 0.3)),  # mountain
    (float("inf"), (0.5, 0.05, 0.9)),  # snow
)


class Map:
    def __init__(self, width, height, sun_pos, block_size=20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.full_width = width * block_size
        self.full_height = height * block_size
        self.map = np.zeros((width, height))
        self.max_dist = math.sqrt(width**2 + height**2 + sun_pos[2] ** 2)

        self.logger = logging.getLogger(__name__)

        # x, y ,z
        self.generate()
        self.max_height = self.map.max()
        self.sun = sun_pos
        self.sun[2] = self.max_height + 10

    def generate(self):
        for x in range(self.width):
            for y in range(self.height):
                dist_centre = math.sqrt(
                    (self.width / 2 - x) ** 2 + (self.height / 2 - y) ** 2
                )
                self.map[x][y] = (
                    10
                    - math.log(dist_centre * 10 + 0.01)
                    - dist_centre
                    + np.random.normal(2, 1)
                )

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(
                    screen,
                    self.get_color(x, y),
                    (
                        x * self.block_size,
                        y * self.block_size,
                        self.block_size,
                        self.block_size,
                    ),
                )

    def draw_sun(self, screen):
        pygame.draw.circle(
            screen,
            (255, 255, 0),
            (self.sun[0] * self.block_size, self.sun[1] * self.block_size),
            10,
        )

    def get_color(self, x, y):
        dist_x = self.sun[0] - x
        dist_y = self.sun[1] - y
        # if water, we get shading from z 0
        if self.map[x, y] < 0:
            dist_z = self.sun[2]
        else:
            dist_z = self.sun[2] - self.map[x, y]
        dist_max = max(dist_x, dist_y, dist_z)
        divider = dist_max * 2
        ray = (dist_x / divider, dist_y / divider, dist_z / divider)
        total_dist = math.sqrt(dist_x**2 + dist_y**2 + dist_z**2)
        # self.logger.debug(f"ray for {x}, {y} is {ray} with total_dist {total_dist}")
        ray_x = x
        ray_y = y
        if self.map[x, y] < 0:
            ray_z = 0
        else:
            ray_z = self.map[x, y]

        height = self.map[x, y]
        # get color at block
        for j in range(len(colors)):
            if height < colors[j][0]:
                pre_color = colors[j][1]
                break
        blocked = False

        for i in range(int(divider)):
            ray_x += ray[0]
            ray_y += ray[1]
            ray_z += ray[2]
            # self.logger.debug(f"ray at {ray_x}, {ray_y}, {ray_z}")
            # check height of block we are in
            block_x = int(np.round(ray_x))
            block_y = int(np.round(ray_y))
            curr_height = self.map[block_x, block_y]
            # water height during shading is 0
            if curr_height < 0:
                curr_height = 0
            # self.logger.debug(f"height of block {block_x}, {block_y} is {curr_height}")
            if ray_z < curr_height:
                # blocked
                self.logger.debug("blocked")
                blocked = True
                break

        # shade color
        color = (
            pre_color[0],
            pre_color[1],
            pre_color[2] - 0.1 if blocked else pre_color[2],
        )
        # convert to 0-255 and rgb
        color = tuple(round(v * 255) for v in colorsys.hsv_to_rgb(*color))
        # self.logger.debug(f"blocked: {blocked}, we get color {color}")
        return color
        # colors[int(self.map[x, y])]

    def move_sun(self):
        self.sun[0] = self.sun[0] + np.random.randint(-1, 2)
        self.sun[1] = self.sun[1] + np.random.randint(-1, 2)
        # clip to be inside map
        self.sun[0] = np.clip(self.sun[0], 0, self.width - 1)
        self.sun[1] = np.clip(self.sun[1], 0, self.height - 1)


def main():
    # print(colorsys.hsv_to_rgb(0.9, 0.5, 0.9))
    # return
    # logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    map = Map(30, 30, [20, 20, 0], block_size=20)
    screen = pygame.display.set_mode((map.full_width, map.full_height))
    pygame.display.set_caption("Map")
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        # map.logger.debug(map.map)
        map.move_sun()
        map.draw(screen)
        map.draw_sun(screen)
        pygame.display.flip()
        clock.tick(60)
        # time.sleep(2)


pygame.quit()

if __name__ == "__main__":
    main()
