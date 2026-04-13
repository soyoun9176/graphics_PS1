from characters.character import Character

class World:
    """
    Manages characters and static objects in the world.
    """
    def __init__(self):
        self.characters = []
        self.static_objects = []

    def add_character(self, character: Character):
        """
        Add a character to the world.
        """
        if isinstance(character, Character):
            self.characters.append(character)
        else:
            raise TypeError("Only Character instances can be added via add_character")

    def add_static_object(self, obj):
        self.static_objects.append(obj)
        obj.update_world()

    def remove_character(self, character: Character):
        if character in self.characters:
            self.characters.remove(character)

    def remove_static_object(self, obj):
        if obj in self.static_objects:
            self.static_objects.remove(obj)

    def update_characters(self, time):
        """
        Update animation and world transforms for characters only.
        """
        for character in self.characters:
            character.update_animation(time)
            character.update_world()

    def get_all_characters_parts(self):
        """
        Returns a list of parts for all characters.
        """
        parts = []
        for character in self.characters:
            parts.extend(character.get_root_and_parts()[1])
        return parts

    def get_all_static_parts(self):
        """
        Returns a list of parts for all static objects.
        """
        parts = []
        for obj in self.static_objects:
            parts.extend(obj.get_root_and_parts()[1])
        return parts

    def get_character_by_name(self, name):
        """
        Get a character by name.
        """
        for character in self.characters:
            if character.name == name:
                return character
        return None

    def pungpung_friends_dance(self):
        pungpung = self.get_character_by_name("Pungpung")
        if pungpung == None : return
        names = ["Friend1", "Friend2", "Friend3", "Friend4"]
        friends = []
        for name in names:
            character = self.get_character_by_name(name)
            if (character == None) : return
            friends.append(character)
        
        friends_pos, friends_dirs = pungpung.get_friends_position_and_direction()

        def _start_moving(dt):
            for i in range(4):
                friends[i].update_target(friends_pos[i], friends_dirs[i])
        
        return _start_moving