from PIL import Image, ImageDraw, ImageChops

from .effect_renderer import EffectRenderer


class ImageEffectRenderer(EffectRenderer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._shapes = {
            "circle": self._render_circle,
            "square": self._render_square
        }

    def _render_particle(self, particle, surface, position):
        if particle.shape in self._shapes.keys():
            texture = self._shapes[particle.shape](particle)
        else:
            texture = self._render_texture(particle)
        surface.paste(texture, (round(position[0]), round(position[1])), texture)
        return surface

    def _render_texture(self, particle):
        texture = self._textures[particle.shape].copy()
        if particle.colourise:
            overlay = Image.new("RGBA", texture.size, tuple([round(i) for i in particle.colour]))
            texture = ImageChops.multiply(overlay, texture)
        size = round(self.base_size * particle.scale)
        texture = texture.rotate(particle.rotation, expand=True)
        texture = texture.resize((size, size), Image.NEAREST)
        texture = Image.blend(texture, Image.new("RGBA", texture.size, (0, 0, 0, 0)), particle.opacity)
        return texture

    def _load_texture(self, filename):
        return Image.open(filename)

    def _get_shape_surface(self, particle):
        size = round(self.base_size * particle.scale)
        return Image.new("RGBA", (size, size), (0, 0, 0, 0)), size

    def _render_circle(self, particle):
        texture, size = self._get_shape_surface(particle)
        draw = ImageDraw.Draw(texture, "RGBA")
        fill = tuple(round(i) for i in list(particle.colour)+[particle.opacity * 255])
        draw.ellipse([(0, 0), (size, size)], fill=fill)
        return texture

    def _render_square(self, particle):
        texture, size = self._get_shape_surface(particle)
        draw = ImageDraw.Draw(texture, "RGBA")
        fill = tuple(round(i) for i in list(particle.colour) + [particle.opacity * 255])
        draw.rectangle([(0, 0), (size, size)], fill=fill)
        texture = texture.rotate(particle.rotation, expand=True)
        return texture
