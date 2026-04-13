---
title: 'Integrating LuaJIT with X-Plane: 64-bit fun'
url: http://hacksoflife.blogspot.com/2012/12/integrating-luajit-with-x-plane-64-bit.html
author: Benjamin Supnik
published: '2012-12-09'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

X-Plane supports a plugin SDK; plugins are dynamic libraries loaded by the sim into it's process address space. X-Plane plugins link against a host library for access to the sim via a controlled API.


A number of popular plugins (Gizmo, SASL, FlyLua) provide Lua scripting to X-Plane add-ons using LuaJIT 2.0 as their Lua runtime engine.


LuaJIT on an x86_64 machine has an odd quirk: it requires all of Lua's allocations to be in the first 2 GB of address space. This requirement comes from its use of offset addresses, which apparently have a signed 32-bit range.


Normally on OS X 64-bit the only special work you have to do is customize the zero page region, as OS X defaults the zero page to the entire bottom 4 GB of memory. (I can only speculate that having the entire 32-bit address range be off limits helps catch programming errors where pointers are truncated to 32-bits because any truncated pointer will point to an illegal page.)


With X-Plane, however, we hit a snag: Lua scripts are often loaded by plugins late in the programs operation, when the user changes airplanes. By this time, the OS has already consumed all of the "Lua-friendly" address space below 2 GB. Looking at vmmap dumps, it looks like both the system malloc and OpenGL driver stack like this region of memory.


Here's how we 'fixed' this for 64-bit X-Plane:


This last step required a modification to LuaJIT itself; the shipping 2.0 code has the API for custom allocators disabled in 64-bits (probably under the assumption that client code wouldn't follow the "bottom 2 GB" requirement.) Fortunately the stub-out is just a series of #defines and the full API functionality is easily restored.A number of popular plugins (Gizmo, SASL, FlyLua) provide Lua scripting to X-Plane add-ons using LuaJIT 2.0 as their Lua runtime engine.

LuaJIT on an x86_64 machine has an odd quirk: it requires all of Lua's allocations to be in the first 2 GB of address space. This requirement comes from its use of offset addresses, which apparently have a signed 32-bit range.

Normally on OS X 64-bit the only special work you have to do is customize the zero page region, as OS X defaults the zero page to the entire bottom 4 GB of memory. (I can only speculate that having the entire 32-bit address range be off limits helps catch programming errors where pointers are truncated to 32-bits because any truncated pointer will point to an illegal page.)

With X-Plane, however, we hit a snag: Lua scripts are often loaded by plugins late in the programs operation, when the user changes airplanes. By this time, the OS has already consumed all of the "Lua-friendly" address space below 2 GB. Looking at vmmap dumps, it looks like both the system malloc and OpenGL driver stack like this region of memory.

Here's how we 'fixed' this for 64-bit X-Plane:

- The host sim pre-allocates as much of the 2 GB region as it can early on, in fixed size chunks. Currently we're using 32 MB chunks, but this may change.
- The host provides a custom Lua realloc function that is implemented using a hacked version of dlmalloc; dlmalloc uses the pool of pre-grabbed 32 MB chunks to form its pools.
- Plugins use lua_newstate to connect the host's "chunk" allocator to the Lua runtime.

The 1.6 GB of virtual address space the sim grabs up front don't become actual memory allocations until plugins request the memory via Lua, because OS X is lazy about committing memory. Because the address space is pre-grabbed, VM allocates and mmaps that happen later in the app's life cycle simply go to higher address spaces.

There is one limitation to the implementation as it runs now: allocations larger than 32 MB will fail because the 'direct' allocation API in dlmalloc is not functional. In theory the host allocator could search for consecutive 32 GB blocks to form larger allocations, but I suspect that in practice we'll simply set the chunk size larger. Typical X-Plane based Lua scripts don't need huge amounts of memory (or at least it appears this way so far) and the number of separate blocks needed is based on the number of simultaneous Lua plugins running, which is also typically quite low.*

* By quite low I mean only one plugin at a time; as far as I can tell Lua plugins often export the runtime with global external symbols, which causes complete chaos. That's the subject of another blog post.

## No comments:

## Post a Comment