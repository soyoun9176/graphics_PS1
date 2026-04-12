from pyglet.math import Mat4, Vec3

class Joint:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.local_transform = Mat4()
        self.world_transform = Mat4()
        
        if parent:
            parent.children.append(self)

    def update_world(self):
        if self.parent:
            self.world_transform = self.parent.world_transform @ self.local_transform
        else:
            self.world_transform = self.local_transform
        
        for child in self.children:
            child.update_world()

class Part:
    def __init__(self, joint, primitive, local_model=None):
        self.joint = joint
        self.primitive = primitive
        self.local_model = local_model if local_model is not None else Mat4()