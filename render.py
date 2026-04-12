import math
import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key

from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_TRIANGLES
from pyglet.math import Mat4, Vec3
from pyglet.gl import *

import shader
from characters.primitives import CustomGroup
from characters.pungpung import Pungpung
from characters.character import Character
from characters.world import World



class RenderWindow(pyglet.window.Window):
    '''
    inherits pyglet.window.Window which is the default render window of Pyglet
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        '''
        View (camera) parameters
        '''
        self.cam_eye = Vec3(0,3,12)
        self.cam_target = Vec3(0,0.7,0)
        self.cam_vup = Vec3(0,1,0)
        self.view_mat = None
        '''
        Projection parameters
        '''
        self.z_near = 0.1
        self.z_far = 100
        self.fov = 60
        self.proj_mat = None

        self.static_shapes = []
        self.character_shapes = []
        self.world = World()
        self._shape_counter = 0
        self.setup()

        self.animate = True
        self.move_cam = False
        self.cam_angle = 0.0
        self.cam_radius = ((self.cam_eye.x - self.cam_target.x)**2 + (self.cam_eye.z - self.cam_target.z)**2)**0.5

    def setup(self) -> None:
        self.set_minimum_size(width = 400, height = 300)
        self.set_mouse_visible(True)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        # 1. Create a view matrix
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
        
        # 2. Create a projection matrix 
        self.proj_mat = Mat4.perspective_projection(
            aspect = self.width/self.height, 
            z_near=self.z_near, 
            z_far=self.z_far, 
            fov = self.fov)

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()

    def update(self,dt) -> None:
        if self.move_cam:
            # update camera angle
            self.cam_angle += dt
            
            # new camera position
            new_x = self.cam_target.x + self.cam_radius * math.sin(self.cam_angle*0.4)
            new_z = self.cam_target.z + self.cam_radius * math.cos(self.cam_angle*0.4)
            self.cam_eye = Vec3(new_x, self.cam_eye.y, new_z)
            
            # new view matrix
            self.view_mat = Mat4.look_at(self.cam_eye, target=self.cam_target, up=self.cam_vup)
        
        if self.animate:
            # update character animation
            time = pyglet.clock.get_default().time()
            self.world.update_characters(time)
            
            # sync character shapes with world transforms
            for character, shapes in zip(self.world.characters, self.character_shapes):
                for part, shape in zip(character.parts, shapes):
                    shape.transform_mat = part.joint.world_transform @ part.local_model

        view_proj = self.proj_mat @ self.view_mat
        # update view-projection for all shapes
        for shapes_list in self.character_shapes:
            for shape in shapes_list:
                shape.shader_program['view_proj'] = view_proj
        for shape in self.static_shapes:
            shape.shader_program['view_proj'] = view_proj

    def on_resize(self, width, height):
        glViewport(0, 0, *self.get_framebuffer_size())
        self.proj_mat = Mat4.perspective_projection(
            aspect = width/height, z_near=self.z_near, z_far=self.z_far, fov = self.fov)
        return pyglet.event.EVENT_HANDLED

    def set_character(self, character):
        """
        Add a single character to the world.
        """
        self.add_character(character)

    def set_world(self, world: World):
        self.world = world
        # Clear existing shapes
        self.character_shapes.clear()
        self.static_shapes.clear()
        
        # Add characters
        for character in world.characters:
            char_shapes = []
            for part in character.parts:
                transform = part.joint.world_transform @ part.local_model
                shape = self.add_shape(transform, part.primitive.vertices, part.primitive.indices, part.primitive.colors)
                char_shapes.append(shape)
            self.character_shapes.append(char_shapes)
            
        # Add static objects
        for obj in world.static_objects:
            for part in obj.parts:
                transform = part.joint.world_transform @ part.local_model
                shape = self.add_shape(transform, part.primitive.vertices, part.primitive.indices, part.primitive.colors)
                self.static_shapes.append(shape)

    def add_character(self, character: Character):
        """
        Add a character to the world.
        """
        self.world.add_character(character)
        char_shapes = []
        # Add shapes for the new character
        for part in character.parts:
            transform = part.joint.world_transform @ part.local_model
            shape = self.add_shape(transform, part.primitive.vertices, part.primitive.indices, part.primitive.colors)
            char_shapes.append(shape)
        self.character_shapes.append(char_shapes)

    def add_static_object(self, obj):
        """
        Add a static object (e.g. ground, tree, box) to the scene.
        """
        self.world.add_static_object(obj)
        # Add shapes for the static object
        for part in obj.parts:
            transform = part.joint.world_transform @ part.local_model
            shape = self.add_shape(transform, part.primitive.vertices, part.primitive.indices, part.primitive.colors)
            self.static_shapes.append(shape)

    def set_characters(self, characters_list):
        """
        Set multiple characters at once via the world.
        """
        # Clear existing character shapes
        self.world.characters = []
        self.character_shapes.clear()
        for character in characters_list:
            self.add_character(character)

    def add_shape(self, transform, vertice, indice, color):
        
        '''
        Assign a group for each shape
        '''
        # Unique order for drawing sorting and to prevent group merging
        order = self._shape_counter
        self._shape_counter += 1
        shape = CustomGroup(transform, order)
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES,
                        batch = self.batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color))
        return shape

         
    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

    