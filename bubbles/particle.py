from pathlib import Path


class Particle:
    """Class for representing an individual Particle."""

    # Some default particle textures for you
    sample_texture_map = {str(i.name): str(i) for i in (Path(__file__).parent / "textures").glob('**/*') if i.is_file()}

    def __init__(self):
        self._current_frame = 0

        # Settable values
        self.lifetime = 30
        self.x = 0
        self.x_speed = 0
        self.x_acceleration = 0
        self.y = 0
        self.y_speed = 0
        self.y_acceleration = 0
        self.scale = 1
        self.scale_end = 1
        self.opacity = 1
        self.opacity_end = 1
        self.rotation = 0
        self.rotation_end = 0
        self.shape = "circle"
        self.colourise = False
        self.colour = [255, 255, 255]
        self.colour_end = [255, 255, 255]

        self._scale_change = 0
        self._opacity_change = 0
        self._rotation_change = 0
        self._colour_change = [0, 0, 0]

    def update(self, deltatime):
        """Performs a single frame of updates to the particle.

        :return: None
        """
        self._current_frame += 1
        self.x_speed += self.x_acceleration
        self.y_speed += self.y_acceleration
        self.x += self.x_speed * deltatime
        self.y += self.y_speed * deltatime
        self.scale += self._scale_change
        self.opacity += self._opacity_change
        self.rotation += self._rotation_change
        for i in range(len(self.colour)):
            self.colour[i] += self._colour_change[i]

    def is_dead(self):
        """Returns True if this Particle instance is dead, and therefore should be deleted.

        :return: Whether this Particle is dead or not
        :rtype: bool
        """
        return self._current_frame > self.lifetime

    def _calculate_changes(self):
        """Calculates and sets the gradient of several parameters for use in the update function

        :return: None
        """
        self._scale_change = (self.scale_end - self.scale) / self.lifetime
        self._opacity_change = (self.opacity_end - self.opacity) / self.lifetime
        self._rotation_change = (self.rotation_end - self.rotation) / self.lifetime
        initial_colour = self.colour
        self.colour = [i for i in initial_colour]
        self._colour_change = [(self.colour_end[i] - initial_colour[i]) / self.lifetime
                               for i in range(len(initial_colour))]

    @staticmethod
    def load_from_dict(settings):
        """Instantiate and initialise a new Particle instance with settings from a dictionary of parameters.

        :param settings: The correctly formatted settings dictionary
        :type settings: dict
        :return: The generated Particle instance
        :rtype: Particle
        """
        particle = Particle()
        for setting in settings.keys():
            if setting in particle.__dict__.keys():
                particle.__dict__[setting] = settings[setting]
        particle._calculate_changes()
        return particle
