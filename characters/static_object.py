from characters.rig import Joint, Part
from pyglet.math import Mat4, Vec3
from characters.primitives import Cube

class StaticObject:
    """
    Base class for non-moving objects in the world.
    """
    def __init__(self, name="StaticObject"):
        self.name = name
        self.root = Joint(name)
        self.parts = []

    def get_root_and_parts(self):
        return self.root, self.parts

    def update_world(self):
        self.root.update_world()

class Ground(StaticObject):
    """
    A simple ground object (flattened cube).
    """
    def __init__(self, size=20.0, color=(100, 100, 100, 255)):
        super().__init__("Ground")
        mesh = Cube(scale=(size, 0.1, size))
        self._solid_color(mesh, color)
        
        # Position it slightly below zero to avoid z-fighting with character feet
        self.root.local_transform = Mat4.from_translation(Vec3(0, -0.05, 0))
        self.parts.append(Part(self.root, mesh))
        self.update_world()

    def _solid_color(self, primitive, color):
        vertex_count = len(primitive.vertices) // 3
        primitive.colors = tuple(color * vertex_count)
