---
title: 'Status report: Tile based deferred shading renderer, LUA and external dependencies'
url: https://anki3d.org/status-report-tile-based-deferred-shading-renderer-lua-and-external-dependencies/
author: Panagiotis Christopoulos Charitos
published: '2012-08-10'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

Some of the planed features of AnKi were discussed in the previous status report. Fortunately some of them were implemented but some are still under way. The interesting ones are a new optimized renderer architecture that uses tile based deferred shading, the other important change is that the engine’s scripting engine is now LUA with a custom binder solution and the last mega feature is the rethinking of the external libraries that AnKi uses.

One of the main goals of the past months were to remove/revise some of the external dependencies that AnKi had. Libraries like boost, Python and SDL were making the building of AnKi a bit complicated especially for some new targeted platforms (ARM Linux, Android etc). To solve that problem first I removed the pre-compiled external libraries (.so and .a) and created CMake for each of these libraries. Now for example libpng source lies in it’s own directory (extern/png) and it is connected to the AnKi general build system. The good thing about this is that we ensure that by having only a C++11 compiler you can build AnKi down to the last bit without the need to install or build anything yourselves. The second step was to remove some of the external libraries that made life difficult and/or lacked a few features. Boost replaced with C++11, Python with the lightweight LUA and the much loved SDL with custom backends (GLX/X11, EGL/X11 and more will follow). To see the external libraries and the way the are organized checkout the the source: svn co http://anki-3d-engine-externals.googlecode.com/svn/trunk

The last feature that is worth writing is the new renderer architecture. The tile based deferred shading renderer boosted the performance quite a bit. To be precise it doubled the speed of the rendering. An article is planed that will explain the implementation that AnKi uses along with some benchmarks.

For the future:

- Renderer: Move everything to using UBOs
- Renderer: Re-enable HDR and SSAO
- Core: Add loading thread that supports GL
- Scene: Finalize the octree optimizations
- Math: Make the library template based. Add NEON support
- Add GLES 3.0 support
- Add Android support