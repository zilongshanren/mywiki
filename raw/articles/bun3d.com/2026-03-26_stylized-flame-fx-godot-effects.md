---
title: Stylized Flame FX | Godot Effects
url: http://bun3d.com/assets/vfx/godot_flame_fx/
author: Binbun
published: '2026-03-26'
source_blog: Binbun3D
source_site: https://bun3d.com/
category: graphics
fetched: '2026-04-19'
---

[Get Effects Here](https://binbun3d.itch.io/flame-fx)

Heat up your Godot 4.x game with these flaming effects! Perfect for ambience, campfires, torches, projectiles and even status effects. These effects are FIRE (sorry for that joke).

## Features[#](http://bun3d.com#features)

- Naturally flowing flames even when moved around.
- Easily control the shape using a Godot’s built in noise.
- Customizable colors, wobble, edge softness and more.
- Animations for turning flames on and off.
- Easy audio integration to animations.
- Overlay materials that can be added to any objects Material Overlay slot. (Demonstrated by our friend Suzanne the Monkey)

![flame_rotating](../../assets/48a4370a163dce48.gif)

## Usage[#](http://bun3d.com#usage)

### Importing Effects to Godot[#](http://bun3d.com#importing-effects-to-godot)

To import Flame FX to Godot, you can simply drag the provided `assets`

folder in your Godot project directory.

In the case you have other assets from me, it’s advised to override your existing `assets`

folder to merge this one with the others.
This is because some of my assets use some shared textures, shaders and scripts, so merging the folders prevents any conflicts and
overall keeps things simpler.

### Using Fire Effects[#](http://bun3d.com#using-fire-effects)

Fire particle effects can be found under `assets/BinbunVFX_Vol2/FlameFX/effects`

.

When imported into **Godot**, you can simply drag the `.tscn`

files from their respective folders to your scene.

### Using Overlay Materials[#](http://bun3d.com#using-overlay-materials)

Overlay materials can be found under `assets/BinbunVFX_Vol2/FlameFX/effects/overlays`


In addition to the fire particle effects, the pack also contains **fire overlay materials** that are meant to be assigned to any object in Godot
as an overlay, meaning it **won’t mess with any existing materials** on that object.

- Select the
**MeshInstance**you want to set on fire. - Under
**GeometryInstance3D > Geometry**you can find**Material Overlay**. - Drag the fire overlay material on the
**Material Overlay**slot and you’re done!

![Material Overlay](../../assets/55ebaa36e9d69fa0.png)

### Resizing Effects[#](http://bun3d.com#resizing-effects)

You have a few different options for changing the size of the effect

To increase the base scale of the emitted particles, you can change `Shape > flame_scale`

property.

![flame scale example](../../assets/d8c5d231c27bd992.png)

You can also make the flames of the fire effect go higher by increasing the `Particles > lifetime`

.

![flame lifetime example](../../assets/3a0e615277ce5062.png)

## It is **not** advised to use `Transform > Scale`


*advised to use*

**not**`Transform > Scale`

Most likely it won’t do anything except mess up the particles

### Wobble[#](http://bun3d.com#wobble)

Using the wobble properties you can give a nice wavy wobbly squiggly feel to the fire. It’s basically using a sine wave based on the y direction to distort the noise texture used in the flame effect.

You are able to increase `wobble_amount`

beyond the suggested range of **0 to 1.0**:

![wobble example](../../assets/c7494f30a76adad2.png)

With `wobble_frequency`

you can make that wobble more frequent, or in other words more tightly packed:

![wobble frequency example](../../assets/a80d7458f7255bd4.png)

### Removing the “Rate This Effect!” button[#](http://bun3d.com#removing-the-rate-this-effect-button)

If you find the “Rate This Effect!” button annoying, you’re absolutely free to remove it. It’s a new thing I’m trying out.

You can find the script for VFXFireBB in `assets/BinbunVFX_Vol2/FlameFX/script/VFXFireBB.gd`

. At the bottom of that script you might see something like this:

```
@export_tool_button("Rate This Effect!", "Favorites") var rate_asset_button : Callable:
get():
return func(): OS.shell_open("https://binbun3d.itch.io/flame-fx/rate")
```


Remove that and you’re free from the button.

## VFXFireBB[#](http://bun3d.com#vfxfirebb)

Fire effects come with a controller script for easy customizations in the inspector.

![VFXFireBB](../../assets/b97deb512c3ae35e.png)

### Color[#](http://bun3d.com#color)

| Property | Description |
|---|---|
`primary_color` | Controls what the color is at the core of the flames. |
`secondary_color` | Controls the color flames transition to at the top. |
`emission` | Emission of the effect. Essentially the brightness |
`color_curve` | The curve used in the transition between `primary_color` and `secondary_color` |

### Light[#](http://bun3d.com#light)

| Property | Description |
|---|---|
`light_color` | Color of the light emitted by the effect |
`light_energy` | Strength multiplier of the light. (
|

`light_indirect_energy`

[godot docs link](https://docs.godotengine.org/en/stable/classes/class_light3d.html#class-light3d-property-light-indirect-energy))`light_volumetric_fog_energy`

[godot docs link](https://docs.godotengine.org/en/stable/classes/class_light3d.html#class-light3d-property-light-volumetric-fog-energy))### Shape[#](http://bun3d.com#shape)

| Property | Description |
|---|---|
`noise_texture` | The noise texture that’s used for the shape of this effect. The entire effect is based on this noise texture, so the biggest changes can be achieved with it. Note that it is suggested to use a seamless texture (for Godot’s NoiseTexture you can enable `seamless` ) for best results. |
`noise_scale` | Value used to scale the `noise_texture` . Higher values make the noise more zoomed out. |
`noise_scroll` | The velocity at which the `noise_texture` moves. |
`flame_density` | Controls the density of the flames. Essentially controls the blending between `noise_texture` and a radial gradient within each particle |
`flame_scale` | Controls the size of meshes used in this effect. Use this to make your flames wider and bigger. |
`hide_core` | Hides an extra part at the root of the flame used to make the root of the flames look more stable. |

### Particles[#](http://bun3d.com#particles)

| Property | Description |
|---|---|
`particles_amount` | Amount of particles used by this effect. Since this effect samples the `noise_texture` using world coordinates, the amount of particles won’t have a big effect on the style of the flames. Increase this if the effect looks jittery. Turning it down a bit might give a slight performance boost. |
`lifetime` | Lifetime of the flame particles. Increasing this will make the flames go higher. |
`explosiveness` | Explosiveness of the flame particles. |

### Wobble[#](http://bun3d.com#wobble-1)

| Property | Description |
|---|---|
`wobble_amount` | How much the flames are distorted side to side. |
`wobble_frequency` | The frequency of wobble on the flames. Higher values results in a tighter wave |
`wobble_scroll` | How fast the wave used to wobble the flames moves along the flames. Negative values move it downward. |

### Transparency[#](http://bun3d.com#transparency)

| Property | Description | Type |
|---|---|---|
`edge_hardness` | Hardness of the edges of flames. Setting this to `1.0` might break the illusion of a continuous flame. | float |
`edge_position` | Position of the edge on the shape. Higher values can make the effect look smaller. | float |
`proximity_fade` | Enables proximity fade. Can be performance intensive, but will also prevent effect from looking like it’s clipping with surfaces. Happens before `edge_hardness` is calculated. | bool |
`proximity_fade_distance` | Distance of `proximity_fade` | float |

### Audio[#](http://bun3d.com#audio)

| Property | Description | Type |
|---|---|---|
`animate_volume` | When enabled, will fade audio based on VFXEmitterBB parameter `emitting` | bool |

Other audio properties are the same as [AudioStreamPlayer3D](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer3d.html).

## Questions[#](http://bun3d.com#questions)

### Can I use the effects in a commercial game?[#](http://bun3d.com#can-i-use-the-effects-in-a-commercial-game)

Yes. This pack is licensed under Creative Commons Zero, meaning you’re free to use it in a commercial game. For more information check the given license.txt file

### Do I have to mention Binbun3D?[#](http://bun3d.com#do-i-have-to-mention-binbun3d)

Nope, but it’s always appreciated!

### I want my game showcased by Binbun3D!!!!![#](../../assets/c3072e6d2d6d3cc5.img)

Hey that’s not a question… It’s a demand. Well lucky you I’d love to showcase games that use my assets! Send me a message on my socials and I’ll see what I can do!