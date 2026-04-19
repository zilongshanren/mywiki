---
title: Visual Scripting the Data-Oriented Way
url: https://bitsquid.blogspot.com/2010/09/visual-scripting-data-oriented-way.html
author: Niklas
published: '2010-09-17'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

The second system, which is the focus of this post, is a visual scripting system that allows artists to add behaviors to levels and entities. We call this system

*Flow*.

Lua and Flow have different roles and complement each other. Lua allows gameplay programmers to quickly test designs and iterate over gameplay mechanics. Flow lets artists enrich their objects by adding effects, destruction sequences, interactivity, etc. When the artists can do this themselves, without the help of a programmer, they can iterate much faster and the quality is raised.

Flow uses a pretty standard setup with nodes representing actions and events. Black links control how events cascade through the graph causing actions to be taken. Blue links represent variables that are fed into the flow nodes:

In this graph, the green nodes represent events and the red node represents an action. The yellow node is an action implemented in Lua. The gameplay programmers can set up such actions on a per-project basis and make them available to the artists.

Each unit (= entity) type can have its own flow graph, specifying that unit's behavior, e.g. an explosion sequence for a barrel. There is also a separate flow graph for the entire level that the level designers can use to set up the level logic.

Since

*Flow*will be used a lot I wanted to implement it as efficiently as possible, both in terms of memory and performance. This means that I

*don't*use a standard object-oriented design where each node is a separate heap-allocated object that inherits from an abstract

*Node*class with a virtual

*do_action()*method. That way lies heap allocation and pointer chasing madness.

Sure, we might use such a design in the

*editor*, where we don't care about performance and where the representation needs to be easy to use, modifiable, stable to version changes, etc. In the

*runtime*, where the graph is static and compiled for a particular platform, we can do a lot better.

(This is why you should keep your editor (source) data format completely separate from your in-game data format. They have very different requirements. One needs to be dynamic, multi-platform and able to handle file format version changes. The other is static, compiled for a specific platform and does not have to care about versioning -- since we can just recompile from source if we change the format. If you don't already -- just use JSON for all your source data, and binary blobs for your in-game data, it's the only sane option.)

The runtime data doesn't even have to be a graph at all. There are at least two other options:

- We could convert the entire graph into a Lua program, representing the nodes as little snippets or functions of Lua code. This would be a very flexible approach that would be easy to extend. However, I don't like it because it would introduce significant overhead in both CPU and memory usage.
- We could "unroll" the graph. For each possible external input event we could trace how it flows through the graph and generate a list of triggered actions as a sort of "bytecode". The runtime data would then just be a bytecode snippet for each external event. This has the potential of being very fast but can be complicated by nodes with state that may cause branching or looping. Also, it could potentially use a lot of extra memory if there are many shared code paths.

So I've decided to use a graph. But not a stupid object-oriented graph. A data-oriented graph, where we put the entire graph in a single blob of cohesive memory:

Oh, these blobs, how I love them. They are really not that complicated. I just concatenate all the node data into a single memory chunk. The data for each node begins with a node type identifier that lets me

*switch*on the node type and do the appropriate action for each node. (Yes, I'll take that over your virtual calls any day.) Pointers to nodes are stored as offsets within the blob. To follow a pointer, just add the offset to the blob's start address, cast the pointer to something useful and presto!

Yes, it is ok to cast pointers. You can do it. You don't have to feel bad about it. You know that there is a

*struct ParticleEffectNode*at that address. Just cast the pointer and get it over with.

The many nice things about blobs with offsets deserve to be repeated:

- We can allocate the entire structure with a single memory allocation. Efficient! And we know exactly how much memory it will use.
- We can make mem-copies of the blob without having to do any pointer patching, because there are no pointers, only offsets.
- We can even DMA these copies over to a SPU. Everything is still valid.
- We can write the data to disk and read it back with a single call. No pointer patching or other fixups needed.

In fact, doesn't this whole blob thing look suspicously like a file format? Yes! That is exactly what it is. A file format for memory. And it shouldn't be surprising. The speed difference between RAM and CPU means that memory is the new disk!

If you are unsure about how to do data-oriented design, thinking "file formats for memory" is not a bad place to start.

Note that there is a separate blob for dynamic data. It is used for the nodes' state data, such as which actor collided with us for a collision event (the blue data fields in the flow graph). We build that blob in the same way. When we compile the graph, any node that needs dynamic data reserves a little space in the dynamic blob and stores the offset to that space from the start of the dynamic block.

When we clone a new entity, we allocate a new dynamic data block and memcopy in the template data from the dynamic data block that is stored in the compiled file.

Sharing of dynamic data (the blue links in the graph) is implemented by just letting nodes point to the same offset in the dynamic data blob.

Since we are discussing performance, I should perhaps also say something about multithreading. How do we parallelize the execution of flow graphs?

The short answer: we don't.

The flow graph is a high level system that talks to a lot of other high level systems. A flow graph may trigger an effect, play a sound, start an animation, disable a light, etc, etc. At the same time there isn't really any heavy CPU processing going on in the flow graph itself. In fact it doesn't really do anything other than calling out to other systems. Multithreading this wouldn't gain a lot (since the compute cost is low to begin with) and add significant costs (since all the external calls would have to be synchronized in some way).

This looks like a really interesting and useful tool, and I could see it being used for simple AI and Animation behavior flow as well, in which case I could also see needing to multithread it (you'd already stated that you can push the entire flow graph off to the SPU for processing pretty easily).


ReplyDeleteIn the cases where a flow graph needs to talk to another system, couldn't you extrapolate out the system interactions into a switchboard / message passing system? Would that make sense or would even when using Flow to diagram animation / behaviors would that add too much overhead?

Yes, in theory you could run the flow graph on an SPU and let it generate a list of action messages to be processed by the PPU. (You also need to let the flow graph query the world, which is trickier, but doable.)






ReplyDeleteBut I don't think you would gain much from that, because the nodes don't really do much besides run actions. I.e., processing the action messsages on the PPU will take almost as much time as running the flow graph. So you haven't really gained anything by involving the SPUs.

As I see it, the flow graph is a high level system that connects a bunch of low level systems. It is in these low level systems that the actual processing happens and they are properly multithreaded.

In the design, I am consciously enforcing this perspective, by not adding anything that is compute-heavy to the flow graph itself. For example, there is no update() call to flow graphs. Flow graphs only react when triggered by a specific event. Everything that needs to tick every frame is handled by a lower level system.

For animation for instance, we have three systems on a lower level than the flow graph. AnimationPlayer, that evaluates curves into poses. AnimationBlender, that blends multiple poses together. And AnimationStateMachine which runs a state machine (also edited with a graph editing tool). All of these systems are multihtreaded.

The flow graph talks to the animation state machine by sending events (32 bit string hashes) such as "jump" or by setting variables, e.g. "jump_height = 2". So the flow graph can drive animation without actually doing much processing by itself.

Nice write up. I really like your phrase "file formats for memory" - this is a brilliant way to explain these ideas to others.




ReplyDeleteInstead of switching on the node type, you could index into a jump-table/vtable although the switch should compile down to a jump too but there is often a range check that cannot be removed without compiler assistance (like GCC's computed goto). This kind of thing might help to alleviate any troubles with OO dogma.

You could perhaps think of the offsets as pointers. What are pointers anyway? They aren't always machine addresses. These things (compressed, less pointerful/pointy data structures) resemble private heaps (or memory spaces/arenas). The static ones are the best because they need such little overhead in terms of maintenance structures like free lists. The dynamic arena you describe would perhaps need no free list either if the Flow script is short lived and the whole dynamic area can be reset when the script has executed.

Are your nodes all the same size? Perhaps if they were different sizes then some of the dynamic data (that isn't truly dynamic) could be moved into the node area?

A vtable might be good idea as you suggest. I don't think it has that much impact on performance, but as you say in some cases it may make for nicer code.



ReplyDeleteYes, I already think of the offsets as pointers. Typically the script is associated with an entity or a level and lives as long as that entity/level lives. When it dies, the entire dynamic area is deallocated at once. The dynamic area does not grow or shrink... the allocation of the dynamic data is done at "compile time".

Nodes can be different sizes. So yes, some of the dynamic data that isn't could be moved to the static area to save dynamic memory. I've thought about that. The downside is that the nodes will have to check on every variable access if it is dynamic or static, so it will make the code a lot more complicated and branchy. So far it hasn't seemed worth it.

Thanks for the reply Niklas. I love how the dynamic areas can be deleted in one foul swoop. Makes for very cheap GC.


ReplyDeleteStill missing the distinction between your static node areas and your dynamic (but precomputed at compile time) areas.

Dynamic means they can change, and each instance gets a separate copy. A typical example would be a Counter node with Increase and Decrease outputs. The Counter node would use a dynamic int to store the current value of the counter.



ReplyDeleteAt data compile time, all nodes specify how much dynamic memory they want (the Counter node wants four bytes) and they get an offset back that specifies where to find their memory in the dynamic data block. The size (and initial value) of the dynamic memory block is determined.

When a flow graph is instanced, a copy is made of that memory and all subsequent operations on that instant use the dynamic copy to store the data.

เว็บสล็อต

ReplyDeleteNiyama is Sanskrit for "rules, instructions, or observances." The niyamas appear in Hindu and Buddhist texts, but are best known as the second branch of the eight branches of yoga as described in Patanjali's Yoga Sutras.


ReplyDelete