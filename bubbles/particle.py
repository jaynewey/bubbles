import math
from pathlib import Path


class Particle:
    """Class for representing an individual Particle."""

    # Some default particle textures for you
    sample_texture_map = {str(i.name): str(i) for i in (Path(__file__).parent / "textures").glob('**/*') if i.is_file()}

    def __init__(self):
        # Interpolation methods
        self.interpolation_methods = {
            "linear": self._linear_interpolate,
            "cosine": self._cosine_interpolate
        }

        self._current_frame = 0

        # Settable values
        self.lifetime = 30
        self.interpolation = "linear"

        self.x = 0
        self.x_speed = 0
        self._x_speed_points = None
        self.x_acceleration = 0
        self._x_acceleration_points = None

        self.y = 0
        self.y_speed = 0
        self._y_speed_points = None
        self.y_acceleration = 0
        self._y_acceleration_points = None

        self.scale = 1
        self._scale_points = None

        self.opacity = 1
        self._opacity_points = None

        self.rotation = 0
        self._rotation_points = None

        self.shape = "square"
        self.colourise = False

        self.red = 255
        self._red_points = None
        self.green = 255
        self._green_points = None
        self.blue = 255
        self._blue_points = None

    def update(self, deltatime):
        """Performs a single frame of updates to the particle.

        :return: None
        """
        self.x_acceleration += self._interpolate(self._x_acceleration_points)
        self.y_acceleration += self._interpolate(self._y_acceleration_points)
        self.x_speed += self._interpolate(self._x_speed_points) + self.x_acceleration
        self.y_speed += self._interpolate(self._y_speed_points) + self.y_acceleration
        self.x += self.x_speed * deltatime
        self.y += self.y_speed * deltatime

        self.scale += self._interpolate(self._scale_points)
        self.opacity += self._interpolate(self._opacity_points)
        self.rotation += self._interpolate(self._rotation_points)

        self.red += self._interpolate(self._red_points)
        self.green += self._interpolate(self._green_points)
        self.blue += self._interpolate(self._blue_points)

        self._current_frame += 1

    def is_dead(self):
        """Returns True if this Particle instance is dead, and therefore should be deleted.

        :return: Whether this Particle is dead or not
        :rtype: bool
        """
        return self._current_frame > self.lifetime

    def _interpolate(self, points):
        if points is None:
            return 0
        frames_per_point = self.lifetime // (len(points) - 1)
        current_point = int(self._current_frame / frames_per_point)
        y1 = points[current_point]
        y2 = points[current_point + 1] if current_point + 1 < len(points) else points[current_point]
        x1 = current_point * frames_per_point
        x2 = (current_point + 1) * frames_per_point
        return self.interpolation_methods[self.interpolation](y1, y2, x1, x2)

    @staticmethod
    def _linear_interpolate(y1, y2, x1, x2):
        return (y2 - y1) / (x2 - x1)

    def _cosine_interpolate(self, y1, y2, x1, x2):
        return ((y2 - y1) / (x2 - x1)) * (math.pi / 2) * math.sin((math.pi * (self._current_frame - x1)) / (x2 - x1))

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
                if type(settings[setting]) is list and len(settings[setting]) > 1:
                    particle.__dict__[setting] = settings[setting][0]
                    particle.__dict__["_" + setting + "_points"] = settings[setting]
                else:
                    particle.__dict__[setting] = settings[setting]
        return particle

    @property
    def colour(self):
        return self.red, self.green, self.blue
