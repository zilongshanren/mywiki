---
title: 'Porting from DirectX11 to OpenGL 4.2: API mapping'
url: https://anteru.net/blog/2013/porting-from-directx11-to-opengl-4-2-api-mapping
published: '2013-10-13'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Welcome to my Direct3D to OpenGL mapping cheat-sheet, which will hopefully help you to get started with adding support for OpenGL to your renderer. The hardest part for me during porting is to find out which OpenGL API corresponds to a specific Direct3D API call, and here is a write-down of what I found out & implemented in my rendering engine. If you find a mistake, please drop me a line so I can fix it!

## Device creation & rendering contexts

In OpenGL, I go through the usual hoops: That is, I create an invisible window, query the extension functions on that, and then finally go on to create an OpenGL context that suits me. For extensions, I use [glLoadGen](https://bitbucket.org/alfonse/glloadgen/wiki/Home) which is by far the easiest and safest way to load OpenGL extensions I have found.

I also follow the Direct3D split of a device and a device context. The device handles all resource creation, and the device context handles all state changes. As using multiple device contexts is not beneficial for performance, my devices only expose the “immediate” context. That is, in OpenGL, a context is just use to bundle the state changing functions, while in Direct3D, it wraps the immediate device context.

## Object creation

In OpenGL, everything is an unsigned integer. I wrap every object type into a class, just like in Direct3D.

## Vertex and index buffers

Work similar to Direct3D. Create a new buffer using [ glGenBuffers](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glGenBuffers.xhtml), bind it to either vertex storage (

[) or to index storage (](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glBindBuffer.xhtml)

`GL_ARRAY_BUFFER`

[) and populate it using](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glBindBuffer.xhtml)

`GL_ELEMENT_ARRAY_BUFFER`

[.](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glBufferData.xhtml)

`glBufferData`

## Buffer mapping

Works basically the same in OpenGL as in Direct3D, just make sure to use [ glMapBufferRange](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glMapBufferRange.xhtml) and not

[, which gives you better control over how the data is mapped, and makes it easy to guarantee that no synchronization happens. With](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glMapBuffer.xhtml)

`glMapBuffer`

[, you can mimic the Direct3D behaviour perfectly and with the same performance.](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glMapBuffer.xhtml)

`glMapBufferRange`

## Rasterizer state

This maps directly to OpenGL; but it’s split across several functions: [ glPolygonMode](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glPolygonMode.xhtml),

[/](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glEnable.xhtml)

`glEnable`

[for things like culling,](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glEnable.xhtml)

`Disable`

[, etc.](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glCullFace.xhtml)

`glCullFace`

## Depth/Stencil state

Similar to the rasterizer state, you need to use [ glEnable](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glEnable.xhtml)/

[to set things like the depth test, and then](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glEnable.xhtml)

`Disable`

[,](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glDepthMask.xhtml)

`glDepthMask`

[, etc.](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glDepthFunc.xhtml)

`glDepthFunc`

## Blend state

And another state which is split across several functions. Here we’re talking about [ glEnable](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glEnable.xhtml)/

[for blending in general, then](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glEnable.xhtml)

`Disable`

[to set the blend equations,](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glBlendEquation.xhtml)

`glBlendEquationi`

[,](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glColorMask.xhtml)

`glColorMaski`

[and](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glBlendFunc.xhtml)

`glBlendFunci`

[. The functions with the](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glBlendColor.xhtml)

`glBlendColor`

`i`

suffix allow you to set the blending equations for each “blend unit” just as in Direct3D.## Vertex layouts

I require a similar approach to Direct3D here. First of all, you can create one vertex layout per vertex shader program. This allows me to query the location of all attributes using [ glGetAttribLocation](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glGetAttribLocation.xhtml) and store them for the actual binding later.

At binding time, I bind the vertex buffer first, and then set the layout for it. I call [ glVertexAttribPointer](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glVertexAttribPointer.xhtml) (or

[, if it is an integer type) followed by](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glVertexAttribPointer.xhtml)

`glVertexAttribIPointer`

[and](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glEnableVertexAttribArray.xhtml)

`glEnableVertexAttribArray`

[to handle per-instance data. Setting the layout after the vertex buffer is bound allows me to handle draw-call specific strides as well. For example, I sometimes render with a stride that is a multiple of the vertex size to skip data, which has to be specified using](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glVertexAttribDivisor.xhtml)

`glVertexAttribDivisor`

[(unlike in Direct3D, where this is a part of the actual draw call.)](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glVertexAttribPointer.xhtml)

`glVertexAttribPointer`

The better solution here is to use [ ARB_vertex_attrib_binding](http://www.opengl.org/registry/specs/ARB/vertex_attrib_binding.txt), which would map directly to a vertex layout in Direct3D parlance and which does not require lots of function calls per buffer. I’m not sure how this interacts with custom vertex strides, though.

## Draw calls

That’s pretty simple once the layouts are bound, as you have to handle the stride setting there. Once this is resolved, just pick the function which maps to the Direct3D equivalent:

:`Draw`

`glDrawArrays`

:`DrawInstanced`

`glDrawArraysInstancedBaseInstance`

:`DrawIndexed`

`glDrawElementsBaseVertex`

:`DrawIndexedInstanced`

`glDrawElementsInstancedBaseVertex`

:`DrawAuto`

`glDrawTransformFeedback`

- DrawIndirect: OpenGL is much more powerful in this area, providing not only the basic
and`glDrawArraysIndirect`

, but also multiple indirect draw calls using the`glDrawElementsIndirect`

extension (core in 4.3)`ARB_multi_draw_indirect`


## Textures & samplers

First, storing texture data. Currently I use [ glTexImage2D](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glTexImage2D.xhtml) and

[for each mip-map individually. The only problem here is to handle the internal format, format and type for OpenGL – I store them along with the texture, as they are all needed at some point. Using](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glCompressedTexImage2D.xhtml)

`glCompressedTexImage2D`

[is however not the best way to define texture storage. These APIs allow you to resize a texture later on, which is something Direct3D doesn’t, and the same behaviour can be obtained in OpenGL using the](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glTexImage2D.xhtml)

`glTexImage2D`

[function. This allocates and fixes the texture storage, and only allows you to upload new data.](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glTexStorage2D.xhtml)

`glTexStorage2D`

Uploading and downloading data is the next part. For a simple update (where I use [ UpdateSubresource](http://msdn.microsoft.com/en-us/library/windows/desktop/ff476486%28v=vs.85%29.aspx) in Direct3D), I simply replace all image data using

[. For mapping I allocate a temporary buffer and on unmap, I call](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glTexSubImage2D.xhtml)

`glTexSubImage2D`

`glTexImage2D`

to replace the storage. Not sure if this is the recommended solution, but it works and allows for the same host code as Direct3D.Binding textures and samplers is a more involved topic that I have previously [blogged about in more detail](https://anteru.net/blog/2013/05/02/2119/). It boils down to statically assigning texture slots to shaders, and manually binding them to samplers and textures. I simply chose to add a new `#pragma`

to the shader source code which I handle in my shader preprocessor to figure out which texture to bind to which slot, and which sampler to bind. On the Direct3D side, this requires me to use numbered samplers, to allow the host & shader code to be as similar as possible.

Texture buffers work just like normal buffers in OpenGL, but you have to associate a texture with your texture buffer. That is, you create a normal buffer first using [ glBindBuffer](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glBindBuffer.xhtml) and

`GL_TEXTURE_BUFFER`

as the target, and with this buffer bound, you bind a texture to it and populate it using [.](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glTexBuffer.xhtml)

`glTexBuffer`

## Constant buffers

This maps to uniform buffers in OpenGL. One major difference is where global variables end up, in Direct3D, they are put into a special constant buffer called [$ Global](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509581%28v=vs.85%29.aspx), in OpenGL they have to be set directly. I added special-case handling for global variables to shader programs; in OpenGL, they set the variables directly and in Direct3D globals are set through a “hidden” constant buffer which is only uploaded when the shader is actually bound.

The nice thing about OpenGL is that it gives you binding of sub-parts of a buffer for free. Instead of using [ glBindBufferBase](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glBindBufferBase.xhtml) to bind the complete constant buffer, you simply use

[, no need to fiddle around with difference device context versions as in Direct3D.](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glBindBufferRange.xhtml)

`glBindBufferRange`

## Shaders

I use the [separate shader programs extension](http://www.opengl.org/registry/specs/ARB/separate_shader_objects.txt) to handle this. Basically, I have a pipeline bound with all stages set and when a shader program is bound, I use [ glUseProgramStages](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glUseProgramStages.xhtml) to set it to its correct slot. The only minor difference here is that I don’t use

[, but instead, I do the steps manually. This allows me to access the set the binary shader program hint (](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glCreateShaderProgram.xhtml)

`glCreateShaderProgram`

[), which you cannot obtain otherwise. Oh I grab the shader program log manually as well, as there is no way from client code to append the shader info log to the program info log.](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glProgramParameter.xhtml)

`GL_PROGRAM_BINARY_RETRIEVABLE_HINT`

For shader reflection, the API is very similar. First, you query how many constant buffers and uniforms a program has using [ glGetProgramiv](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glGetProgram.xhtml). Then, you can use

[to query a global variable and](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glGetActiveUniform.xhtml)

`glGetActiveUniform`

[,](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glGetActiveUniformBlock.xhtml)

`glGetActiveUniformBlockiv`

[to query everything about a buffer.](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glGetActiveUniformBlockName.xhtml)

`glGetActiveUniformBlockName`

## Unordered access views

These are called [image load/store](http://www.opengl.org/registry/specs/ARB/shader_image_load_store.txt) in OpenGL. You can take a normal texture and bind it to an image unit using [ glBindImageTexture](https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glBindImageTexture.xhtml). In the shader, you have a new data type called

`image2D`

or `imageBuffer`

, which is the equivalent to an unordered access view.## Acknowledgements

That’s it. What I found super-helpful during porting was the [OpenGL wiki](http://www.opengl.org/wiki/Main_Page) and the 8th edition of the [OpenGL programming guide](http://www.opengl-redbook.com/). Moreover, thanks to the following people (in no particular order): [Johan Andersson](https://twitter.com/repi) of DICE fame who knows the performance of every Direct3D API call, [Aras Pranckevičius](https://twitter.com/aras_p), graphics guru at Unity, [Christophe Riccio](https://twitter.com/g_truc), who has used every OpenGL API call, and [Graham Sellers](https://twitter.com/grahamsellers), who has probably implemented every OpenGL API call.