import logging
import math
import time
import numpy as np
import pygame as pygame

colors = (
    (0, 0, 153),
    (0, 204, 255),
    (255, 255, 204),
    (102, 255, 51),
    (0, 102, 0),
    (137, 144, 144),
    (245, 245, 245),
)


class Map:
    def __init__(self, width, height, sun_pos, block_size=20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.full_width = width * block_size
        self.full_height = height * block_size
        self.map = np.zeros((width, height))

        self.logger = logging.getLogger(__name__)

        # x, y ,z
        self.sun = sun_pos

    def generate(self):
        for x in range(self.width):
            for y in range(self.height):
                self.map[x][y] = (
                    self.height / 2
                    + self.width / 2
                    - (abs((self.width / 2) - x) + abs((self.height / 2) - y))
                ) - np.random.normal(0, 2)
        # scale map to 0-6
        self.map = self.map - self.map.min()
        self.map = (self.map / self.map.max()) * 6
        # round to nearest integer
        self.map = np.round(self.map)

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

    def get_color(self, x, y):
        dist_x = self.sun[0] - x
        dist_y = self.sun[1] - y
        dist_z = self.sun[2] - self.map[x, y]
        dist_max = max(dist_x, dist_y, dist_z)
        divider = dist_max * 2
        ray = (dist_x / divider, dist_y / divider, dist_z / divider)
        total_dist = math.sqrt(dist_x**2 + dist_y**2 + dist_z**2)
        self.logger.debug(f"ray for {x}, {y} is {ray} with total_dist {total_dist}")
        ray_x = x
        ray_y = y
        ray_z = self.map[x, y]
        self.logger.debug(divider)
        for i in range(int(divider)):
            ray_x += ray[0]
            ray_y += ray[1]
            ray_z += ray[2]
            self.logger.debug(f"ray at {ray_x}, {ray_y}, {ray_z}")
            # check height of block we are in
            block_x = int(np.round(ray_x))
            block_y = int(np.round(ray_y))
            height = self.map[block_x, block_y]
            self.logger.debug(f"height of block {block_x}, {block_y} is {height}")
            if ray_z < height:
                # blocked
                self.logger.debug("blocked")
                return (0, 0, 0)
        # ray_slope = max((self.sun[2] - self.map[x, y]), 0) / (
        #     math.sqrt((self.sun[0] - x) ** 2 + (self.sun[1] - y) ** 2)
        # )
        # self.logger.debug(f"ray_slope for {x}, {y} is {ray_slope}")
        self.logger.debug(f"not blocked, we get color {colors[int(self.map[x, y])]}")
        return colors[int(self.map[x, y])]

    def move_sun(self):
        self.sun[0] = self.sun[0] + np.random.randint(-1, 2)
        self.sun[1] = self.sun[1] + np.random.randint(-1, 2)
        # clip to be inside map
        self.sun[0] = np.clip(self.sun[0], 0, self.width - 1)
        self.sun[1] = np.clip(self.sun[1], 0, self.height - 1)


def main():
    pygame.init()
    map = Map(30, 30, [9, 9, 9])
    screen = pygame.display.set_mode((map.full_width, map.full_height))
    pygame.display.set_caption("Map")
    clock = pygame.time.Clock()
    running = True
    map.generate()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        map.logger.debug(map.map)
        map.move_sun()
        map.draw(screen)
        pygame.display.flip()
        clock.tick(1)
        # time.sleep(2)


pygame.quit()

if __name__ == "__main__":
    main()
