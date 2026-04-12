import math

from characters.rig import Joint, Part
from characters.character import Character
from pyglet.math import Mat4, Vec3
import pyglet
from characters.primitives import Cube, Sphere
from characters.pungpung_head import create_head


def _solid_color(primitive, color):
    vertex_count = len(primitive.vertices) // 3
    primitive.colors = tuple(color * vertex_count)


def create_pungpung():
    pungpung = Pungpung()
    return pungpung.root, pungpung.parts


class Pungpung(Character):
    def __init__(self):
        super().__init__()
        self.name = "Pungpung"
        self.state = "idle"  # Default to idle
        self.root = Joint("root")
        self.set_time = 0
        self.walk_last_time = None

        body_color = (255, 145, 15, 255)
        arm_leg_color = (255, 165, 0, 255)
        light_color = (255, 205, 115, 255)
        dark_color = (200, 90, 15, 255)

        self.parts = []

        # Body
        self.torso = Joint("torso", parent=self.root)
        self.torso.base_transform = Mat4.from_translation(Vec3(0, 1.85, 0))
        self.torso.local_transform = self.torso.base_transform
        
        self.belly = Joint("belly", parent=self.torso)
        self.belly.base_transform = Mat4.from_translation(Vec3(0, -0.2, 0))
        self.belly.local_transform = self.belly.base_transform
        belly_mesh = Sphere(32, 32, 1.0)
        _solid_color(belly_mesh, body_color)
        self.parts.append(Part(self.belly, belly_mesh, Mat4.from_scale(Vec3(0.75, 0.75, 0.75))))

        # Breast
        self.breast = Joint("breast", parent=self.torso)
        self.breast.base_transform = Mat4.from_translation(Vec3(0, 0, 0))
        self.breast.local_transform = self.breast.base_transform
        breast_mesh = Sphere(32, 32, 1.0)
        _solid_color(breast_mesh, body_color)
        self.parts.append(Part(self.breast, breast_mesh, Mat4.from_scale(Vec3(0.60, 1.0, 0.60))))

        # Head base
        self.head_base = Joint("head_base", parent=self.torso)
        self.head_base.base_transform = Mat4.from_translation(Vec3(0, 1.05, 0))
        self.head_base.local_transform = self.head_base.base_transform
        
        # Head & Face
        self.head_root, self.head_parts, self.head_eye_parts, self.head_alt_eye_parts = create_head(self.head_base)
        self.head = self.head_root
        self.head.base_transform = Mat4()
        self.head.local_transform = self.head.base_transform
        self.parts.extend(self.head_parts)

        self.eye_original_models = {
            "eye_l": self.head_eye_parts["eye_l"].local_model,
            "pupil_l": self.head_eye_parts["pupil_l"].local_model,
            "eye_r": self.head_eye_parts["eye_r"].local_model,
            "pupil_r": self.head_eye_parts["pupil_r"].local_model,
        }
        self.alt_eye_original_models = {
            "alt_eye_l1": self.head_alt_eye_parts["alt_eye_l1"].local_model,
            "alt_eye_l2": self.head_alt_eye_parts["alt_eye_l2"].local_model,
            "alt_eye_r1": self.head_alt_eye_parts["alt_eye_r1"].local_model,
            "alt_eye_r2": self.head_alt_eye_parts["alt_eye_r2"].local_model,
        }

        # Keep alternate eyes hidden until the timed mouth_fart window.
        for part in self.head_alt_eye_parts.values():
            part.local_model = Mat4.from_scale(Vec3(0, 0, 0))

        # Left arm # left for the user if the user faces pungpung
        self.left_shoulder = Joint("left_shoulder", parent=self.torso)
        self.left_shoulder.base_transform = Mat4.from_translation(Vec3(-0.4, 0.7, 0.05)) @ Mat4.from_rotation(math.radians(-40), Vec3(0, 0, 1))
        self.left_shoulder.local_transform = self.left_shoulder.base_transform
        upper_arm_left = Sphere(18, 18, 1.0)
        _solid_color(upper_arm_left, arm_leg_color)
        left_upper_model = Mat4.from_translation(Vec3(0, -0.34, 0)) @ Mat4.from_scale(Vec3(0.15, 0.37, 0.15))
        self.parts.append(Part(self.left_shoulder, upper_arm_left, left_upper_model))

        self.left_elbow = Joint("left_elbow", parent=self.left_shoulder)
        self.left_elbow.base_transform = Mat4.from_translation(Vec3(0, -0.6, 0))
        self.left_elbow.local_transform = self.left_elbow.base_transform
        forearm_left = Sphere(18, 18, 1.0)
        _solid_color(forearm_left, arm_leg_color)
        left_forearm_model = Mat4.from_translation(Vec3(0, -0.38, 0)) @ Mat4.from_scale(Vec3(0.14, 0.41, 0.14)) @ Mat4.from_rotation(math.radians(-10), Vec3(0, 0, 1))
        self.parts.append(Part(self.left_elbow, forearm_left, left_forearm_model))

        self.left_hand = Joint("left_hand", parent=self.left_elbow)
        self.left_hand.base_transform = Mat4.from_translation(Vec3(0, -0.8, 0.09))
        self.left_hand.local_transform = self.left_hand.base_transform
        hand_left = Sphere(20, 20, 1.0)
        _solid_color(hand_left, light_color)
        self.parts.append(Part(self.left_hand, hand_left, Mat4.from_scale(Vec3(0.17, 0.17, 0.17))))

        # Right arm
        self.right_shoulder = Joint("right_shoulder", parent=self.torso)
        self.right_shoulder.base_transform = Mat4.from_translation(Vec3(0.4, 0.7, 0.05)) @ Mat4.from_rotation(math.radians(40), Vec3(0, 0, 1))
        self.right_shoulder.local_transform = self.right_shoulder.base_transform
        upper_arm_right = Sphere(18, 18, 1.0)
        _solid_color(upper_arm_right, arm_leg_color)
        right_upper_model = Mat4.from_translation(Vec3(0, -0.34, 0)) @ Mat4.from_scale(Vec3(0.15, 0.37, 0.15))
        self.parts.append(Part(self.right_shoulder, upper_arm_right, right_upper_model))

        self.right_elbow = Joint("right_elbow", parent=self.right_shoulder)
        self.right_elbow.base_transform = Mat4.from_translation(Vec3(0, -0.6, 0))
        self.right_elbow.local_transform = self.right_elbow.base_transform
        forearm_right = Sphere(18, 18, 1.0)
        _solid_color(forearm_right, arm_leg_color)
        right_forearm_model = Mat4.from_translation(Vec3(0, -0.38, 0)) @ Mat4.from_scale(Vec3(0.14, 0.41, 0.14)) @ Mat4.from_rotation(math.radians(-10), Vec3(0, 0, 1))
        self.parts.append(Part(self.right_elbow, forearm_right, right_forearm_model))

        self.right_hand = Joint("right_hand", parent=self.right_elbow)
        self.right_hand.base_transform = Mat4.from_translation(Vec3(0, -0.8, 0.09))
        self.right_hand.local_transform = self.right_hand.base_transform
        hand_right = Sphere(20, 20, 1.0)
        _solid_color(hand_right, light_color)
        self.parts.append(Part(self.right_hand, hand_right, Mat4.from_scale(Vec3(0.17, 0.17, 0.17))))

        # Left leg
        self.left_hip = Joint("left_hip", parent=self.torso)
        self.left_hip.base_transform = Mat4.from_translation(Vec3(-0.22, -0.6, 0.1))
        self.left_hip.local_transform = self.left_hip.base_transform
        thigh_left = Sphere(18, 18, 1.0)
        _solid_color(thigh_left, body_color)
        self.parts.append(Part(self.left_hip, thigh_left, Mat4.from_translation(Vec3(0, -0.30, 0.08)) @ Mat4.from_scale(Vec3(0.2, 0.40, 0.2))))

        self.left_knee = Joint("left_knee", parent=self.left_hip)
        self.left_knee.base_transform = Mat4.from_translation(Vec3(0, -0.60, 0.05))
        self.left_knee.local_transform = self.left_knee.base_transform
        shin_left = Sphere(18, 18, 1.0)
        _solid_color(shin_left, body_color)
        self.parts.append(Part(self.left_knee, shin_left, Mat4.from_translation(Vec3(0, -0.27, 0.08)) @ Mat4.from_scale(Vec3(0.17, 0.27, 0.17))))

        self.left_foot = Joint("left_foot", parent=self.left_knee)
        self.left_foot.base_transform = Mat4.from_translation(Vec3(0, -0.50, 0.14))
        self.left_foot.local_transform = self.left_foot.base_transform
        foot_left = Sphere(20, 20, 1.0)
        _solid_color(foot_left, dark_color)
        self.parts.append(Part(self.left_foot, foot_left, Mat4.from_translation(Vec3(0, -0.12, 0.14)) @ Mat4.from_scale(Vec3(0.26, 0.13, 0.36))))

        # Right leg
        self.right_hip = Joint("right_hip", parent=self.torso)
        self.right_hip.base_transform = Mat4.from_translation(Vec3(0.22, -0.6, 0.1))
        self.right_hip.local_transform = self.right_hip.base_transform
        thigh_right = Sphere(18, 18, 1.0)
        _solid_color(thigh_right, body_color)
        self.parts.append(Part(self.right_hip, thigh_right, Mat4.from_translation(Vec3(0, -0.30, 0.08)) @ Mat4.from_scale(Vec3(0.2, 0.40, 0.2))))

        self.right_knee = Joint("right_knee", parent=self.right_hip)
        self.right_knee.base_transform = Mat4.from_translation(Vec3(0, -0.60, 0.05))
        self.right_knee.local_transform = self.right_knee.base_transform
        shin_right = Sphere(18, 18, 1.0)
        _solid_color(shin_right, body_color)
        self.parts.append(Part(self.right_knee, shin_right, Mat4.from_translation(Vec3(0, -0.27, 0.08)) @ Mat4.from_scale(Vec3(0.17, 0.27, 0.17))))

        self.right_foot = Joint("right_foot", parent=self.right_knee)
        self.right_foot.base_transform = Mat4.from_translation(Vec3(0, -0.50, 0.14))
        self.right_foot.local_transform = self.right_foot.base_transform
        foot_right = Sphere(20, 20, 1.0)
        _solid_color(foot_right, dark_color)
        self.parts.append(Part(self.right_foot, foot_right, Mat4.from_translation(Vec3(0, -0.12, 0.14)) @ Mat4.from_scale(Vec3(0.26, 0.13, 0.36))))

        self.root.update_world()
        self._reset_pose()

    def _set_mouth_fart_eye_expression(self, use_alt):
        """Toggle between normal eyes and cube-style mouth-fart eyes."""
        hidden_model = Mat4.from_scale(Vec3(0, 0, 0))  # Use scale 0 to hide parts
        for key, part in self.head_eye_parts.items():
            part.local_model = hidden_model if use_alt else self.eye_original_models[key]

        for key, part in self.head_alt_eye_parts.items():
            part.local_model = self.alt_eye_original_models[key] if use_alt else hidden_model

    def _reset_pose(self):
        """
        Reset all joints to their base transforms.
        """
        joints = [
            self.torso,
            self.belly,
            self.breast,
            self.head,
            self.left_shoulder,
            self.left_elbow,
            self.left_hand,
            self.right_shoulder,
            self.right_elbow,
            self.right_hand,
            self.left_hip,
            self.left_knee,
            self.left_foot,
            self.right_hip,
            self.right_knee,
            self.right_foot
        ]
        for joint in joints:
            if hasattr(joint, 'base_transform'):
                joint.local_transform = joint.base_transform

    def set_state(self, new_state):
        """
        Set the current animation state
        now supporting waving, walking, idle, and mouth fart
        """
        self._reset_pose()
        self.set_time = pyglet.clock.get_default().time()
        self.state = new_state

        if new_state != "mouth_fart":
            self._set_mouth_fart_eye_expression(False)
        if (new_state == "walking") : self.walk_last_time = None


    def update_animation(self, time):
        """
        Update pungpung's animation based on current state
        """
        if self.state == "waving":
            self._wave_arms_animation(time)
        elif self.state == "walking":
            self._walk_animation(time)
        elif self.state == "idle":
            self._idle_animation(time)
        elif self.state == "mouth_fart":
            self._mouth_fart(time)

    def _wave_arms_animation(self, time):
        """
        Arm waving animation
        """
        # left
        base_transform = Mat4.from_translation(Vec3(-0.4, 0.6, 0.05)) @ Mat4.from_rotation(math.radians(-40), Vec3(0, 0, 1))
        anim_rotation = Mat4.from_rotation(math.sin((time-self.set_time) * 3) * 0.3, Vec3(1, 0, 0))
        self.left_shoulder.local_transform = base_transform @ anim_rotation
        
        base_transform = Mat4.from_translation(Vec3(0, -0.55, 0))
        anim_rotation = Mat4.from_rotation(math.sin((time-self.set_time) * 3 + math.pi/4) * 0.2, Vec3(1, 0, 0))
        self.left_elbow.local_transform = base_transform @ anim_rotation
        
        # right
        base_transform = Mat4.from_translation(Vec3(0.4, 0.6, 0.05)) @ Mat4.from_rotation(math.radians(40), Vec3(0, 0, 1))
        anim_rotation = Mat4.from_rotation(math.sin((time-self.set_time) * 3 + math.pi) * 0.3, Vec3(1, 0, 0))
        self.right_shoulder.local_transform = base_transform @ anim_rotation
        
        base_transform = Mat4.from_translation(Vec3(0, -0.55, 0))
        anim_rotation = Mat4.from_rotation(math.sin((time-self.set_time) * 3 + math.pi + math.pi/4) * 0.2, Vec3(1, 0, 0))
        self.right_elbow.local_transform = base_transform @ anim_rotation


    def _walk_animation(self, time):
        """
        periodical modeling of walking
        """
        # periods
        stride_time = 1.2
        cycle = ((time - self.set_time) / stride_time) % 1.0
        phi = cycle * 2 * math.pi
        walk_speed = 0.35 

        # hip & knee
        def calc_leg_joints(phase_offset):
            p = (phi + phase_offset) % (2 * math.pi)
            hip = math.sin(p) * walk_speed
            if math.sin(p) < 0:
                knee = -math.sin(p) * 0.8  #앞
            else: 
                knee = math.sin(p) * 0.1  # 뒤
            return hip, knee

        l_hip, l_knee = calc_leg_joints(0)
        self.left_hip.local_transform = self.left_hip.base_transform @ Mat4.from_rotation(l_hip, Vec3(1, 0, 0))
        self.left_knee.local_transform = self.left_knee.base_transform @ Mat4.from_rotation(l_knee, Vec3(1, 0, 0))


        r_hip, r_knee = calc_leg_joints(math.pi)
        self.right_hip.local_transform = self.right_hip.base_transform @ Mat4.from_rotation(r_hip, Vec3(1, 0, 0))
        self.right_knee.local_transform = self.right_knee.base_transform @ Mat4.from_rotation(r_knee, Vec3(1, 0, 0))

        # Arm moving
        arm_swing_amp = 0.4
        elbow_base_flex = math.radians(-25)
        elbow_swing_amp = math.radians(20)

        l_arm_swing = -math.sin(phi) # amount left arm moved = amount right hip moved
        self.left_shoulder.local_transform = self.left_shoulder.base_transform @ \
                                             Mat4.from_rotation(l_arm_swing * arm_swing_amp, Vec3(1, 0, 0))
        
        l_elbow_rotation = elbow_base_flex - (l_arm_swing * elbow_swing_amp) # 팔꿈치 원래 구부러져 있음, 좀 더 구부렸다 폈다
        self.left_elbow.local_transform = self.left_elbow.base_transform @ \
                                          Mat4.from_rotation(l_elbow_rotation, Vec3(1, 0, 0))

        r_arm_swing = math.sin(phi)
        self.right_shoulder.local_transform = self.right_shoulder.base_transform @ \
                                              Mat4.from_rotation(r_arm_swing * arm_swing_amp, Vec3(1, 0, 0))
        
        r_elbow_rotation = elbow_base_flex - (r_arm_swing * elbow_swing_amp)
        self.right_elbow.local_transform = self.right_elbow.base_transform @ \
                                           Mat4.from_rotation(r_elbow_rotation, Vec3(1, 0, 0))
        
        if (self.walk_last_time != None):
            self.move_forward((time - self.walk_last_time) * walk_speed)
        self.walk_last_time = time
    
    def _idle_animation(self, time):
        """
        Idle animation (subtle head nodding, breast breathing, and arm spreading) **very cute!!!!!**
        """
        # Subtle head nodding
        head_nod_angle = math.sin((time-self.set_time) * 2) * 0.05  # Very small angle
        self.head.local_transform = self.head.base_transform @ Mat4.from_rotation(head_nod_angle, Vec3(1, 0, 0))
        
        # Subtle breast&belly breathing
        breath_scale = 1.0 - math.sin((time-self.set_time) * 2) * 0.05  # ±5% scale change
        self.breast.local_transform = self.breast.base_transform @ Mat4.from_scale(Vec3(breath_scale, breath_scale, breath_scale))
        self.belly.local_transform = self.belly.base_transform @ Mat4.from_scale(Vec3(breath_scale, breath_scale, breath_scale))
        
        # Subtle arm spreading/closing
        spread_angle = - math.sin((time-self.set_time) * 2) * 0.1  # ±0.15 radian (~9 degrees)
        self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(-spread_angle, Vec3(0, 0, 1))
        self.right_shoulder.local_transform = self.right_shoulder.base_transform @ Mat4.from_rotation(spread_angle, Vec3(0, 0, 1))

    def _mouth_fart(self, time):
        """
        Mouth fart animation
        """
        time_flewed = time - self.set_time
        show_alt_eyes = 2 <= time_flewed < 4
        self._set_mouth_fart_eye_expression(show_alt_eyes)

        if time_flewed < 2:
            ratio = time_flewed / 2
            self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(math.radians(-90 * ratio), Vec3(1, 0, 0))
            self.left_elbow.local_transform = self.left_elbow.base_transform @ Mat4.from_rotation(math.radians(-95 * ratio), Vec3(0.9, -0.55, 0))
        elif time_flewed < 4:
            self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(math.radians(-90), Vec3(1, 0, 0))
            self.left_elbow.local_transform = self.left_elbow.base_transform @ Mat4.from_rotation(math.radians(-95), Vec3(0.9, -0.55, 0))
        elif time_flewed < 6:
            ratio = (6 - time_flewed) / 2
            self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(math.radians(-90 * ratio), Vec3(1, 0, 0))
            self.left_elbow.local_transform = self.left_elbow.base_transform @ Mat4.from_rotation(math.radians(-95 * ratio), Vec3(0.9, -0.55, 0))
        else:
            self.set_state("idle")

