from random import uniform

from .particle import Particle


class Emitter:
    """Class for spawning batches of particles."""
    def __init__(self):
        # Gets default settings from Particle
        self.particle_settings = {}
        # Specifies variable parameters
        self.particle_variation = {
            "lifetime": 0,
            "x_speed": 0,
            "y_speed": 0,
            "x_acceleration": 0,
            "y_acceleration": 0,
            "scale": 0,
            "opacity": 0,
            "rotation": 0,
            "red": 0,
            "green": 0,
            "blue": 0
        }

        self.particles = set()

        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

        self.spawns = -1
        self._current_spawn = 0

        self.frames = 30
        self._current_frame = 0

        self.max_particles = 1000
        self.spawn_amount = 10

    def update(self):
        """Updates the Emitter.

        :return: None
        """
        if self._current_frame == 0:
            self._spawn_batch()

        self._current_frame += 1
        self._current_frame %= self.frames

    def is_dead(self):
        """Returns True if this Emitter instance is dead, and therefore should be deleted or reset.

        :return: Whether this Emitter is dead or not
        :rtype: bool
        """
        return self._current_spawn > self.spawns != -1 and not self.particles

    def reset(self):
        """Resets the Emitter's spawn timeline back to the start so that it can be played again.

        :return: None
        """
        self._current_spawn = 0

    def _spawn_particle(self):
        """Creates a new Particle instance, based on the settings of the Emitter.

        :return: The generated Particle instance
        :rtype: Particle
        """
        values = {}

        for parameter, value in self.particle_settings.items():
            if parameter in self.particle_variation.keys():
                if type(value) is list:
                    values[parameter] = [uniform(base - variation, base + variation)
                                         for base, variation in zip(value, self.particle_variation[parameter])]
                else:
                    values[parameter] = uniform(value-self.particle_variation[parameter],
                                                value+self.particle_variation[parameter])
            else:
                values[parameter] = value
        values["x"] = uniform(self.x, self.x + self.width)
        values["y"] = uniform(self.y, self.y + self.height)

        return Particle.load_from_dict(values)

    def _spawn_batch(self):
        """Spawns a batch of Particle instances based on Emitter settings

        :return: None
        """
        if self.spawns != -1:
            self._current_spawn += 1
        if self._current_spawn <= self.spawns or self.spawns == -1:
            for particle in range(self.spawn_amount):
                if len(self.particles) < self.max_particles:
                    self.particles.add(self._spawn_particle())

    @staticmethod
    def load_from_dict(settings):
        """Instantiate and initialise a new Emitter instance with settings from a dictionary of parameters.

        :param settings: The correctly formatted settings dictionary
        :type settings: dict
        :return: The generated Emitter instance
        :rtype: Emitter
        """
        emitter = Emitter()
        for setting in settings.keys():
            if setting in emitter.__dict__.keys():
                emitter.__dict__[setting] = settings[setting]
        return emitter
