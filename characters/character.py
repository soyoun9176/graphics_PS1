from characters.rig import Joint, Part

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