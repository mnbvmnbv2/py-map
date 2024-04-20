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
) -> torch.Tensor:
    grid = torch.clip(torch.normal(0, alpha, (width + beta * 2, height + beta * 2)), -1, 1)
    # grid = deterministic_grid(
    #     width + beta * 2, height + beta * 2, x - beta, y - beta, alpha, seed
    # )
    smoother = torch.nn.AvgPool2d(3, stride=1, padding=0)
    for _ in range(beta):
        grid = smoother(grid[None, None, :, :]).squeeze()
    return grid


def map_from_pooled_noise(
    width: int,
    height: int,
    alpha: float = 0.45,
    beta: int = 5,
) -> np.array:
    noise = pooled_noise(width, height, alpha, beta) * 80
    return noise.numpy()


def basic_map(width: int, height: int) -> tuple[np.array, np.array, np.array]:
    map = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            dist_centre = math.sqrt((width / 2 - x) ** 2 + (height / 2 - y) ** 2)
            map[x, y] = 25 - dist_centre * 2 + np.random.normal(0, 1)

    deriv_x = np.gradient(map, axis=0)
    deriv_y = np.gradient(map, axis=1)
    # normalize to 0-1
    # deriv_x = (deriv_x - deriv_x.min()) / (deriv_x.max() - deriv_x.min())
    # deriv_y = (deriv_y - deriv_y.min()) / (deriv_y.max() - deriv_y.min())
    return map, deriv_x, deriv_y
