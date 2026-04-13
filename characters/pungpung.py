from characters.pungpung_base import PungpungBase
import math
import pyglet
from characters.rig import Joint, Part
from characters.character import Character
from pyglet.math import Mat4, Vec3
from characters.primitives import Cube, Sphere
from characters.pungpung_head import create_pungpung_head

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
    
    def get_friends_position_and_direction(self):
        """
        get position and direction for friends dancing
        returns:
        friends_pos, friends_dirs : list of Vec3
        """
        pp_position = Vec3(self.root.world_transform[12], 
                        self.root.world_transform[13], 
                        self.root.world_transform[14])
        pp_right_direction = Vec3(self.root.world_transform[0], 
                        self.root.world_transform[1], 
                        self.root.world_transform[2]).normalize()
        pp_front_direction = Vec3(self.root.world_transform[8], 
                        self.root.world_transform[9], 
                        self.root.world_transform[10]).normalize()
        friend_position_offsets = [-4,-2,2,4]
        friends_pos = []
        friends_dirs = []
        
        for offset in friend_position_offsets:
            position = pp_position + (offset*pp_right_direction)
            friends_pos.append(position)
            friends_dirs.append(pp_front_direction)
        return friends_pos, friends_dirs



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
