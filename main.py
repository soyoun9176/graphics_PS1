import pyglet
from pyglet.math import Mat4, Vec3

from render import RenderWindow
from characters.pungpung import create_pungpung, Pungpung
from control import Control


if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    renderer = RenderWindow(width, height, "뿡뿡이")
    renderer.set_location(200, 200)

    # Keyboard/Mouse control.
    controller = Control(renderer)

    # Setup World Environment
    from characters.static_object import Ground, StaticObject
    from characters.primitives import Cube
    from characters.rig import Part

    # Create and add a green ground
    ground = Ground(size=200.0, color=(200, 200, 200, 255))
    renderer.add_static_object(ground)

    # Add the main character
    pungpung = Pungpung()
    renderer.set_character(pungpung) 

    # Run the application
    renderer.run()
