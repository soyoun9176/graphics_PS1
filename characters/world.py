from characters.character import Character

class World:
    """
    Manages multiple characters in the game world.
    Provides methods to add, remove, and update characters.
    """
    def __init__(self):
        self.characters = []  # List of Character objects

    def add_character(self, character: Character):
        """
        Add a character to the world.
        """
        if isinstance(character, Character):
            self.characters.append(character)
        else:
            raise TypeError("Only Character instances can be added to the world")

    def remove_character(self, character: Character):
        """
        Remove a character from the world.
        """
        if character in self.characters:
            self.characters.remove(character)

    def update_all(self, time):
        """
        Update all characters in the world.
        """
        for character in self.characters:
            character.update_animation(time)
            character.update_world()

    def get_all_roots_and_parts(self):
        """
        Get root joints and parts for all characters.
        Returns a list of (root, parts) tuples.
        """
        return [character.get_root_and_parts() for character in self.characters]

    def get_character_by_name(self, name):
        """
        Get a character by name.
        """
        for character in self.characters:
            if character.name == name:
                return character
        return None