import math

from characters.rig import Joint, Part
from pyglet.math import Mat4, Vec3
from characters.primitives import Cube, Sphere
from characters.pungpung_head import create_head


def _solid_color(primitive, color):
    vertex_count = len(primitive.vertices) // 3
    primitive.colors = tuple(color * vertex_count)


def create_pungpung():
    root = Joint("root")

    body_color = (255, 145, 15, 255)
    arm_leg_color = (255, 165, 0, 255)
    light_color = (255, 205, 115, 255)
    dark_color = (200, 90, 15, 255)
    eye_color = (40, 40, 40, 255)

    parts = []

    # Body
    torso = Joint("torso", parent=root)
    torso.local_transform = Mat4.from_translation(Vec3(0, 0.85, 0))
    torso_mesh = Sphere(32, 32, 1.0)
    _solid_color(torso_mesh, body_color)
    parts.append(Part(torso, torso_mesh, Mat4.from_scale(Vec3(0.65, 1.0, 0.65))))
    belly = Joint("belly", parent=torso)
    belly.local_transform = Mat4.from_translation(Vec3(0, -0.2, 0))
    belly_mesh = Sphere(32, 32, 1.0)
    _solid_color(belly_mesh, body_color)
    parts.append(Part(belly, belly_mesh, Mat4.from_scale(Vec3(0.8, 0.8, 0.8))))

    # Head & Face
    head_root, head_parts = create_head(torso)
    parts.extend(head_parts)

    # Left arm
    left_shoulder = Joint("left_shoulder", parent=torso)
    left_shoulder.local_transform = Mat4.from_translation(Vec3(-0.4, 0.6, 0.05)) @ Mat4.from_rotation(math.radians(-40), Vec3(0, 0, 1))
    upper_arm_left = Sphere(18, 18, 1.0)
    _solid_color(upper_arm_left, arm_leg_color)
    left_upper_model = Mat4.from_translation(Vec3(0, -0.31, 0)) @ Mat4.from_scale(Vec3(0.15, 0.31, 0.15))
    parts.append(Part(left_shoulder, upper_arm_left, left_upper_model))

    left_elbow = Joint("left_elbow", parent=left_shoulder)
    left_elbow.local_transform = Mat4.from_translation(Vec3(0, -0.55, 0))
    forearm_left = Sphere(18, 18, 1.0)
    _solid_color(forearm_left, arm_leg_color)
    left_forearm_model = Mat4.from_translation(Vec3(0, -0.29, 0)) @ Mat4.from_scale(Vec3(0.14, 0.29, 0.14)) @ Mat4.from_rotation(math.radians(-10), Vec3(0, 0, 1))
    parts.append(Part(left_elbow, forearm_left, left_forearm_model))

    left_hand = Joint("left_hand", parent=left_elbow)
    left_hand.local_transform = Mat4.from_translation(Vec3(0, -0.55, 0.09))
    hand_left = Sphere(20, 20, 1.0)
    _solid_color(hand_left, light_color)
    parts.append(Part(left_hand, hand_left, Mat4.from_scale(Vec3(0.17, 0.17, 0.17))))

    # Right arm
    right_shoulder = Joint("right_shoulder", parent=torso)
    right_shoulder.local_transform = Mat4.from_translation(Vec3(0.4, 0.6, 0.05)) @ Mat4.from_rotation(math.radians(40), Vec3(0, 0, 1))
    upper_arm_right = Sphere(18, 18, 1.0)
    _solid_color(upper_arm_right, arm_leg_color)
    right_upper_model = Mat4.from_translation(Vec3(0, -0.29, 0)) @ Mat4.from_scale(Vec3(0.15, 0.31, 0.15))
    parts.append(Part(right_shoulder, upper_arm_right, right_upper_model))

    right_elbow = Joint("right_elbow", parent=right_shoulder)
    right_elbow.local_transform = Mat4.from_translation(Vec3(0, -0.55, 0))
    forearm_right = Sphere(18, 18, 1.0)
    _solid_color(forearm_right, arm_leg_color)
    right_forearm_model = Mat4.from_translation(Vec3(0, -0.29, 0)) @ Mat4.from_scale(Vec3(0.14, 0.29, 0.14)) @ Mat4.from_rotation(math.radians(-10), Vec3(0, 0, 1))
    parts.append(Part(right_elbow, forearm_right, right_forearm_model))

    right_hand = Joint("right_hand", parent=right_elbow)
    right_hand.local_transform = Mat4.from_translation(Vec3(0, -0.55, 0.09))
    hand_right = Sphere(20, 20, 1.0)
    _solid_color(hand_right, light_color)
    parts.append(Part(right_hand, hand_right, Mat4.from_scale(Vec3(0.17, 0.17, 0.17))))

    # Left leg
    left_hip = Joint("left_hip", parent=torso)
    left_hip.local_transform = Mat4.from_translation(Vec3(-0.22, -0.15, 0.1))
    thigh_left = Sphere(18, 18, 1.0)
    _solid_color(thigh_left, body_color)
    parts.append(Part(left_hip, thigh_left, Mat4.from_translation(Vec3(0, -0.30, 0.08)) @ Mat4.from_scale(Vec3(0.15, 0.30, 0.15))))

    left_knee = Joint("left_knee", parent=left_hip)
    left_knee.local_transform = Mat4.from_translation(Vec3(0, -0.60, 0.05))
    shin_left = Sphere(18, 18, 1.0)
    _solid_color(shin_left, body_color)
    parts.append(Part(left_knee, shin_left, Mat4.from_translation(Vec3(0, -0.27, 0.08)) @ Mat4.from_scale(Vec3(0.14, 0.27, 0.14))))

    left_foot = Joint("left_foot", parent=left_knee)
    left_foot.local_transform = Mat4.from_translation(Vec3(0, -0.55, 0.14))
    foot_left = Sphere(20, 20, 1.0)
    _solid_color(foot_left, dark_color)
    parts.append(Part(left_foot, foot_left, Mat4.from_translation(Vec3(0, -0.12, 0.14)) @ Mat4.from_scale(Vec3(0.26, 0.13, 0.36))))

    # Right leg
    right_hip = Joint("right_hip", parent=torso)
    right_hip.local_transform = Mat4.from_translation(Vec3(0.22, -0.15, 0.1))
    thigh_right = Sphere(18, 18, 1.0)
    _solid_color(thigh_right, body_color)
    parts.append(Part(right_hip, thigh_right, Mat4.from_translation(Vec3(0, -0.30, 0.08)) @ Mat4.from_scale(Vec3(0.15, 0.30, 0.15))))

    right_knee = Joint("right_knee", parent=right_hip)
    right_knee.local_transform = Mat4.from_translation(Vec3(0, -0.60, 0.05))
    shin_right = Sphere(18, 18, 1.0)
    _solid_color(shin_right, body_color)
    parts.append(Part(right_knee, shin_right, Mat4.from_translation(Vec3(0, -0.27, 0.08)) @ Mat4.from_scale(Vec3(0.14, 0.27, 0.14))))

    right_foot = Joint("right_foot", parent=right_knee)
    right_foot.local_transform = Mat4.from_translation(Vec3(0, -0.55, 0.14))
    foot_right = Sphere(20, 20, 1.0)
    _solid_color(foot_right, dark_color)
    parts.append(Part(right_foot, foot_right, Mat4.from_translation(Vec3(0, -0.12, 0.14)) @ Mat4.from_scale(Vec3(0.26, 0.13, 0.36))))


    return root, parts
