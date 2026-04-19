---
title: Intro to Toolbag Custom Shaders
url: https://alain.xyz/blog/intro-toolbag-custom-shaders
author: Alain Galvan
published: '2021-06-03'
source_blog: Alain Galvan · Ray Tracing Driver Engineer at AMD
source_site: https://alain.xyz/
category: graphics
fetched: '2026-04-19'
---

Some artistic visions are hard to achieve without some level of engineering. Creating detailed characters and environments can benefit from using procedural materials to avoid visual repetition and speed up their design. Simulating natural phenomena like broken glass, water caustics [[Brinck et al. 2021]](https://alain.xyz#ref_brinck2021), newton's rings, or stylistic effects like volumetric hue shifting from Pixar's Soul requires some understanding of the fundamental design of a rendering system.

Let's discuss writing custom shaders with **Marmoset Toolbag 4**. We'll approach this from the perspective of rendering a raymarched scene, similar to what you might expect from a [ShaderToy](https://www.shadertoy.com/).

The goal here will be to use this raymarched scene as a *generated background* for our scene, but it's possible to take this a step further, such as [using a raymarched scene as an environment map](https://alain.xyz/research/realtime-celestial-rendering).

So the example we'll be using is an effect I made that was heavily inspired by the YouTube channel [MKBHD](https://www.youtube.com/user/marquesbrownlee).

The design here isn't too complicated, we use our own camera to ray march a scene of repeating spheres [[Quílez 2013]](https://alain.xyz#ref_inigo2013) that shift and move according to sinusoidal functions.

![Custom Subroutine Screenshot](../../assets/f783ab043ae8c543.jpg)


Every material in Toolbag can have a *Custom* subroutine attached to it, which can then use a shader file to execute your shader. Custom shaders are executed after all the other logic for rendering has occurred, and can be used to overload that logic with your own behavior.

If you want uniforms to be controllable within the material settings UI, expose a uniform with a comment describing that uniform with the following format:

```
// 🎨 Color
uniform vec3 uColor; //color name "My Color" default 0.5,0.5,0.5
// 🗃️ Dropdown
uniform int uDropdown; //name "My Dropdown" default 0 labels "Option 1" "Option 2" "Option 3"
// 🎚️ Slider
uniform float uSlider; //name "My Slider" default 1.0 min 0 max 10
```


Toolbag has a series of categorized executable steps called *Subroutines*. Each render pass of Toolbag can use a different set of subroutines, allowing toolbag to easily *permute the material shader* to match the needs of that render pass. [[Russell 2014]](https://alain.xyz#ref_russell2014)

![Material Settings Drawers](../../assets/a261cc54056c3c94.jpg)


You can actually see all subroutines you can overload with custom shaders, they're the drawers that make up the material settings, with the name of the subroutine on the right, and the currently active one on the left. You can also spot all the different subroutines over in the `runSubroutines(...)`

function in `<Your Toolbag Installation>/data/shader/mat/mat.frag`

and `<Your Toolbag Installation>/data/shader/mat/mat.comp`

for ray tracing specific subroutines. [Marmoset has a blog post that details each subroutine here](https://marmoset.co/posts/toolbag_custom_shaders/).

Nearly all Toolbag subroutines follow a simple interface where they accept one argument, the *shader state* `FragmentState`

, which stores relative information like eye direction, normals, etc. to be used across each subroutine in order.

So here's the full custom shader, basically, I'm feeding the output of the shader above to the albedo output, with a material's *Diffusion* subroutine set to unlit. The material is placed in an object covering the camera, a sphere with all normals pointing inward, and the signed distance field camera is set to match the camera in Toolbag.

```
#define DISTMARCH_STEPS 128
#define DISTMARCH_MAXDIST 256.
uniform vec3 uColor1; //color name "Color 1" default (14.0 / 255.0), (135.0 / 255.0), (163.0 / 255.0)
uniform vec3 uColor2; //color name "Color 2" default (11.0 / 255.0), (96.0 / 255.0), (178.0 / 255.0)
// 🌊 Distance Fields
float spheredf(vec3 pos, float r) { return length(pos) - r; }
float opRep(vec3 p, vec3 c)
{
// Modulus Repeat on XZ
vec3 spread = max(vec3(0.0, 0.0, 0.0), vec3(uCustomAnimationTime - 1.0,
uCustomAnimationTime - 1.0,
uCustomAnimationTime - 1.0));
vec3 q = mod(abs(p), c) - 0.5 * c;
q.y = p.y;
// Wave effect
float yy = sin(uCustomAnimationTime + .3 * p.x) +
cos(uCustomAnimationTime * .9 + .2 * p.z);
q += .5 * vec3(0.0, yy, 0.0);
return spheredf(q, .1);
}
vec2 scenedf(vec3 p)
{
p.y += max(2.0 / (uCustomAnimationTime + .001), 0.001);
vec2 obj = vec2(opRep(p, vec3(2.5, 2.5, 2.5)), p.y);
return obj;
}
vec3 distmarch(vec3 ro, vec3 rd, float maxd)
{
float epsilon = 0.001;
float dist = 10. * epsilon;
float t = 0.;
float material = -1.0;
float iterations = 0.;
for (int i = 0; i < DISTMARCH_STEPS; i++)
{
if (abs(dist) < epsilon || t > maxd) break;
// advance the distance of the last lookup
t += dist;
vec2 dfresult = scenedf(ro + t * rd);
dist = dfresult.x;
material = dfresult.y;
iterations++;
}
if (t > maxd)
{
iterations = -1.0;
}
return vec3(t, iterations, material);
}
void CustomAlbedo(inout FragmentState s)
{
vec2 uv = s.screenTexCoord;
uv.y = 1.0 - uv.y;
vec4 outColor = vec4(0., 0., 0., 0.);
// 🎥 Setup Camera
vec3 camOrigin = vec3(45.0, -32.0, 45.0);
vec3 camDir = normalize(-vertexEye);
// aspect ratio
vec2 st = uv.xy - .5;
st *= (float(screenCoord.y) / float(screenCoord.x));
// Perspective Transform
float fov = 3.142 * .625;
vec3 iu = vec3(0., 1., 0.);
vec3 iz = camDir;
vec3 ix = normalize(cross(iz, iu));
vec3 iy = cross(ix, iz);
vec3 dir = normalize(st.x * ix + st.y * iy + fov * iz);
// 🥁 Scene Marching
vec3 scenemarch = distmarch(camOrigin, dir, DISTMARCH_MAXDIST);
float sceneCol = 0.0;
sceneCol = clamp(sceneCol, 0.0, 1.0);
// 🌫️ Fog
if (scenemarch.x > 0.0001)
{
sceneCol = clamp(scenemarch.y, 0.,
mix(1.0, 0.0, smoothstep(10., 180., scenemarch.x)));
}
// 🖼️ Output
outColor.xyz = mix(uColor1, .95 * uColor2,
smoothstep(0.0, 1.0, scenemarch.z)) *
sceneCol;
outColor.a = sceneCol;
// Write to albedo/baseColor
s.albedo = outColor;
s.baseColor = outColor.xyz;
}
#ifdef Albedo
#undef Albedo
#endif
#define Albedo CustomAlbedo
```


Every installation of Marmoset Toolbag has examples of custom shaders that can be found in `<Your Toolbag Installation>/data/shader/mat/custom/`

.

Marmoset maintains a [library of user submitted custom shaders here](https://marmoset.co/toolbag/add-ons/).

For more information on writing Python add-ons in Toolbag, I wrote [a blog post here](https://alain.xyz/blog/marmoset-toolbag-python-intro).

| [Brinck et al. 2021] |
| [Quílez 2013] |
| [Russell 2014] |