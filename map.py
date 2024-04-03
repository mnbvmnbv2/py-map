import colorsys
import logging
import math
import numpy as np
import pygame as pygame

# range and value
colors = (
    (-8, (0.6, 0.6, 0.7)),  # deep water
    (0, (0.5, 0.8, 0.8)),  # shallow water
    (2, (0.15, 0.6, 0.8)),  # sand
    (5, (0.27, 0.6, 0.8)),  # grass
    (10, (0.22, 0.6, 0.5)),  # forest
    (25, (0.5, 0.1, 0.3)),  # mountain
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
        self.pre_colors = []
        self.max_dist = math.sqrt(width**2 + height**2 + sun_pos[2] ** 2)

        self.logger = logging.getLogger(__name__)

        # x, y ,z
        self.generate()
        self.generate_sun_path()
        self.max_height = self.map.max()
        self.sun = sun_pos
        self.sun[2] = self.max_height + 30

    def generate(self):
        for x in range(self.width):
            self.pre_colors.append([])
            for y in range(self.height):
                dist_centre = math.sqrt(
                    (self.width / 2 - x) ** 2 + (self.height / 2 - y) ** 2
                )
                self.map[x][y] = (
                    25
                    # - math.log(dist_centre * 10 + 0.01)
                    - dist_centre * 2
                    + np.random.normal(0, 1)
                )
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

        self.xs = []
        self.ys = []
        self.sun_pos = 0
        for i in range(0, 360, 15):
            x, y = f(self.width / 2, self.height / 2, 10, i)
            self.xs.append(x)
            self.ys.append(y)

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
        ray_x = x
        ray_y = y
        if self.map[x, y] < 0:
            ray_z = 0
        else:
            ray_z = self.map[x, y]

        blocked = False

        for i in range(int(divider)):
            ray_x += ray[0]
            ray_y += ray[1]
            ray_z += ray[2]
            self.logger.debug(f"ray at {ray_x}, {ray_y}, {ray_z}")
            if ray_z > self.max_height:
                break
            # check height of block we are in
            block_x = round(ray_x)
            block_y = round(ray_y)
            # break if outside of map
            if (
                block_x < 0
                or block_x >= self.width
                or block_y < 0
                or block_y >= self.height
            ):
                break
            curr_height = self.map[block_x, block_y]
            # water height during shading is 0
            if curr_height < 0:
                curr_height = 0
            if ray_z < curr_height:
                blocked = True
                break

        # shade color
        pre_color = self.pre_colors[x][y]
        color = (
            pre_color[0],
            pre_color[1],
            pre_color[2] - 0.1 if blocked else pre_color[2],
        )
        # convert to 0-255 and rgb
        color = tuple(round(v * 255) for v in colorsys.hsv_to_rgb(*color))
        return color
        # colors[int(self.map[x, y])]

    def move_sun(self):
        # direction centre
        self.sun_pos += 1
        if self.sun_pos >= len(self.xs):
            self.sun_pos = 0
        # move sun
        self.sun[0] = self.xs[self.sun_pos]
        self.sun[1] = self.ys[self.sun_pos]
        self.sun[2] = 50
        # time.sleep(1)
        # clip to be inside map
        # self.sun[0] = np.clip(self.sun[0], 0, self.width - 1)
        # self.sun[1] = np.clip(self.sun[1], 0, self.height - 1)


def main():
    # logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    map = Map(50, 30, [10, 10, 0], block_size=15)
    screen = pygame.display.set_mode((map.full_width, map.full_height))
    pygame.display.set_caption("Map")
    clock = pygame.time.Clock()
    running = True
    # for i in range(10):
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
