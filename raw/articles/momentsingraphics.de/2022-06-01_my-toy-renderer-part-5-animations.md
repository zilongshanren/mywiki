---
title: 'My toy renderer, part 5: Animations'
url: http://momentsingraphics.de/ToyRenderer5Animations.html
published: '2022-06-01'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# My toy renderer, part 5: Animations

I was not planning to have a fifth part in this [series about my toy renderer](http://momentsingraphics.de/ToyRendererOverview.html) but there were some interesting changes for our [paper on vertex-blend attribute compression](http://momentsingraphics.de/I3D2022.html). The renderer now supports animations with linear vertex-blend animation (also known as skinning). That means there is a skeleton consisting of animated bones and those influence the mesh. I had to export these animations from Blender to my renderer and I wanted to [keep it simple](http://momentsingraphics.de/ToyRenderer1KeepItSimple.html). Thus, the Blender exporter just dumps all bone transforms for each frame into one big texture that vertex shaders read directly. And as for other parts of [the file format](http://momentsingraphics.de/ToyRenderer2SceneManagement.html), there is some reasonable compression.

## Exporting animations from Blender

Linear vertex-blend animation [[MagnenatThalmann1988]](http://momentsingraphics.de#_MagnenatThalmann1988) uses a skeleton, i.e. a tree of bones. Each of these bones has an animated transformation relative to its parent bone (or to the world if it is a root bone). The difference between the animated bone to world space transform and the same transform for the rest-pose is applied to the mesh. The animation of each bone is typically controlled by keyframes but it can be more complicated than that. For example, Blender supports different interpolation modes and procedural curves to add noise and such. These data could be exported by just exporting all keyframes but then subtleties of the interpolation are lost. Reimplementing all these features correctly in the renderer is challenging. A better solution is to create more keyframes during export, e.g. 60 per second, to ensure that everything is interpolated as it should be.

That is still too complicated for my taste. Remember, I [keep it simple](http://momentsingraphics.de/ToyRenderer1KeepItSimple.html). I do not care about having any sort of physics simulation or interactivity in my animations. They should simply be played back exactly the way they play in Blender. Thus, I opt for a completely flattened representation, similar to the [geometry format](http://momentsingraphics.de/ToyRenderer2SceneManagement.html#Quantization). The Blender exporter samples the transformation matrix of each bone at a fixed rate (by default 60 frames per second). For each sample and each bone, it writes the bone to world space transform, relative to the rest pose, to the scene file. These transformations are exactly the ones that have to be applied to vertices in the vertex shader. Thus, this 2D array of transformations can be uploaded to the GPU as is and used directly. I use a texture for that. The only work that the CPU does to drive animations is writing the current frame index to a constant buffer.

You can take a look at the [implementation in the exporter](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/tools/io_export_vulkan_animated_blender28.py#L473). First, it [builds a list of all relevant bones](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/tools/io_export_vulkan_animated_blender28.py#L455). Then it uses [ bpy.types.Scene.frame_set()](https://docs.blender.org/api/current/bpy.types.Scene.html#bpy.types.Scene.frame_set) repeatedly to play back the animation (once for the whole scene). For each bone, it

[grabs the current bone to armature space transform](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/tools/io_export_vulkan_animated_blender28.py#L492)from

[bpy.types.PoseBone.matrix](https://docs.blender.org/api/current/bpy.types.PoseBone.html#bpy.types.PoseBone.matrix). Finally, it

[makes transforms relative](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/tools/io_export_vulkan_animated_blender28.py#L507)to the rest pose described by

[bpy.types.Bone.matrix_local](https://docs.blender.org/api/current/bpy.types.Bone.html#bpy.types.Bone.matrix_local)and

[accounts for the transform of the skeleton](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/tools/io_export_vulkan_animated_blender28.py#L510)as a whole. Combining all these transforms correctly is always a bit tricky but I think I got it right. The documentation of Blender's Python API is often a bit unclear when it comes to that. The good thing about my approach here is that interactions with Blender are rather minimal. For example, I only extract transforms relative to the skeleton rather than dealing with transforms relative to parent bones. A drawback of this approach is that it might change the scene during export because it plays back the animation.

## Compression of animations

In my first attempt, the texture of bone transforms held 3×4 matrices, where each entry was a 32-bit float. So if a vertex is affacted by 8 bones, the vertex shader has to load \(3\cdot4\cdot8\cdot4=384\) bytes for the animations alone. That is quite a lot, and indeed Nsight profiling revealed that the renderer as a whole wound up being limited by L1-cache bandwidth. The L1 cache is pretty fast but so is everything else in this renderer. After all, the only thing it does is rendering some animated models. To some extent, the cost of loading these transforms hid the cost of reading and decompressing vertex attributes (especially the ones for blending). Since this cost is what I wanted to evaluate for our [paper on vertex-blend attribute compression](http://momentsingraphics.de/I3D2022.html), I needed better compression for the animation data.

The main thing to exploit for better compression is that arbitrary transforms are not allowed. The transforms that I needed (at least for all of my test models) consist of rotations, translations and uniform scaling. There is no shearing and no different scaling along different axes. The goal is to store all required quantities using a fixed-point format (16-bit `uint`

). To store the rotation, I use a quaternion, i.e. a unit vector with four entries. The sign does not matter, so I can always make the last entry positive. Converting [rotation matrices to quaternions](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/tools/io_export_vulkan_animated_blender28.py#L80) works using a method from the evergreen [matrix and quaternion FAQ](https://www.j3d.org/matrix_faq/matrfaq_latest.html). Translations are suitable for fixed-point quantization right away. Scalings may have high dynamic range (i.e. get really small or big), so using fixed-point quantization directly is a bad idea. Instead, I store the base-2 logarithm of the scaling.

In the end, a transformation is represented by eight scalars (four for the quaternion, three for the translation, one for the logarithmic scaling). Compared to the 12 scalars for a 3×4 matrix, that is already an improvement but quantization improves matters further. The exporter sees all these scalars for all bones and all frames at once. For each of the eight scalars, it determines a single [minimal and maximal value](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/tools/io_export_vulkan_animated_blender28.py#L152). Within these bounds, it performs fixed-point quantization using rounding to nearest. Mapping one of the `uint`

s in the texture to the dequantized scalar value only takes one [fma](http://momentsingraphics.de/FMA.html) in the [vertex shader](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/src/shaders/forward_pass.vert.glsl#L112).

With this scheme, 16-bit quantization is good enough in my use cases. Thus, we go down from \(4\cdot 3\cdot 4=48\) bytes per transform to \((4+3+1)\cdot 2=16\) bytes. Three times less, not bad. In my experiments, that was enough to eliminate the bottleneck in the L1 cache. Certainly, transformations could be quantized more aggressively but this feels like a good middle ground between simplicity, efficiency and size. I like how nicely it maps to [ VK_FORMAT_R16G16B16A16_UINT](https://www.khronos.org/registry/vulkan/specs/1.3-extensions/man/html/VkFormat.html). Two reads provide one transform.

One could also use `VK_FORMAT_R16G16B16A16_UNORM`

to get somewhat reasonable results out of linear texture interpolation between frames but I did not dare to try it. I think the interpolation for rotations and translations individually would make sense (at least with some additional sign flips on the quaternions) but their combination would not behave as desired. Since transforms are already sampled at 60 frames per second, there is little need for further interpolation.

## Compression of blend attributes

For each vertex, linear vertex-blend animation needs the indices of all bones that affect the vertex and the corresponding weights. A typical real-time renderer stores four indices and weights per vertex. The whole point of this project was to evaluate techniques for [compression of these blend attributes](http://momentsingraphics.de/I3D2022.html). The resulting methods compress so heavily that one can easily afford more influences per vertex. A bit contradictingly, this aspect of the file format is least sophisticated. Normally, I would directly store [compressed vertex attributes](http://momentsingraphics.de/ToyRenderer2SceneManagement.html#Quantization) in the file format, probably 8 bones in 48 bits using [permutation coding](http://momentsingraphics.de/I3D2022.html). Then this buffer is simply copied to the GPU during loading (along with the table of bone indices) and that's it.

Contrary to that, the file format stores 16-bit bone indices and 32-bit floats for weights. That takes quite a lot of memory but there are no rounding errors during export. [Upon loading](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/src/scene.c#L295) of the scene, many different compression methods can be applied to these data. That allows for direct comparisons. It is also possible to load ground truth and compressed data at the same time to analyze compression errors.

## Linear vertex-blend animation on the GPU

A classic way to implement linear vertex-blend animation is to let the CPU compute the transform for each bone in each frame. Then all transforms are uploaded to the GPU in a constant buffer. Contrary to that, my format makes the transforms for all frames available in one big texture. It is uploaded at startup. The only work the CPU has to do per frame is to write the frame index that should be displayed to a constant buffer.

Then the first step to apply animations in the vertex shader is to [decompress the blend attributes](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/src/shaders/forward_pass.vert.glsl#L156), i.e. the bone indices and the corresponding weights. There are plenty of interesting things to say about how that works but [the paper on permutation coding](http://momentsingraphics.de/I3D2022.html) covers this part well. To [apply vertex blending](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/src/shaders/forward_pass.vert.glsl#L258), the bone transforms for the bones with non-zero weights indicated by the bone indices are [loaded from the texture and decompressed](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/src/shaders/forward_pass.vert.glsl#L97). Then the transform is applied to the vertex position and the normal vector and the results are combined using the weights. [Applying quaternions](https://github.com/MomentsInGraphics/vulkan_renderer/blob/dd70c75f38ddb2fd439ad3a337eeff6846f8046f/src/shaders/forward_pass.vert.glsl#L122) is done most efficiently using a [method due to Fabian Giessen](https://fgiesen.wordpress.com/2019/02/09/rotating-a-single-vector-using-a-quaternion/). That's all.

Note that this is a fairly primitive way to go about vertex-blend animation. Techniques like dual-quaternion skinning [[Kavan2007]](http://momentsingraphics.de#_Kavan2007) could eliminate a few artifacts. Compared to more classic implementations, there is a bit more computation going on due to all the decompression but the reduced bandwidth requirements still make this run faster. [Figure 1](http://momentsingraphics.de#BlendAnimationBenchmark) shows a stress test. Without any level of detail or culling, it is no problem to handle 1400 character models with 100 million vertices.

![BlendAnimationBenchmark](../../assets/c409cf904760e127.png)

**Figure 1:**1400 animated character models with 100 million vertices where each vertex is influenced by up to 8 bones. This scene renders in 12.6 milliseconds on an NVIDIA RTX 2070 Super.

## Conclusions

When it comes to export and import of models, there are four basic things to take care of. Usually, geometry is the easiest. Simple standards like [Wavefront OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file) work. Materials get messy quickly since there are lots of subtleties to get wrong in the definition of BRDFs and material definitions may involve things like shader graphs. My approach of using [three textures to control the Frostbite BRDF](http://momentsingraphics.de/ToyRenderer2SceneManagement.html#Materials) is a good middle ground between simplicity and diversity of appearance. Then there are all the other scene objects, especially light sources and cameras. I have not bothered with those yet.

And finally, there are animations. Those also tend to get pretty complicated, especially when the animation system of the modeling software becomes intertwined with the one in the engine. Supporting inverse kinematics, physics simulation and various types of interactive control of animations is only possible if a lot of meta data about the skeleton are exported alongside the animation itself. By doing none of that, I have arrived at a very simple way to handle animations. I do not even export the tree structure of the skeleton, it is simply not needed. The exporter and importer are simple, there is no per-frame CPU overhead whatsoever and applying animations in the vertex shader is pretty efficient and straight forward.

## References

[ Magnenat-Thalmann, Nadia and Laperrière, Richard and Thalmann, Daniel (1989). Joint-Dependent Local Deformations for Hand Animation and Object Grasping. Proceedings on Graphics Interface '88, Canadian Information Processing Society. ][Official version](https://graphicsinterface.org/proceedings/gi1988/gi1988-4/)

[ Kavan, Ladislav and Collins, Steven and Žára, Jiří and O'Sullivan, Carol (2007). Skinning with Dual Quaternions. I3D '07: Proceedings of the 2007 Symposium on Interactive 3D Graphics and Games, ACM. ][Official version](https://doi.org/10.1145/1230100.1230107) | [Author's version](https://www.cs.utah.edu/~ladislav/kavan07skinning/kavan07skinning.html)