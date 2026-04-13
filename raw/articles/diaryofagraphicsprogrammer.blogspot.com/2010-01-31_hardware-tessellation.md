---
title: Hardware Tessellation
url: http://diaryofagraphicsprogrammer.blogspot.com/2010/01/hardware-tessellation.html
author: Wolfgang Engel
published: '2010-01-31'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I was thinking about the advantages of Hardware Tessellation. I can see mainly three:

- Compression

Reduces on-disk storage, system, video memory usage ->only the coarse mesh is stored

Animation data is only stored for the coarse mesh

- Memory bandwidth

GPU fetches only vertex data of coarse mesh through PCI-E bus -> higher vertex cache and fetch performance

- Scalability

Subdivision is recursive -> offers auto-LOD with adaptive metrics


With the DirectX 11 implementation it might also reduce the workload of the vertex shader because the shader transforms or animates only the coarse mesh. But if we add up the additional workload of the hull and domain shader it might be a wash.


For console developers, being able to store more world geometry on disc and in memory would be a great advantage. The reduction of the read memory bandwidth -while reading the data from memory- would also increase the efficiency.

The main question is if tessellating the geometry puts such a huge workload on the GPU that it is not feasible. I would love to have some real-world data here ...

## 9 comments:

Hello,



There is the Unigine benchmarck which feature such tesselation but I did not found performance test on the web.

If you have a DX11 card may be you can run it and at least give us the framerate difference w and w/o tesselation! (even if frame time in ms would have been better)

Also, I wonder which one is the fastest:

- render LoD 0 with tesselation to LoD 10 (10 "subdivisions" on the GPU), or,

- render LoD 5 with tesseleation to LoD 10 (5 "subdivision" on the GPU)

But in the end, the rendered mesh could be visually different...

The biggest problem with tesselation is that you basically need to support it from the start. If you end up making the scene look great without it there is very little reason to do twice the work getting hardware tesselation going.



Here are some benchmarks of the Heaven Benchmark sebh.

http://www.hardocp.com/article/2009/11/06/unigine_heaven_benchmark_dx11_tessellation/

You have to remember that without tesselation enabled all of the geometry is completely flat. So it is not comparable to real world results (as seen in Dirt 2 etc)

The hardocp numbers are interesting. Thanks for posting this. This is a substantial difference in performance. Looking at the Heaven Benchmark: it is probably not comparable to an open-world game level in size.

Tessellation in D3D11 isn't really recursive though. You have to specify tessellation per-patch, you can't say "okay, do one more iteration and ask me again for each sub-patch" like you'd need to do in order to get good adaptive LOD. Right now you'd have to pre-tessellate the control mesh to isolate the high detail areas and the flat areas into different patches so you can make a good decision per-patch ("this patch is flat"/"this patch is detailed"), you can't have a patch that's 99% flat with a spike in the middle that needs extra detail.

Not sure if this makes sense, but maybe a fourth reason for hw tess: make the GPU-created illusion of smooth surfaces available for algorithms that really only look at geometry.




Before our title had per pixel lighting, we had a phase where third party authors were manually over-tessellating meshes to reduce lighting error. With per pixel lighting this is unneeded.

But the over-tessellated meshes produced better GPU-generated shadows, since the silhouette is accurate.

If the "curve" of a triangle (per pixel, for lighting) comes from varying interpolation and not from the original art asset, tessellation with a scheme like PN-triangles could make an asset look equally "curved" for shadow map generation.

Another advantage for tesselation i realized recently is the dramatic quality increase in dual paraboloid shadow maping and reflections (which basically look wrong because geometry can't "bend"). With tesselation, i guess geometry should bend perfectly.

Tessellation can make facet shadow map more efficient. It can eliminate the several times of geometry rendering part with stencil.


The reason why the facet shadow map renders 8 times with a stencil buffer is on vertex shader we cannot bend geometry so that we mimic it.

Try playing Sculptris, its a small program for Digital sculpting..

I think the method is automatic subdivision & mesh tesselation..

Hello,


I get the whole concept of this tessellation process. But what I don't quite understand is the way the tessellation is being done. Can someone elaborate on the step by step process of the tessellation. As in, how, with what and such sorta questions. Would be great :)

P.S. Wolfgang Engel. You, sir are doing a great work ! Respect from India !!

Post a Comment