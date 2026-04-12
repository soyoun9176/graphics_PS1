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

        self.shapes = []
        self.character_root = None
        self.character_parts = []
        self.world = None
        self.characters = []  # List of characters for multiple character support
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
            # 1. update camera angle
            self.cam_angle += dt
            
            # 2. new camera position
            new_x = self.cam_target.x + self.cam_radius * math.sin(self.cam_angle*0.4)
            new_z = self.cam_target.z + self.cam_radius * math.cos(self.cam_angle*0.4)
            self.cam_eye = Vec3(new_x, self.cam_eye.y, new_z)
            
            # 3. new view matrix
            self.view_mat = Mat4.look_at(self.cam_eye, target=self.cam_target, up=self.cam_vup)
        
        if self.animate:
            # 4. update character animation
            time = pyglet.clock.get_default().time()
            if self.world:
                self.world.update_all(time)
                # Update shapes transforms for all characters in the world
                shape_index = 0
                for root, parts in self.world.get_all_roots_and_parts():
                    for part in parts:
                        self.shapes[shape_index].transform_mat = part.joint.world_transform @ part.local_model
                        shape_index += 1
            elif self.characters:
                # Update all characters in the list
                for character in self.characters:
                    character.update_animation(time)
                    character.update_world()
                # Update shapes transforms for all characters
                shape_index = 0
                for character in self.characters:
                    for part in character.parts:
                        self.shapes[shape_index].transform_mat = part.joint.world_transform @ part.local_model
                        shape_index += 1

        view_proj = self.proj_mat @ self.view_mat
        for i, shape in enumerate(self.shapes):
            '''
            Update view and projection matrix. There exist only one view and projection matrix 
            in the program, so we just assign the same matrices for all the shapes
            '''
            shape.shader_program['view_proj'] = view_proj

    def on_resize(self, width, height):
        glViewport(0, 0, *self.get_framebuffer_size())
        self.proj_mat = Mat4.perspective_projection(
            aspect = width/height, z_near=self.z_near, z_far=self.z_far, fov = self.fov)
        return pyglet.event.EVENT_HANDLED

    def set_character(self, character):
        """
        Add a single character to the characters list.
        """
        self.characters.append(character)
        # Add shapes for the character
        for part in character.parts:
            transform = part.joint.world_transform @ part.local_model
            self.add_shape(transform, part.primitive.vertices, part.primitive.indices, part.primitive.colors)

    def set_world(self, world: World):
        self.world = world
        # Clear existing shapes
        self.shapes.clear()
        # Add all characters from the world
        for root, parts in world.get_all_roots_and_parts():
            for part in parts:
                transform = part.joint.world_transform @ part.local_model
                self.add_shape(transform, part.primitive.vertices, part.primitive.indices, part.primitive.colors)

    def add_character(self, character: Character):
        """
        Add a character to the renderer's character list.
        """
        self.characters.append(character)
        # Add shapes for the new character
        for part in character.parts:
            transform = part.joint.world_transform @ part.local_model
            self.add_shape(transform, part.primitive.vertices, part.primitive.indices, part.primitive.colors)

    def set_characters(self, characters_list):
        """
        Set multiple characters at once.
        """
        self.characters = characters_list
        self.shapes.clear()
        for character in self.characters:
            for part in character.parts:
                transform = part.joint.world_transform @ part.local_model
                self.add_shape(transform, part.primitive.vertices, part.primitive.indices, part.primitive.colors)

    def add_shape(self, transform, vertice, indice, color):
        
        '''
        Assign a group for each shape
        '''
        shape = CustomGroup(transform, len(self.shapes))
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES,
                        batch = self.batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color))
        self.shapes.append(shape)
         
    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

    