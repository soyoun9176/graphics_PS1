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
        
        # Stage Floor
        floor_mesh = Cube(scale=(size*3, 0.1, size*3))
        self._solid_color(floor_mesh, color)
        # Floor is centered at (0, -0.05, 0)
        self.parts.append(Part(self.root, floor_mesh, Mat4.from_translation(Vec3(0, -0.05, 0))))
        
        # Back Wall
        wall_height = size * 0.5
        wall_mesh = Cube(scale=(size, wall_height*0.5, 0.1))
        wall_color = tuple(max(0, c - 30) for c in color[:3]) + (color[3],)
        self._solid_color(wall_mesh, wall_color)
        wall_center = Cube(scale=(size*0.6, wall_height*0.5, 0.1))
        self._solid_color(wall_center, wall_color)
        backwall_color = tuple(max(0, c - 60) for c in color[:3]) + (color[3],)
        wall_back = Cube(scale=(size*3, wall_height, 0.1))
        self._solid_color(wall_back, backwall_color)
        
        self.parts.append(Part(self.root, wall_mesh, Mat4.from_translation(Vec3(0, wall_height*0.75, -size/2))))
        self.parts.append(Part(self.root, wall_center, Mat4.from_translation(Vec3(0, wall_height*0.25, -size/2))))
        self.parts.append(Part(self.root, wall_back, Mat4.from_translation(Vec3(0, wall_height*0.5, -size/2 - 10))))
        
        # Left/Right Side Walls
        side_wall_mesh = Cube(scale=(0.1, wall_height, size))
        self._solid_color(side_wall_mesh, wall_color)
        
        # Left Wall
        self.parts.append(Part(self.root, side_wall_mesh, Mat4.from_translation(Vec3(-size/2, wall_height/2, 0))))
        # Right Wall
        self.parts.append(Part(self.root, side_wall_mesh, Mat4.from_translation(Vec3(size/2, wall_height/2, 0))))
        
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
