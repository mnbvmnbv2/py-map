import pygame as pg
import moderngl as mgl
import glm

from meshes.map_mesh import MapMesh


class GameEngine:
    def __init__(self, width: int, height: int, block_size: int) -> None:
        self.width = width
        self.height = height
        self.block_size = block_size

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 2)  # anti-aliasing
        pg.display.set_mode(
            (self.height * self.block_size, self.width * self.block_size), pg.DOUBLEBUF | pg.OPENGL
        )

        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)
        self.ctx.gc_mode = "auto"

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.running = True

        self.objects = []

        self.on_init()

    def on_init(self):
        map_mesh = MapMesh(self, width=self.width, height=self.height)
        self.objects.append(map_mesh)

    def run(self):
        while self.running:
            self.delta_time = self.clock.tick(60) / 1000.0
            self.events()
            self.update()
            self.render()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        pass

    def render(self):
        self.ctx.clear(color=glm.vec3(1, 0.16, 0.25))
        for obj in self.objects:
            obj.render()
        pg.display.flip()

    def get_program(self, name):
        with open(f"shaders/{name}.vert") as file:
            vertex_shader = file.read()

        with open(f"shaders/{name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        return program


def main():
    game = GameEngine(25, 40, 30)
    game.run()


if __name__ == "__main__":
    main()
