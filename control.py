import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key
from pyglet.math import Mat4, Vec3



class Control:
    """
    Control class controls keyboard & mouse inputs.
    """
    def __init__(self, window):
        window.on_key_press = self.on_key_press
        window.on_key_release = self.on_key_release
        window.on_mouse_motion = self.on_mouse_motion
        window.on_mouse_drag = self.on_mouse_drag
        window.on_mouse_press = self.on_mouse_press
        window.on_mouse_release = self.on_mouse_release
        window.on_mouse_scroll = self.on_mouse_scroll
        self.window = window
        self.keys = key.KeyStateHandler()
        window.push_handlers(self.keys)
        pyglet.clock.schedule_interval(self.update_continuous_input, 1/60.0)
        self.setup()

    def setup(self):
        pass

    def update(self, vector):
        pass

    def on_key_press(self, symbol, modifier):
        # TODO:
        if symbol == pyglet.window.key.C:
            self.window.move_cam = not self.window.move_cam
        elif symbol == pyglet.window.key.W:
            pungpung = self._find_character_by_name("Pungpung")
            if pungpung:
                pungpung.set_state("waving")
        elif symbol == pyglet.window.key.I:
            pungpung = self._find_character_by_name("Pungpung")
            if pungpung:
                pungpung.set_state("idle")
        elif symbol == pyglet.window.key.K:
            pungpung = self._find_character_by_name("Pungpung")
            if pungpung:
                pungpung.set_state("walking")
        elif symbol == pyglet.window.key.M:
            pungpung = self._find_character_by_name("Pungpung")
            if pungpung:
                pungpung.set_state("mouth_fart")
        elif symbol == pyglet.window.key.B:
            pungpung = self._find_character_by_name("Pungpung")
            if pungpung:
                pungpung.set_state("base_dance")
        elif symbol == pyglet.window.key.P:
            if self.window.camera_target_character:
                self.window.camera_target_character = None
                self.window.view_mat = Mat4.look_at(self.window.cam_eye, target=self.window.cam_target, up=self.window.cam_vup)
            else:
                pungpung = self._find_character_by_name("Pungpung")
                if pungpung:
                    self.window.camera_target_character = pungpung



    def update_continuous_input(self, dt):
        """
        Handle keys that need to be checked every frame (like rotation).
        """
        if not self.window.camera_target_character:
            return

        rotation_speed = 1.0 # radians per second
        
        if self.keys[key.LEFT]:
            self.window.camera_target_character.root.local_transform = \
                self.window.camera_target_character.root.local_transform @ Mat4.from_rotation(rotation_speed * dt, Vec3(0, 1, 0))
            self.window.camera_target_character.update_world()
        
        if self.keys[key.RIGHT]:
            self.window.camera_target_character.root.local_transform = \
                self.window.camera_target_character.root.local_transform @ Mat4.from_rotation(-rotation_speed * dt, Vec3(0, 1, 0))
            self.window.camera_target_character.update_world()

    def _find_character_by_name(self, name):
        """
        Find a character by name in the window's world.
        """
        return self.window.world.get_character_by_name(name)
    
    def on_key_release(self, symbol, modifier):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        elif symbol == pyglet.window.key.SPACE:
            self.window.animate = not self.window.animate
        # TODO:
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        # TODO:
        pass

    def on_mouse_press(self, x, y, button, modifier):
        # TODO:
        pass

    def on_mouse_release(self, x, y, button, modifier):
        # TODO:
        pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifier):
        # TODO:
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # TODO:
        pass