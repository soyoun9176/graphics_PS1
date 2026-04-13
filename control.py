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
        Handle keys that need to be checked every frame.
        """
        if not self.window.camera_target_character:
            return

        rotation_speed = 0.5
        char = self.window.camera_target_character
        
        if self.keys[key.LEFT] or self.keys[key.RIGHT]:
            world_mat = char.root.world_transform
            char_pos = Vec3(world_mat[12], world_mat[13], world_mat[14])
            local_right = Vec3(world_mat[0], world_mat[1], world_mat[2])
            
            if self.keys[key.RIGHT]:
                char.turn_twards(rotation_speed * dt, char_pos - local_right)
            else:
                char.turn_twards(rotation_speed * dt, char_pos + local_right)

        if self.keys[key.UP] or self.keys[key.DOWN]:
            char.walk_direction = 1 if self.keys[key.UP] else -1
            if char.state != "walking":
                char.set_state("walking")
        elif char.state == "walking" and char.walk_target is None:
            char.set_state("idle")

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