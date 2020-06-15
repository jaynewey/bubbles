# bubbles

A lightweight, flexible particle system written in Python.

## Examples

Here are some examples of simple particle effects with bubbles.

![Alt Text](https://media.giphy.com/media/H5wjqqavoLRy5JiEXh/giphy.gif)
![Alt Text](https://media.giphy.com/media/fxYWAMX1UC9RSmxdeO/giphy.gif)
![Alt Text](https://media.giphy.com/media/L0evOjJujJuDLSzuTa/giphy.gif)

You can find the .json for these in the examples folder.

## Usage

The easiest way to create particle effects with bubbles, is by specifying all your settings in a python `dict` and passing it into `ParticleEffect.load_from_dict()`. More details on how to structure this and parameters you can specify are below. This is useful as you can store your effect settings in .json files, load them into python as a dict:
 
 ```python
import json
with open("filename.json") as f:
    d = json.load(f)
```
 
...and straight into bubbles:
 
```python
particle_effect = ParticleEffect.load_from_dict(d)
```

You can then render a `ParticleEffect` using your own or one of the builtin `EffectRenderer` classes.

It is useful to note that when using `load_from_dict()` any parameters not specified in your dictionary will be remain as their default, meaning you need only specify parameters you want to change.

### Particle

Particles are the small, individual parts that make up a collective effect. `Emitter` instances are used to spawn them. Particles have the following default attributes that can be set with a `dict` like so:

```python
{	
    # How many frames the particle lives for
    "lifetime": 30,
    
    # The x posiiton of the particle relative to the effect
    "x": 0,
    "x_speed": 0,
    "x_acceleration": 0,
    
    # The y position of the particle relative to the effect
    "y": 0,
    "y_speed": 0,
    "y_acceleration": 0,
    
    # A multiplier of the size of the particle's shape. Generally <= 1, >= 0
    "scale": 1,
    "scale_end": 1,
    
    # How opaque the particle is
    "opacity": 1,
    "opacity_end": 1,
    
    # Rotation of the particle in degrees
    "rotation": 0,
    "rotation_end": 0,
    
    # The shape of the particle (renderer dependant). Can be a texture
    "shape": "square",  # The name of the shape (renderer dependent) or the path to your texture.
        
    # The RGB colour overlay of the particle
    "colourise": False,  # If the particle is a texture, whether the particle should be coloured or not
    "colour": [255, 255, 255],   
    "colour_end": [255, 255, 255]
}
```

Any parameters that have the suffix `_end` are, well, the end values of the parameter. For example if we have:

bubbles supports drawing of vector shapes, or using a texture instead. The default shape is square. The drawing of these shapes is renderer dependent however. All renderers should really have a square drawer as it is the default for particles. Refer to the `ÈffectRenderer` section to see renderers and whats shapes they can draw.

bubbles provides some sample textures which can be accessed using `Particle.sample_texture_map[texture_name]`. Have a look in `bubbles/textures` to see them.

```python
{
    "scale": 0,
    "scale_end": 1
}
```

The particle will start its life will a scale of 0, and linearly grow to a scale of 1 by the end of its lifetime.

At current, only linear transitions between start and end values are possible.

### Emitter

You would want some form of variation between these particles, and to actually spawn them. Use emitters for this. You can have multiple emitters per effect and place wherever you like relative to the effect. The following values are set by default.

```python
{
    # Position relative to the effect
    "x": 0,
    "y": 0,
    
    # The area in which particles can spawn, by default is a single point
    "width": 0,
    "height": 0,
    
    # How many spawn bursts the emitter performs, by default is infinite
    "spawns": -1,
    
    # How many particles are spawned with each spawn burst
    "spawn_amount": 10,
    
    # How many frames between each spawn burst
    "frames": 30,
    
    # The maximum number of particles spawned with this emitter that can live at once
    "max_particles": 1000,
    
    # What kind of particles to spawn
    "particle_settings": {},
    "particle_variation": {
        	# Only these parameters can be varied:
            "lifetime": 0,
            "x_speed": 0,
            "y_speed": 0,
            "x_acceleration": 0,
            "y_acceleration": 0,
            "scale": 0,
            "scale_end": 0,
            "opacity": 0,
            "opacity_end": 0,
            "rotation": 0,
            "rotation_end": 0,
        }
}
```

You want to tell the Emitter what kind of particles to spawn. You can set `particle_settings` as a dictionary with the particle attributes you want.

Particle variation specifies how varied you'd like the particles to be on a +- basis. For example, setting the `lifetime` in settings to 60 and the `lifetime` variation to 30 means that the lifetime of particles spawned by the emitter is between 30 and 90. Note you cannot vary colour (yet, anyway).

### ParticleEffect

Particle effects handle Emitters and Particles. You can specify an effect's emitters and the following attributes, the default being:

```python
{
    # Position of the entire effect relative to where it is drawn
    "x":0,
    "y":0,
    
    # How many loops of the effect until this effect is finished, by default is infinite
    "loops": -1,
    
    # The emitters that belong to the effect
    "emitters": []
}
```

This effect does nothing since there are no emitters and hence no particles to draw. The `emitters` array is here is a an array of emitter settings dictionaries.

### EffectRenderer

You need to actually render your effects to see them of course. Use an `EffectRenderer` for this. It is an abstract class you can inherit from to draw your effects onto any kind of surface. One builtin renderers comes with bubbles at present, and works with pygame surfaces, called `PygameEffectRenderer`.

You can use `render_effect(particle_effect, surface)` to render an entire particle effect onto a given surface.

However you might want to write your own for a specific purpose. In this case make a class and inherit from `EffectRenderer`, then implement all required methods in your renderer. There is annotation in `effect_renderer.py` to help with this.

##### base_size

The `base_size` constructor parameter is used for vector shape drawing. It determines the size in pixels of a particle when a particle's scale is 1.

#### PygameEffectRenderer

`PygameEffectRenderer` is a renderer built to render particle effects to pygame `Surface` objects for easy use with pygame.

If you want to use partial transparency with a texture you can do so by passing the optional parameter `per_pixel_alpha=True` in the constructor and using a pygame surface with the `pygame.SRCALPHA` flag. Note that this will make rendering somewhat slower though.

Something to note is any black (RGB=(0, 0, 0)) particles are transparent by default. If you want to use a texture that has black in it, change the colorkey using the optional parameter `colorkey` when constructing a `PygameEffectRenderer`. The built-in shapes and textures rely on the colorkey being black so only do this per your specific requirements.