import math
from pyglet.math import Mat4, Vec3
from characters.rig import Joint, Part
from characters.primitives import Cube, Sphere

def _solid_color(primitive, color):
    vertex_count = len(primitive.vertices) // 3
    primitive.colors = tuple(color * vertex_count)

def create_head(parent_joint):
    parts = []
    
    # === colors ===
    semi_light_color = (255, 150, 20, 255)
    head_color = (255, 145, 15, 255)     # base orange
    nose_color = (255, 50, 50, 255)      # red
    eye_color = (30, 30, 30, 255)        # black
    pupil_color = (255, 255, 255, 255)   # white
    blush_color = (255, 215, 0, 255)     # yellow
    leaf_color = (34, 139, 34, 255)      # green
    mouth_color = (255, 255, 255, 255)   # white

    # head root
    head_root = Joint("head", parent=parent_joint)
    head_root.local_transform = Mat4()

    # head main
    head_main = Joint("head_main", parent=head_root)
    head_main_mesh = Sphere(32, 32, 1.0)
    _solid_color(head_main_mesh, semi_light_color)
    parts.append(Part(head_main, head_main_mesh, Mat4.from_scale(Vec3(0.5, 0.5, 0.5))))

    # 2. cheak (포동포동 볼따구 히히)
    head_cheeks = Joint("head_cheeks", parent=head_root)
    head_cheeks.local_transform = Mat4.from_translation(Vec3(0, -0.2, 0)) # 살짝 아래로
    head_cheeks_mesh = Sphere(32, 32, 1.0)
    _solid_color(head_cheeks_mesh, semi_light_color)
    parts.append(Part(head_cheeks, head_cheeks_mesh, Mat4.from_scale(Vec3(0.6, 0.4, 0.6))))

    # 3. nose
    nose = Joint("nose", parent=head_root)
    nose.local_transform = Mat4.from_translation(Vec3(0, -0.1, 0.57))
    nose_mesh = Sphere(16, 16, 1.0)
    _solid_color(nose_mesh, nose_color)
    parts.append(Part(nose, nose_mesh, Mat4.from_scale(Vec3(0.08, 0.08, 0.1))))

    # 4. eye
    # left eye
    eye_l = Joint("eye_l", parent=head_root)
    eye_l.local_transform = Mat4.from_translation(Vec3(-0.16, 0.08, 0.45))
    eye_l_mesh = Sphere(16, 16, 1.0)
    _solid_color(eye_l_mesh, eye_color)
    eye_l_part = Part(eye_l, eye_l_mesh, Mat4.from_scale(Vec3(0.06, 0.09, 0.04)))
    parts.append(eye_l_part)

    # left pupil
    pupil_l = Joint("pupil_l", parent=eye_l)
    pupil_l.local_transform = Mat4.from_translation(Vec3(0.02, 0.03, 0.03))
    pupil_l_mesh = Sphere(16, 16, 1.0)
    _solid_color(pupil_l_mesh, pupil_color)
    pupil_l_part = Part(pupil_l, pupil_l_mesh, Mat4.from_scale(Vec3(0.02, 0.02, 0.02)))
    parts.append(pupil_l_part)

    # right eye
    eye_r = Joint("eye_r", parent=head_root)
    eye_r.local_transform = Mat4.from_translation(Vec3(0.16, 0.08, 0.45))
    eye_r_mesh = Sphere(16, 16, 1.0)
    _solid_color(eye_r_mesh, eye_color)
    eye_r_part = Part(eye_r, eye_r_mesh, Mat4.from_scale(Vec3(0.06, 0.09, 0.04)))
    parts.append(eye_r_part)

    # right pupil
    pupil_r = Joint("pupil_r", parent=eye_r)
    pupil_r.local_transform = Mat4.from_translation(Vec3(0.02, 0.03, 0.03))
    pupil_r_mesh = Sphere(16, 16, 1.0)
    _solid_color(pupil_r_mesh, pupil_color)
    pupil_r_part = Part(pupil_r, pupil_r_mesh, Mat4.from_scale(Vec3(0.02, 0.02, 0.02)))
    parts.append(pupil_r_part)

    # alternate eyes for mouth fart expression (><) - using 4 cubes
    # Left eye: two cubes for \
    eye_fx_l1 = Joint("eye_fx_l1", parent=head_root)
    eye_fx_l1.local_transform = Mat4.from_translation(Vec3(-0.18, 0.15, 0.45))
    eye_fx_l1_mesh = Cube()
    _solid_color(eye_fx_l1_mesh, eye_color)
    eye_fx_l1_model = Mat4.from_rotation(math.radians(-45), Vec3(0, 0, 1)) @ Mat4.from_scale(Vec3(0.03, 0.08, 0.02))
    eye_fx_l1_part = Part(eye_fx_l1, eye_fx_l1_mesh, eye_fx_l1_model)
    parts.append(eye_fx_l1_part)

    eye_fx_l2 = Joint("eye_fx_l2", parent=head_root)
    eye_fx_l2.local_transform = Mat4.from_translation(Vec3(-0.14, 0.15, 0.45))
    eye_fx_l2_mesh = Cube()
    _solid_color(eye_fx_l2_mesh, eye_color)
    eye_fx_l2_model = Mat4.from_rotation(math.radians(45), Vec3(0, 0, 1)) @ Mat4.from_scale(Vec3(0.03, 0.08, 0.02))
    eye_fx_l2_part = Part(eye_fx_l2, eye_fx_l2_mesh, eye_fx_l2_model)
    parts.append(eye_fx_l2_part)

    # Right eye: two cubes for /
    eye_fx_r1 = Joint("eye_fx_r1", parent=head_root)
    eye_fx_r1.local_transform = Mat4.from_translation(Vec3(0.14, 0.15, 0.45))
    eye_fx_r1_mesh = Cube()
    _solid_color(eye_fx_r1_mesh, eye_color)
    eye_fx_r1_model = Mat4.from_rotation(math.radians(-45), Vec3(0, 0, 1)) @ Mat4.from_scale(Vec3(0.03, 0.08, 0.02))
    eye_fx_r1_part = Part(eye_fx_r1, eye_fx_r1_mesh, eye_fx_r1_model)
    parts.append(eye_fx_r1_part)

    eye_fx_r2 = Joint("eye_fx_r2", parent=head_root)
    eye_fx_r2.local_transform = Mat4.from_translation(Vec3(0.18, 0.15, 0.45))
    eye_fx_r2_mesh = Cube()
    _solid_color(eye_fx_r2_mesh, eye_color)
    eye_fx_r2_model = Mat4.from_rotation(math.radians(45), Vec3(0, 0, 1)) @ Mat4.from_scale(Vec3(0.03, 0.08, 0.02))
    eye_fx_r2_part = Part(eye_fx_r2, eye_fx_r2_mesh, eye_fx_r2_model)
    parts.append(eye_fx_r2_part)

    head_eye_parts = {
        "eye_l": eye_l_part,
        "pupil_l": pupil_l_part,
        "eye_r": eye_r_part,
        "pupil_r": pupil_r_part,
    }
    head_alt_eye_parts = {
        "alt_eye_l1": eye_fx_l1_part,
        "alt_eye_l2": eye_fx_l2_part,
        "alt_eye_r1": eye_fx_r1_part,
        "alt_eye_r2": eye_fx_r2_part,
    }

    # 5. blush
    blush_l = Joint("blush_l", parent=head_root)
    blush_l.local_transform = Mat4.from_translation(Vec3(-0.32, -0.05, 0.42)) @ Mat4.from_rotation(math.radians(-35), Vec3(0, 1, 0))
    blush_l_mesh = Sphere(16, 16, 1.0)
    _solid_color(blush_l_mesh, blush_color)
    parts.append(Part(blush_l, blush_l_mesh, Mat4.from_scale(Vec3(0.12, 0.06, 0.05))))

    blush_r = Joint("blush_r", parent=head_root)
    blush_r.local_transform = Mat4.from_translation(Vec3(0.32, -0.05, 0.42)) @ Mat4.from_rotation(math.radians(35), Vec3(0, 1, 0))
    blush_r_mesh = Sphere(16, 16, 1.0)
    _solid_color(blush_r_mesh, blush_color)
    parts.append(Part(blush_r, blush_r_mesh, Mat4.from_scale(Vec3(0.12, 0.06, 0.05))))

    # 6. gulggokji
    flower_root = Joint("flower_root", parent=head_root)
    flower_root.local_transform = Mat4.from_translation(Vec3(0, 0.50, 0)) 

    for i in range(5):
        leaf = Joint(f"leaf_{i}", parent=flower_root)
        
        angle = math.radians(i * (360 / 5))
        leaf.local_transform = Mat4.from_rotation(angle, Vec3(0, 1, 0)) @ Mat4.from_rotation(math.radians(20), Vec3(1, 0, 0))
        
        leaf_mesh = Sphere(16, 16, 1.0)
        _solid_color(leaf_mesh, leaf_color)
        
        leaf_model = Mat4.from_translation(Vec3(0, 0, 0.15)) @ Mat4.from_scale(Vec3(0.1, 0.08, 0.25))
        parts.append(Part(leaf, leaf_mesh, leaf_model))
    
    # 7. mouth
    mouth = Joint("mouth", parent=head_root)
    mouth.local_transform = Mat4.from_translation(Vec3(0, -0.23, 0.59))
    mouth_mesh = Sphere(16, 16, 1.0)
    _solid_color(mouth_mesh, mouth_color)
    parts.append(Part(mouth, mouth_mesh, Mat4.from_scale(Vec3(0.09, 0.04, 0.01))))
    

    return head_root, parts, head_eye_parts, head_alt_eye_parts
