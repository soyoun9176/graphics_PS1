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

# joint overlap
OVERLAP_FACTOR = 1.15

# Arm
ARM_UPPER_LEN = 0.6
ARM_LOWER_LEN = 0.8
ARM_THICK = 0.15
SHOULDER_POS = Vec3(0.4, 0.7, 0.05)
SHOULDER_ROT_DEG = 40

# Leg
HIP_POS = Vec3(0.22, -0.6, 0.1)
LEG_THIGH_LEN = 0.6
LEG_CALF_LEN = 0.6
LEG_THICK = 0.18

# Foot&Hand
FOOT_SCALE = Vec3(0.26, 0.13, 0.36)
FOOT_MESH_POS = Vec3(0, -0.12, 0.14)
HAND_SCALE = Vec3(0.17, 0.17, 0.17)

# Z-axis offset
KNEE_OFFSET_Z = 0.05
FOOT_OFFSET_Z = 0.14
HAND_OFFSET_Z = 0.09

MAX_LEG_DROP = LEG_THIGH_LEN + LEG_CALF_LEN
TORSO_BASE_Y = abs(HIP_POS.y) + MAX_LEG_DROP + abs(FOOT_MESH_POS.y) + FOOT_SCALE.y


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
        self.speed = 0.7
        self.walk_target = None
        self.walk_direction = 1
        self.target_direction = None
        
        # Sound effects
        self.fart_sound_played = False
        try:
            self.fart_sound = pyglet.media.load('sounds/pungsound_cute.mp3', streaming=False)
        except Exception:
            self.fart_sound = None

        self.parts = []
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
        self.torso.base_transform = Mat4.from_translation(Vec3(0, TORSO_BASE_Y, 0))
        
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

        arm_leg_color = self.colors["arm_leg"]
        light_color = self.colors["light"]

        # Arms (Left & Right)
        for side, sign in [("left", -1), ("right", 1)]:
            # Shoulder
            shoulder = Joint(f"{side}_shoulder", parent=self.torso)
            shoulder.base_transform = Mat4.from_translation(Vec3(SHOULDER_POS.x * sign, SHOULDER_POS.y, SHOULDER_POS.z)) @ Mat4.from_rotation(math.radians(SHOULDER_ROT_DEG * sign), Vec3(0, 0, 1))
            upper_arm = Sphere(18, 18, 1.0)
            _solid_color(upper_arm, arm_leg_color)
            self.parts.append(Part(shoulder, upper_arm, Mat4.from_translation(Vec3(0, -ARM_UPPER_LEN / 2, 0)) @ Mat4.from_scale(Vec3(ARM_THICK, (ARM_UPPER_LEN / 2) * OVERLAP_FACTOR, ARM_THICK))))

            # Elbow
            elbow = Joint(f"{side}_elbow", parent=shoulder)
            elbow.base_transform = Mat4.from_translation(Vec3(0, -ARM_UPPER_LEN, 0))
            forearm = Sphere(18, 18, 1.0)
            _solid_color(forearm, arm_leg_color)
            self.parts.append(Part(elbow, forearm, Mat4.from_translation(Vec3(0, -ARM_LOWER_LEN / 2, 0)) @ Mat4.from_scale(Vec3(ARM_THICK*0.93, (ARM_LOWER_LEN / 2) * OVERLAP_FACTOR, ARM_THICK*0.93)) @ Mat4.from_rotation(math.radians(-10), Vec3(0, 0, 1))))

            # Hand
            hand = Joint(f"{side}_hand", parent=elbow)
            hand.base_transform = Mat4.from_translation(Vec3(0, -ARM_LOWER_LEN, HAND_OFFSET_Z))
            hand_mesh = Sphere(20, 20, 1.0)
            _solid_color(hand_mesh, light_color)
            self.parts.append(Part(hand, hand_mesh, Mat4.from_scale(HAND_SCALE)))

            if side == "left":
                self.left_shoulder, self.left_elbow, self.left_hand = shoulder, elbow, hand
            else:
                self.right_shoulder, self.right_elbow, self.right_hand = shoulder, elbow, hand

        body_color = self.colors["body"]
        dark_color = self.colors["dark"]

        # Legs (Left & Right)
        for side, sign in [("left", -1), ("right", 1)]:
            # Hip
            hip = Joint(f"{side}_hip", parent=self.torso)
            hip.base_transform = Mat4.from_translation(Vec3(HIP_POS.x * sign, HIP_POS.y, HIP_POS.z))
            thigh = Sphere(18, 18, 1.0)
            _solid_color(thigh, body_color)
            self.parts.append(Part(hip, thigh, Mat4.from_translation(Vec3(0, -LEG_THIGH_LEN / 2, 0)) @ Mat4.from_scale(Vec3(LEG_THICK, (LEG_THIGH_LEN / 2) * OVERLAP_FACTOR, LEG_THICK))))

            # Knee
            knee = Joint(f"{side}_knee", parent=hip)
            knee.base_transform = Mat4.from_translation(Vec3(0, -LEG_THIGH_LEN, KNEE_OFFSET_Z))
            shin = Sphere(18, 18, 1.0)
            _solid_color(shin, body_color)
            self.parts.append(Part(knee, shin, Mat4.from_translation(Vec3(0, -LEG_CALF_LEN * OVERLAP_FACTOR / 2, 0)) @ Mat4.from_scale(Vec3(LEG_THICK*0.85, (LEG_CALF_LEN / 2) * OVERLAP_FACTOR, LEG_THICK*0.85))))

            # Foot
            foot = Joint(f"{side}_foot", parent=knee)
            foot.base_transform = Mat4.from_translation(Vec3(0, -LEG_CALF_LEN, FOOT_OFFSET_Z))
            foot_mesh = Sphere(20, 20, 1.0)
            _solid_color(foot_mesh, dark_color)
            self.parts.append(Part(foot, foot_mesh, Mat4.from_translation(FOOT_MESH_POS) @ Mat4.from_scale(FOOT_SCALE)))

            if side == "left":
                self.left_hip, self.left_knee, self.left_foot = hip, knee, foot
            else:
                self.right_hip, self.right_knee, self.right_foot = hip, knee, foot

    def _build_head(self):
        self.head_base = Joint("head_base", parent=self.torso)
        self.head_base.base_transform = Mat4.from_translation(Vec3(0, 1.05, 0))
        self.head = Joint("placeholder_head", parent=self.head_base)
        self.head_eye_parts = {}
        self.head_alt_eye_parts = {}

    def _register_eyes(self, eye_parts, alt_eye_parts):
        self.head_eye_parts = eye_parts
        self.head_alt_eye_parts = alt_eye_parts
        self.eye_original_models = {k: v.local_model for k, v in eye_parts.items()}
        self.alt_eye_original_models = {k: v.local_model for k, v in alt_eye_parts.items()}
        for part in alt_eye_parts.values():
            part.local_model = Mat4.from_scale(Vec3(0, 0, 0))

    def _set_mouth_fart_eye_expression(self, use_alt):
        if not self.head_eye_parts or not self.head_alt_eye_parts: return
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
        if new_state != "mouth_fart": self._set_mouth_fart_eye_expression(False)
        if new_state == "walking": self.walk_last_time = None

    def update_animation(self, time):
        if self.state == "waving": self._wave_arms_animation(time)
        elif self.state == "walking": 
            if (self.walk_target):
                current_position = Vec3(self.root.world_transform[12], self.root.world_transform[13], self.root.world_transform[14])
                if (self.walk_target - current_position).length() < 0.1:
                    if self.target_direction: self.set_state("turning")
                    else: self.set_state("base_dance")
                    self.walk_target = None
                else: self.turn_twards(0.5 / 60 ,self.walk_target)
            self._walk_animation(time)
        elif self.state == "turning": self._turn()
        elif self.state == "idle": self._idle_animation(time)
        elif self.state == "mouth_fart": self._mouth_fart(time)
        elif self.state == "base_dance": self._base_dance(time)
    
    def update_target(self, target_pos: Vec3, target_direction : Vec3 = None):
        self.walk_target = target_pos
        self.target_direction = target_direction
        self.walk_direction = 1
        self.set_state("walking")

    # animations
    def _wave_arms_animation(self, time):
        """
        pungpung waves arms
        """
        dt = time - self.set_time
        self.left_shoulder.local_transform = (Mat4.from_translation(Vec3(-SHOULDER_POS.x, SHOULDER_POS.y - 0.1, SHOULDER_POS.z)) @ 
                                              Mat4.from_rotation(math.radians(-SHOULDER_ROT_DEG), Vec3(0, 0, 1)) @
                                              Mat4.from_rotation(math.sin(dt * 3) * 0.3, Vec3(1, 0, 0)))
        self.left_elbow.local_transform = (Mat4.from_translation(Vec3(0, -ARM_UPPER_LEN + 0.05, 0)) @
                                           Mat4.from_rotation(math.sin(dt * 3 + math.pi/4) * 0.2, Vec3(1, 0, 0)))
        
        self.right_shoulder.local_transform = (Mat4.from_translation(Vec3(SHOULDER_POS.x, SHOULDER_POS.y - 0.1, SHOULDER_POS.z)) @
                                               Mat4.from_rotation(math.radians(SHOULDER_ROT_DEG), Vec3(0, 0, 1)) @
                                               Mat4.from_rotation(math.sin(dt * 3 + math.pi) * 0.3, Vec3(1, 0, 0)))
        self.right_elbow.local_transform = (Mat4.from_translation(Vec3(0, -ARM_UPPER_LEN + 0.05, 0)) @
                                            Mat4.from_rotation(math.sin(dt * 3 + math.pi + math.pi/4) * 0.2, Vec3(1, 0, 0)))

    def _walk_animation(self, time):
        """
        pungpung walks
        """
        walk_speed = self.speed
        stride_time = (1.2 / walk_speed) * 0.7
        cycle = ((time - self.set_time) / stride_time) % 1.0
        phi = cycle * 2 * math.pi
        
        # legs swing
        def calc_leg_joints(phase_offset):
            p = (phi + phase_offset) % (2 * math.pi)
            hip = math.sin(p) * walk_speed
            knee = -math.sin(p) * 0.8 if math.sin(p) < 0 else math.sin(p) * 0.1 # knee only bends forward, TODO: appeal this on readme
            return hip, knee
        
        l_hip, l_knee = calc_leg_joints(0)
        self.left_hip.local_transform = self.left_hip.base_transform @ Mat4.from_rotation(l_hip, Vec3(1, 0, 0))
        self.left_knee.local_transform = self.left_knee.base_transform @ Mat4.from_rotation(l_knee, Vec3(1, 0, 0))
        
        r_hip, r_knee = calc_leg_joints(math.pi)
        self.right_hip.local_transform = self.right_hip.base_transform @ Mat4.from_rotation(r_hip, Vec3(1, 0, 0))
        self.right_knee.local_transform = self.right_knee.base_transform @ Mat4.from_rotation(r_knee, Vec3(1, 0, 0))

        # Arms swing
        swing = 0.4; elbow_flex = math.radians(-25); elbow_swing = math.radians(20)
        l_swing = -math.sin(phi)
        self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(l_swing * swing, Vec3(1, 0, 0))
        self.left_elbow.local_transform = self.left_elbow.base_transform @ Mat4.from_rotation(elbow_flex - (l_swing * elbow_swing), Vec3(1, 0, 0))
        
        r_swing = math.sin(phi)
        self.right_shoulder.local_transform = self.right_shoulder.base_transform @ Mat4.from_rotation(r_swing * swing, Vec3(1, 0, 0))
        self.right_elbow.local_transform = self.right_elbow.base_transform @ Mat4.from_rotation(elbow_flex - (r_swing * elbow_swing), Vec3(1, 0, 0))
        
        if self.walk_last_time is not None: 
            self.move_forward((time - self.walk_last_time) * walk_speed * 2 * self.walk_direction)
        self.walk_last_time = time

    def _idle_animation(self, time):
        """
        pungpung breathes
        """
        dt = time - self.set_time
        self.head.local_transform = self.head.base_transform @ Mat4.from_rotation(math.sin(dt * 2) * 0.05, Vec3(1, 0, 0)) # cute!! head nodding
        breath = 1.0 - math.sin(dt * 2) * 0.05
        self.breast.local_transform = self.breast.base_transform @ Mat4.from_scale(Vec3(breath, breath, breath))
        self.belly.local_transform = self.belly.base_transform @ Mat4.from_scale(Vec3(breath, breath, breath))
        spread = -math.sin(dt * 2) * 0.1
        self.left_shoulder.local_transform = self.left_shoulder.base_transform @ Mat4.from_rotation(-spread, Vec3(0, 0, 1))
        self.right_shoulder.local_transform = self.right_shoulder.base_transform @ Mat4.from_rotation(spread, Vec3(0, 0, 1))

    def _mouth_fart(self, time):
        """
        pungpung does mouth fart
        """
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
        """
        pungpung does base dance; bends knee, with his hand on his hip
        """
        theta = math.fabs(math.sin((time - self.set_time)*2))

        current_drop = MAX_LEG_DROP * math.cos(theta)
        current_torso_y = TORSO_BASE_Y - (MAX_LEG_DROP - current_drop)
        self.torso.local_transform = Mat4.from_translation(Vec3(0, current_torso_y, 0))

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

    def _turn(self):
        if self.target_direction is None:
            self.set_state("idle")
            return

        # current direction and new direction
        current_dir = self.get_forward_vector()
        c_dir_2d = Vec3(current_dir.x, 0, current_dir.z).normalize()
        t_dir_2d = Vec3(self.target_direction.x, 0, self.target_direction.z).normalize()

        turn_amount = 0.5 / 60.0

        # calculate angle -> if smaller than turn_amount no turn
        dot_val = max(-1.0, min(1.0, c_dir_2d.dot(t_dir_2d)))
        angle_diff = math.acos(dot_val)

        if angle_diff <= turn_amount:
            self.target_direction = None
            self.set_state("base_dance")
        else:
            target_coordinate = Vec3(self.root.world_transform[12], 
                                    self.root.world_transform[13], 
                                    self.root.world_transform[14])
            target_coordinate = target_coordinate + t_dir_2d
            self.turn_twards(turn_amount, target_coordinate)

class Pungpung(PungpungBase):
    def __init__(self):
        super().__init__(name="Pungpung")

    def _build_head(self):
        self.head_base = Joint("head_base", parent=self.torso)
        self.head_base.base_transform = Mat4.from_translation(Vec3(0, 1.05, 0))
        
        h_root, h_parts, h_eyes, h_alt_eyes = create_pungpung_head(self.head_base)
        self.head = h_root
        self.head.base_transform = Mat4()
        self.parts.extend(h_parts)
        
        self._register_eyes(h_eyes, h_alt_eyes)

def create_pungpung():
    p = Pungpung()
    return p.root, p.parts

class FriendPung(PungpungBase):
    """
    A simpler friend variation of Pungpung with custom features.
    """
    def __init__(self, name="FriendPung", body_color=(255, 200, 200, 255)):
        self.head_skin_color = (255, 224, 189, 255)  # 살색
        self.blush_pink = (255, 182, 193, 255)       # 핑크
        self.mouth_red = (255, 50, 50, 255)          # 빨강
        super().__init__(
                        name=name, 
                        body_color=body_color, 
                        arm_leg_color=(
                                        min(body_color[0], 255), 
                                        min(body_color[1], 255), 
                                        min(body_color[1], 255), 
                                        255
                                        )
                        )

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
