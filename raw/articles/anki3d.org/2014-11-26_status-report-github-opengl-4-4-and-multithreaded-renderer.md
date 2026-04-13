---
title: 'Status report: github, OpenGL 4.4 and multithreaded renderer'
url: https://anki3d.org/status-report-github-opengl-4-4-and-multithreaded-renderer/
author: Panagiotis Christopoulos Charitos
published: '2014-11-26'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

The first important change is the new home of AnKi. From now on AnKi’s source code lives on github and the address is [https://github.com/godlikepanos/anki-3d-engine](https://github.com/godlikepanos/anki-3d-engine). In the technical side of things there is a brand new OpenGL 4.4 backend with a multithreaded rendering thread. In this new concept there is a dedicated thread exclusively serving OpenGL work. Other small features are the screenspace local reflections effect, removal of C++ exceptions, some steps towards a complete removal of STL (new string, dynamic array etc).

For the future we have plans to add Windows support. Steps have been made with AnKi compiling on Windows. Unfortunately there are some bugs that we need to address before declaring full Windows support. Another planed feature is integration with Newton Dynamics physics engine. Compared to bullet Newton seems less buggy, with more features and the most important for me is that its interface is superior (a simple C API). Other small features is an improved tile base deferred renderer, improved transparency, cascaded shadowmaps, OpenGL ES 3.1 support and other.