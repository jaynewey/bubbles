import pygame

from .effect_renderer import EffectRenderer


class PygameEffectRenderer(EffectRenderer):
    def __init__(self, per_pixel_alpha=False, colorkey=(0, 0, 0), **kwargs):
        super().__init__(**kwargs)
        self._per_pixel_alpha = per_pixel_alpha
        self._colorkey = colorkey
        self._shapes = {
            "square": self._render_square,
            "circle": self._render_circle
        }

    def _render_particle(self, particle, surface, position):
        if particle.shape in self._shapes.keys():
            texture = self._shapes[particle.shape](particle)
        else:
            texture = self._render_texture(particle)
        if self._per_pixel_alpha:
            texture.fill((255, 255, 255, round(255 * particle.opacity)), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            texture.set_alpha(round(255 * particle.opacity))
        if particle.rotation != 0:
            texture = pygame.transform.rotate(texture, particle.rotation)
        surface.blit(texture, (position[0], position[1]))

    def _render_texture(self, particle):
        texture = self._textures[particle.shape].copy()
        width, height = texture.get_size()
        if particle.colourise:
            texture.fill(particle.colour, special_flags=pygame.BLEND_MULT)
        texture = pygame.transform.scale(texture, (round(width * particle.scale), round(height * particle.scale)))
        return texture

    def _load_texture(self, filename):
        if self._per_pixel_alpha:
            texture = pygame.image.load(filename).convert_alpha()
        else:
            texture = pygame.image.load(filename).convert()
            texture.set_colorkey(self._colorkey)
        return texture

    def _get_shape_surface(self, particle):
        size = round(self.base_size * particle.scale)
        texture = pygame.Surface((size, size))
        texture.set_colorkey(self._colorkey)
        return texture, size

    def _render_circle(self, particle):
        texture, size = self._get_shape_surface(particle)
        pygame.draw.circle(texture, particle.colour, (size // 2, size // 2),
                           size // 2)
        return texture

    def _render_square(self, particle):
        texture, size = self._get_shape_surface(particle)
        texture.fill(particle.colour)
        return texture
