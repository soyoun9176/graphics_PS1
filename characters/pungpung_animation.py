import math
from pyglet.math import Mat4, Vec3

def wave_arms(root, time):
    """
    pungpung arm shaking
    root: root joint of pungpung
    time: current time in seconds
    """
    # left
    left_shoulder = find_joint(root, "left_shoulder")
    if left_shoulder:
        base_transform = Mat4.from_translation(Vec3(-0.4, 0.6, 0.05)) @ Mat4.from_rotation(math.radians(-40), Vec3(0, 0, 1))
        anim_rotation = Mat4.from_rotation(math.sin(time * 3) * 0.3, Vec3(1, 0, 0))  # X축 회전
        left_shoulder.local_transform = base_transform @ anim_rotation
    
    left_elbow = find_joint(root, "left_elbow")
    if left_elbow:
        base_transform = Mat4.from_translation(Vec3(0, -0.55, 0))
        anim_rotation = Mat4.from_rotation(math.sin(time * 3 + math.pi/4) * 0.2, Vec3(1, 0, 0))
        left_elbow.local_transform = base_transform @ anim_rotation
    
    # right
    right_shoulder = find_joint(root, "right_shoulder")
    if right_shoulder:
        base_transform = Mat4.from_translation(Vec3(0.4, 0.6, 0.05)) @ Mat4.from_rotation(math.radians(40), Vec3(0, 0, 1))
        anim_rotation = Mat4.from_rotation(math.sin(time * 3 + math.pi) * 0.3, Vec3(1, 0, 0))
        right_shoulder.local_transform = base_transform @ anim_rotation
    
    right_elbow = find_joint(root, "right_elbow")
    if right_elbow:
        base_transform = Mat4.from_translation(Vec3(0, -0.55, 0))
        anim_rotation = Mat4.from_rotation(math.sin(time * 3 + math.pi + math.pi/4) * 0.2, Vec3(1, 0, 0))
        right_elbow.local_transform = base_transform @ anim_rotation

def find_joint(root, name):
    """find joint based on given name"""
    if root.name == name:
        return root
    for child in root.children:
        result = find_joint(child, name)
        if result:
            return result
    return None