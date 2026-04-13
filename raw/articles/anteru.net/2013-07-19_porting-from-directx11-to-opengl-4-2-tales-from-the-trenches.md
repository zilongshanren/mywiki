---
title: 'Porting from DirectX11 to OpenGL 4.2: Tales from the trenches'
url: https://anteru.net/blog/2013/porting-from-directx11-to-opengl-4-2-tales-from-the-trenches
published: '2013-07-19'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I’m still busy porting my framework from DirectX 11 to OpenGL 4.2. I’m not going into the various reasons why someone might want to port to OpenGL, but rather take a look at my experience doing it.

## Software design

In my framework, the render system is a really low-level interface which is just enough to abstract from Direct3D and OpenGL, and not much more. It explicitly deals with vertex buffers, shader programs, and rasterizer states, but does so in an API agnostic manner. Higher-level rendering services like rendering meshes are built on top of this API. For games, it might make sense to do the render layer abstraction slightly higher and deal with rendering of complete objects, but for me, low-level access is important and the abstraction has worked fine so far.

What I did every time I added a feature to my rendering backend is to double-check the OpenGL and Direct3D documentation to make sure I only introduce functions that will work with both APIs. Typically, I would stub out the method in the OpenGL backend and implement it properly in Direct3D, but remove any parameter which is not supported by the other API.

I’m targeting OpenGL 4.2 and Direct3D 11.0 in my framework. There three reasons for OpenGL 4.2:

- It’s the first OpenGL to support
(or UAVs in Direct3D.)`shader_image_load_store`

- It’s the latest one supported both by AMD and NVIDIA
- It has everything I need in core, so I can avoid using extensions.

Let me elaborate the last point a bit. Previously, with OpenGL 2 and 3, I did use extensions a lot. This turned out to be no good solution, as I often ran into issues where one extension would be missing, incorrectly implemented, or other problems. In my new OpenGL backend, extensions are thus nearly completely banned. Currently, I only use three extensions: Debug output, anisotropic filtering and compressed texture format support. The debug output extension is only used in debug builds, and the reason I’m not using the core version is that AMD does not yet expose it.

Enough about the design, let’s go ahead into practice!

## Differences

Truth to be told, OpenGL and Direct3D are really similar and most of the porting is straightforward. There are some complications when binding resources to the shader stages. This includes the texture handling as well as things like constant buffers. I’ve described my approach to [textures and samplers previously](https://anteru.net/blog/2013/05/02/2119/); for constant buffers (uniform blocks in OpenGL), I use a similar scheme where I statically partition them between shader stages. One area which I don’t like at all is however how input layouts are handled. This is solved mostly by OpenGL 4.3 which provides [ vertex_attrib_binding](http://www.opengl.org/registry/specs/ARB/vertex_attrib_binding.txt), but currently I have to bind the layout after binding the buffer using lots of

`glVertexAttribPointer`

function calls. Works, but not so nicely.For texture storage, there’s no difference now as OpenGL has [ texture_storage](http://www.opengl.org/registry/specs/ARB/texture_storage.txt). For image buffers and UAVs, there’s no difference either, you simply bind them to a slot and you’re done; with OpenGL, it’s a bit easier as you don’t need to do anything when creating the resource. Shader reflection is very similar as well, except how OpenGL exposes names stored in constant buffers. In Direct3D, you query a block for all its variables. In OpenGL, you’ll get variables stored in buffers too if you just ask for all active uniforms, and if you query a buffer, you get the full name of each variable including the buffer name. This requires some special care to abstract away. Otherwise, the only major difference I can think of is the handling of the render window, which is pretty special in OpenGL as it also holds the primary rendering context.

Interestingly, while I have been extending and fixing the OpenGL support, I didn’t have to change the API. This shows how close they actually are, because all my early checking was a brief look into the OpenGL specification to find the corresponding function and make sure I don’t expose parameters which are not available in either of the APIs.

## Porting

For the actual porting, we have to look back a bit into the history of my framework. Originally, it started with an OpenGL 2.0 backend, and Direct3D 9 was added later. When I switched over to Direct3D 10, the OpenGL backend got updated to 3.0 and I was keeping feature parity mostly between the Direct3D 9 & 10 and the OpenGL 3.0 backend. Later, I removed the Direct3D 9 backend and rewrote the render API around the Direct3D 10/11 model. At this point, I’ve also updated the OpenGL backend from 3.0 to 4.0, but I only implemented a subset of the complete renderer interface due to time constraints.

This year, I’ve starting porting by converting applications over, one-by-one. Typically, I would take a small tool like the geometry viewer and make it run with OpenGL, implementing all stubs and fixing all problems along the way. For testing, I would simply run the application in question and switch the rendering backend using a configuration option. If both produced the same result, I would be happy and move along to the next application. This turned out to work quite well most of the time, but recently, I’ve hit some major issues which required a more systematic and thorough approach to testing.

In particular, my voxel viewer, which is a pretty complex application with manual GPU memory management, UAVs, complex shaders and a highly optimized inner rendering loop, just didn’t work when I implemented the three missing features in the OpenGL backend (texture buffers, image load/store support, and buffer copies.) And here is where the sad story starts, debugging OpenGL is in a terrible state currently. I tried:

[apitrace](http://apitrace.github.io/), which mostly worked (seems to have some issues with separate shader objects and state inspection)[GPUPerfStudio2](http://developer.amd.com/tools-and-sdks/graphics-development/gpu-perfstudio-2/): Would make my application produce errors which it didn’t have before (invalid parameters being passed to functions)[NSIGHT](http://www.nvidia.com/object/nsight.html): Doesn’t work with Visual Studio 2012 …[Intel GPA](http://software.intel.com/en-us/vcsource/tools/intel-gpa): No OpenGL

Well, which means I had to get back to the simple debugging methods, writing small test applications for each individual feature. Behold, the triforce of instanced draw calls:

![Instanced draw debug application running under OpenGL 4.2.](../../assets/95fed3ee2b7cfbed.png)

![Instanced draw debug application running under Direct3D 11.](../../assets/b11cc7889fede93e.png)

You have to believe me that the applications do actually use different backends, even though they look similar. Actually, they are pixel-perfect equal to allow me to do automated testing some day in the future. Writing such small tests is how I spent the last two days, and while I haven’t nailed down the particular issue with the voxel viewer, I’ve found quite a few quirks and real issues along the way. For the images above, this is the complete source code of the test application:

```
#include <iostream>
#include "niven.Core.Runtime.h"
#include "niven.Core.Exception.h"
#include "niven.Engine.BaseApplication3D.h"
#include "niven.Render.DrawCommand.h"
#include "niven.Render.Effect.h"
#include "niven.Render.EffectLoader.h"
#include "niven.Render.EffectManager.h"
#include "niven.Render.RenderContext.h"
#include "niven.Render.VertexBuffer.h"
#include "niven.Render.VertexLayout.h"
#include "niven.Core.Logging.Context.h"
using namespace niven;
namespace {
const char* LogCat = "DrawInstancedTest";
}
/////////////////////////////////////////////////////////////////////////////
class DrawInstancedTestApplication : public BaseApplication3D
{
NIV_DEFINE_CLASS(DrawInstancedTestApplication, BaseApplication3D)
public:
DrawInstancedTestApplication ()
{
}
private:
void InitializeImpl ()
{
Log::Context ctx (LogCat, "Initialization");
Super::InitializeImpl ();
camera_->GetFrustum ().SetPerspectiveProjectionInfinite (
Degree (75.0f),
renderWindow_->GetAspectRatio (), 0.1f);
camera_->SetPosition (0, 0, -16.0f);
effectManager_.Initialize (renderSystem_.get (), &effectLoader_);
shader_ = effectManager_.GetEffectFromBundle ("RenderTest",
"DrawInstanced");
static const Render::VertexElement layout [] = {
Render::VertexElement (0, Render::VertexElementType::Float_3, Render::VertexElementSemantic::Position)
};
layout_ = renderSystem_->CreateVertexLayout (layout,
shader_->GetVertexShaderProgram ());
static const Vector3f vertices [] = {
Vector3f (-6, -4, 4),
Vector3f (0, 4, 4),
Vector3f (6, -4, 4)
};
vertexBuffer_ = renderSystem_->CreateVertexBuffer (sizeof (Vector3f),
3, Render::ResourceUsage::Static, vertices);
}
void ShutdownImpl ()
{
Log::Context ctx (LogCat, "Shutdown");
effectManager_.Shutdown ();
Super::ShutdownImpl ();
}
void DrawImpl ()
{
shader_->Bind (renderContext_);
Render::DrawInstancedCommand dc;
dc.SetVertexBuffer (vertexBuffer_);
dc.vertexCount = 3;
dc.SetVertexLayout (layout_);
dc.type = Render::PrimitiveType::TriangleList;
dc.instanceCount = 3;
renderContext_->Draw (dc);
shader_->Unbind (renderContext_);
}
private:
Render::EffectManager effectManager_;
Render::EffectLoader effectLoader_;
Render::Effect* shader_;
Render::IVertexLayout* layout_;
Render::IVertexBuffer* vertexBuffer_;
};
NIV_IMPLEMENT_CLASS(DrawInstancedTestApplication, AppDrawInstancedTest)
int main (int /* argc */, char* /* argv */ [])
{
RuntimeEnvironment env;
try {
env.Initialize ();
DrawInstancedTestApplication app;
app.Initialize ();
app.Run ();
app.Shutdown ();
} catch (const Exception& e) {
std::cout < e < std::endl;
} catch (const std::exception& e) {
std::cout < e.what () < std::endl;
}
return 0;
}
```


While certainly time consuming, this seems to be the way forward to guarantee feature parity between my two backends and also to have easy to check test cases. In the future, this stuff seems like a good candidate for automated testing, but this requires quite a bit of work on the test runner side. In particular, it should be able to capture the screen contents from outside of the application itself to guarantee that the result on-screen is actually the same and it should be written in a portable manner.

So much for now from the OpenGL porting front, if you have questions, just comment or drop me an email.