---
title: A Macro View of Nanite
url: https://www.elopezr.com/a-macro-view-of-nanite/
author: Redorav
published: '2021-05-30'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

After showing an impressive demo last year and unleashing recently with the UE5 preview, Nanite is all the rage these days. I just had to go in and have some fun trying to figure it out and explain how I think it operates and the technical decisions behind it using a [renderdoc](https://renderdoc.org/) capture. Props to Epic for being open with their tech which makes it easier to learn and pick apart; the editor has markers and debug information that are going to be super helpful.

This is the frame we’re going to be looking at, from the epic showdown in the Valley of the Ancient demo project. It shows the interaction between Nanite and non-Nanite geometry and it’s just plain badass.

**Nanite::CullRasterize**

The first stage in this process is Nanite::CullRasterize, and it looks like this. In a nutshell, this entire pass is responsible for culling instances and triangles and rasterizing them. We’ll refer to it as we go through the capture.

**Instance Culling**

Instance culling is one of the first things that happens here. It looks to be a GPU form of frustum and occlusion culling. There is instance data and primitive data bound here, I guess it means it culls at the instance level first, and if the instance survives it starts culling at a finer-grained level. The Nanite.Views buffer provides camera info for frustum culling, and hierarchical depth buffer (HZB) is used for occlusion culling. ~~The HZB is sourced from the previous frame and forward projected to this one. I’m not sure how it deals with dynamic objects, it may be that it uses such a large mip (small resolution) that it is conservative enough.~~ EDIT: According to the [Nanite paper](http://advances.realtimerendering.com/s2021/Karis_Nanite_SIGGRAPH_Advances_2021_final.pdf), the HZB is generated this frame with the previous frame’s visible objects. The HZB is tested with the previous objects as well as anything new and visibility updated for the next frame.

Both visible and non-visible instances are written into buffers. For the latter I’m thinking this is the way of doing what occlusion queries used to do in the standard mesh pipeline: inform the CPU that a certain entity is occluded and it should stop processing until it becomes visible. The visible instances are also written out into a list of candidates.

**Persistent Culling**

Persistent culling seems to be related to streaming. It is a fixed number of compute threads, suggesting it is unrelated to the complexity of the scene and instead maybe checks some spatial structure for occlusion. This is one complicated shader, but based on the inputs and outputs we can see it writes out how many triangle clusters are visible of each type (compute and traditional raster) into a buffer called MainRasterizeArgsSWHW (SW:compute, HW:raster).

**Clustering and LODding**

It’s worth mentioning LODs at this point as it is probably around here where those decisions are made. Some people [speculated](https://twitter.com/reduzio/status/1398467641782714371) [geometry images](http://hhoppe.com/proj/gim/) as a way to do continuous LODding but I see no indication of this. Triangles are grouped into patches called clusters, and some amount of culling is done at the cluster level. The clustering technique has been described before in papers by [Ubisoft](https://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf) and [Frostbite](https://frostbite-wp-prd.s3.amazonaws.com/wp-content/uploads/2016/03/29204330/GDC_2016_Compute.pdf). For LODs, clusters start appearing and disappearing as the level of detail descends within instances. Some very clever magical incantations are employed here that ensure all the combinations of clusters stitch into each other seamlessly.

**Rasterization**

There seem to be two forms of rasterization present in the capture: compute and traditional draw-based. The previous buffer contained the arguments for two indirect executes that run these drawcalls.

- Render 3333 instances of 384 vertices each
- Run 34821 groups of this compute shader

The first drawcall uses traditional hardware-based rasterization. The criteria for choosing one or the other is unclear but if I had to guess it would be related to the size of the triangles relative to the size of the pixels. Epic has mentioned [before](https://twitter.com/briankaris/status/1261098487279579136) that a compute rasterizer can outperform hardware in specific scenarios whereas in others the hardware has an edge. These scenarios relate to how the hardware chokes on very small triangles as it’s unable to schedule them efficiently, hurting occupancy and performance. I can find several instances of large triangles, but it’s hard to tell by just looking at it.

The information above also gives us an insight into cluster size (384 vertices, i.e. 128 triangles), a suspicious multiple of 32 and 64 that is generally chosen to efficiently fill the wavefronts on a GPU. So 3333 clusters are rendered using the hardware, and the dispatch then takes care of the rest of the Nanite geometry. Each group is 128 threads, so my assumption is that each thread processes a triangle (as each cluster is 128 triangles). A whopping ~5 million triangles! These numbers tell us over 90% of the geometry is software rasterized, a confirmation of what Brian Karis said [here](https://www.eurogamer.net/articles/digitalfoundry-2020-unreal-engine-5-playstation-5-tech-demo-analysis). For shadows the same process is followed, except at the end only depth is output.

The above process is repeated for a subset of geometry in the Post Pass. The reason for this seems to be that Nanite creates a more up to date HZB (in BuildPreviousOccluderHZB) with this frame’s depth information up to that point, combines it with the ZPrepass information (that stage happened before Nanite began) and uses that information to do more up to date occlusion culling. I wonder if the selection criteria for what gets culled here is at the “edges” of the previous depth buffer to avoid popping artifacts, or on geometry that was not visible last frame.In any case the output from the rasterization stage is a single texture that we’ll talk about next.

**Visibility Buffer**

One of Nanite’s star features is the visibility buffer. It is a R32G32_UINT texture that contains triangle and depth information for each pixel. At this point no material information is present, so the first 32-bit integer is data necessary to access the properties later. Visibility buffers are not a new idea and have been discussed before (for example [here](https://www.gdcvault.com/play/1023792/4K-Rendering-Breakthrough-The-Filtered) and [here](http://diaryofagraphicsprogrammer.blogspot.com/2018/03/triangle-visibility-buffer.html)) but as far as I know no commercial game has shipped with it. If deferred rendering decouples materials from lighting, this idea decouples geometry from materials: every pixel/triangle’s material is evaluated exactly once and no textures, buffers or resources are accessed that are later occluded. The visibility buffer is encoded as follows:

R [31:7] | R [6:0] | G |
ClusterID (25 bits) | Triangle ID (7 bits) | 32-bit Depth |


There is an upper limit of ~4 billion (232) triangles, which I would have said is plenty in another time; now I’m not so sure anymore. One thing I have found very interesting here is how limited the information is. Other [visibility buffer proposals](https://onedrive.live.com/view.aspx?resid=EBE7DEDA70D06DA0!115&app=PowerPoint&authkey=!AP-pDh4IMUug6vs) suggested storing barycentric coordinates. Everything is being derived later by intersecting the triangle with the camera ray, reading the data from the original buffer, and recomputing/interpolating vertex quantities on the fly. This is described [here](http://jcgt.org/published/0002/02/04/) in detail. As a final note, it is remarkable to see that crevice behind where the character is supposed to be standing to see the culling efficiency of the system.

**Nanite::EmitDepthTargets**

This phase outputs three important quantities: depth, motion vectors and ‘material depths’. The first two are standard quantities that are later used for things like TAA, reflections, etc. There is an interesting texture called the Nanite Mask that just indicates where Nanite geometry was rendered. Other than that, this is what they look like:


**Material Depth**

However, by far the most interesting texture output by this phase is the Material Depth. This is essentially a material ID turned into a unique depth value and stored in a depth-stencil target. Effectively, there is one shade of grey per material. This is going to be used next as an optimization that takes advantage of Early Z.


**Nanite::BasePass**

Hopefully by now we have a good understanding of the geometry pipeline. Up to now, we’ve talked nothing at all about materials. This is quite interesting because between the visibility buffer generation and now, the frame actually spends a lot of time doing other things: light grid, sky atmosphere, etc and also renders the GBuffer as it would normally. This really drives home the separation between geometry and materials that the Visibility Buffer aims for. The important steps are inside Classify Materials and Emit GBuffer.

**Classify Materials**

The material classification pass runs a compute shader that analyzes the fullscreen visibility buffer. This is very important for the next pass. The output of the process is a 20×12 (= 240) pixels R32G32_UINT texture called Material Range that encodes the range of materials present in the 64×64 region represented by each tile. It looks like this when viewed as a color texture.

**Emit GBuffer**

We have finally reached the point where visibility meets materials, the point that the visibility buffer is all about, turning triangle information into surface properties. Unreal allows users to define arbitrary materials to surfaces so how do we efficiently manage that complexity? This is what Emit GBuffer looks like.

We have what looks like a drawcall per material ID, and every drawcall is a fullscreen quad chopped up into 240 squares rendered across the screen. One fullscreen drawcall per material? Have they gone mad? Not quite. We mentioned before that the material range texture was 240 pixels, so every quad of this fullscreen drawcall has a corresponding texel. The quad vertices sample this texture and check whether the tile is relevant to them, i.e. whether any pixel in the tile has the material they are going to render. If not, the x coordinate will be set to NaN and the whole quad discarded which is a [well-defined operation](https://twitter.com/MittringMartin/status/1107770271119736833).

As far as I can tell, the system uses 14 bits for material IDs, for a total of 16384 maximum materials. A constant buffer sends the material ID to the vertex shader so that it can check whether it’s in range.

On top of that, let’s remember that we created a material depth texture where every material ID is set to be a certain depth. These quads are output to the depth represented by their material and the depth mode is set to equal, so the hardware can then very quickly discard any pixels that aren’t relevant. As an extra step the engine has previously marked the stencil buffer as pixels that have nanite geometry and regular pixels, also used for Early Stencil optimizations. To see what this all means let’s look at the albedo buffer.


You may have noticed some of the quads are completely red, which I would have thought would be completely discarded by the vertex shader. However I think the material range texture is exactly what it says, a range of materials covered by that tile. If a material happens to be “in the middle” but none of the pixels have it, it will be considered as a candidate even though the depth test will discard it totally later. In any case that’s the main idea, the same process as shown in the images is repeated until all materials are processed. The final GBuffer is shown as tiles below.

**Closing Remarks**

Nanite ends at this point, and the rest of the pipeline carries on as normal thanks to the material decoupling deferred rendering offers. The work that has been put into this is truly remarkable. I’m sure there are a ton of details I am not aware of and imprecisions regarding how it works so I’m really looking forward to seeing what Brian Karis has to say about it at his SIGGRAPH deep dive this year.

HI,

can you give some hint on how to capture with render doc ?

1. I tried loaded the renderdoc plugin, then I can see the capture button in viewport, when it is not PLAY

2. If I play it, then the renderdoc icon inside viewport goes away.

how do we capture with renderdoc when in play mode ?

Hi jackz,

One thing you can do from renderdoc is “Attach to running instance” which will display applications that have renderdoc currently injected. From UE5 you can also select Play options, wheter to spawn in a new window or current window, etc. which might help you

Hello, I am a CG domain from China. Can I translate into Chinese to share it on our platform?

Hi pansking,

I’m happy for you to translate it into whatever language you like as long as you credit and link to this article

I don’t speak a word of Chinese but I’d love to see it anyway 🙂

Came here from CG domain. Thanks Emilio, Thank you pansking.

Thank you for your kind comment Xingyan, I hope you enjoyed it

Emilio, thanks a bunch for sharing this, supeer helpful

Thanks Rodrigo, I’m glad you liked it

Pingback: Unreal’s Nanite – A brief overview – Flying Pixels!

Thank you for doing such a detailed study! The culling techniques in use is what frightens me the most, because I watched the presentation, and it seems so complicated with the combination of compute shaders and data structures.

Do you think that driver vendors will be implementing this in the near foreseeable future?

I’m hoping that Khronos and Microsoft are taking long notes, because artist LOD’s should be a thing of the past, but I just don’t see how writing a pipeline like this is viable for game developers. Unless, of course, everybody starts using Unreal. Which is bad for competition.

Hi Alexander,

I don’t see how this is something a driver vendor would or should implement, in the same way that LODs aren’t something they currently take care of. I wouldn’t see the culling itself as the most complicated part, it’s the data format, meshlet decimation, the image continuity that I think is the secret sauce and where most of the research has probably gone into.

In the same way LOD generation is something tooling like Simplygon can help with, meshlet generation is something tools can do. However, 3rd party software for videogames is something there seems to be not a lot of lately, and companies like Epic and Unity gobble up whatever’s still left.

Epic has created an artist first ecosystem that is very hard for inhouse engines to compete with. It’s very hard to predict where it will go, and it looks like it will change the way many people work. I’d say though only the most realism-intensive game shops will benefit a lot from it. Other studios have been creating impressive games with proven pipelines and they’ll probably continue to do so using different tech. Even for UE5 studios, there are other considerations beside raw performance like size on disk/RAM, streaming requirements, etc. that every studio will have to make a judgement call on.

I am with you though on the idea that slowly, most studios seem to be moving to UE5. While the innovations Epic is putting out there are impressive, it is sad that it all seems to converge to a single way of making games.

Thank you for your reply. I will be a bit philosophical (I hope that’s okay) – I’m not an expert, far from it, but I see a trend:

20 years ago there were no standardizations. Nowadays, most game companies converge to standardized rendering strategies (deferred, decals, post FX, TAA, etc.). PBR is becoming a standard. We are seeing certain file formats take over (glTF), and others slowly dying out (obj).

Making games is a ridiculously complicated undertaking. But having standards means that we can share work with others, get help online, read the same books, program for the same platforms (libraries, memory models, joystick buttons, multi-threaded hardware). I would not mind, really, if the approach that Unreal is taking with Nanite becomes a universal standard, because in most ways it seems better – they just need to solve a few “minor” issues like animation, foliage, and over-drawing (apparently?).

I think the only way to make games, going forward, is for everybody to use the same tools (with minor variations). But it all has to be open-source and royalty-free. I don’t see it working any other way.

Am I dreaming? My thoughts are long-term (like 20-30 years). Or perhaps, nobody will be programming anymore – we will just tell an AI what kind of game we want and it will make it in a couple of seconds.. world is going to get crazy!