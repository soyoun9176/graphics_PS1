from pyglet.math import Mat4, Vec3


class Character:
    """
    Base class for all characters in the game world.
    Provides common interface for rendering and animation.
    """
    def __init__(self):
        self.root = None  # Root joint of the character
        self.parts = []   # List of Part objects for rendering
        self.name = "Character"  # Character name for identification

    def update_animation(self, time):
        """
        Update character animation based on time.
        Subclasses should override this method.
        """
        pass

    def update_world(self):
        """
        Update world transforms for all joints.
        """
        if self.root:
            self.root.update_world()

    def get_root_and_parts(self):
        """
        Return root joint and parts list for rendering.
        """
        return self.root, self.parts
    
    def get_forward_vector(self):
        if (self.root == None or self.root.local_transform == None) : return Vec3(0,1,0)
        forward = Vec3(self.root.local_transform[8], self.root.local_transform[9], self.root.local_transform[10])
        return forward.normalize()
    
    def move_forward(self, amount :float):
        self.root.local_transform = Mat4.from_translation(self.get_forward_vector() * amount) @ self.root.local_transform
        self.update_world()

    def get_camera_matrix(self):
        """
        Calculate a view matrix that looks at the character from behind and above.
        Uses the character's forward vector and root position.
        """
        if self.root is None:
            return Mat4()
            
        char_pos = Vec3(self.root.world_transform[12], self.root.world_transform[13], self.root.world_transform[14])
        
        forward = self.get_forward_vector()
        up = Vec3(0, 1, 0)
        
        distance_behind = 8.0
        height_above = 4.0
        
        eye = char_pos - (forward * distance_behind) + (up * height_above)
        
        target = char_pos + (up * 1.5)
        
        return Mat4.look_at(eye, target, up)