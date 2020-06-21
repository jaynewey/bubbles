from .emitter import Emitter


class ParticleEffect:
    """Class for handling emitters and their particles, representing an entire effect."""
    def __init__(self):
        self._emitters = set()
        self._dead_emitters = set()

        self.x = 0
        self.x_speed = 0
        self.y = 0
        self.y_speed = 0

        self.loops = -1
        self._current_loop = 1

    def update(self, deltatime=1):
        """Performs a frame of updates to the effect, updating emitters and their particles.

        :param deltatime: Target fps / actual fps. To ensure that particles are framerate independent
        :type deltatime: float
        :return: None
        """
        self.x += self.x_speed * deltatime
        self.y += self.y_speed * deltatime

        for emitter in self._emitters:
            emitter.update()
            if emitter.is_dead():
                self._dead_emitters.add(emitter)

            dead_particles = set()
            for particle in emitter.particles:
                particle.update(deltatime)
                particle.x -= self.x_speed * deltatime
                particle.y -= self.y_speed * deltatime
                if particle.is_dead():
                    dead_particles.add(particle)

            # Purge dead particles and emitters
            for dead_particle in dead_particles:
                emitter.particles.remove(dead_particle)

        if len(self._dead_emitters) == len(self._emitters):
            if self._current_loop < self.loops or self.loops == -1:
                for dead_emitter in self._dead_emitters:
                    dead_emitter.reset()
                if self.loops != -1:
                    self._current_loop += 1
                self._dead_emitters.clear()

    def add_emitter(self, *emitters):
        """Adds a number of Emitter instances to this effect.

        :param emitters: The Emitter instance(s) you want to add
        :type emitters: Emitter
        :return: This ParticleEffect instance so that calls can be chained
        :rtype: ParticleEffect
        """
        for emitter in emitters:
            self._emitters.add(emitter)
        return self

    def get_emitters(self):
        """Gets the emitters that belong to this effect.

        :return: The emitters that belong to this particle effect
        :rtype: set
        """
        return self._emitters

    def set_pos(self, x, y):
        """Sets the position of this particle effect

        :param x: The new x position for the effect
        :param y: The new y position for the effect
        :return: This object so that calls can be chained
        :rtype: ParticleEffect
        """
        self.x, self.y = x, y
        return self

    def is_dead(self):
        """Returns True if this particle effect has ended. Use this to remove your particles after using them.

        :return: Whether this particle effect has ended or not
        :rtype: bool
        """
        return self._current_loop > self.loops != -1 and bool(self._emitters)

    @staticmethod
    def load_from_dict(settings):
        """Instantiate and initialise a new ParticleEffect instance with settings from a dictionary of parameters.

        :param settings: The correctly formatted settings dictionary
        :type settings: dict
        :return: The generated ParticleEffect instance
        :rtype: ParticleEffect
        """
        particle_effect = ParticleEffect()
        for setting in settings.keys():
            if setting == "emitters":
                for emitter in settings["emitters"]:
                    particle_effect.add_emitter(Emitter.load_from_dict(emitter))
            else:
                if setting in particle_effect.__dict__.keys():
                    particle_effect.__dict__[setting] = settings[setting]
        return particle_effect
