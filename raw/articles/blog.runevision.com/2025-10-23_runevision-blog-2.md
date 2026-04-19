---
title: runevision blog
url: https://blog.runevision.com/2025/10/
published: '2025-10-23'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

I've actually been working on a cool erosion technique I'll post about later, but during some downtime, I had an impulse to see if I could make a basic hair shader that doesn't require any specially made meshes or textures. I ended up making *three* hair shaders.

The shapes below are just standard Unity spheres and capsules and only [a simple normal map](https://www.filterforge.com/filters/9157-normal.html) is used; no other textures. The hair strands follow the vertical V direction of the UV map of the mesh.

![](../../assets/829fa84fff4831dd.png)

I also found some characters on the Asset Store and tried changing the hair material to use my shader. Luckily they all already had hair aligned vertically in the UV map (although not 100% for wavy/curly hair, which compromises my shader slightly).

You can see a video here with the shader in action on both basic shapes and characters:

I ended up making these three hair shader implementations:

- Full multisample hair shader
- Specular multisample hair shader
- Approximation hair shader

All three shaders support a diffuse map, a normal map, and properties for color, smoothness, and normal map strength. The diffuse map alpha is used for cutout transparency.

The strategy was to start with Unity's Standard shading model (based on BRDF physically based shading), but modify it to simulate anisotropic shading, that is, to simulate that the surface is made from lots of little parallel cylinders rather than a flat surface.

This approach ensures that the hair shader looks consistent with other materials based on Unity's Standard shader (and other Surface shaders) under a wide variety of lighting conditions and environments.

### 1) Full Multisample Hair Shader

I started out doing brute force anisotropic shading, running the Unity's physically based BRDF shading function up to 50 times and taking a weighted average of the sample colors.

The normals in those samples are spread out in a 180 degree fan of directions centered around the original normal, using the hair strand direction as the axis of rotation. The final color is a weighted average of the samples.

Much of the "magic" of the simulated anisotropic shading comes from the way the samples are weighted in the two multisample shaders (and emulated in the third).

![](../../assets/aa164ca6b415cc5c.png)

The weight of each sample is a product of two functions:

- The cosine of the angle between the original and modified normal. This is because strands of hair occlude other strands of hair when the hair "surface" is seen from the side, and the parts of strands that face outward tend to be less occluded.
- The cosine of the angle between the modified normal and the view direction. This is because the part of the strand that's facing the camera takes up more of the view than parts that are seen at an angle.

Both cosines are clamped to a zero-to-one range before the two are multiplied.

With this weight function to base the weighted average on, the results looked surprisingly good. Of course, running the entire shading up to 50 times is not exactly the fastest approach, performance-wise.

### 2) Specular Multisample Hair Shader

I made a second implementation that reduces computations somewhat by only multi-sampling certain calculations, namely dot products with the normal, and most of the specular term of the lighting. The diffuse term, fresnel, and other calculations are performed only once. The result is nearly indistinguishable from the full multisample hair shader.

There is still a significant amount of calculations being performed up to 50 times though.

### 3) Approximation Hair Shader

Of course, non-brute force approaches to hair shading are possible too, but way harder to make look good. Still, I eventually came up with something fairly decent.

The third implementation does not perform multisampling but instead emulates the same result. The math formulas required for this were devised by means of a combination of partial understanding, intuition, and trial and error, while carefully comparing the results with the full multisample hair shader. As such, it's difficult to explain the details of the logic behind it with any exactness, but you can see the details in the shader source code.

### Closing thoughts

This was just a little experiment I did as a random side project. I haven't looked much at existing research on hair shaders, as I tend to not understand graphics papers very well. My impression is that this has less to do with the subject matter itself, and more to do with the manner in which it's explained.

The one research entry I did look at – [Hair Rendering and Shading by Thorsten Scheuermann](https://web.engr.oregonstate.edu/~mjb/cs557/Projects/Papers/HairRendering.pdf) – only shows the results on a complex multi-layered haircut model; not simple spheres like I used for testing, which makes it impossible to compare results meaningfully.

I'm not planning any further work on the hair shaders, but I've [released them as open source on GitHub](https://github.com/runevision/HairShader). If anyone makes changes or improvements to them – or just use them in a project – I'd love to hear about it.