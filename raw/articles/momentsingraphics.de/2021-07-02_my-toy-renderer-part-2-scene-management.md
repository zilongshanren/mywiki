---
title: 'My toy renderer, part 2: Scene management'
url: http://momentsingraphics.de/ToyRenderer2SceneManagement.html
published: '2021-07-02'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# My toy renderer, part 2: Scene management

Part 2 of this [series about my toy renderer](http://momentsingraphics.de/ToyRendererOverview.html) is all about scene data. The requirements are fairly lax, since I only care about static triangle meshes. For the most part, I want to be able to render the [ORCA assets](https://developer.nvidia.com/orca) and a couple of scenes from [Blendswap](https://blendswap.com). However, I emphasized how much long compile times harm productivity in the [previous post](http://momentsingraphics.de/ToyRenderer1KeepItSimple.html). All of that applies equally to load times since they interrupt work in a similar way. I want to be able to load huge scenes within seconds and I want to render them quickly. Besides results must be reproducible.

## Just read that file

The least that needs to happen to load a scene is that a file is read and some data is written to VRAM. In my opinion, that is also the only thing that should happen. Correspondingly, the core of my scene loading function is this tiny code snippet.

```
for (uint32_t i = 0; i != mesh_buffer_count; ++i)
fread(staging_data
+ scene->mesh.buffers[i].offset,
scene->mesh.buffers[i].size, 1, file);
```


The scene file simply holds a big chunk of binary data. This is exactly the data that should go into the vertex buffers. The file format is tailor-made for this renderer so that this can work. Of course, there is a bit more code to read meta data (e.g. triangle count and material names) and to actually copy that data to VRAM but it is not much.

The speed of this process is only limited by drive and PCIe bandwidth. Many practices that make scene loading slow in other systems are avoided. I'm not [loading FBX files through Assimp](https://github.com/nvidiagameworks/falcor), tidying up the geometry at load time or [reading JSON in quadratic time](https://nee.lv/2021/02/28/How-I-cut-GTA-Online-loading-times-by-70/). All of this should be done upon export, not upon loading since loading happens much more frequently. If the files that you load into your renderer are the masters that you use for editing (e.g. Blender files), you are making things hard for no good reason. And if you have a third format between the master and the representation for your renderer, I really do not know what you are hoping to accomplish.

## Blender export

With this design, I have pushed lots of responsibilities to the software creating scene files, namely my [Blender](https://www.blender.org/) exporter. Nonetheless, this exporter has only 602 lines of Python code. Since Blender can import almost anything, I have a fairly convenient way to get most models into my renderer. Of course, fast export is nice to have so that it is easy and quick to view models in the renderer.

Fast and Python do not always go together but [NumPy](https://numpy.org/) is here to help. It actually ships with Blender's Python interpreter. The exporter has to apply transformations to each vertex, merge vertex attributes, merge meshes and so forth. All of these operations can be expressed naturally in terms of component-wise operations on arrays, array writes masked by index arrays or concatenations of arrays. Thus, the heavy lifting is done by the native code inside NumPy, not by loops in Python. And thankfully, Blender has [foreach_get()](https://docs.blender.org/api/current/bpy.types.bpy_prop_collection.html#bpy.types.bpy_prop_collection.foreach_get), which writes the source data to an array for us, again without loops in Python. It takes some practice to get this kind of thing right, but the resulting code is lean and fast.

The exporter flattens the geometry representation as much as possible. Modifiers get applied, animations evaluated at the current frame, hierarchical transforms resolved, etc. In the end, the scene is a single triangle soup with a position, normal and texture coordinate per vertex.

## Quantization

VRAM bandwidth is often a limiting resource on GPUs. Thus, it is always worthwhile to squeeze the data in VRAM a bit so that fewer bytes need to be read. As convenient as it may be, it is a bad idea to use a 32-bit float for each vertex attribute. And of course, we also want small scene files and fast export and load.

My scene files store 128 bits per vertex and 8 bits per triangle. A vertex position takes 64 bits with 21 bits per coordinate. One bit is unused. I use [fixed-point](https://en.wikipedia.org/wiki/Fixed-point_arithmetic) coordinates relative to a global bounding box, so accuracy is the same throughout the scene. If the scene is 1 km³ large, the maximal quantization error in coordinates is \(\frac{1~\mathrm{km}}{2^{22}} = 238~\mathrm{\mu m}\) (a [tardigrade](https://en.wikipedia.org/wiki/Tardigrade) could barely fit between two coordinates). Going down to 32 bits per position would be too extreme but anything between 32 and 64 is always awkward to deal with. This scheme is efficient and accurate enough to ignore its inaccuracies. Dequantization is a breeze:

```
vec3 decode_position_64_bit(
uvec2 quantized_position,
vec3 dequantization_factor,
vec3 dequantization_summand)
{
vec3 position = vec3(
quantized_position[0] & 0x1FFFFF,
((quantized_position[0] & 0xFFE00000) >> 21) | ((quantized_position[1] & 0x3FF) << 11),
(quantized_position[1] & 0x7FFFFC00) >> 10
);
return position * dequantization_factor
+ dequantization_summand;
}
```


My rasterization pass only cares about positions (more on that in the next post). Thus, it would be pointless to use an index buffer. Reading a 32-bit index only to figure out where to read a 64-bit position does more harm than good. I simply store three vertices per triangle. The 8 bits per triangle are only for the material index (i.e. more than 256 materials are not supported).

For normal vectors, I use octahedral maps [[Meyer2010]](http://momentsingraphics.de#_Meyer2010) with 2·16 bits per normal vector. For texture coordinates, I use two 16-bit fixed-point coordinates to cover the range from 0 to 8. On a 4k texture, that still gives a resolution of a quarter texel, which is good. However, it means that I have to force texture coordinates into this range. I assume that textures wrap periodically (indeed, they do in my renderer) so there is no harm in applying the same integer offset to all texture coordinates of a triangle. I only run into problems when a texture repeats more than seven times within a triangle. In that case, coordinates get clamped and the exporter prints a warning. This happens every once in a while but I never observed any artifacts because of it. Nonetheless, I am a bit unhappy with this aspect but using more than 16 bits for a texture coordinate also seems wasteful.

## Triangle ordering

Cache coherence is also important for the efficiency of renderers. One way to improve it is to ensure that triangles that are nearby in the scene are also nearby in memory. My exporter ensures that in a fairly simple manner. Per triangle, it computes the centroid (i.e. the mean of its vertex positions). Then it converts that centroid to a 32-bit [Morton code](https://fgiesen.wordpress.com/2009/12/13/decoding-morton-codes/) with respect to the global bounding box. Finally, triangles get sorted by these Morton codes. This way, most nearby triangles get nearby indices but there are a few sudden jumps at bounds of large octree cells ([Figure 1](http://momentsingraphics.de#MortonTriangleOrder)).

![MortonTriangleOrder](../../assets/074989052521c94d.png)

## Materials

Exporting materials from Blender is practically impossible. The standard way to define them is by means of node graphs. These can use several procedural textures, an arbitrary number of image files and lots of different nodes. All of that functionality would have to be replicated in a renderer, which is not what I am here for at all.

I took the opposite route: The only information about materials that gets exported is their name and an array with the material index for each triangle. Upon loading, the renderer expects to find three textures for each material: `<name>`

_BaseColor.vkt, `<name>`

_Normal.vkt and `<name>`

_Specular.vkt. These textures hold attributes for the Frostbite BRDF [[Lagarde2015]](http://momentsingraphics.de#_Lagarde2015) (see the next post). All [ORCA assets](https://developer.nvidia.com/orca) come with textures like that and I think the same is true for models on [Sketchfab](https://sketchfab.com/) and [3D Model Haven](https://3dmodelhaven.com/). For models where such textures are unavailable (e.g. from [Blendswap](https://blendswap.com/)), I have a few Python scripts to aid me in their creation.

Once again, I want small files, fast loading and minimal bandwidth usage. Therefore, I use [block compression](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VkFormat.html) (BC1 for base color and specular, BC5 for normal maps). My vkt texture file format follows the same philosophy as the scene files. It holds binary data that can be copied to VRAM directly, much like the [DDS file format](https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide). I could have used a more established format but I do not want to evoke the impression that my renderer can load whatever you throw at it because it cannot. Instead I have a little C conversion utility that loads images using [stb_image.h](https://github.com/nothings/stb/blob/master/stb_image.h), generates mipmaps for a texture, does block compression using [stb_dxt.h](https://github.com/nothings/stb/blob/master/stb_dxt.h) and writes a vkt file. I did not bother to implement mipmap filtering for textures of arbitrary resolution, so it is restricted to powers of two. A Python script uses this utility to do batch conversion for a whole directory.

## Camera and lights

Of course, a scene consists of more than just triangles and materials. We need some light sources and a camera to look at it all. All this scene state is held by a single struct:

```
typedef struct scene_specification_s {
//! Path to the *.vks file holding
//! scene geometry
char* file_path;
//! Path to the directory holding
//! scene textures
char* texture_path;
//! Path to the file from which light
//! sources and camera have been loaded
char* quick_save_path;
//! The current camera
first_person_camera_t camera;
//! Number of polygonal lights
//! illuminating the scene
uint32_t polygonal_light_count;
//! The polygonal lights illuminating
//! the scene
polygonal_light_t* polygonal_lights;
} scene_specification_t;
```


First-person camera controls and construction of camera transforms are implemented in 116 lines of code. I do not have a utility for matrix math because there are very few spots in this renderer where I would need it. Matrix multiplication is implemented on the spot as needed. Light sources are defined through the [Dear ImGui](https://github.com/ocornut/imgui) interface.

Additionally, there is a struct `render_settings_t`

to define the choice of rendering techniques and their parameters. Together with the swapchain resolution and the seed for random numbers, that determines the rendered image completely. There is a render setting to fix random numbers, otherwise they change each frame. As emphasized before, reproducibility is important and this aspect worked out well. A while ago, I revived a part of the project after doing other things with the renderer for a year. I merged a lot of old code with new code. Still, after fixing one discrepancy, I was able to reproduce my old screenshots almost down to the last bit.

## Quicksave and quickload

Reproducibility massively benefits from a feature to save the current state of camera and lights to a file. In my opinion, every research renderer should have that bound to some hot keys. My renderer, uses a simple binary file format where I just dump the binary representation of `first_person_camera_t`

and `polygonal_light_t`

. Admittedly, this part is a bit messy. Different platforms may have different padding in structs, which could cause problems (though I never encountered that). What is worse is that it is annoying to make changes to this file format. Anyway, it works.

## Reproducible experiments

With the streamlined state described above, it is easy to reproduce a single rendering. On top of that, I have a mechanism to reproduce all the renderings used for the evaluation of different techniques in [my](http://momentsingraphics.de/Siggraph2021.html) [papers](http://momentsingraphics.de/HPG2021.html). The file experiment_list.c defines the `scene_specification_t`

and `render_settings_t`

for all these screenshots. Creating this list through code is far more convenient than using e.g. a JSON file because it is easy to make many slightly different versions of the same experiment. When the button in [Figure 2](http://momentsingraphics.de#ReproduceButton) is pressed, the renderer sets up one experiment after the other. For each it waits a little while until timings stabilize and then it stores a screenshot. Python scripts further process these images to produce the versions for the paper (e.g. by adding magnified insets).

![ReproduceButton](../../assets/b5a6846f9c239fd5.png)

**Figure 2:**With the click of a button, my renderer takes all the screenshots shown in the paper and its supplemental material and measures timings for different techniques.

When you write a paper, you should not postpone the production of results for too long because that is a recipe for unpleasant surprises. On the other hand, if you have already produced all results, you have an incentive not to make improvements to your renderer anymore because then you should recreate those results. If this process is fully automated, you can conveniently change anything you like after first producing your results.

## Conclusions

My scene representation is flat, compact and GPU-friendly. It is one big triangle soup, coupled with a list of textures and a bit of additional state. The files are reasonably small to begin with and for shipping, zip compression shrinks them quite effectively. All of this benefits load times and render times. The resulting timings speak for themselves: Startup of my renderer with the [Lumberyard bistro exterior](https://developer.nvidia.com/orca/amazon-lumberyard-bistro) takes 5 seconds the first time I do it. The scene has 2.9 million triangles and 937 MB of textures and I measured that on a system with an SATA SSD and an RTX 2080 Ti. And it gets better: If I close the renderer and start it again some time later, startup with that same scene only takes 2.5 seconds because the OS kindly caches these files for me. I suppose a faster SSD would accomplish the same for the first load. Smaller scenes are even faster. Including compile and link times, my turnaround time is comfortably below five seconds.

## References

[ Lagarde, Sébastian and de Rousiers, Charles (2015). Physically Based Shading in Theory and Practice: Moving Frostbite to PBR. ACM SIGGRAPH 2014 Courses, article 23.
][Author's version](https://seblagarde.files.wordpress.com/2015/07/course_notes_moving_frostbite_to_pbr_v32.pdf)

[ Meyer, Quirin and Süßmuth, Jochen and Sußner, Gerd and Stamminger, Marc and Greiner, Günther (2010). On Floating-Point Normal Vectors. Computer Graphics Forum 29(4). Eurographics. ][Official version](https://doi.org/10.1111/j.1467-8659.2010.01737.x)