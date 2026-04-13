---
title: 'Status report: New scene graph, OpenGL, C++11 and other'
url: https://anki3d.org/status-report-scene-graph-opengl-c11/
author: Panagiotis Christopoulos Charitos
published: '2012-05-27'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

It’s been a long time since we had a status report. This doesn’t mean that AnKi is left behind but the new features are so difficult to implement and they require a big period of design, thinking and prototyping. One of the most important things that are going to be redesigned is the scene graph. It will move from a hierarchy based design to a component based one. This makes the engine very configurable and the process of adding new kind of objects far more easier. The downside of the scene graph reconstruction is that it requires re-design of the renderer as well. Both these modules are complex and changing them is very time consuming. At the present moment the scene is finished but the renderer is not yet.

Another module that got a face lift is the OpenGL. The idea is to make a wrapper that sits on top of OpenGL API that will offer an abstraction for different OpenGL implementations and latter who knows, maybe an API abstraction as well. The interesting things about the OpenGL module though is it’s thread safety and numerous optimizations that minimize the GL API calls. Especially the Texture class offers quite a few optimizations with the texture units and how the binding works.

Apart from the individual modules there is a broader change that affects almost everything, the move from C++03 to C++11. The idea here is to drop the boost library and make the engine more self sustained and less dependent to external libraries. This choice introduced and it will introduce quite a few problems though. The first is that the compilers are not that stable yet. Some of the features only live on the latest GCC and LLVM versions and I doubt they have been tested for production quality software. Another drawback is that some of the C++11 features have been implemented in the latest versions of LLVM and GCC. This practically means that you won’t be able to compile AnKi without GCC > 4.7 and LLVM > 3.1. The last drawback is to compiler support in general. At the present time only GCC and LLVM have a good C++11 support. This is not bad because AnKi is targeted for those two compilers but it wouldn’t hurt to be compilable by Intel’s compiler as well.

When the scene graph and renderer are over there are lots of changes and features that wait in line:

- Optimize the renderer. Removal of multiple render targets in deferred shading.
- Implement the loose octrees for visibility tests. Also add and test occlusion queries.
- Remove Python and put LUA. Preferably without LUA bind (because it requires boost).
- Remove SDL and write code for X11 directly. SDL still does not support shared context creation.
- Introduce two OpenGL targets. OpenGL 4.x and OpenGL ES 3.x. Especially the ES one (far future)
- Port the engine to Android with OpenGL ES 3.x hardware (far future)

That’s all.

PS: AnKi always seeks developers that want to help so if you are interested in contributing contact the main developer.