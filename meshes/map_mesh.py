import numpy as np
from meshes.base_mesh import BaseMesh
from generation import basic_map, map_from_pooled_noise
import glm


class MapMesh(BaseMesh):
    def __init__(self, app, width, height):
        super().init()
        self.app = app
        self.ctx = self.app.ctx
        self.program = self.app.get_program("map")

        self.width = width
        self.height = height

        self.vbo_format = "3f 3f"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("in_position", "in_normal")
        self.vao = self.get_vao()

    def update(self):
        sun_x = np.cos(self.app.total_time) * 0.4 + 0.5
        sun_y = np.sin(self.app.total_time) * 0.4 + 0.5
        sun_z = 0.5  # np.sin(self.app.total_time) * 0.4 + 0.5
        print(sun_x, sun_y)
        self.program["sun_dir"].write(glm.vec3(sun_x, sun_y, sun_z))

    def get_vertex_data(self):
        height_map, der_x, der_y = basic_map(self.width + 1, self.height + 1)
        # height_map = map_from_pooled_noise(self.width + 1, self.height + 1)
        normal_map = np.zeros((self.height + 1, self.width + 1, 3))
        normal_map[:, :, 0] = der_x.T
        normal_map[:, :, 1] = der_y.T
        # scale 0-1
        height_map = (height_map - height_map.min()) / (height_map.max() - height_map.min())
        height_map = height_map.T
        print(height_map.shape, normal_map.shape)
        # xyz, normal, two-triangles, 20x20 grid
        vertex_data = np.zeros((2 * 3 * 6 * self.width * self.height,), dtype="f4")
        # first triangle upper left triangle, starting from 0,0 coordinate
        # xyz
        vertex_data[::36] = np.tile(np.arange(self.width) / (self.width / 2) - 1, self.height)
        vertex_data[1::36] = np.repeat((np.arange(self.height) + 1) / (self.height / 2) - 1, self.width)[::-1]
        vertex_data[2::36] = height_map[:-1, :-1].flatten()
        # normal
        vertex_data[3::36] = normal_map[:-1, :-1, 0].flatten()
        vertex_data[4::36] = normal_map[:-1, :-1, 1].flatten()
        vertex_data[5::36] = normal_map[:-1, :-1, 2].flatten()
        # down left coordinate
        vertex_data[6::36] = np.tile(np.arange(self.width) / (self.width / 2) - 1, self.height)
        vertex_data[7::36] = np.repeat(np.arange(self.height) / (self.height / 2) - 1, self.width)[::-1]
        vertex_data[8::36] = height_map[1:, :-1].flatten()
        # normal
        vertex_data[9::36] = normal_map[1:, :-1, 0].flatten()
        vertex_data[10::36] = normal_map[1:, :-1, 1].flatten()
        vertex_data[11::36] = normal_map[1:, :-1, 2].flatten()
        # upper right
        vertex_data[12::36] = np.tile((np.arange(self.width) + 1) / (self.width / 2) - 1, self.height)
        vertex_data[13::36] = np.repeat((np.arange(self.height) + 1) / (self.height / 2) - 1, self.width)[
            ::-1
        ]
        vertex_data[14::36] = height_map[:-1, 1:].flatten()
        # normal
        vertex_data[15::36] = normal_map[:-1, 1:, 0].flatten()
        vertex_data[16::36] = normal_map[:-1, 1:, 1].flatten()
        vertex_data[17::36] = normal_map[:-1, 1:, 2].flatten()
        # second triangle
        # down left
        vertex_data[18::36] = np.tile(np.arange(self.width) / (self.width / 2) - 1, self.height)
        vertex_data[19::36] = np.repeat(np.arange(self.height) / (self.height / 2) - 1, self.width)[::-1]
        vertex_data[20::36] = height_map[1:, :-1].flatten()
        # normal
        vertex_data[21::36] = normal_map[1:, :-1, 0].flatten()
        vertex_data[22::36] = normal_map[1:, :-1, 1].flatten()
        vertex_data[23::36] = normal_map[1:, :-1, 2].flatten()
        # down right
        vertex_data[24::36] = np.tile((np.arange(self.width) + 1) / (self.width / 2) - 1, self.height)
        vertex_data[25::36] = np.repeat(np.arange(self.height) / (self.height / 2) - 1, self.width)[::-1]
        vertex_data[26::36] = height_map[1:, 1:].flatten()
        # normal
        vertex_data[27::36] = normal_map[1:, 1:, 0].flatten()
        vertex_data[28::36] = normal_map[1:, 1:, 1].flatten()
        vertex_data[29::36] = normal_map[1:, 1:, 2].flatten()
        # upper right
        vertex_data[30::36] = np.tile((np.arange(self.width) + 1) / (self.width / 2) - 1, self.height)
        vertex_data[31::36] = np.repeat((np.arange(self.height) + 1) / (self.height / 2) - 1, self.width)[
            ::-1
        ]
        vertex_data[32::36] = height_map[:-1, 1:].flatten()
        # normal
        vertex_data[33::36] = normal_map[:-1, 1:, 0].flatten()
        vertex_data[34::36] = normal_map[:-1, 1:, 1].flatten()
        vertex_data[35::36] = normal_map[:-1, 1:, 2].flatten()

        return vertex_data
