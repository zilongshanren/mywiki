---
title: Validating physical light units
url: https://interplayoflight.wordpress.com/2020/04/19/validating-physical-light-units/
author: Kostas Anagnostou
published: '2020-04-19'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Recently I added support for physical light units to my toy engine, based on [Frostbite’s](https://seblagarde.files.wordpress.com/2015/07/course_notes_moving_frostbite_to_pbr_v32.pdf) and [Filament’s](https://google.github.io/filament/Filament.md.html) great guides. Switching to physical lights units allows one to use “real-world” light intensities (for example in lux and lumens), camera settings (eg aperture, shutter speed and ISO) as well as mix analytical and captured light sources (HDR environment maps) correctly.

![](../../assets/899d7fd90a445799.jpg)


![](../../assets/899d7fd90a445799.jpg)

One thing to ensure in the process of adding physical light unit support to a renderer is to add back the division by PI sometimes removed from the BRDFs for performance reasons. That division was either performed, on the CPU, to the light intensity or colour or not at all, as artists could implicitly apply it to the light intensity when tweaking the scene illumination (for example, by making the light ~3 times less intense to compensate). With physical light units though the light intensity has a real word reference, so it is not longer possible to tune it “by eye” to get the correct intensity level.

It is tempting to apply the division by PI to the light colour or intensity on the CPU in an attempt to avoid the multiplication in the shader, but this might upset other systems that use the light’s colour or intensity that don’t rely on a BRDF, such as volumetric fog. It is better to keep the division local to the BRDF to keep everything consistent and reduce opportunities for errors, ALU is cheap nowadays, especially when compared to texture instructions.

Back to the physical light units support, the visual result depends on a lot of factors: the actual light intensity, light attenuation, camera settings and I wanted some way to validate it to ensure its correctness. For this I tried using [Mitsuba](https://www.mitsuba-renderer.org/download.html), which seems to used in other renderers as well (both Frostbite and Filament mention that they use it for validation).

Mitsuba is an easy to use physically based pathtracer, using an [XML scene description](https://www.mitsuba-renderer.org/releases/current/documentation.pdf). It supports mesh loading and basic shapes like cubes and planes, a wide range of light types and a camera definition. I am not particularly fond of writing XML by hand so I added a quick and dirty XML exporter to my toy engine which goes through the scene and exports meshes, lights and the camera settings.

I started with a simple array of point lights. In the toy engine, the light intensities are set in lumens and converted to luminous intensity (candelas) before they are sent to the shader, as discussed in Frostbite’s guide. This is convenient as this is the light unit used in Mitsuba as well.

```
<emitter type = "point">
<point name = "position" x = "-7.100000" y = "1.000000" z = "-2.500000" />
<spectrum name = "intensity" value = "397.887360, 102.175262, 3.229814" />
</emitter>
```

A simple cube description looks like this:

```
<shape type = "cube">
<transform name = "toWorld">
<scale x = "0.125000" y = "4.000000" z = "7.500000" />
<translate x = "-7.500000" y = "4.000000" z = "-0.000000" />
<rotate x = "1" angle = "0.000000" />
<rotate y = "1" angle = "0.000000" />
<rotate z = "1" angle = "0.000000" />
</transform>
<bsdf type = "diffuse">
<rgb name = "diffuseReflectance" value = "0.500000, 0.500000, 0.500000" />
</bsdf>
</shape>
```

I am also using a diffuse only brdf with an albedo of (0.5, 0.5, 0.5) on all scene meshes.

Finally the camera description looks something like this:

```
<sensor type = "perspective">
<float name = "farClip" value = "200.000000" />
<float name = "nearClip" value = "0.100000" />
<float name = "fov" value = "45.000000" />
<string name = "fovAxis" value = "y" />
<transform name = "toWorld">
<lookat target = "0.000000, 1.000000, -0.000000" origin = "7.000000, 4.000000, -7.000000" up = "0.000000, 1.000000, 0.000000" />
</transform>
<sampler type = "ldsampler">
<integer name = "sampleCount" value = "16" />
</sampler>
<film type = "ldrfilm">
<integer name = "height" value = "720" />
<integer name = "width" value = "1280" />
<float name = "exposure" value = "-10.000000" />
<rfilter type = "gaussian" />
</film>
</sensor>
```

By default Mitsuba does not apply any tonemapping to the final radiance value, only the gamma correction, which is exactly what we want. Two more things worth pointing out, samplerCount sets the number of rays per pixel and the ldrfilm section defines the output image resolution and exposure. The exposure is set in EV100. Worth noting that Mitsuba uses that value to scale the resulting radiance by a factor of 2^(EV100) to bring it into displayable values. EV100 is set as negative in the “exposure” attribute so this is really 1.0/2^abs(EV100). If you are using Frostbite’s EV100 to exposure conversion: 1.0 / (1.2 * 2^EV100), you will need to adjust the exposure value specified in the XML as EV100 – log(1.2) to achieve the same result, else there will be a difference in the resulting image brightness.

Also, in the toy engine, I am using the attenuation profile described in the Frostbite documentation.

![](../../assets/e1cb292f64ecb062.png)

Light radii do not really exist in nature, it is a rendering optimisation, Mitsuba does not support them as well. In this instance I set a very large number (eg 20,000) in the toy renderer to emulate this.

One important thing to point out is to set the “integrator” used by Mitsuba to “direct” instead of “path”. Direct will not calculate secondary light bounces and the visual result will be closer to what you’d get in-game with analytical lights only and no GI.

Alright, ready for some visuals, with the resulting XML description, Mitsuba’s output is (for 128 rays/pixels)

![](../../assets/7fc1e5f17c77655e.png)


![](../../assets/7fc1e5f17c77655e.png)

And the toy renderer output is

![](../../assets/b6f5713c6081ac17.png)


![](../../assets/b6f5713c6081ac17.png)

The results are pretty close. Trying a slightly more complex scene with more lights and geometry in Mitsuba (for 128 rays/pixel):

![](../../assets/9b2599eb74c8645e.png)


![](../../assets/9b2599eb74c8645e.png)

The toy renderer version is:

![](../../assets/f860ce3f70ee702a.png)


![](../../assets/f860ce3f70ee702a.png)

Again, the results are quite close. In this instance I activated raytraced shadows in the toy engine as well.

One final test I made was to activate specular in both the toy engine and Mitsuba. For Mitsuba I used a “roughplastic” bsdf as described in [MJP’s blog post](https://mynameismjp.wordpress.com/2015/04/04/mitsuba-quick-start-guide/), with the GGX distribution. The 1.5 for Index of Refraction (IOR) corresponds to the 0.04 F0 value I am using for non metals in the toy renderer (check Sebastien Lagarde’s [blog post](https://seblagarde.wordpress.com/2013/04/29/memo-on-fresnel-equations/) for the conversion formula).

```
<bsdf type = "roughplastic">
<string name = "distribution" value = "ggx" />
<float name = "alpha" value = "0.200000" />
<rgb name = "diffuseReflectance" value = "0.500000, 0.500000, 0.500000" />
<float name = "intIOR" value = "1.5" />
</bsdf>
```

Mitsuba’s output for 128 rays/pixels is

![](../../assets/7147fd546b197639.png)


![](../../assets/7147fd546b197639.png)

While the real-time one is:

![](../../assets/d9b3518ae8d9838c.png)


![](../../assets/d9b3518ae8d9838c.png)

In overall the results are quite close, although there are some differences in the falloff and intensity of the specular highlight which probably have something to do with my implementation, worth investigating further.

Finally, a few more gotchas I found in the process of using Mitsuba to validate the physical light units: firstly, it is using a Y-up, right-hand coordinate system, which means that you will have to convert if you are using a left-hand one, by flipping for example the z-coordinate. Secondly, it supports simple geometric shapes like cubes like I mentioned about, worth noting though that the cube shape runs from [-1,-1,-1]->[1,1,1]. This is important to bear in mind when you are trying to reconstruct the in-game scene in Mitsuba, as slight differences in light-surface distance can lead to radically different visual results due to the attenuation function.

For reference, I am including the full XML scene I used for the validation.

```
<?xml version = '1.0' encoding = 'utf-8' ?>
<scene version = "0.5.0">
<integrator type = "direct" />
<shape type = "obj" id = "Scene_Mesh_0">
<string name = "filename" value = "Assets\Meshes\teapot.obj" />
<transform name = "toWorld">
<scale x = "0.300000" y = "0.300000" z = "0.300000" />
<translate x = "0.000000" y = "0.000000" z = "-3.000000" />
<rotate x = "1" angle = "0.000000" />
<rotate y = "1" angle = "0.000000" />
<rotate z = "1" angle = "0.000000" />
</transform>
<bsdf type = "roughplastic">
<string name = "distribution" value = "ggx" />
<float name = "alpha" value = "0.200000" />
<rgb name = "diffuseReflectance" value = "0.500000, 0.500000, 0.500000" />
<float name = "intIOR" value = "1.5" />
</bsdf>
</shape>
<shape type = "obj" id = "Scene_Mesh_1">
<string name = "filename" value = "Assets\Meshes\teapot.obj" />
<transform name = "toWorld">
<scale x = "0.300000" y = "0.300000" z = "0.300000" />
<translate x = "3.000000" y = "0.000000" z = "-0.000000" />
<rotate x = "1" angle = "0.000000" />
<rotate y = "1" angle = "0.000000" />
<rotate z = "1" angle = "0.000000" />
</transform>
<bsdf type = "roughplastic">
<string name = "distribution" value = "ggx" />
<float name = "alpha" value = "0.200000" />
<rgb name = "diffuseReflectance" value = "0.500000, 0.500000, 0.500000" />
<float name = "intIOR" value = "1.5" />
</bsdf>
</shape>
<shape type = "cube">
<transform name = "toWorld">
<scale x = "0.125000" y = "4.000000" z = "7.500000" />
<translate x = "-7.500000" y = "4.000000" z = "-0.000000" />
<rotate x = "1" angle = "0.000000" />
<rotate y = "1" angle = "0.000000" />
<rotate z = "1" angle = "0.000000" />
</transform>
<bsdf type = "roughplastic">
<string name = "distribution" value = "ggx" />
<float name = "alpha" value = "0.200000" />
<rgb name = "diffuseReflectance" value = "0.500000, 0.500000, 0.500000" />
<float name = "intIOR" value = "1.5" />
</bsdf>
</shape>
<shape type = "cube">
<transform name = "toWorld">
<scale x = "0.125000" y = "4.000000" z = "7.500000" />
<translate x = "7.500000" y = "4.000000" z = "-0.000000" />
<rotate x = "1" angle = "0.000000" />
<rotate y = "1" angle = "0.000000" />
<rotate z = "1" angle = "0.000000" />
</transform>
<bsdf type = "roughplastic">
<string name = "distribution" value = "ggx" />
<float name = "alpha" value = "0.200000" />
<rgb name = "diffuseReflectance" value = "0.500000, 0.500000, 0.500000" />
<float name = "intIOR" value = "1.5" />
</bsdf>
</shape>
<shape type = "cube">
<transform name = "toWorld">
<scale x = "7.500000" y = "4.000000" z = "0.125000" />
<translate x = "0.000000" y = "4.000000" z = "7.500000" />
<rotate x = "1" angle = "0.000000" />
<rotate y = "1" angle = "0.000000" />
<rotate z = "1" angle = "0.000000" />
</transform>
<bsdf type = "roughplastic">
<string name = "distribution" value = "ggx" />
<float name = "alpha" value = "0.200000" />
<rgb name = "diffuseReflectance" value = "0.500000, 0.500000, 0.500000" />
<float name = "intIOR" value = "1.5" />
</bsdf>
</shape>
<shape type = "cube">
<transform name = "toWorld">
<scale x = "7.500000" y = "4.000000" z = "0.125000" />
<translate x = "0.000000" y = "4.000000" z = "-7.500000" />
<rotate x = "1" angle = "0.000000" />
<rotate y = "1" angle = "0.000000" />
<rotate z = "1" angle = "0.000000" />
</transform>
<bsdf type = "roughplastic">
<string name = "distribution" value = "ggx" />
<float name = "alpha" value = "0.200000" />
<rgb name = "diffuseReflectance" value = "0.500000, 0.500000, 0.500000" />
<float name = "intIOR" value = "1.5" />
</bsdf>
</shape>
<shape type = "cube">
<transform name = "toWorld">
<scale x = "7.500000" y = "0.125000" z = "7.500000" />
<translate x = "5.000000" y = "8.000000" z = "-0.000000" />
<rotate x = "1" angle = "0.000000" />
<rotate y = "1" angle = "0.000000" />
<rotate z = "1" angle = "0.000000" />
</transform>
<bsdf type = "roughplastic">
<string name = "distribution" value = "ggx" />
<float name = "alpha" value = "0.200000" />
<rgb name = "diffuseReflectance" value = "0.500000, 0.500000, 0.500000" />
<float name = "intIOR" value = "1.5" />
</bsdf>
</shape>
<shape type = "cube">
<transform name = "toWorld">
<scale x = "7.500000" y = "0.025000" z = "7.500000" />
<translate x = "0.000000" y = "0.000000" z = "-0.000000" />
<rotate x = "1" angle = "0.000000" />
<rotate y = "1" angle = "0.000000" />
<rotate z = "1" angle = "0.000000" />
</transform>
<bsdf type = "roughplastic">
<string name = "distribution" value = "ggx" />
<float name = "alpha" value = "0.200000" />
<rgb name = "diffuseReflectance" value = "0.500000, 0.500000, 0.500000" />
<float name = "intIOR" value = "1.5" />
</bsdf>
</shape>
<emitter type = "point">
<point name = "position" x = "-5.000000" y = "0.500000" z = "5.000000" />
<spectrum name = "intensity" value = "397.887360, 314.446167, 250.422607" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-2.500000" y = "0.500000" z = "5.000000" />
<spectrum name = "intensity" value = "397.887360, 259.851288, 150.306030" />
</emitter>
<emitter type = "point">
<point name = "position" x = "0.000000" y = "0.500000" z = "5.000000" />
<spectrum name = "intensity" value = "397.887360, 189.927185, 60.864887" />
</emitter>
<emitter type = "point">
<point name = "position" x = "2.500000" y = "0.500000" z = "5.000000" />
<spectrum name = "intensity" value = "397.887360, 102.175262, 3.229814" />
</emitter>
<emitter type = "point">
<point name = "position" x = "5.000000" y = "0.500000" z = "5.000000" />
<spectrum name = "intensity" value = "397.887360, 3.438933, 0.000000" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-5.000000" y = "0.500000" z = "2.500000" />
<spectrum name = "intensity" value = "397.887360, 314.446167, 250.422607" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-2.500000" y = "0.500000" z = "2.500000" />
<spectrum name = "intensity" value = "397.887360, 259.851288, 150.306030" />
</emitter>
<emitter type = "point">
<point name = "position" x = "0.000000" y = "0.500000" z = "2.500000" />
<spectrum name = "intensity" value = "397.887360, 189.927185, 60.864887" />
</emitter>
<emitter type = "point">
<point name = "position" x = "2.500000" y = "0.500000" z = "2.500000" />
<spectrum name = "intensity" value = "397.887360, 102.175262, 3.229814" />
</emitter>
<emitter type = "point">
<point name = "position" x = "5.000000" y = "0.500000" z = "2.500000" />
<spectrum name = "intensity" value = "397.887360, 3.438933, 0.000000" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-5.000000" y = "0.500000" z = "-0.000000" />
<spectrum name = "intensity" value = "397.887360, 314.446167, 250.422607" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-2.500000" y = "0.500000" z = "-0.000000" />
<spectrum name = "intensity" value = "397.887360, 259.851288, 150.306030" />
</emitter>
<emitter type = "point">
<point name = "position" x = "0.000000" y = "0.500000" z = "-0.000000" />
<spectrum name = "intensity" value = "397.887360, 189.927185, 60.864887" />
</emitter>
<emitter type = "point">
<point name = "position" x = "2.500000" y = "0.500000" z = "-0.000000" />
<spectrum name = "intensity" value = "397.887360, 102.175262, 3.229814" />
</emitter>
<emitter type = "point">
<point name = "position" x = "5.000000" y = "0.500000" z = "-0.000000" />
<spectrum name = "intensity" value = "397.887360, 3.438933, 0.000000" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-5.000000" y = "0.500000" z = "-2.500000" />
<spectrum name = "intensity" value = "397.887360, 314.446167, 250.422607" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-2.500000" y = "0.500000" z = "-2.500000" />
<spectrum name = "intensity" value = "397.887360, 259.851288, 150.306030" />
</emitter>
<emitter type = "point">
<point name = "position" x = "0.000000" y = "0.500000" z = "-2.500000" />
<spectrum name = "intensity" value = "397.887360, 189.927185, 60.864887" />
</emitter>
<emitter type = "point">
<point name = "position" x = "2.500000" y = "0.500000" z = "-2.500000" />
<spectrum name = "intensity" value = "397.887360, 102.175262, 3.229814" />
</emitter>
<emitter type = "point">
<point name = "position" x = "5.000000" y = "0.500000" z = "-2.500000" />
<spectrum name = "intensity" value = "397.887360, 3.438933, 0.000000" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-5.000000" y = "0.500000" z = "-5.000000" />
<spectrum name = "intensity" value = "397.887360, 314.446167, 250.422607" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-2.500000" y = "0.500000" z = "-5.000000" />
<spectrum name = "intensity" value = "397.887360, 259.851288, 150.306030" />
</emitter>
<emitter type = "point">
<point name = "position" x = "0.000000" y = "0.500000" z = "-5.000000" />
<spectrum name = "intensity" value = "397.887360, 189.927185, 60.864887" />
</emitter>
<emitter type = "point">
<point name = "position" x = "2.500000" y = "0.500000" z = "-5.000000" />
<spectrum name = "intensity" value = "397.887360, 102.175262, 3.229814" />
</emitter>
<emitter type = "point">
<point name = "position" x = "5.000000" y = "0.500000" z = "-5.000000" />
<spectrum name = "intensity" value = "397.887360, 3.438933, 0.000000" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-5.000000" y = "1.000000" z = "7.100000" />
<spectrum name = "intensity" value = "397.887360, 314.446167, 250.422607" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-2.500000" y = "1.000000" z = "7.100000" />
<spectrum name = "intensity" value = "397.887360, 259.851288, 150.306030" />
</emitter>
<emitter type = "point">
<point name = "position" x = "0.000000" y = "1.000000" z = "7.100000" />
<spectrum name = "intensity" value = "397.887360, 189.927185, 60.864887" />
</emitter>
<emitter type = "point">
<point name = "position" x = "2.500000" y = "1.000000" z = "7.100000" />
<spectrum name = "intensity" value = "397.887360, 102.175262, 3.229814" />
</emitter>
<emitter type = "point">
<point name = "position" x = "5.000000" y = "1.000000" z = "7.100000" />
<spectrum name = "intensity" value = "397.887360, 3.438933, 0.000000" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-7.100000" y = "1.000000" z = "5.000000" />
<spectrum name = "intensity" value = "397.887360, 314.446167, 250.422607" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-7.100000" y = "1.000000" z = "2.500000" />
<spectrum name = "intensity" value = "397.887360, 259.851288, 150.306030" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-7.100000" y = "1.000000" z = "-0.000000" />
<spectrum name = "intensity" value = "397.887360, 189.927185, 60.864887" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-7.100000" y = "1.000000" z = "-2.500000" />
<spectrum name = "intensity" value = "397.887360, 102.175262, 3.229814" />
</emitter>
<emitter type = "point">
<point name = "position" x = "-7.100000" y = "1.000000" z = "-5.000000" />
<spectrum name = "intensity" value = "397.887360, 3.438933, 0.000000" />
</emitter>
<sensor type = "perspective">
<float name = "farClip" value = "200.000000" />
<float name = "nearClip" value = "0.100000" />
<float name = "fov" value = "45.000000" />
<string name = "fovAxis" value = "y" />
<transform name = "toWorld">
<lookat target = "0.000000, 1.000000, -0.000000" origin = "7.000000, 4.000000, -7.000000" up = "0.000000, 1.000000, 0.000000" />
</transform>
<sampler type = "ldsampler">
<integer name = "sampleCount" value = "128" />
</sampler>
<film type = "ldrfilm">
<integer name = "height" value = "720" />
<integer name = "width" value = "1280" />
<float name = "exposure" value = "-10.000000" />
<rfilter type = "gaussian" />
</film>
</sensor>
</scene>
```