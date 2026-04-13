---
title: 'My toy renderer, part 3: Rendering basics'
url: http://momentsingraphics.de/ToyRenderer3RenderingBasics.html
published: '2021-07-16'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# My toy renderer, part 3: Rendering basics

Part 3 of this [series about my toy renderer](http://momentsingraphics.de/ToyRendererOverview.html) covers some basic techniques for rendering. My renderer does nothing fundamentally new on this front but some choices are a bit exotic. It is ultimately about real-time ray tracing, so everything should play nicely with that. Besides I want it to be slick and fast. Disregarding [dear ImGui](https://github.com/ocornut/imgui), the whole thing only makes two draw calls per frame. It uses a visibility buffer [[Burns2013]](http://momentsingraphics.de#_Burns2013) and the same reflectance model for all surfaces [[Lagarde2015]](http://momentsingraphics.de#_Lagarde2015). A 3D table of linearly transformed cosines [[Heitz2016]](http://momentsingraphics.de#_Heitz2016) approximates this reflectance model when needed. It almost has a [Shadertoy](https://www.shadertoy.com/) vibe since the bulk of all work happens in a single fragment shader for the shading pass. To get stratified random numbers, it uses a recent work [[Ahmed2020]](http://momentsingraphics.de#_Ahmed2020) for 2D [polygonal lights](http://momentsingraphics.de/Siggraph2021.html) and [my blue noise textures](http://momentsingraphics.de/BlueNoise.html) for 1D [linear lights](http://momentsingraphics.de/HPG2021.html).

## Rendering visibility buffers

Visibility buffers [[Burns2013]](http://momentsingraphics.de#_Burns2013) are a flavor of deferred shading. In a way, a visibility buffer is the smallest conceivable G-buffer. In my renderer, its size is 32 bits per pixel. It stores nothing but the index of the visible triangle. Visibility buffers go together well with ray tracing for two reasons. Firstly, ray tracing is expensive, so it is wasteful to do it for occluded surfaces. Deferred shading guarantees that it happens at most once per pixel. Secondly, a ray may hit any triangle in the scene. Then you get an index and maybe some barycentric coordinates and have to figure out how to do shading with that. Visibility buffers force you to solve the same problem. Solving it once and benefiting twice feels like a good deal.

The selling point of visibility buffers is that they save bandwidth in more than just one way. The obvious saving is that the buffers themselves are small. Writing 32 bits per fragment is extremely affordable. You do not even have to keep the depth buffer. Common G-buffer layouts are closer to 160 bits. The approach is also known as deferred texturing because the geometry phase never samples the material textures. Overall, rasterization of the scene becomes extremely fast. The vertex shader transforms dequantized positions, the fragment shader writes `gl_VertexIndex/3`

and that's it. Creating the visibility buffer for the frame in [Figure 1](http://momentsingraphics.de#BistroExteriorLinearLight) takes 0.36 ms in spite of the fact that I did not implement any culling whatsoever.

The second saving, which is overlooked more easily, is that the shading pass accesses block-compressed textures directly. Creating the G-buffer decompresses all the textures, which increases bandwidth usage during the shading pass. BC1 compression makes textures eight times smaller, so that is a big saving.

![BistroExteriorLinearLight](../../assets/a6de303465c183db.webp)

**Figure 1:**The

[Lumberyard bistro](https://developer.nvidia.com/orca/amazon-lumberyard-bistro)lit by a long linear light with ray traced shadows. This frame renders in 1.6 ms at 1920×1080 on an NVIDIA RTX 2080 Ti. Most of this frame time goes to ray tracing. The scene has 2.9 million triangles.

## No alpha testing

Above I said that the geometry phase never samples material textures. This design is problematic for triangles that are mostly opaque but use an alpha test to make some parts fully transparent. Foliage is typically modeled like that. This problem is absolutely solvable with visibility buffers. I'd have to load the material index and texture coordinates in the vertex shader and sample the alpha channel in the fragment shader.

However, this problem is difficult to solve efficiently with ray tracing. Any hit shaders are one way to go about it but they incur a substantial cost. There is already research to overcome this problem [[Gruen2020]](http://momentsingraphics.de#_Gruen2020) but for now, I do not want to deal with it. If I cannot do it well, I have the luxury to not do it at all in my toy renderer. All triangles are fully opaque. That's not ideal but it's keeping things simple.

## Access to material textures

As explained in the [previous post](http://momentsingraphics.de/ToyRenderer2SceneManagement.html) every triangle stores a material index, every material is fully characterized by three textures (base color, normal and specular) and every material has all of those (sometimes their size is just 4×4 to store a constant value). To implement shading with a visibility buffer, the shading pass must have random access to all of these textures. Vulkan makes that relatively easy. On the C side, a function writes an array of descriptors for all these textures:

```
VkDescriptorImageInfo* get_materials_descriptor_infos(
uint32_t* texture_count,
const materials_t* materials)
{
(*texture_count) = (uint32_t) materials->material_count * material_texture_count;
VkDescriptorImageInfo* texture_infos = malloc(sizeof(VkDescriptorImageInfo) * *texture_count);
for (uint32_t i = 0; i != *texture_count; ++i) {
texture_infos[i].imageLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
texture_infos[i].imageView = materials->textures.images[i].view;
texture_infos[i].sampler = materials->sampler;
}
return texture_infos;
}
```


The shader uses this global declaration:

```
//! Textures (base color, specular, normal
//! consecutively) for each material
layout (binding = 5) uniform sampler2D
g_material_textures[3 * MATERIAL_COUNT];
```


## The shading pass

Implementing a shading pass with a classic G-buffer is fairly straight forward. You unpack data from the G-buffer and then all data needed for shading is available. This part is quite a bit more complicated with visibility buffers. My renderer implements it with a single function in 101 lines of code. It takes the 2D index of a pixel, the triangle index from the visibility buffer and a ray direction for this pixel. Then it fills a struct with data that you would normally find in a G-buffer and some other useful attributes.

```
shading_data_t get_shading_data(
ivec2 pixel, int primitive_index,
vec3 ray_direction)
```


There is some fancy math in there, so you might want to take a closer look at [the code](https://github.com/MomentsInGraphics/vulkan_renderer/blob/31bafe912524803f81c27a1f9c70cd2c74088e8e/src/shaders/shading_pass.frag.glsl#L714). Here is an overview of what it does:

- Read and dequantize position, normal vector and texture coordinates for all three vertices of the relevant triangle. In total, 3·128=384 bits per pixel are read from two buffers but these reads are very cache coherent because there is no index buffer and
[triangles are sorted](http://momentsingraphics.de/ToyRenderer2SceneManagement.html#Triangle_ordering).

- Compute
[barycentric coordinates](https://en.wikipedia.org/wiki/Barycentric_coordinate_system)for the point where the view ray intersects the triangle.

- Compute derivatives of the barycentric coordinates with respect to screen space coordinates. We need those for texture filtering.

- Use the barycentric coordinates to compute the interpolated position, normal and texture coordinates for the fragment.

- Compute the screen space derivatives for the texture coordinates (using the derivatives for the barycentric coordinates).

- Read the 8-bit material index.

- Sample all three textures of the material using
. Thanks to the derivatives, mipmapping and anisotropic filtering work correctly.`textureGrad()`


- Apply some conversions to the data from the textures to get the parameters for the Frostbite BRDF (e.g. the diffuse albedo).

- Construct a tangent frame (more on that below) and transform the shading normal to world space.

- Apply a little hack to avoid shading normals where the viewing direction is below the horizon.

There is quite a lot of arithmetic going on here. On the other hand, all memory reads are either heavily cache coherent (partly due to the [triangle ordering](http://momentsingraphics.de/ToyRenderer2SceneManagement.html#Triangle_ordering)) or access block-compressed textures. Compared to a classic G-buffer, I am trading reduced bandwidth requirements for increased computation. That may or may not be a good trade, dependent on which resource is limiting performance. In any case, there is the added benefit that it becomes much easier to perform shading for surfaces encountered in a path tracer. The renderer only has ray traced shadows at this time but it is nice to be future proof, isn't it?

## Computing tangent frames

Now on to an aspect that is simultaneously cool and mildly embarrassing. To compute a tangent frame for a triangle, all I need are the texture coordinates and positions for all three vertices. That is readily available in the method that prepares the shading data. Thus, I implement it on the spot in the fragment shader. This moderate computational overhead lets me avoid loads of six 3D vectors per pixel.

But I promised embarrassment: Tangent frames for triangles are not the same as tangent frames for vertices. On smooth surfaces, the established practice is to merge the tangent frames of all adjacent triangles at the vertices. Then these tangents are interpolated across the triangles. Since I only look at one triangle at a time and lack connectivity information, I cannot do that, especially not in the fragment shader. I do construct the tangents so that they are orthogonal to the interpolated normal, so at least this way smooth surfaces are accounted for. However, there can be discontinuous changes of tangent vectors at triangle boundaries.

The other embarrassing aspect that makes me feel less bad about the first one is that I already lost this game at an earlier stage. I obtain models with normal maps from various sources and load all of those into Blender. Maybe some of these models come with tangent frames but as far as I know Blender drops those during import. My exporter would have to come up with tangent frames on its own. These could be a bit nicer than the ones computed in the fragment shader but most likely they won't be defined in exactly the right way to match whatever was used to bake the normal maps originally.

Getting tangent frames right is hard when you do not control the authoring of normal maps. If I'm going to do it wrong, I can at least do that efficiently.

## The Frostbite BRDF

There are lots of great BRDF models that help us approach the diversity of real surfaces. The flipside is that this sometimes leads into a babel of similar alternatives where nobody understands what anybody else is doing. Getting shading to look the same in different renderers is a daunting task. There are different choices for diffuse and specular microfacet models, normal distribution functions, masking and shadowing and Fresnel approximations. Since microfacet BRDFs are sort of modular, these options give rise to a combinatoric explosion. And on top of that, people do not always agree how to define the input parameters for these models.

However, in recent years we got a glimpse of unification under the slogan “physically based shading.” An appreciable portion of people in real-time rendering now defines most materials in a fairly standardized way. As far as I can tell, the introduction of the Frostbite BRDF [[Lagarde2015]](http://momentsingraphics.de#_Lagarde2015) has been a major catalyst for that. It is not really a new BRDF, all building blocks have been described in detail before (Disney diffuse, GGX, Smith masking-shadowing, Fresnel-Schlick approximation) [[Heitz2014]](http://momentsingraphics.de#_Heitz2014). But it sets a well-defined standard for how to combine them and how to feed them with parameters from textures. It also strikes a good balance between efficiency and versatility, which probably helped it to get a rather wide adoption. Probably, there are many slightly different variants out there but at least they will give similar shading for identical parameters.

My renderer uses the Frostbite BRDF for absolutely all surfaces. In my opinion, it gives appealing shading for a wide range of solid surfaces ([Figure 2](http://momentsingraphics.de#ArcadePolygonalLight)). The three textures define base color, normal, an occlusion parameter that I do not use, roughness and metalicity. These attributes are stored in the order listed here (e.g. roughness in the green channel). Metalicity is 1 for metals (where the base color defines the specular color) and 0 for dielectrics (where the base color defines the diffuse albedo and specular highlights are white). The roughness in the texture gets squared before it is used for the GGX normal distribution function. Models from [ORCA](https://developer.nvidia.com/orca), [Sketchfab](https://sketchfab.com/) and [3D Model Haven](https://3dmodelhaven.com/) all provide such textures.

If you want to check out my reasonably optimized implementation, you should look at [ evaluate_brdf() in brdfs.glsl](https://github.com/MomentsInGraphics/vulkan_renderer/blob/31bafe912524803f81c27a1f9c70cd2c74088e8e/src/shaders/brdfs.glsl#L49) and at

[.](https://github.com/MomentsInGraphics/vulkan_renderer/blob/31bafe912524803f81c27a1f9c70cd2c74088e8e/src/shaders/shading_pass.frag.glsl#L714)

`get_shading_data()`

in shading_pass.frag.glsl![ArcadePolygonalLight](../../assets/ca3dfbc9d6f00b47.webp)

## Linearly transformed cosines (LTCs)

As I wrote the toy renderer, my goal was to implement new techniques for shading with area lights. That's where LTCs [[Heitz2016]](http://momentsingraphics.de#_Heitz2016) come into play. In short, they provide an approximation to specular BRDFs that makes it much easier to integrate over the area light for shading. Eric Heitz wrote a [more detailed explanation](https://eheitzresearch.wordpress.com/415-2/) and of course there's the paper [[Heitz2016]](http://momentsingraphics.de#_Heitz2016). Originally, you could not have shadows with LTCs. Now you can, but more on that in the [next post](http://momentsingraphics.de/ToyRenderer4RayTracing.html).

To fit coefficients of LTCs, I used [Eric Heitz's code](https://drive.google.com/open?id=0BzvWIdpUpRx_ZDZwTVg5bzRRTlE) (Stephen Hill pointed out that there is an [updated version](https://github.com/selfshadow/ltc_code)). I have not published this code since it is just slightly modified. All I really did was to put the Frostbite BRDF in there. Then I dump this data to another lazy binary file format and load it into my renderer. There are two noteworthy aspects of my implementation though: It uses a 3D table instead of a 2D table and quantizes LTC coefficients in an unusual way.

To use LTCs, I have to store a few precomputed coefficients for every relevant BRDF and for each viewing direction. For isotropic materials, the viewing direction boils down to a single inclination angle \(\theta_o\). The appearance of the Frostbite specular BRDF depends on the roughness and on Fresnel \(F_0\), i.e. the color of the specular reflection when we look at the material at a right angle. For my renderer, I have created a 3D table that accounts for all three parameters. However, Stephen Hill pointed out that he has proposed an alternative where a 2D table suffices [[Hill2017]](http://momentsingraphics.de#_Hill2017). Inspired by prior work on prefiltered environment maps, [the idea](https://blog.selfshadow.com/publications/s2016-advances/s2016_ltc_fresnel.pdf) is to only store LTCs for Fresnel \(F_0=1\). Then an additional channel stores the overall brightness of the specular reflection (i.e. the albedo) for Fresnel \(F_0=0\). The correct albedo is obtained by using \(F_0\) to interpolate between the albedos for the two extreme values.

My approach with the 3D table gives more accurate fits because the shape of the specular lobe provided by the LTC can depend on Fresnel \(F_0\) as it should. However, it is a bit more complicated to implement, the table of LTCs is bigger (namely 2.5 MB) and if Fresnel \(F_0\) varies quickly (in my test scenes it doesn't) texture reads have worse cache locality. To give you an idea whether it is worthwhile to invest these resources, I decided to do a direct comparison. All information needed to implement Stephen Hill's method is available in my table, so I only had to modify the shader a bit. You can download the modified code below.

[Figure 3](http://momentsingraphics.de#Weighted3D) shows results with my 3D table and [Figure 4](http://momentsingraphics.de#Weighted2D) uses Stephen Hill's method. As expected, there is more noise with the 2D table. The difference is quite visible, especially on the rough plane to the left, but results with the 2D table are still good. The surfaces here are not metallic, so this example should be considered a worst case for the 2D table.

![Weighted3D](../../assets/244c8776b85fcd20.webp)

**Figure 3:**Three planes of different roughness with Fresnel \(F_0=0.02\) shaded using

[BRDF importance sampling for polygonal lights](http://momentsingraphics.de/Siggraph2021.html). This rendering uses the weighted balance heuristic, i.e. if the LTC fit would be perfect, there would be no noise. The LTCs used here come from a 3D table.

In practice, samples for diffuse and specular components of the BRDF should be combined in a different manner. It improves results in penumbras but causes more noise in fully lit regions. More on that in the [next post](http://momentsingraphics.de/ToyRenderer4RayTracing.html). [Figure 5](http://momentsingraphics.de#Clamped3D) and [Figure 6](http://momentsingraphics.de#Clamped2D) show a comparison in this setting. The parts where diffuse shading dominates get worse but for specular highlights, the conclusions are essentially the same as before. Though, the increased noise with the 2D table appears less problematic when there is more noise to begin with.

Overall, I would say both options are absolutely legitimate. If you do not mind creating and using the slightly bigger table, you get a visible quality improvement out of it. Otherwise, the quality of the results will still be good and you can be more confident that you are not thrashing caches with LTCs.

The other interesting aspect of my implementation is the representation of LTCs in GPU memory. It differs a bit from the solution in the published implementation [[Heitz2016]](http://momentsingraphics.de#_Heitz2016). A linearly transformed cosine is described by a matrix of the form

Additionally, the table stores the specular albedo (or two specular albedos with Stephen Hill's method). My implementation, stores one additional entry explicitly (i.e. six values per LTC):

\[ M:=\begin{pmatrix}a & 0 & b\\ 0 & c & 0\\ d & 0 & e \end{pmatrix} \]Scaling all entries by the same factor does not change the LTC. Thus, I can ensure that the maximal absolute value among all entries is exactly one. I also know the sign for each entry. Therefore, I can use 16-bit fixed point numbers instead of 16-bit floats. Filtering works fine thanks to an [UNORM format](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VkFormat.html). Since I do not use any bits for float exponents, accuracy is better but I also use 16 bits more. Maybe it also makes interpolation behave more reasonably in some boundary cases. I am not sure whether this change is really necessary but it doesn't hurt either. Besides, I have a fondness for fixed-point formats. I guess it goes back to [moment shadow mapping](http://momentsingraphics.de/I3D2015.html).

## Stratified random numbers (blue noise)

My renderer uses Monte Carlo integration for shading with either [linear lights](http://momentsingraphics.de/HPG2021.html) or [polygonal lights](http://momentsingraphics.de/Siggraph2021.html). A random point on the light is picked and a shadow ray determines whether it is visible. For that I need either 1D or 2D random numbers on each pixel. Crucially, these random numbers do not have to be independent across pixels. Introducing anticorrelations into random numbers of neighboring pixels in just the right way pushes noise into higher frequencies. That makes it harder to perceive and easier to remove through denoising. Therefore, I do not use any of the great pseudorandom number generators [[Jarzynski2020]](http://momentsingraphics.de#_Jarzynski2020) out there. Instead, I use precomputed textures of stratified random numbers. I have an array of 64 textures and select a random one in each frame that also gets offset randomly.

For the 1D linear lights, it should not come as a surprise that I use [my blue noise textures](http://momentsingraphics.de/BlueNoise.html) [[Ulichney93]](http://momentsingraphics.de#_Ulichney93). Apparently, everybody does that nowadays and I made them exactly for this sort of situation. Results are great, especially in combination with uniform jittered sampling [[Ramamoorthi2012]](http://momentsingraphics.de#_Ramamoorthi2012) ([Figure 7](http://momentsingraphics.de#BistroInsideJitteredBlue)). Particularly in spots where a single contiguous part of the linear light is visible/occluded, the ray traced shadows essentially just apply a thresholding to the random numbers. Thus, we get cleanly dithered gradients.

![BistroInsideJitteredBlue](../../assets/b7a0c0cbbf65b9ac.webp)

**Figure 7:**Shadows from a long linear light rendered using blue noise textures and six samples per pixel (three diffuse, three specular). Results are improved further through uniform jittered sampling as described in

[the paper](http://momentsingraphics.de/HPG2021.html).

But what about 2D polygonal lights? Should I just use two independent 1D blue noise textures? That's what I did for the longest time and it is not so bad but there is a better solution now [[Ahmed2020]](http://momentsingraphics.de#_Ahmed2020). The idea is to start from a 2D Sobol sequence. This sequence offers a progressive point set with a special property. Each prefix of \(2^{2^n}\) points (e.g. 256·256 points) places exactly one point in certain axis-aligned rectangles of various aspect ratios (so-called elementary intervals). If one such elementary interval corresponds to a part of the area light that is completely occluded or completely visible, the outcome is no longer random. We know that we place exactly one sample there and get the corresponding contribution. Thus, variance is decreased.

This reasoning only works at high sample counts but it points us in the right direction. For nearby pixels, similar parts of the area light will be visible or occluded. So if we use nearby entries in the Sobol sequence for nearby pixels, we probably get many of the same advantages. [Morton codes](https://fgiesen.wordpress.com/2009/12/13/decoding-morton-codes/) could be used to unroll the 1D sequence onto the 2D screen in such a way but that gives rise to regular patterns. Ahmed et al. take a slightly different approach by traversing a quadtree with randomly shuffled children. The order in the depth-first traversal maps Sobol points to pixels. Locality is preserved but regular patterns are broken. I would definitely recommend that you read the full paper [[Ahmed2020]](http://momentsingraphics.de#_Ahmed2020) instead of this mile high summary. In my opinion, it addresses an important problem for modern real-time rendering well.

One of the benefits of this approach is that it is reasonably efficient to compute the random numbers from the pixel index. However, I already had the infrastructure for precomputed noise tables in place and preferred to stick to it. Thus, I use a slightly modified version of [Abdalla Ahmed's code](http://abdallagafar.com/publications/zsampler/files/zcode.zip) to compute noise tables ([published as well](http://momentsingraphics.de/Siggraph2021.html)). These tables are created for rendering at one sample per pixel. At higher sample counts, they still work but are suboptimal because consecutive samples for a single pixel should also be consecutive entries of the Sobol sequence.

[Figure 8](http://momentsingraphics.de#ChairShadowWhite), [Figure 9](http://momentsingraphics.de#ChairShadowBlue) and [Figure 10](http://momentsingraphics.de#ChairShadowAhmed) compare white noise, blue noise and Ahmed's approach. White noise is clearly inferior. The improvement over blue noise with Ahmed's approach is subtle but I found it to be consistently present. Bright and dark pixels cluster together slightly less.

![ChairShadowWhite](../../assets/974369f6c5ca225d.png)

**Figure 8:**Shadow from a rectangular light for the leg of a chair using white noise.

![ChairShadowBlue](../../assets/c162768d0fc5306a.png)

**Figure 9:**Shadow from a rectangular light for the leg of a chair using blue noise.

![ChairShadowAhmed](../../assets/2bb54b1917b2b2a2.png)

**Figure 10:**Shadow from a rectangular light for the leg of a chair using Ahmed's approach.

I also tried many other options:

- Using the first two dimensions of a
[4D Sobol sequence](https://web.maths.unsw.edu.au/~fkuo/sobol/)to determine where samples should go in a 2D noise table, gave fairly good results but with structured noise.

- Using
[Owen-scrambled Sobol](https://utk-team.github.io/utk/sampler_owen/)in the same manner gave even more structured artifacts. I am not sure why.

[Burley's take on Owen-scrambled Sobol](http://jcgt.org/published/0009/04/01/)[[Burley2020]](http://momentsingraphics.de#_Burley2020)gave better results than the other implementation but the results were similar to Sobol without Owen scrambling.

[Halton](http://gruenschloss.org/)gives less structured noise but also a bit more low-frequent noise. To get it to look good, I had to use a 2048×1152 resolution, so the precomputed textures took 1.1 GB in the end.

- The
[implementation of blue noise dithered sampling](https://github.com/githole/blueNoise)that I found performed slightly worse than 1D blue noise textures.

Overall, Ahmed's approach is the winner in this comparison for direct illumination with polygonal area lights. Its lead is not huge but it performs consistently well in every aspect. It never looked clearly worse than one of the other options.

## Conclusions

In my renderer, the life of a triangle is short. It does so little with the geometry that the complete lack of culling is irrelevant. Most work happens in the shading pass but this pass also has low bandwidth requirements. The image quality does not stem from geometric complexity but from sophisticated shading. In particular, linear lights or area lights can look really nice when used appropriately. In the [next post](http://momentsingraphics.de/ToyRenderer4RayTracing.html), I'll look beyond the random numbers and explain how my renderer supports large linear and polygonal lights with ray-traced shadows without resorting to approximations or introducing a lot of noise.

## References

[ Ahmed, Abdalla G. M. and Wonka, Peter (2020). Screen-Space Blue-Noise Diffusion of Monte Carlo Sampling Error via Hierarchical Ordering of Pixels. ACM Transactions on Graphics (proc. SIGGRAPH Asia), 39(6). ][Official version](https://doi.org/10.1145/3414685.3417881) | [Author's version](http://abdallagafar.com/publications/zsampler/)

[ Burley, Brent (2020). Practical Hash-based Owen Scrambling. Journal of Computer Graphics Techniques, 9(4):1-20. ][Official version](http://jcgt.org/published/0009/04/01/)

[ Burns, Christopher A. and Hunt, Warren A. (2013). The Visibility Buffer: A Cache-Friendly Approach to Deferred Shading. Journal of Computer Graphics Techniques, 2(2):55-69. ][Official version](http://jcgt.org/published/0002/02/04/)

[ Gruen, Holger and Benthin, Carsten and Woop, Sven (2020). Sub-triangle opacity masks for faster ray tracing of transparent objects. Proceedings of the ACM on Computer Graphics and Interactive Techniques (proc. HPG), 3(2). ][Official version](https://doi.org/10.1145/3406180)

[ Heitz, Eric (2014). Understanding the Masking-Shadowing Function in Microfacet-Based BRDFs. Journal of Computer Graphics Techniques (JCGT), 3(2):48-107. ][Official version](http://jcgt.org/published/0003/02/03/)

[ Heitz, Eric and Dupuy, Jonathan and Hill, Stephen and Neubelt, David (2016). Real-time Polygonal-light Shading with Linearly Transformed Cosines. ACM Transactions on Graphics (proc. SIGGRAPH), 35(4). ][Official version](https://doi.org/10.1145/2897824.2925895) | [Author's version](https://eheitzresearch.wordpress.com/415-2/)

[ Hill, Stephen and Heitz, Eric (2017). Physically Based Shading in Theory and Practice: Real-Time Area Lighting: a Journey from Research to Production. ACM SIGGRAPH 2017 Courses, article 7. ][Official version](https://doi.org/10.1145/3084873.3084893) | [Author's version](https://blog.selfshadow.com/publications/s2016-advances/)

[ Jarzynski, Mark and Olano, Marc (2020). Hash Functions for GPU Rendering. Journal of Computer Graphics Techniques, 9(3):21-38. ][Official version](http://jcgt.org/published/0009/03/02/)

[ Lagarde, Sébastian and de Rousiers, Charles (2015). Physically Based Shading in Theory and Practice: Moving Frostbite to PBR. ACM SIGGRAPH 2014 Courses, article 23.
][Author's version](https://seblagarde.files.wordpress.com/2015/07/course_notes_moving_frostbite_to_pbr_v32.pdf)

[ Ramamoorthi, Ravi and Anderson, John and Meyer, Mark and Nowrouzezahrai, Derek (2012). A Theory of Monte Carlo Visibility Sampling. ACM Transactions on Graphics, 31(5). ][Official version](https://doi.org/10.1145/2231816.2231819) | [Author's version](http://www.iro.umontreal.ca/~derek/files/Ramamoorthi-ATO-2012-02.pdf)

[ R. A. Ulichney (1993). Void-and-cluster method for dither array generation. Proc. SPIE 1913, Human Vision, Visual Processing, and Digital Display IV.
][Official version](https://dx.doi.org/10.1117/12.152707) | [Author's version](http://cv.ulichney.com/papers/1993-void-cluster.pdf)