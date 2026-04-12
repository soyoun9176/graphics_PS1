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
    ground = Ground(size=100.0, color=(111, 79, 40, 255))
    renderer.add_static_object(ground)

    # Add random grass clumps
    from characters.static_object import Grass
    import random
    
    for _ in range(1000):
        # Random position within ground bounds
        gx = random.uniform(-40, 40)
        gz = random.uniform(-40, 40)
        
        # Avoid putting grass right at the origin where character starts
        if abs(gx) < 2 and abs(gz) < 2:
            continue
            
        g_scale = random.uniform(0.3, 0.8)
        grass = Grass(scale=g_scale)
        grass.root.local_transform = Mat4.from_translation(Vec3(gx, 0, gz))
        renderer.add_static_object(grass)

    # Add the main character
    pungpung = Pungpung()
    renderer.set_character(pungpung) 

    # Run the application
    renderer.run()
