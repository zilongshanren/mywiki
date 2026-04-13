---
title: 'Experiments in GPU-based occlusion culling part 2: MultiDrawIndirect and mesh
  lodding'
url: https://interplayoflight.wordpress.com/2018/01/15/experiments-in-gpu-based-occlusion-culling-part-2-multidrawindirect-and-mesh-lodding/
author: Kostas Anagnostou
published: '2018-01-15'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

A few weeks ago I posted an [article](https://interplayoflight.wordpress.com/2017/11/15/experiments-in-gpu-based-occlusion-culling/) on how the GPU can be used to cull props, using a Hi-Z buffer of occluding geometry depths and a computer shader, and drive rendering without involving the CPU. This approach worked well but there were 2 issues that were not addressed: the first was being forced to call DrawInstancedIndirect once per prop, due to the lack of support for MultiDrawInstancedIndirect in DX11, and the second was the lack of support for mesh level-of-detail (LOD) rendering. The second point is particularly important as most games will resort to this type of mesh optimisation to improve performance. So I revisited the described GPU culling method to investigate how one could address those. As in the previous blog post, I tried to maintain the requirement for minimal art modification and content pipeline changes.


Although MultiDrawInstancedIndirect is not supported by Direct3D 11, it is exposed by some IHVs via [driver extensions](https://docs.google.com/spreadsheets/d/1J_HIRVlYK8iI4u6AJrCeb66L5W36UDkd9ExSCku9s_o/edit#gid=0). Both NVidia and AMD (unfortunately not Intel) support this so I went ahead and integrated the [NVAPI](https://developer.nvidia.com/nvapi) to my test application to use that feature. The Multidraw API is simple, after NVAPI has be initialised all one has to do is to call the method like this.

NvAPI_D3D11_MultiDrawIndexedInstancedIndirect( d3dImmediateContext, drawCount, //drawCount, renderingContext.m_instanceArgsBuffer->GetBuffer(), 0, //alignedByteOffsetForArgs 5 * sizeof(UINT) //alignedByteStrideForArgs );

The main input to NvAPI_D3D11_MultiDrawIndexedInstancedIndirect is the arguments buffer, which contains per drawcall data used for rendering. The buffer format and contents are the same as in the case of DrawIndexedInstancedIndirect and it contains drawCount “rows” (or groups of 5 unsigned ints, if you prefer), one per drawcall:

UINT IndexCountPerInstance UINT InstanceCount UINT StartIndexLocation UINT BaseVertexLocation UINT StartInstanceLocation

Picking up from the [previous blog post](https://interplayoflight.wordpress.com/2017/11/15/experiments-in-gpu-based-occlusion-culling/) (if you haven’t read it yet, it might be worth reading it first), we have a system in place that culls, using a Hi-Z buffer, all instances of all meshes in the scene, and produces an array of drawcall arguments that is then used for rendering using one DrawIndexedInstancedIndirect per mesh.

This system can be used in this case as well with few modifications, we will mainly need to account not only for instances of a mesh, but also for mesh lods and to batch rendering data.

### Batching

In contrast to DrawIndexedInstancedIndirect, which is called once per prop (mesh) to render all its instances and supports “per prop” set up (textures, shaders, constant buffers etc), MultiDrawIndexedInstancedIndirect should ideally be called once to render all instances of all props. This requires large amounts batching to work properly, for example adding all vertices to a single, large vertex buffer (same for index and instance data), add textures to texture arrays and all constants to a large constant buffer.

For this demo I copied geometry data for all props to large buffers (for vertices and indices). Last time I used a structured buffer to pass instance data to the vertex shader, instead of a separate vertex buffer, this time I went all-buffer using one typed buffer per vertex attribute (position, normal and uv coordinate in my case). Then we can perform manual vertex data fetching in the vertex shader using the VertexID (which is provided by the system to the vertex shader). I still used a regular index buffer to pass the vertex indices through as it is the only way to activate the [post transform cache](https://www.khronos.org/opengl/wiki/Post_Transform_Cache) to avoid redundantly shading vertices.

A sidenote, since each drawcall in the Arguments buffer is accompanied by offsets to vertex and index data, we don’t have to modify indices at all, it is just a matter of copying data over.

There [are](https://forum.beyond3d.com/threads/programmable-vertex-fetching-and-index-buffering.57591/) [reports](https://turanszkij.wordpress.com/2017/06/05/should-we-get-rid-of-vertex-buffers/) that feeding data to the vertex shader with typed buffers can increase performance on AMD’s GCN, but probably not on NVidia GPUs. An additional, potential advantage of manual vertex fetching, especially in cases where heavy batching takes place (like MultiDrawIndexedInstancedIndirect), is that it allows us to make on-the-fly decisions about what data to fetch for each batched prop, based on its material/distance from the camera etc. If we don’t care about normal mapping because a prop is far away and doesn’t need it, we can choose not to read from the tangents buffer and avoid the tangent frame calculations. Finally, by [creatively using the index buffer](https://forum.beyond3d.com/threads/programmable-vertex-fetching-and-index-buffering.57591/) to store more than one indices per element we can achieve different frequency per vertex attribute. This can be useful in cases, for example, we need hard edges with more than one normal per vertex.

Additionally, one would need to add all textures to texture arrays, which will be accessed by a drawcall/mesh/mesh lod ID. This works well for textures of same size but might be problematic if we support different texture resolutions per prop. In some cases it might make sense to add material property textures of the same type in a separate texture array, i.e. all albedo textures to a single array, all normal maps to a different one etc. It is worth bearing in mind the restriction of 2048 textures per texture array as well.

We also have to consider per material constant data which typically would live in a separate constant buffer per drawcall. In this case it is possible to batch the constant data for all drawcalls in a single constant buffer “array”, accessed by the drawcall or mesh ID (any id we find convenient really, could be per mesh lod):

struct PerObjectData { float4 Colour; float Roughness; float Metalness; float Emissive; // more data }; cbuffer cbPerObject : register(b2) { PerObjectData PropData[2]; };

If we know the maximum number of required constant buffers beforehand we can declare the array accordingly, else we can leave it “dynamic” (declaring it of size 2) which works as long as we don’t try to read outside the bounds of the bound constant buffer.

Worth remembering is that a constant buffer can store a maximum of 4096 float4 values. In case we have more data to store we can use a structured buffer instead, although this might come with a [performance hit](https://developer.nvidia.com/content/how-about-constant-buffers).

In this experiment I didn’t go as far as batching textures in textures arrays but I have used a constant buffer array to implement different materials.

### Mesh Level of Detail

[Mesh Level of Detail (lod)](https://en.wikipedia.org/wiki/Level_of_detail) is a widely used optimisation technique in which we produce simplified (lower vertex count) versions of a mesh to use when rendering the mesh far away from the camera. This not only reduces the vertex shader cost but also improves the triangle to pixel ratio so that we don’t shade subpixel triangles. Rendering lower lod meshes can also speed up the shadow pass and even the Hi-Z generation for the occlusion pass.

In this case I have added a few lods for each mesh, each lod having a different index/vertex count. I am using a single buffer to store all vertices (across mesh/lods), the same for indices and instance data. Each mesh lod is handled as a different drawcall in the argument buffer. This is convenient since every mesh lod can have different number of vertices and indices, without the need to add any padding.

In summary, this is what the buffers look like, after the culling/stream compaction step:

![buffers](../../assets/82afdbd18de5a20a.png)


It is worth pointing out that the instance data are stored, grouped, per mesh lod. This is necessary as each drawcall accesses the instance data with an offset and a count. This also means that we can’t globally sort all instances (across all meshes) based on distance, although this is also a problem with instanced rendering in general. In the demo I try to mitigate this by distance sorting (on the CPU) the instances of a specific mesh before I copy the data to the instance data buffer.

Finally, it is quite possible that a drawcall does not do any rendering (does not point at anything in the instance data buffer), meaning that all the instances for a the particular mesh lod got culled.

### Rendering

Since I pass all data through typed buffers and not regular vertex buffers, the offsets provided in the arguments buffers are not of much use, they are only useful when data is passed through the Input Assembler. The only data exposed in this case is the VertexID and the InstanceID, with no offsets applied. In the previous blog post I bypassed this limitation by binding the Arguments buffer to the vertex shader and accessing per-drawcall data with a drawcall ID I passed through a constant buffer. In case of MultidrawIndirect this is not possible as I can’t bind different constant buffers per drawcall. To make matters worse there is no DrawcallID system value for Direct3D like the gl_DrawID that is available in OpenGL.

One option would be to abandon my plan to use typed buffers and use regular vertex buffers for all data instead. In such a case the offsets would kick in and each drawcall would access the correct data. After some head scratching, and not wanting to give up, I decided at first to pass the drawcall ID through the index buffer, combining 2, 16 bit values (one for the drawcall ID and the other for the vertex index) to a 32 bit one. That worked, since the offset to the index buffer is applied, and I could then retrieve the drawcall ID and access the correct data in the arguments buffer, but it doubled the size of my index buffer which is not very appealing. A sidenote: in cases where 16 bits for the index buffer is not enough but 32 is too much and you end up using a smaller range than the available, this approach might have some merit, for example use 24 bits for the index and the rest 8 for the drawcall ID.

I needed something with less frequency to the index buffer to store the drawcall ID and this is the instance buffer, which has one entry per instance. In the end I had to compromise a bit and create a single 16-bit vertex buffer which stored the drawcall ID per instance and bind it to the vertex shader via the Input Assembler. In this case the Instance buffer offset stored in the Arguments buffer kicked in and provided me the correct drawcall ID per instance.

struct VS_INPUT { uint DrawcallID : DRAWCALLID; uint VertexID : SV_VertexID; uint InstanceID : SV_InstanceID; }; VS_OUTPUT VSMain(VS_INPUT Input) { VS_OUTPUT Output; //get index to the arguments buffer and the vertex index uint meshLodIndex = Input.DrawcallID; uint vertexIndex = Input.VertexID; //get offset into the vertex buffer uint vertexBufferOffset = InstanceArgs[meshLodIndex * 5 + 3]; //get offset into the instances buffer uint instanceBufferOffset = InstanceArgs[meshLodIndex * 5 + 4]; //get vertex position float3 position = Positions[vertexIndex + vertexBufferOffset].xyz; //get normal float3 normal = Normals[vertexIndex + vertexBufferOffset].xyz; //get uv coord float2 uv = UVs[vertexIndex + vertexBufferOffset].xy; //get world matrix for this instance matrix world = Instances[Input.InstanceID + instanceBufferOffset].World; // perform rest of processing }

The vertex buffer for the drawcall ID is written to, via an Unordered Access View, in the computer shader that performs the stream compaction. This is necessary as it has to match the data in the instance data buffer.

Finally all we need to do is bind everything, call NvAPI_D3D11_MultiDrawIndexedInstancedIndirect() and get all lodded props rendering with one drawcall per pass!

In the above video I have used different colours/roughness per prop to demonstrate constant buffer batching in action. Also the big occluders are rendered “semi transparent” so that we can see the results of the culling pass.

Also, the following video demonstrates the lodding that takes place during rendering, using different colours per mesh lod (red is LOD0, closer to the camera, yellow is LOD1, etc).

To be able to perform per lod and per mesh rendering, I combined the mesh LOD and the mesh ID in a value that I store per instance. That way I can access the constant buffer data, which in my case is per mesh (not mesh lod).

That’s it more or less, we managed to get all meshes rendering, with lods, with a single drawcall and without any changes to the content pipeline/art.

As I mentioned earlier, this extension is only supported, in Direct3D11, by NVidia and AMD but not Intel. In case we need to support Intel GPUs, MultiDrawIndexedInstancedIndirect is pretty much a direct replacement of the for-loop I used in the previous blog post and we could use that in its place:

for (UINT i = 0; i < drawCount; i++) { d3dImmediateContext->DrawIndexedInstancedIndirect( argumentsBuffer, i * 5 * sizeof(UINT) ); }

The question now is: is it worth doing all that work if we can’t access a MultiDrawIndexedInstancedIndirect extension? The answer would be, in most cases, yes especially if the number of shader permutations in a pass is low, as is often if, for example, you are using g-prepass. Most of the cost in a drawcall is not the drawcall itself but in the setting up we need to do before it, setting buffers, textures, shaders etc. With batching we eliminate all that and the game will still benefit even if we have to call DrawIndexedInstancedIndirect multiple times.

Here is a [link to the source code/executable](https://1drv.ms/u/s!AmOPA68QU4JIiNY8eHBrKOCtLOxp6A) if anyone wants to investigate further. To compile it you will need to download the [NvAPI](https://developer.nvidia.com/nvapi) and the [Assimp](http://assimp.sourceforge.net/main_downloads.html) library.

[…] Experiments in GPU-based occlusion culling part 2: MultiDrawIndirect and mesh lodding […]

[…] Experiments in GPU-based occlusion culling part 2: MultiDrawIndirect and mesh lodding […]

[…] Experiments in GPU-based occlusion culling part 2: MultiDrawIndirect and mesh lodding […]

[…] Информацию об его использовании см. в [1] и [2]. RenderDoc блокирует расширение MultiDraw, поэтому в […]

[…] shows calls to NvAPI_D3D11_MultiDrawIndexedInstancedIndirect. For information on its use, see (1) and (2) RenderDoc blocks the MultiDraw extension, so in EventBrowser they are expanded into many […]