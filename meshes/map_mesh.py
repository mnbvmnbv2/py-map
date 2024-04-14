import numpy as np
from meshes.base_mesh import BaseMesh
from generation import basic_map


class MapMesh(BaseMesh):
    def __init__(self, app):
        super().init()
        self.app = app
        self.ctx = self.app.ctx
        self.program = self.app.get_program("map")

        self.vbo_format = "3f"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("in_position",)
        self.vao = self.get_vao()

    def get_vertex_data(self):
        height_map = np.zeros((21, 21))
        basic_map(height_map)
        # scale 0-1
        height_map = (height_map - height_map.min()) / (
            height_map.max() - height_map.min()
        )
        vertex_data = np.zeros((3 * 6 * 20 * 20,), dtype="f4")
        # first triangle
        # set x on first index of upper left
        vertex_data[::18] = np.tile(np.arange(20) / 10 - 1, 20)
        # second index
        vertex_data[3::18] = np.tile(np.arange(20) / 10 - 1, 20)
        # third index
        vertex_data[6::18] = np.tile((np.arange(20) + 1) / 10 - 1, 20)
        # set ys
        vertex_data[1::18] = np.repeat((np.arange(20) + 1) / 10 - 1, 20)[::-1]
        vertex_data[4::18] = np.repeat(np.arange(20) / 10 - 1, 20)[::-1]
        vertex_data[7::18] = np.repeat((np.arange(20) + 1) / 10 - 1, 20)[::-1]
        # set zs
        vertex_data[2::18] = height_map[:-1, :-1].flatten()
        vertex_data[5::18] = height_map[1:, :-1].flatten()
        vertex_data[8::18] = height_map[:-1, 1:].flatten()
        # second triangle
        # set xs
        vertex_data[9::18] = np.tile(np.arange(20) / 10 - 1, 20)
        vertex_data[12::18] = np.tile((np.arange(20) + 1) / 10 - 1, 20)
        vertex_data[15::18] = np.tile((np.arange(20) + 1) / 10 - 1, 20)
        # set ys
        vertex_data[10::18] = np.repeat(np.arange(20) / 10 - 1, 20)[::-1]
        vertex_data[13::18] = np.repeat(np.arange(20) / 10 - 1, 20)[::-1]
        vertex_data[16::18] = np.repeat((np.arange(20) + 1) / 10 - 1, 20)[::-1]
        # set zs
        vertex_data[11::18] = height_map[1:, :-1].flatten()
        vertex_data[14::18] = height_map[1:, 1:].flatten()
        vertex_data[17::18] = height_map[:-1, 1:].flatten()

        return vertex_data
