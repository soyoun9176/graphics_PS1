import pyglet
from pyglet.math import Mat4, Vec3

from render import RenderWindow
from characters.pungpung import create_pungpung
from characters.pungpung_animation import wave_arms
from control import Control


if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    renderer = RenderWindow(width, height, "뿡뿡이", resizable=True)
    renderer.set_location(200, 200)

    # Keyboard/Mouse control.
    controller = Control(renderer)

    root, parts = create_pungpung()
    renderer.set_character(root, parts)  # 캐릭터 설정

    # draw shapes
    renderer.run()
