import math
import pyglet
from characters.rig import Joint, Part
from characters.character import Character
from pyglet.math import Mat4, Vec3
from characters.primitives import Cube, Sphere
from characters.pungpung_head import create_pungpung_head

def _solid_color(primitive, color):
    vertex_count = len(primitive.vertices) // 3
    primitive.colors = tuple(color * vertex_count)

class PungpungBase(Character):
    """
    Base class for Pungpung-like characters. 
    Handles common body structure, animations, and eye-toggling logic.
    """
    def __init__(self, name="PungpungBase", 
                 body_color=(255, 145, 15, 255), 
                 arm_leg_color=(255, 165, 0, 255), 
                 light_color=(255, 205, 115, 255), 
                 dark_color=(200, 90, 15, 255)):
        super().__init__()
        self.name = name
        self.state = "idle"
        self.root = Joint("root")
        self.set_time = pyglet.clock.get_default().time()
        self.walk_last_time = None
        
        # Sound effects
        self.fart_sound_played = False
        try:
            self.fart_sound = pyglet.media.load('sounds/pungsound_cute.mp3', streaming=False)
        except Exception:
            self.fart_sound = None

        self.parts = []
        
        # Colors
        self.colors = {
            "body": body_color,
            "arm_leg": arm_leg_color,
            "light": light_color,
            "dark": dark_color
        }

        self._build_body()
        self._build_head()
        
        self.root.update_world()
        self._reset_pose()

    def _build_body(self):
        # Body (Torso, Belly, Breast)
        self.torso = Joint("torso", parent=self.root)
        self.torso.base_transform = Mat4.from_translation(Vec3(0, 1.95, 0))
        
        self.belly = Joint("belly", parent=self.torso)
        self.belly.base_transform = Mat4.from_translation(Vec3(0, -0.2, 0))
        belly_mesh = Sphere(32, 32, 1.0)
        _solid_color(belly_mesh, self.colors["body"])
        self.parts.append(Part(self.belly, belly_mesh, Mat4.from_scale(Vec3(0.75, 0.75, 0.75))))

        self.breast = Joint("breast", parent=self.torso)
        self.breast.base_transform = Mat4.from_translation(Vec3(0, 0, 0))
        breast_mesh = Sphere(32, 32, 1.0)
        _solid_color(breast_mesh, self.colors["body"])
        self.parts.append(Part(self.breast, breast_mesh, Mat4.from_scale(Vec3(0.60, 1.0, 0.60))))

        # Arms
        arm_leg_color = self.colors["arm_leg"]
        light_color = self.colors["light"]
        
        # Left
        self.left_shoulder = Joint("left_shoulder", parent=self.torso)
        self.left_shoulder.base_transform = Mat4.from_translation(Vec3(-0.4, 0.7, 0.05)) @ Mat4.from_rotation(math.radians(-40), Vec3(0, 0, 1))
        upper_arm_l = Sphere(18, 18, 1.0)
        _solid_color(upper_arm_l, arm_leg_color)
        self.parts.append(Part(self.left_shoulder, upper_arm_l, Mat4.from_translation(Vec3(0, -0.34, 0)) @ Mat4.from_scale(Vec3(0.15, 0.37, 0.15))))

        self.left_elbow = Joint("left_elbow", parent=self.left_shoulder)
        self.left_elbow.base_transform = Mat4.from_translation(Vec3(0, -0.6, 0))
        forearm_l = Sphere(18, 18, 1.0)
        _solid_color(forearm_l, arm_leg_color)
        self.parts.append(Part(self.left_elbow, forearm_l, Mat4.from_translation(Vec3(0, -0.38, 0)) @ Mat4.from_scale(Vec3(0.14, 0.41, 0.14)) @ Mat4.from_rotation(math.radians(-10), Vec3(0, 0, 1))))

        self.left_hand = Joint("left_hand", parent=self.left_elbow)
        self.left_hand.base_transform = Mat4.from_translation(Vec3(0, -0.8, 0.09))
        hand_l = Sphere(20, 20, 1.0)
        _solid_color(hand_l, light_color)
        self.parts.append(Part(self.left_hand, hand_l, Mat4.from_scale(Vec3(0.17, 0.17, 0.17))))

        # Right
        self.right_shoulder = Joint("right_shoulder", parent=self.torso)
        self.right_shoulder.base_transform = Mat4.from_translation(Vec3(0.4, 0.7, 0.05)) @ Mat4.from_rotation(math.radians(40), Vec3(0, 0, 1))
        upper_arm_r = Sphere(18, 18, 1.0)
        _solid_color(upper_arm_r, arm_leg_color)
        self.parts.append(Part(self.right_shoulder, upper_arm_r, Mat4.from_translation(Vec3(0, -0.34, 0)) @ Mat4.from_scale(Vec3(0.15, 0.37, 0.15))))

        self.right_elbow = Joint("right_elbow", parent=self.right_shoulder)
        self.right_elbow.base_transform = Mat4.from_translation(Vec3(0, -0.6, 0))
        forearm_r = Sphere(18, 18, 1.0)
        _solid_color(forearm_r, arm_leg_color)
        self.parts.append(Part(self.right_elbow, forearm_r, Mat4.from_translation(Vec3(0, -0.38, 0)) @ Mat4.from_scale(Vec3(0.14, 0.41, 0.14)) @ Mat4.from_rotation(math.radians(-10), Vec3(0, 0, 1))))

        self.right_hand = Joint("right_hand", parent=self.right_elbow)
        self.right_hand.base_transform = Mat4.from_translation(Vec3(0, -0.8, 0.09))
        hand_r = Sphere(20, 20, 1.0)
        _solid_color(hand_r, light_color)
        self.parts.append(Part(self.right_hand, hand_r, Mat4.from_scale(Vec3(0.17, 0.17, 0.17))))

        # Legs
        body_color = self.colors["body"]
        dark_color = self.colors["dark"]

        # Left Leg
        self.left_hip = Joint("left_hip", parent=self.torso)
        self.left_hip.base_transform = Mat4.from_translation(Vec3(-0.22, -0.6, 0.1))
        thigh_l = Sphere(18, 18, 1.0)
        _solid_color(thigh_l, body_color)
        self.parts.append(Part(self.left_hip, thigh_l, Mat4.from_translation(Vec3(0, -0.30, 0.08)) @ Mat4.from_scale(Vec3(0.2, 0.40, 0.2))))

        self.left_knee = Joint("left_knee", parent=self.left_hip)
        self.left_knee.base_transform = Mat4.from_translation(Vec3(0, -0.60, 0.05))
        shin_l = Sphere(18, 18, 1.0)
        _solid_color(shin_l, body_color)
        self.parts.append(Part(self.left_knee, shin_l, Mat4.from_translation(Vec3(0, -0.35, 0.08)) @ Mat4.from_scale(Vec3(0.17, 0.35, 0.17))))

        self.left_foot = Joint("left_foot", parent=self.left_knee)
        self.left_foot.base_transform = Mat4.from_translation(Vec3(0, -0.60, 0.14))
        foot_l = Sphere(20, 20, 1.0)
        _solid_color(foot_l, dark_color)
        self.parts.append(Part(self.left_foot, foot_l, Mat4.from_translation(Vec3(0, -0.12, 0.14)) @ Mat4.from_scale(Vec3(0.26, 0.13, 0.36))))

        # Right Leg
        self.right_hip = Joint("right_hip", parent=self.torso)
        self.right_hip.base_transform = Mat4.from_translation(Vec3(0.22, -0.6, 0.1))
        thigh_r = Sphere(18, 18, 1.0)
        _solid_color(thigh_r, body_color)
        self.parts.append(Part(self.right_hip, thigh_r, Mat4.from_translation(Vec3(0, -0.30, 0.08)) @ Mat4.from_scale(Vec3(0.2, 0.40, 0.2))))

        self.right_knee = Joint("right_knee", parent=self.right_hip)
        self.right_knee.base_transform = Mat4.from_translation(Vec3(0, -0.60, 0.05))
        shin_r = Sphere(18, 18, 1.0)
        _solid_color(shin_r, body_color)
        self.parts.append(Part(self.right_knee, shin_r, Mat4.from_translation(Vec3(0, -0.35, 0.08)) @ Mat4.from_scale(Vec3(0.17, 0.35, 0.17))))

        self.right_foot = Joint("right_foot", parent=self.right_knee)
        self.right_foot.base_transform = Mat4.from_translation(Vec3(0, -0.60, 0.14))
        foot_r = Sphere(20, 20, 1.0)
        _solid_color(foot_r, dark_color)
        self.parts.append(Part(self.right_foot, foot_r, Mat4.from_translation(Vec3(0, -0.12, 0.14)) @ Mat4.from_scale(Vec3(0.26, 0.13, 0.36))))

    def _build_head(self):
        """Must be overridden by subclasses to build the specific head."""
        self.head_base = Joint("head_base", parent=self.torso)
        self.head_base.base_transform = Mat4.from_translation(Vec3(0, 1.05, 0))
        self.head = Joint("placeholder_head", parent=self.head_base)
        self.head_eye_parts = {}
        self.head_alt_eye_parts = {}

    def _register_eyes(self, eye_parts, alt_eye_parts):
        """Helper to register eyes for animation logic."""
        self.head_eye_parts = eye_parts
        self.head_alt_eye_parts = alt_eye_parts
        self.eye_original_models = {k: v.local_model for k, v in eye_parts.items()}
        self.alt_eye_original_models = {k: v.local_model for k, v in alt_eye_parts.items()}
        
        # Hide alternates by default
        for part in alt_eye_parts.values():
            part.local_model = Mat4.from_scale(Vec3(0, 0, 0))

    def _set_mouth_fart_eye_expression(self, use_alt):
        if not self.head_eye_parts or not self.head_alt_eye_parts:
            return
        hidden_model = Mat4.from_scale(Vec3(0, 0, 0))
        for key, part in self.head_eye_parts.items():
            part.local_model = hidden_model if use_alt else self.eye_original_models[key]
        for key, part in self.head_alt_eye_parts.items():
            part.local_model = self.alt_eye_original_models[key] if use_alt else hidden_model

    def _reset_pose(self):
        joints = [self.torso, self.belly, self.breast, self.head_base, self.head,
                  self.left_shoulder, self.left_elbow, self.left_hand,
                  self.right_shoulder, self.right_elbow, self.right_hand,
                  self.left_hip, self.left_knee, self.left_foot,
                  self.right_hip, self.right_knee, self.right_foot]
        for joint in joints:
            if hasattr(joint, 'base_transform'):
                joint.local_transform = joint.base_transform

    def set_state(self, new_state):
        self._reset_pose()
        self.set_time = pyglet.clock.get_default().time()
        self.state = new_state
        self.fart_sound_played = False
        if new_state != "mouth_fart":
            self._set_mouth_fart_eye_expression(False)
        if new_state == "walking":
            self.walk_last_time = None

    def update_animation(self, time):
        if self.state == "waving": self._wave_arms_animation(time)
        elif self.state == "walking": self._walk_animation(time)
        elif self.state == "idle": self._idle_animation(time)
        elif self.state == "mouth_fart": self._mouth_fart(time)
        elif self.state == "base_dance": self._base_dance(time)

    def _wave_arms_animation(self, time):
        dt = time - self.set_time
        # Use slightly safer access to joints
        self.left_shoulder.local_transform = (Mat4.from_translation(Vec3(-0.4, 0.6, 0.05)) @ 
                                              Mat4.from_rotation(math.radians(-40), Vec3(0, 0, 1)) @
                                              Mat4.from_rotation(math.sin(dt * 3) * 0.3, Vec3(1, 0, 0)))
        self.left_elbow.local_transform = (Mat4.from_translation(Vec3(0, -0.55, 0)) @
                                           Mat4.from_rotation(math.sin(dt * 3 + math.pi/4) * 0.2, Vec3(1, 0, 0)))
        self.right_shoulder.local_transform = (Mat4.from_translation(Vec3(0.4, 0.6, 0.05)) @
                                               Mat4.from_rotation(math.radians(40), Vec3(0, 0, 1)) @
                                               Mat4.from_rotation(math.sin(dt * 3 + math.pi) * 0.3, Vec3(1, 0, 0)))
        self.right_elbow.local_transform = (Mat4.from_translation(Vec3(0, -0.55, 0)) @
                                            Mat4.from_rotation(math.sin(dt * 3 + math.pi + math.pi/4) * 0.2, Vec3(1, 0, 0)))

    def _walk_animation(self, time):
        stride_time = 1.2
        cycle = ((time - self.set_time) / stride_time) % 1.0
        phi = cycle * 2 * math.pi
        walk_speed = 0.35
        def calc_leg_joints(phase_offset):
            p = (phi + phase_offset) % (2 * math.pi)
            hip = math.sin(p) * walk_speed
            knee = -math.sin(p) * 0.8 if math.sin(p) < 0 else math.sin(p) * 0.1
            return hip, knee
        l_hip, l_knee = calc_leg_joints(0)
        self.left_hip.local_transform = self.left_hip.base_transform @ Mat4.from_rotation(l_hip, Vec3(1, 0, 0))
        self.left_knee.local_transform = self.left_knee.base_transform @ Mat4.from_rotation(l_knee, Vec3(1, 0, 0))
        r_hip, r_knee = calc_leg_joints(math.pi)
        self.right_hip.local_transform = self.right_hip.base_transform @ Mat4.from_rotation(r_hip, Vec3(1, 0, 0))
        self.right_knee.local_transform = self.right_knee.base_transform @ Mat4.from_rotation(r_knee, Vec3(1, 0, 0))
        swing = 0.4; elbow_flex = math.radians(-25); elbow_swing = math.radians(20)
        l_swing = -math.sin(phi)
        self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(l_swing * swing, Vec3(1, 0, 0))
        self.left_elbow.local_transform = self.left_elbow.base_transform @ Mat4.from_rotation(elbow_flex - (l_swing * elbow_swing), Vec3(1, 0, 0))
        r_swing = math.sin(phi)
        self.right_shoulder.local_transform = self.right_shoulder.base_transform @ Mat4.from_rotation(r_swing * swing, Vec3(1, 0, 0))
        self.right_elbow.local_transform = self.right_elbow.base_transform @ Mat4.from_rotation(elbow_flex - (r_swing * elbow_swing), Vec3(1, 0, 0))
        if self.walk_last_time is not None: self.move_forward((time - self.walk_last_time) * walk_speed * 2)
        self.walk_last_time = time

    def _idle_animation(self, time):
        dt = time - self.set_time
        self.head.local_transform = self.head.base_transform @ Mat4.from_rotation(math.sin(dt * 2) * 0.05, Vec3(1, 0, 0))
        breath = 1.0 - math.sin(dt * 2) * 0.05
        self.breast.local_transform = self.breast.base_transform @ Mat4.from_scale(Vec3(breath, breath, breath))
        self.belly.local_transform = self.belly.base_transform @ Mat4.from_scale(Vec3(breath, breath, breath))
        spread = -math.sin(dt * 2) * 0.1
        self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(-spread, Vec3(0, 0, 1))
        self.right_shoulder.local_transform = self.right_shoulder.base_transform @ Mat4.from_rotation(spread, Vec3(0, 0, 1))

    def _mouth_fart(self, time):
        dt = time - self.set_time
        show_alt = 2 <= dt < 4
        self._set_mouth_fart_eye_expression(show_alt)
        if dt < 2:
            r = dt / 2
            self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(math.radians(-90 * r), Vec3(1, 0, 0))
            self.left_elbow.local_transform = self.left_elbow.base_transform @ Mat4.from_rotation(math.radians(-95 * r), Vec3(0.9, -0.55, 0))
        elif dt < 4:
            if not self.fart_sound_played and self.fart_sound:
                self.fart_sound.play()
                self.fart_sound_played = True
            self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(math.radians(-90), Vec3(1, 0, 0))
            self.left_elbow.local_transform = self.left_elbow.base_transform @ Mat4.from_rotation(math.radians(-95), Vec3(0.9, -0.55, 0))
        elif dt < 6:
            r = (6 - dt) / 2
            self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(math.radians(-90 * r), Vec3(1, 0, 0))
            self.left_elbow.local_transform = self.left_elbow.base_transform @ Mat4.from_rotation(math.radians(-95 * r), Vec3(0.9, -0.55, 0))
        else:
            self.set_state("idle")

    def _base_dance(self, time):
        theta = math.fabs(math.sin(time - self.set_time))
        self.torso.local_transform = Mat4.from_translation(Vec3(0, 0.85 + (math.cos(theta) * 1.19), 0))
        self.left_hip.local_transform = self.left_hip.base_transform @ Mat4.from_rotation(-theta, Vec3(1, 0, 0)) @ Mat4.from_translation(Vec3(-0.05, 0, 0))
        self.right_hip.local_transform = self.right_hip.base_transform @ Mat4.from_rotation(-theta, Vec3(1, 0, 0)) @ Mat4.from_translation(Vec3(0.05, 0, 0))
        self.left_knee.local_transform = self.left_knee.base_transform @ Mat4.from_rotation(2*theta, Vec3(1, 0, 0))
        self.right_knee.local_transform = self.right_knee.base_transform @ Mat4.from_rotation(2*theta, Vec3(1, 0, 0))
        self.left_foot.local_transform = self.left_foot.base_transform @ Mat4.from_rotation(-theta, Vec3(1, 0, 0))
        self.right_foot.local_transform = self.right_foot.base_transform @ Mat4.from_rotation(-theta, Vec3(1, 0, 0))
        self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(math.radians(-20), Vec3(0, 0, 1))
        self.right_shoulder.local_transform = self.right_shoulder.base_transform @ Mat4.from_rotation(math.radians(20), Vec3(0, 0, 1))
        self.left_elbow.local_transform = self.left_elbow.base_transform @ Mat4.from_rotation(math.radians(75), Vec3(0, 0, 1))
        self.right_elbow.local_transform = self.right_elbow.base_transform @ Mat4.from_rotation(math.radians(-75), Vec3(0, 0, 1))
        
        

class Pungpung(PungpungBase):
    def __init__(self):
        super().__init__(name="Pungpung")

    def _build_head(self):
        self.head_base = Joint("head_base", parent=self.torso)
        self.head_base.base_transform = Mat4.from_translation(Vec3(0, 1.05, 0))
        
        # Load specific head parts
        h_root, h_parts, h_eyes, h_alt_eyes = create_pungpung_head(self.head_base)
        self.head = h_root
        self.head.base_transform = Mat4()
        self.parts.extend(h_parts)
        
        # Register eyes for animation
        self._register_eyes(h_eyes, h_alt_eyes)

def create_pungpung():
    p = Pungpung()
    return p.root, p.parts

class FriendPung(PungpungBase):
    """
    A simpler friend variation of Pungpung with custom features.
    """
    def __init__(self, name="FriendPung", body_color=(255, 200, 200, 255)):
        # Feature colors as requested
        self.head_skin_color = (255, 224, 189, 255) # 살색
        self.blush_pink = (255, 182, 193, 255)       # 핑크
        self.mouth_red = (255, 50, 50, 255)          # 빨강
        super().__init__(name=name, body_color=body_color)

    def _build_head(self):
        self.head_base = Joint("head_base", parent=self.torso)
        self.head_base.base_transform = Mat4.from_translation(Vec3(0, 1.05, 0))
        
        from characters.pungpung_head import create_base_head
        h_root, h_parts, h_eyes, h_alt_eyes = create_base_head(
            self.head_base, 
            head_color=self.head_skin_color,
            blush_color=self.blush_pink,
            mouth_color=self.mouth_red
        )
        self.head = h_root
        self.head.base_transform = Mat4()
        self.parts.extend(h_parts)
        self._register_eyes(h_eyes, h_alt_eyes)
