---
title: Collaborative design experiment
url: http://c0de517e.blogspot.com/2010/03/collaborative-design-experiment.html
author: M
published: '2010-03-14'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Every time I discuss about engine design, there is quite some interest and feedback going on.

So I figured out I could start a little experiment.

I've created a shared notepad with a few ideas, just open it and start adding your considerations, proposals and so on.


Update: I'd consider this experiment ended. I'm happy to see that many people took part of it, and it was a very nice experience, with some good discussions.


In the end the result may be probably more the expression of what I think than community driven but I think that's understandable, I don't believe that you can really successfully design something in a crowd. Also, I'm a tyrant and that does not help.


I'll post here a snapshot of the result of this game, but I'll keep the pad up and running until it dies naturally.


I'll be organizing something similar again soon, but I want to find something more specific and focused. Maybe some sort of competition using

Update: I'd consider this experiment ended. I'm happy to see that many people took part of it, and it was a very nice experience, with some good discussions.

In the end the result may be probably more the expression of what I think than community driven but I think that's understandable, I don't believe that you can really successfully design something in a crowd. Also, I'm a tyrant and that does not help.

I'll post here a snapshot of the result of this game, but I'll keep the pad up and running until it dies naturally.

I'll be organizing something similar again soon, but I want to find something more specific and focused. Maybe some sort of competition using

[codepad](http://codepad.org/).**- Layer -1: Prerequisites**

- Coding guidelines

- Along the lines of: Fuck C++ OOP. Data is the king. Keep compile times low.

- Build system

- Continous build system

- Static syntax checking

- Versioning system

- Code review system

**- Layer 0: Language extensions**

- Compiler abstraction

- Whyemory alignment and packing, forcing inline, branch hints and so on and on

- Stack walker

- Module/services system

- Why: avoid dependency hell. A module should be able to request access to another module, and depends on its interface, but it should not assume that any other module is up and running in order to execute.

- Proposal

- Each module will expose its interface for the other modules to statically link to. Upon loading, the module registers an instance implementing the interface in the module system, that is a (name,pointer) hashmap. Modules can declare dependencies on other modules, failing to load if the dependency is not loaded already, and being notified if the dependency unloads.

- 'root' object model

- Why: we need to have a common base interface for our objects. That will be used for RTTI (really, just a typeId, reflection can take care of everything else) and lifetime management (i.e. reference counting, creationg etc). A COM-like interface can be a solution.

- Memory allocators

- Why: Performance, debugging, quotas etc...

- Proposal

- A thin interface to request allocations and deallocations. Overrides for built-in C/C++ allocators to reroute third-party code. A configurable allocation framework that lets specify which algorithms to use for a given pools, memory quotas etc. Logging to debug fragmentation and leaks. Should support thread specific memory pools as well to avoid costly un-needed context switches in certain systems (would turn a bit complicated if ptrs were shared between threaded systems though)

- Object lifetime management

- Why: Explicit allocations and desctruction is not composable. It doesn't work well with a modularized code base.

- Proposals

- Smart-pointers. They are the only structure that lets you implement either garbage collection or reference counting. Prefer using only those

- Garbage collection: Reference counting is not so cool. Can leak in nasty ways (loops) and it's not so fast either. Requires to queque destructions in order to be executed in the "right" thread (i.e. graphic objects)

- Reference counting: A performant garbage collector is very hard to write. RC should not be made using intermediate handlers to hold refcount, for maximum performance the refcount should be inside the classes. Also, refcounts should not be explicitly accessible. Each class can implement its own AddRef/Release, the smart-pointers will statically dispatch those calls via templates. AddRef/Release methods still have to be virtual in order to support reflection (i.e. for scripting languages).

**- Layer 1: Core libraries**

- Multithreading support

- Why: To support multicore and heterogeneous computing environments

- Proposals

- Threads and locks support (C++ does not have a standard, we need our interface). Job scheduler/Thread pool with dependencies between jobs (data parallelism). Has to be SPU friendly. ParallelFor support. Dependencies between jobs can be of different types: normal (just sync), data (a job writes in a memory area, the dependants have access to that, data-parallel (a job processes an array of data structures, the scheduler manages the splitting of the array in different instances of the job), buffered (the jobs writes in a circular-buffer, the dependants read what the job produced last time it ran), steamed (like data-parallel, but assumes that the dependents do not need to wait for the whole array to be processed but can be fired as soon as any element is done).

- Inter-thread messaging is needed in many cases (i.e. schedule GPU work from the game or loading threads that do not own the rendering device)

- Check out: Intel TBB, Apple Grand Central, C# Parallel FX

- Resource layer

- Why: provide an abstracted access to file and network resources. Support for hotloading/swapping/streaming/async loading

- Proposal

- Hotloading means that everything has to be accessed using handles... (Not neccesarily, but not using them makes it messier. You have to notify the resource consumers that a resource has changed)

- Reflection system

- Why: Reflection/Introspection is needed for serialization, networking, live-editing (tools), scripting, garbage collection and so on

- Proposals

- A simple name hash for the type id. Parse the program debug database (i.e. PDB) and convert it into a reflection DB, as a compile step. Provide a pretty generic interface for reflection queries

- Pros: Avoids template/macro magic and stuff like that. The database can be loaded on demand and split to alleviate memory requirements. Complex queries are possible. Changing implementation does not require changing everything in the source. The database is accessible easily from other languages, can be used to gather code metrics, do coverage analysis and other stuff. Works with third-party code and libraries

- Cons: Less easy to provide custom attributes. Serialization often requires custom functions for some class members. Calling reflected functions (i.e. to instantiate a reflected class) requires compiler-specific trickery (You can use packaged function pointers - elaborate?)

- Math library

- Proposals

- Linear algebra: classes for Vector2, Vector3, Vector4, Matrix4x4, Matrix2x2, Quaternion and ScaleRotationTranslation class. Geometry: classes for primitive intersection, distance and various other shit as needed. Classes for VPU abstraction (SIMD). Random numbers...

- Pros: Having an SRT class lets you use a 3x4 affine matrix or quaternions internally. Also you can make sure that no skews are ever generated. The main math library should be SIMD friendly (align data) but VPU operations can be actually slower for general purpose computation (i.e. when doing a lot of logic, and scalar operations, branches). SIMD processing should be hand-optimized inside loops.

- Collections library

- Why: STL is not alignment-friendly. STL is not designed to be used in interfaces. Standard STL implementations are very hard to debug. Standard STL implementations won't play nicely with reflection. Performance varies on different platforms.

- Proposals

- We need a few specific containers that are fast when used as templates, but can be also generically passed around (an inspiration can be the C# containers). The API should stay close to STL when possible. vector, fixed_vector, hash_map, queue, stack, lockless_queque, n-ary tree, skip lists, probabilistic set (i.e. bloom filter), perfect hashing...

- Second option: Creating custom containers is too hard, just choose a good STL and add to that (memory allocators that respect a given alignment and maybe some extensions in terms of algorithms). Reflection would still be quite a problem

- Global parameter system

- Why: we need support for shared runtime parameters, reflection is 'only' about per-object stuff. Also reflection can't handle a parameter database like the one that is needed for shader parameters and so on...
- Proposal
- Parameters have to be organized in sections. We can have different types of sections, but I'd say we need at least: "external" read-only and linked to a database where the values can be organized in a meaningful way, "shared" where a spinlock is used to regulate the access to the class, "thread" that have to be accessed always from the same thread, "threadmessage" that are like "thread" but support a list of callbacks to be called when a parameter chages.

- Simply networking layer

- Why: to connect to pc-side tools. Needs to provide RFC (can leverage on reflection!). RFC can be used for automated testing as well...

- Profiling

- Logging

- Serialization/versioning

*Critique*

*To me here there is a dilemma. Should the framework be based, for its data, on reflection and serialization, or should it use a parameter database (materials, properties) and specific file formats (meshes, textures...)? Of course an answer could be "both" and I guess you need code for both, but there is still a design decision to be made here*

**- Layer 2: Low-level rendering infrastructure**

- Rendering device abstraction

- Why: to support multiple platforms/API

- Proposals

- DX11 style. No direct access to single renderstates and resources, block uploads. Support for multiple devices/command buffer recording. Mesh dispatch interface. Needs wrappers for meshes/streams/textures etc. Native API have always to be usable: device has to be stateless, or support state flushing/invalidation.

- Debug rendering interface

- Why: tools, graphs etc

- Proposals

- Primitives, text, lines etc... Immediate-mode drawing (beginPrimitive-pushVertex...-endPrimitive). Thread-safe (i.e. every command gets pushed into a lockless queque). Needs to support command sorting (i.e. differentiate between 2d draw and 3d debug objects)

- Debug GUI

- Why: widgets and so on...

- Proposals

- Effect system

- Why: To simplify creation of shaders and implentation of graphic techniques

- Proposals

- Similar to D3DXEffect, CgFx

- Natively integrated into low-level rendering infrastructure

- Parameter editing GUI

- Why: In game inspection and editing of the parameter system, uses the debug rendering and debug gui

- Graphic resource loaders

- Why: Implementation of resources (see the resource layer) for graphics assets

- Graphic data manipulation

- Why: Conditioning and runtime data generation. We need texture and mesh tools, that make working on the CPU with those resources as easy as doing that in the GPU. DXT compression is also needed.

**- Layer 3: User-level libraries**

- Scripting system/hooks

- Proposals

- Code-generated bindings from the reflection data
- still a lot of things missing obviously here, i.e. skinning, vertex/uv/geometry processing, lods, shadows, posteffects and so on. No consensus was reached on those

**- External Layer: Tools**

- Reflection inspector

- Automated testing

## 3 comments:

I've been building an engine and editor, with some of these goals. Added some text I had lying around from when I designed the core of my engine, though some stuff has changed, now that I have some more experience. See http://vapor3d.org/ for more information. :)

http://etherpad.com/ZPBJU3L3zV gives a 404 error

Yes, the experiment is over and etherpad does not exist anymore.

Post a Comment