---
title: 'Debris: Opening the box'
url: https://fgiesen.wordpress.com/2012/02/13/debris-opening-the-box/
published: '2012-02-13'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Debris: Opening the box

It’s now been almost 5 years since we (farbrausch) released [fr-041: debris](http://www.farbrausch.com/prod.py?which=2), and almost 8 years since the somewhat ill-fated [.kkrieger](http://www.farbrausch.com/prod.py?which=114). We tried to package that technology up and sell it for a while, which I wasn’t particularly happy with when we decided to start doing it and extremely unhappy with by the time we stopped :). We decided to dissolve the company that owned the IP (.theprodukkt GmbH) about two years ago, a process that was finished last summer. Some months ago we got the tax returns for our last fiscal year; I missed the party on account of currently being on another continent from my other co-founders.

So now both the tech and the code are somewhat orphaned. We could just release the source code into the public, but frankly it’s an unholy mess, and you’re likely to miss all the cool bits among the numerous warts. I’ve done source releases before, and we might still do it with Werkkzeug3 (the tool/framework behind the two aforementioned productions and nineteen others). But I’d really rather present it in a somewhat more curated form, where I highlight the interesting bits and get to sweep all the mess behind it under the rug. So here’s the idea: this post contains a list of things in Debris that I think might make for an interesting post. Unlike my “Trip Through The Graphics Pipeline 2011” series, this list is far too long to just decide on a whim to do all of it. So instead, you get to vote: if there’s anything on this list that you’d like me to write about, post a comment. If there’s sufficient interest and I’m in the mood, I’ll write a post about it. :)

The one thing I’m *not* going to talk about is about our [tool](http://www.farbrausch.com/prod.py?which=115)-centric way of producing demos. Chaos and me have talked about that several times and I’m getting bored of the topic (I think there’s videos on the net, but didn’t find anything on my first Google-sweep; will re-check later). Also, some of the topics have dependencies among each other, so I might decide to post something on the basics first before I get into specifics. Just so you’re warned. Anyway, here’s the list:

### Source code

### Basics / execution environment

- Operators (the building block of our procedural system)
- Writing small code on Win32/x86 (in C++)
- Executable compression
- Memory Management on the editor side
- The Operator Execution Engine (demo/player side)

### Texture generation

- How to generate cellular textures
[part 1](https://fgiesen.wordpress.com/2010/03/28/how-to-generate-cellular-textures/)and[part 2](https://fgiesen.wordpress.com/2010/03/29/how-to-generate-cellular-textures-2/). - Fast blurs
[part 1](https://fgiesen.wordpress.com/2012/07/30/fast-blurs-1/)and[part 2](https://fgiesen.wordpress.com/2012/08/01/fast-blurs-2/). - Fast Perlin noise-based texture generation
- Shitting bricks

### Compression

[x86 code compression in kkrunchy](https://fgiesen.wordpress.com/2011/01/24/x86-code-compression-in-kkrunchy/)- Squeezing operator data

### Animation

- Operator “initialization” versus “execution” (animatable parameters)
- Animation scripts
- The timeline

### Mesh Generation

[Half-edge based mesh representations: theory](https://fgiesen.wordpress.com/2012/02/21/half-edge-based-mesh-representations-theory/)[Half-edge based mesh representations: practice](https://fgiesen.wordpress.com/2012/03/24/half-edge-based-mesh-representations-practice/)[Half-edges redux](https://fgiesen.wordpress.com/2012/04/03/half-edges-redux/)- Extrusions
- Catmull-Clark subdivision surfaces
- Bones and Bends
- 3D Text

### Sound

- Debris and kkrieger use Tammo “kb” Hinrichs’s V2 synth, described on his blog:
[part I](http://blog.kebby.org/?p=34),[part II](http://blog.kebby.org/?p=36),[part III](http://blog.kebby.org/?p=38), and[part IV](http://blog.kebby.org/?p=40).

### Effects

- Swarms of cubes
- Exploding geometry
- Image postprocessing

### Shaders and 3D engine

- Shadergen (directly generates D3D9 bytecode for ubershaders, code
[here](http://www.farbrausch.com/~fg/code/shadergen/)) - The old material/lighting system: .kkrieger, PS1.3, cubes
- The new material/lighting system: PS2.0, the city, multipass madness
- Basic engine architecture – lights, layers and passes
- Converting generated meshes to rendering-ready meshes
- Skinning and Shadow Volumes

### Other

[Metaprogramming for madmen](https://fgiesen.wordpress.com/2012/04/08/metaprogramming-for-madmen/)(a small story about .kkrieger)

That’s not all of it, but it’s all I can think of right now that is a) somewhat interesting (to me that is) and b) something I can write about – for example, I wouldn’t be comfortable writing about the music/sound or overall flow/direction of the demo, since frankly I had little to do with that. And of course I didn’t write the code for all of the above either :), but I do know most of the code well enough to do a decent job describing it. That said, if you think there’s something I missed, just ping me and I’ll put it on the list.

So there you go. Your turn!

I vote for the half-edge redux. You’ve already told me about some parts of it a few times in person, and the world would be a better place if this was written up somewhere rather than kept in your head. :)

+1

+1

Sure, another +1 from me!

I’d also love to see this, I’ve dabbled with half-edge before but always got stuck with various bits of clunkiness. Hints on a clean design would be great.

+1

+1

+1

I’m interested in anything about texture generation and also the practical half edge. Lord knows my implementation of half edge is a bloated mess.

+1 to the above

Also, I’m curious about the swarm of cubes.

+1 For the whole mesh generation section.

On a side question, I have always wondered why Werkkzeug use CPU instead of GPU for texture generation? (Apart from some laborious cases to implement on GPU like the worley cellular)

Most of the texture generator was initially written late 2002/early 2003. Pixel Shader 2.0 HW wasn’t out yet and PS 1.x hardware is completely inadequate for texture synthesis. Also, this was before PCI Express, when readbacks from the graphics card were

reallydamn slow. We couldn’t do everything on the GPU, and shuttling data between CPU and GPU was expensive enough back then to be a showstopper. Also, all our texture generators after about 2001 use 16 bit/color channel (integer), because 8 bits is just not enough if you chain lots of operations. The first GPU to support an adequate format (GeForce FX, which had float16 textures) was to launch later, and their float16 supportsucked(no filtering, for once). Finally, GPUs back then usually had 64 or 128MB of memory; texture generation was our most memory-intensive step and we needed about 256MB workspace to do a good job (much more in the editor – it started to be fun with around 750MB of texture cache – yes, in 2003/2004!). And video memory management in drivers was piss-poor at the time; basically, if you started thrashing at any point, you were screwed for the lifetime of the process.If I had written a texture generator in 2007, I probably would’ve gone for fully GPU-based. But in 2002, the tech just wasn’t there yet.

Oh, forgot to say kudos for the initiative to share your knowledge!

First of all, thanks for sharing!

I think texture generation would make for an interesting read.

Other than that the architecture in general and software blurrrrrrr!

Thanks :)

Anything about mesh generation please. :) I am curious about what your approach on this matter is.

Also, while I’m commenting here and since you mentioned size coding, on a slightly different topic, I’m interested in hearing you thoughts on 64kB demomaking on 64 bits platforms.

Keep it up the good work!

This is probably beyond the scope of what you where planning to do, but I alwats thought that what would really be useful to the computer graphics community would be an open file format + implementation for texture generation. This would allow for more competing tools to be created and implementations for standard rendering packages (3dsmax, maya etc) and game engines .. Well, one can dream, right? ;)

Establishing an open format? Considering how well COLLADA went, I think I’ll pass. I’ve made that mistake once and have no plan of repeating it. (I did sketch a spec+reference implementation, years ago, as contract work for a company that wanted to get it into a standard. I spent a summer on it, got paid, then was later asked to do a presentation about it at a committee meeting where I was told by the other committee members that this was the first time they ever heard about it. You can guess how things went after that.)

Well COLLADA isn’t the best example yeah ;)

I am voting for memory management and image post-processing.

I’d +1 both Effects and Shaders and 3D engine, specially Shaders and 3D engine (basic engine architecture, the new material/lighting system, converting generated meshes to rendering-ready meshes and Skinning and Shadow Volumes).

Kudos for the initiative!

I’d love to learn the details for the whole Animation section and how “The Operator Execution Engine (demo/player side)” relates to that. It’d be doubly awesome if you could share your philosophy on procedural vs keyframe animation and how/if you combine the two. I’d also like to know if you use arc-length parametrised animation curves as well.

I saw a video of Chaos’ talk at Assembly from a few years ago on the tool but it wasn’t clear to me why he chose a ‘stacked blocks’ visual representation over a more traditional graph-based one. Any insights into this would be great, if this doesn’t fall under your ‘not talking about the tool’ clause :-)

Thanks again for your generosity!

About the stack operator, from my own experiments, it provides a far more efficient layout to quickly connect blocks without having to drag a line between each block. Thus the layout is more compact and allow to display a complex graph more easily, without having to scroll or to zoom. The downside compare to a line connected graph is that it is not well suited to connect an output to a specific pin-input of an operator (which could be interesting when you want to modulate an input parameter/property of a block with the output of another block. For texture gen in Werkkzeug, input and outputs were only textures). Also any kind of feedback link need to go through a store/load operator which could be annoying (that’s what Werkkzeuk is using).

Thanks for the offer! I put my vote on Mesh Extrusions & Catmull-Clark subdivision surfaces

I’d love to see a post on writing small code in C++, memory management sounds cool too

+1

+1 (any of the execution environment stuff except executable compression, but writing small code in particular)

+1

+1 (small code AND memory management)

Edit: again sorry for the mistake – THIS is the right post!

There’s lots of resources on e.g. texture generation out there – I would much rather hear about the specific innards of wz. So my vote goes for basics / compression / animation.

Half-edge, material system. I’m also semi-curious what you think about the possibilities of doing texture synthesis in WebGL to save bandwidth (although I think I remember you commented on Molly that the procedural descriptions ended up as large as compressed images).

Yes to the mesh-generation and half-edge stuff, as so many others have said. I have done a bunch of this in the past but always wondered if I could do it better.

Thanks for your articles, while I’m here. And I enjoyed the Farbrausch demos back in the day.

Thank you for sharing your knowledge!

I vote for the mesh generation section. More precisely: my #1 would be the half-edge section, #2 the 3D text, then the rest without order of preference.

The meshes data structures as well… or the source code even if I know I won’t ever touch it,

I hope you end up writing about all the topics, but as “write all of them” is not a very useful suggestion I’m going to vote for engine architecture.

My votes go for:

1. Shadergen (directly generates D3D9 bytecode for ubershaders, code here)

2. Basic engine architecture – lights, layers and passes

Concerning your half-edge redux, how close was it to directed edges (Campagna/Kobbelt/Seidel circa 2007)?

As for the topics to describe, I’d like your comments on all of them.

I guess any particular insight you’re particularly proud of, and any other non-obvious insight would be great (something along the the lines “this is way more complicated than you’d think, and here’s why” or “this is easy and so powerful, strongly recommend!”). Also, things to avoid would be interesting (I assume you tried a bunch of things, and didn’t always succeed).

And while we’re at it, how about business lessons (since you folded)?

It’s close to directed edges. We use convex N-edged polys (N<=8 in the newer mesh generator) so we waste some space. The main point is that the newer mesh generator has throw-away connectivity information. Some operators (those that need connectivity) read and update it, others don't touch connectivity at all, and some destroy it. Allowing the latter (if necessary, we just regenerate adjacency information) simplifies things a great deal. It's easier to create meshes without full adjacency and fill it in later, and it's also easier to regenerate adjacency than it is to maintain it throughout complex operations. I'll fill in the details in the actual article :)

Oh, and about business: Don’t start a business doing something you don’t really believe in with everyone already having a different day job that they prefer. The end. :)

Operators + execution engine, animation, animation timeline, basic engine architecture.

+1 for “Converting generated meshes to rendering-ready meshes”, and the half-edge mesh stuff that everybody else is voting for.

These are my votes (in order):

Exploding geometry

Half-edge based mesh representations redux

Extrusions

Fast Perlin noise-based texture generation

Converting generated meshes to rendering-ready meshes

Fast software blurs

Writing small code on Win32/x86 (in C++)

I’m interessted in:

# Operators (the building block of our procedural system)

# The Operator Execution Engine (demo/player side)

Honestly, all of it.. but if I *had* to choose, my bucket list of things to read would be:

Operators (the building block of our procedural system)

The Operator Execution Engine (demo/player side)

How to generate cellular textures part 1 and part 2.

Fast software blurs

Fast Perlin noise-based texture generation

Shitting bricks

Swarms of cubes

+1 for Basic engine architecture – lights, layers and passes :)

+1

If I had to choose what I’d like to read from you, it would be:

* The new material/lighting system: PS2.0, the city, multipass madness

* Basic engine architecture – lights, layers and passes

* Shitting bricks

* Swarms of cubes

kb’s articles on the sound system can now be found on the Conspircay website

https://conspiracy.hu/articles/