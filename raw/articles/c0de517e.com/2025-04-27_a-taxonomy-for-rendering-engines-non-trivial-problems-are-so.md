---
title: A Taxonomy for Rendering Engines.Non-trivial problems are solved only in context.
url: https://c0de517e.com/021_taxonomy.htm
author: Angelo Pesce
published: '2025-04-27'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

**It's time to grow up.**
One of the main objectives behind the

[REAC](https://enginearchitecture.org) conference we (Steve, Stephanie, Natalya, Michael and I) organize now every year is to share the kind of "hard won" lessons on the craft of real-time rendering that are currently not possible to learn outside working in our industry for decades (and possibly, on many different projects and companies...).

Gamedevs and Computer Graphics people are a great community, we do share a lot when it comes to how things are made, we are proud of pushing the state of the art forward and we want others to know about it! It's undeniable that without this openness, we would not be able to produce the incredible technology we have today. But, in many ways, we are still a young industry, we love to talk about shiny things, not as much the "less glamorous" behind the scene decisions that most often make all of the difference.

And because we are not used to doing this, we are not great at it! I was talking with someone (I'll ask them later if they want to appear by name) a few days ago about how they "hate" architecture talks, as most often are just showing how a given thing works - whilst not providing with the kind of context useful to evaluate if that solution would be good to consider.

I fully agree! I think it will take us, as an industry, some time to understand how to best present these lessons. It's the difference between a lazy post about the "10 habits of successful CEOs" and an academic text that tries to develop a theory of management.

**Theories require assumptions, context, they need to be replicable, falsifiable.**
A good start would be to develop a taxonomy of real-time rendering engines. A language to describe the context.

This is... normal, in all mature technologies. Let's think for example about

[databases](https://db-engines.com). Nobody would say "this is how you make a database", that's such a vague statement. What kind of database? Relational, key-value, time-series, vector, graph, spatial, columnar? With what characteristics? Concurrent reads, writes or both? Distributed? Consistent? Persistent (durable)? Transactional? From the set of high-level use-cases and technological requirements we then can talk about algorithms and data structures, architectures - develop a theory and practice.

Perhaps we also were spoiled by the relative simplicity of graphics-related objectives. The rendering equation, in the rush towards photorealism, provided a simple, objective metric of progress we could compare to. And for the rest, more objects, more polygons, more textures, per unit of memory and time - was a good universal proxy of what we wanted to achieve. The tight loops that power our GPUs are relatively simpler to talk about than the remaining 90% of the engine around them.

**A(n example) taxonomy: 3x3 dimensions.**
Here are a few dimensions we might want to consider:


1) Product characteristics.


- Engine users. From narrow to widest: Single team proprietary, Multiple teams, Single-genre middleware, Multi-genre middleware, User-Generated Content platform.


- Platform support. Single-platform (e.g. web, or PlayStation), Multi-platform, Multimodal (Computers, Mobiles, Consoles, Web, Cars, VR...)


- Scalability needs. Is it a goal to target primarily a small set of devices with roughly comparable capabilities, or is the engine made to scale? Scale content down (level of detail), up (procedural detail generation) or both?


2) Production: people & process.


- Content abstraction. Is the engine an API for ad-hoc rendering code (i.e. no content pipelines, engine is a draw abstraction), or is it data-driven? If the latter, is the data "generic" (arbitrary mesh attributes with shaders / shadergraphs) or must it adhere to narrow schemas (specialized/"hardcoded" rendering loops per schema type)?


- Iteration. Does the engine prioritize live editing of its data (no baking - common for UGC as well) or is it made for "baking"? How long does it take from change to review?


- Users. Who is the engine made for? Artist-driven or Engineering-driven production? Does the engine target experts or is it meant to be easy to use?


3) Technological requirements.


- Latency. Can data be double and triple buffered to aid parallelism, or do we need to execute as eagerly as possible?


- Dynamics. What data do we constrain to remain static, and what is allowed to change?


- Streaming. None (in-core rendering), local (disk-to-memory), distributed (cloud/server to client).


**The tenth dimension.**
...is success (or scale). This is arguably the most important one, but I consider this to be true for software engineering in general - not something specific about 3d rendering.

**Technology with no users is** (mostly)

**trivial**. Engineering problems scale exponentially with the number of users of a product, both current and total during its historical development. And similarly, with the team size needed to develop said product.

It might be tempting to think that code is orthogonal to scale - a good idea is a good idea, but that's not true. Team size and organization changes how code needs to be structured, but even algorithmically, certain solutions might be harder to maintain at scale, too complex to develop and so on.

**Conclusions?**
With these attributes we could describe most architectural choices in-context. What is the best threading model? Depends on latency requirements. What's the best API or draw call abstraction? Depends on platform support and content type. What's the best way to get updates from the game/simulation? Depends on how dynamic our engine needs to be, how many entities can change per frame and how. What's the best data structure to describe a scene? Depends on the content type and user expectations - and so on.

And yet, I'm not calling for the adoption of these categories as a standard for engine discourse, it would be needlessly verbose and I don't think there is any value in a rigid structure. Mine is an invitation for people to think more, and present what they consider the best descriptors of the context relevant to given choices - not to blindly follow this example.

Narrowly applied engines might need more specification in order to provide context. An engine made to push the state-of-the-art in interactive photorealism for architectural visualization might need different choices from an engine for a racing game or one for a top-down strategy tile - and nowadays, real-time 3d is used by more and more industries. But I suspect it to be relatively rare that "stylistic" choices make a big difference on architectural choices compared to these more structural attributes.

We are becoming a mature industry, it's less likely we'll invent new gaming ideas that will get us orders-of-magnitude bigger franchises, more likely AAA will want to reach more people more efficiently. "Commoditization". We'll need a better language for that, and a new focus.

(thanks to M.Vance for reviewing an advance copy)