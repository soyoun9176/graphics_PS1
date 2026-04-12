import math
from characters.rig import Joint, Part
from pyglet.math import Mat4, Vec3
from characters.primitives import Cube, Tetrahedron

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

class Grass(StaticObject):
    """
    A clump of grass made of three tetrahedrons.
    """
    def __init__(self, scale=1.0, color=(60, 140, 30, 255)):
        super().__init__("Grass")
        
        for i in range(3):
            blade_mesh = Tetrahedron(scale=(0.2 * scale, 1.0 * scale, 0.2 * scale))
            self._solid_color(blade_mesh, color)
            
            angle_y = math.radians(i * 120)
            tilt_angle = math.radians(15)
            
            blade_transform = (
                Mat4.from_rotation(angle_y, Vec3(0, 1, 0)) @ 
                Mat4.from_rotation(tilt_angle, Vec3(1, 0, 0))
            )
            
            self.parts.append(Part(self.root, blade_mesh, blade_transform))
        
        self.update_world()
    

    def _solid_color(self, primitive, color):
        vertex_count = len(primitive.vertices) // 3
        primitive.colors = tuple(color * vertex_count)
