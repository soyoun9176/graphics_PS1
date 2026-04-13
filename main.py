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

    # Create and add a light grey ground
    ground = Ground(size=20.0, color=(255, 200, 200, 255)) # Ground(size=100.0, color=(111, 79, 40, 255))
    renderer.add_static_object(ground)

    # Add the main character
    pungpung = Pungpung()
    renderer.set_character(pungpung) 

    # Add Pungpung's friends at specified positions
    from characters.pungpung import FriendPung
    friend_configs = [
        ("Friend1", (-6, 0, -5), (150, 255, 150, 255)), # Mint
        ("Friend2", (-3, 0, -5), (200, 150, 255, 255)), # Lavender
        ("Friend3", (3, 0, -5), (150, 200, 255, 255)),  # Sky
        ("Friend4", (6, 0, -5), (255, 255, 150, 255))   # Lemon
    ]

    for name, pos, color in friend_configs:
        friend = FriendPung(name=name, body_color=color)
        friend.root.local_transform = Mat4.from_translation(Vec3(*pos))
        renderer.add_character(friend)

    renderer.world.get_character_by_name("Friend1").update_target(Vec3(6, 0, 0))
    renderer.world.get_character_by_name("Friend2").update_target(Vec3(3, 0, 0))
    renderer.world.get_character_by_name("Friend3").update_target(Vec3(-3, 0, 0))
    renderer.world.get_character_by_name("Friend4").update_target(Vec3(-6, 0, 0))

    # Run the application
    renderer.run()
