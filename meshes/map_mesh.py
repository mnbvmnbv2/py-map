import numpy as np
from meshes.base_mesh import BaseMesh
from generation import basic_map


class MapMesh(BaseMesh):
    def __init__(self, app, width, height):
        super().init()
        self.app = app
        self.ctx = self.app.ctx
        self.program = self.app.get_program("map")

        self.width = width
        self.height = height

        self.vbo_format = "3f"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("in_position",)  # ) "in_normal")
        self.vao = self.get_vao()

    def get_vertex_data(self):
        height_map = np.zeros((self.width + 1, self.height + 1))
        basic_map(height_map)
        # scale 0-1
        height_map = (height_map - height_map.min()) / (
            height_map.max() - height_map.min()
        )
        # xyz, normal, two-triangles, 20x20 grid
        vertex_data = np.zeros((3 * 6 * self.width * self.height,), dtype="f4")
        # first triangle upper left triangle, starting from 0,0 coordinate
        # x
        vertex_data[::18] = np.tile(
            np.arange(self.width) / (self.width / 2) - 1, self.width
        )
        # y
        vertex_data[1::18] = np.repeat(
            (np.arange(self.height) + 1) / (self.height / 2) - 1, self.height
        )[::-1]
        # z
        vertex_data[2::18] = height_map[:-1, :-1].flatten()
        # down left coordinate
        vertex_data[3::18] = np.tile(
            np.arange(self.width) / (self.width / 2) - 1, self.width
        )
        vertex_data[4::18] = np.repeat(
            np.arange(self.height) / (self.height / 2) - 1, self.height
        )[::-1]
        vertex_data[5::18] = height_map[1:, :-1].flatten()
        # upper right
        vertex_data[6::18] = np.tile(
            (np.arange(self.width) + 1) / (self.width / 2) - 1, self.width
        )
        vertex_data[7::18] = np.repeat(
            (np.arange(self.height) + 1) / (self.height / 2) - 1, self.height
        )[::-1]
        vertex_data[8::18] = height_map[:-1, 1:].flatten()
        # second triangle
        # down left
        vertex_data[9::18] = np.tile(
            np.arange(self.width) / (self.width / 2) - 1, self.width
        )
        vertex_data[10::18] = np.repeat(
            np.arange(self.height) / (self.height / 2) - 1, self.height
        )[::-1]
        vertex_data[11::18] = height_map[1:, :-1].flatten()
        # down right
        vertex_data[12::18] = np.tile(
            (np.arange(self.width) + 1) / (self.width / 2) - 1, self.width
        )
        vertex_data[13::18] = np.repeat(
            np.arange(self.height) / (self.height / 2) - 1, self.height
        )[::-1]
        vertex_data[14::18] = height_map[1:, 1:].flatten()
        # upper right
        vertex_data[15::18] = np.tile(
            (np.arange(self.width) + 1) / (self.width / 2) - 1, self.width
        )
        vertex_data[16::18] = np.repeat(
            (np.arange(self.height) + 1) / (self.height / 2) - 1, self.height
        )[::-1]
        vertex_data[17::18] = height_map[:-1, 1:].flatten()

        return vertex_data
