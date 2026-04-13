import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse, key
from pyglet.math import Mat4, Vec3

class Control:
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

    def setup(self): pass
    def update(self, vector): pass

    def on_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.C:
            self.window.move_cam = not self.window.move_cam
        elif symbol == pyglet.window.key.M:
            pungpung = self._find_character_by_name("Pungpung")
            if pungpung:
                pungpung.set_state("mouth_fart")
                _start_moving = self.window.world.pungpung_friends_dance()
                pyglet.clock.schedule_once(_start_moving, 3.0)
        elif symbol == pyglet.window.key.B:
            pungpung = self._find_character_by_name("Pungpung")
            if pungpung:
                pungpung.set_state("base_dance")
        elif symbol == pyglet.window.key.P:
            if self.window.camera_target_character:
                self.window.camera_target_character = None
                self.window.cam_target = Vec3(0, 0, 0) 
            else:
                pungpung = self._find_character_by_name("Pungpung")
                if pungpung:
                    self.window.camera_target_character = pungpung
        elif symbol == pyglet.window.key.F:
            names = ["Friend1", "Friend2", "Friend3", "Friend3"]
            for name in names:
                character = self.window.world.get_character_by_name(name)
                if (character == None) :continue
                character.set_state("idle")

    def update_continuous_input(self, dt):
        """
        Handle keys that need to be checked every frame.
        """
        # character movement
        char = self._find_character_by_name("Pungpung")
        if char:
            rotation_speed = 2.0
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

        if not self.window.camera_target_character:
            cam_speed = 2.0 # TODO: fit this
            zoom_speed = 15.0
            if self.keys[key.A]:
                self.window.orbit_theta -= cam_speed * dt
            if self.keys[key.D]:
                self.window.orbit_theta += cam_speed * dt
            if self.keys[key.W]:
                self.window.orbit_y += cam_speed * dt
            if self.keys[key.S]:
                self.window.orbit_y -= cam_speed * dt
            if self.keys[key.Z]:
                self.window.orbit_radius -= zoom_speed * dt
            if self.keys[key.X]:
                self.window.orbit_radius += zoom_speed * dt

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
        # TODO: cannot test now
        pass