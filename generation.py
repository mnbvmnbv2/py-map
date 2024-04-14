import math
import numpy as np
import torch as torch


def pooled_noise(
    width: int,
    height: int,
    alpha: float = 0.45,
    beta: int = 5,
    x: int = 0,
    y: int = 0,
    seed: int = 0,
):
    grid = torch.clip(
        torch.normal(0, alpha, (width + beta * 2, height + beta * 2)), -1, 1
    )
    # grid = deterministic_grid(
    #     width + beta * 2, height + beta * 2, x - beta, y - beta, alpha, seed
    # )
    smoother = torch.nn.AvgPool2d(3, stride=1, padding=0)
    for _ in range(beta):
        grid = smoother(grid[None, None, :, :]).squeeze()
    return grid


def map_from_pooled_noise(
    map: np.ndarray,
    alpha: float = 0.45,
    beta: int = 5,
):
    noise = pooled_noise(map.shape[0], map.shape[1], alpha, beta) * 80
    map[:] = noise.numpy()


def basic_map(map: np.ndarray):
    width, height = map.shape
    print(map.shape)
    for x in range(width):
        for y in range(height):
            dist_centre = math.sqrt((width / 2 - x) ** 2 + (height / 2 - y) ** 2)
            map[x, y] = (
                25
                # - math.log(dist_centre * 10 + 0.01)
                - dist_centre * 2
                + np.random.normal(0, 1)
            )
