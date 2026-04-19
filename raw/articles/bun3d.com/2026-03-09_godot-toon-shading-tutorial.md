---
title: Godot Toon Shading | Tutorial
url: http://bun3d.com/tutorials/shading/godot-toon-shading/
author: Binbun
published: '2026-03-09'
source_blog: Binbun3D
source_site: https://bun3d.com/
category: graphics
fetched: '2026-04-19'
---

One thing almost every game developer has at least come across is toon shading.

## What is toon shading[#](http://bun3d.com#what-is-toon-shading)

As the name suggests, toon shading aims for a car**toon**y shading instead of a realistic one.
Maybe that’s also why toon shading is a form of [Non-photorealistic rendering](https://en.wikipedia.org/wiki/Non-photorealistic_rendering).
It’s also known as cel shading.

There’s no * one true toon shading*, but usually you’ll see a few things:

- Hard shadows
- Defined rim light
- Clear highlights

*mentioned, but it’s less of a shading thing.*

**outlines**![toon shading](../../assets/3c1f3d98b162270d.png)

[NicholasSourd](https://commons.wikimedia.org/wiki/User:NicolasSourd)(

[CC BY 2.5](https://creativecommons.org/licenses/by/2.5/))

## Simple Method[#](http://bun3d.com#simple-method)

The simplest method for toon shading is to use Godot’s own **StandardMaterial3D**.

- Add the
**StandardMaterial3D**to object. - Open the material and switch it to
*toon mode*:**Shading > Diffuse Mode**to**Toon****Shading > Specular Mode**to**Toon**

- Drag the
**Roughness**of the material to`0.0`

**(Optional)**: Enable**Rim > Enabled**

![standard_toon](../../assets/8d0a4da250ab99f9.png)

Easy as that. A great benefit for this is you can use all the other things that come with **StandardMaterial3D**.

## Custom Shader[#](http://bun3d.com#custom-shader)

Of course we want full control, so we’ll go ahead and build our very own toon shader! But before we get to the good stuff we can add some color to our material.

```
shader_type spatial; // Since this is a 3D shader, it'll be spatial
uniform vec3 albedo : source_color; // We can set this in the editor
void fragment() {
ALBEDO = albedo;
}
void light() {
// This is what we'll be focusing on from now
}
```


### The `light()`

function[#](http://bun3d.com#the-light-function)

As a first example, instead of jumping directly to the toon shader, we’ll start with [lambertian lighting](https://en.wikipedia.org/wiki/Lambertian_reflectance).
You can read more about it from the link, but for our purposes it’s pretty much just **matte lighting without highlights**

```
void light() {
DIFFUSE_LIGHT += max(dot(NORMAL, LIGHT), 0.0) * ATTENUATION * LIGHT_COLOR / PI;
}
```


![lambertian](../../assets/aaf03beef0fc94a1.png)

There’s a lot happening here so let’s break it down:

`dot(NORMAL, LIGHT)`

is the**core**of our whole lighting`NORMAL`

is the**direction of the surface**,`LIGHT`

is the**direction of the light**- By using
`dot()`

we’re calculating the**angle**between`NORMAL`

and`LIGHT`

([the dot product](https://en.wikipedia.org/wiki/Dot_product)). - So when the light points towards the surface, the angle between the surface and the light is 180 degrees (which is PI in radians,
**that’s why we divide by**), which means the more the light points towards the surface, the higher the value`PI`

later

`max(dot(NORMAL, LIGHT), 0.0)`

simply means we choose which value is higher, so in practice it means our**light value can never be less than 0.0**`ATTENUATION`

represents how much the intensity of the light is reduced due to things like**distance**from the light source and**shadows from other objects**.`LIGHT_COLOR`

is pretty self explanatory. Colored lights wouldn’t work without it

The reason we add onto `DIFFUSE_LIGHT`

is because the `light()`

function runs **per-pixel** * per-light*, so if we just set it to our value
we’d override all the previously processed lights.

![ndotl](../../assets/d76ef6dfa32d754b.png)

### Hard Shadows[#](http://bun3d.com#hard-shadows)

For clarity, we’ll break down our previous `light()`

into multiple lines so we can work with individual values.
Then we can use the `step()`

function to get a hard edge for the shading.

```
void light() {
float light = max(dot(NORMAL, LIGHT), 0.0) * ATTENUATION;
light = step(0.1, light); // Here
vec3 diffuse = vec3(light) * LIGHT_COLOR / PI;
DIFFUSE_LIGHT += diffuse;
}
```


![stepped_light](../../assets/5ae14749f70da84f.png)

#### Multiple Steps[#](http://bun3d.com#multiple-steps)

We can go even further and instead of using `step()`

we can:

**Multiply**our`light`

by the amount of steps we want it to have.**Round**the value.**Divide**it with the amount of steps to scale the value back.

```
void light() {
float light = max(dot(NORMAL, LIGHT), 0.0) * ATTENUATION;
light = round(light * 4.0) / 4.0; // Here
vec3 diffuse = vec3(light) * LIGHT_COLOR / PI;
DIFFUSE_LIGHT += diffuse;
}
```


![multi_stepped_light](../../assets/46ec1bfbca039550.png)

### Rim light[#](http://bun3d.com#rim-light)

For rim light we can use the fresnel effect. We’ll write a seperate function for it:

```
float fresnel(vec3 normal, vec3 view)
{
return 1.0 - clamp(dot(normalize(normal), normalize(view)), 0.0, 1.0));
}
```


![fresnel](../../assets/82766c1c2c33d174.png)

- Again we use
`dot()`

, but this time to find the angle between the view direction and the surface`NORMAL`

- So when the surface points directly to us, the value is higher.

- Then we invert it by subtracting it from
**1.0**- So when the surface points directly to us, the value is
**0.0**

- So when the surface points directly to us, the value is

Next we can actually use it in our `light()`

function.

```
void light() {
float light = max(dot(NORMAL, LIGHT), 0.0) * ATTENUATION;
light = round(light * 4.0) / 4.0;
vec3 diffuse = vec3(light) * LIGHT_COLOR / PI;
DIFFUSE_LIGHT += diffuse;
float rim = fresnel(NORMAL, VIEW);
rim = step(0.7, rim);
rim *= light;
SPECULAR_LIGHT += vec3(rim) * LIGHT_COLOR / PI;
}
```


![rim_light](../../assets/b9fdbbeead4bc192.png)

- We get
`rim`

by using our`fresnel()`

**Step**it using`step()`

like we did with the shading earlier- We
**multiply**the`rim`

with our`light`

value so that the rim light is only visible in the lighter areas **Add**it to`SPECULAR_LIGHT`

instead of`DIFFUSE_LIGHT`

. Idk why but it feels more appropriate.

### Fake Specular highlights[#](http://bun3d.com#fake-specular-highlights)

We already used `SPECULAR_LIGHT`

here, but we haven’t added actual specular highlights yet. Let’s fix that!
To keep things a simple, we won’t actually implement * real specular highlights*. It’s a whole topic itself.

Instead we’ll simply implement fake specular highlights using the same method as we did with `diffuse`

.

```
void light() {
float light = max(dot(NORMAL, LIGHT), 0.0) * ATTENUATION;
light = round(light * 4.0) / 4.0;
vec3 diffuse = vec3(light) * LIGHT_COLOR / PI;
DIFFUSE_LIGHT += diffuse;
float rim = fresnel(NORMAL, VIEW);
rim = step(0.7, rim);
rim *= light;
SPECULAR_LIGHT += vec3(rim) * LIGHT_COLOR / PI;
float specular = max(dot(NORMAL, LIGHT), 0.0) * ATTENUATION;
SPECULAR_LIGHT += vec3(specular) * LIGHT_COLOR / PI;
}
```


![specular](../../assets/bb3632a9cc250e5f.png)

If you’d like to do actual specular highlights I suggest [looking here](https://github.com/RustyRoboticsBV/GodotStandardLightShader).

## Full Shader[#](http://bun3d.com#full-shader)

Here’s the full shader:

```
shader_type spatial;
uniform vec3 albedo : source_color;
void fragment() {
ALBEDO = albedo;
}
float fresnel(vec3 normal, vec3 view)
{
return 1.0 - clamp(dot(normalize(normal), normalize(view)), 0.0, 1.0));
}
void light() {
float light = max(dot(NORMAL, LIGHT), 0.0) * ATTENUATION;
light = round(light * 4.0) / 4.0;
vec3 diffuse = vec3(light) * LIGHT_COLOR / PI;
DIFFUSE_LIGHT += diffuse;
float rim = fresnel(NORMAL, VIEW);
rim = step(0.7, rim);
rim *= light;
SPECULAR_LIGHT += vec3(rim) * LIGHT_COLOR / PI;
float specular = max(dot(NORMAL, LIGHT), 0.0) * ATTENUATION;
SPECULAR_LIGHT += vec3(specular) * LIGHT_COLOR / PI;
}
```