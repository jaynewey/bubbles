from abc import ABC, abstractmethod

from ..particle import Particle


class EffectRenderer(ABC):
    """Generic class for rendering a ParticleEffect.
       Inherit from this class when writing your own renderers.
    """
    def __init__(self, base_size=32):
        self._textures = {}
        self._shapes = {}  # A set of key value pairs "shape_name":render_function
        self.base_size = base_size  # The base size of a particle before it is scaled

    def render_effect(self, particle_effect, surface):
        """Renders an entire particle effect onto a given surface.

        :param particle_effect: The particle effect to be rendered
        :type particle_effect: ParticleEffect
        :param surface: The surface on which the effect is drawn
        :return: None
        """
        for emitter in particle_effect.get_emitters():
            for particle in emitter.particles:
                position = (particle_effect.x + particle.x - (self.base_size * particle.scale) / 2,
                            particle_effect.y + particle.y - (self.base_size * particle.scale) / 2)
                self._render_particle(particle, surface, position)

    @abstractmethod
    def _render_particle(self, particle, surface, position):
        """Renders a single particle onto the surface at the given position.

        :param particle: The Particle instance you are rendering
        :type particle: Particle
        :param surface: The surface on which the particle is drawn
        :param position: The (x, y) position to draw the Particle at.
        :type position: tuple
        :return: None
        """
        pass

    @abstractmethod
    def _render_texture(self, particle):
        """Returns a surface with the texture rendered on it so that it can be drawn on the main surface.

        :param particle: The Particle to have its texture rendered
        :return: The surface with the texture rendered on it
        """
        pass

    @abstractmethod
    def _load_texture(self, filename):
        """Loads a texture into the correct format to be rendered by the system

        :param filename: The name of the texture file
        :type filename: str
        :return: The loaded texture in the format required
        """
        pass

    def register_effect(self, particle_effect):
        """Register a ParticleEffect with the renderer so that required textures are loaded.

        :param particle_effect: The ParticleEffect instance you want registered
        :type particle_effect: ParticleEffect
        :return: None
        """
        for emitter in particle_effect.get_emitters():
            if "shape" in emitter.particle_settings.keys():
                if not emitter.particle_settings["shape"] in self._shapes.keys():
                    if emitter.particle_settings["shape"] in Particle.sample_texture_map.keys():
                        relative_path = emitter.particle_settings["shape"]
                        absolute_path = Particle.sample_texture_map[emitter.particle_settings["shape"]]
                    else:
                        relative_path = absolute_path = emitter.particle_settings["shape"]
                    if absolute_path not in self._textures.keys():
                        self._textures[relative_path] = self._load_texture(absolute_path)

    def register_texture(self, texture_name, texture):
        """Manually register a texture with the renderer.
        Useful if you already have a texture loaded in memory.

        :param texture_name: The name that the particles reference this texture by.
        :type texture_name: str
        :param texture: The texture you want loaded.
        :return: None
        """
        self._textures[texture_name] = texture
