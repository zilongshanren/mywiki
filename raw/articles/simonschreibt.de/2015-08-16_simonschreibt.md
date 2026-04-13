---
title: Simonschreibt.
url: https://simonschreibt.de/gat/renderhell-book1/
author: Simon
published: '2015-08-16'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/10c681ccc40de8ae.jpg)


Artists must be strong now: From a computers perspective, your assets are just lists of vertex- and texture data. Converting this raw data into a next-gen image, is mainly done by your system processor (**CPU**) and your graphics processor (**GPU**).

1. Copy the data into system memory for fast access

At first all necessary data is loaded from your hard drive (**HDD**) into the system memory (**RAM**) for faster access. Now the necessary meshes and textures are loaded into the memory on the graphic card (**VRAM**). This is because the graphic card can access the VRAM a lot faster.

If a texture isn’t needed anymore (after loading it into the VRAM), it can be thrown out of the RAM (but you should be sure, that you won’t need it again soon, because reloading it from HDD costs a lot time). The meshes should stay in the RAM because it’s most likely that the CPU wants to have access to them e.g. for collision detection.

Therefore the hardware engineers put small memory **directly inside** the processor chips, typically called on-chip caches. It’s not a lot of memory because it’s crazy expensive to put it inside the processor chip. The GPU copies currently necessary data in small portions there.

Our copied data lays in the so called L2 Cache now. This is basically a small memory (on NVIDIA GM204: 2048 KB) which sits on the GPU and can be accessed **faster** than the VRAM.

But even this is too slow to work efficient! So there’s an even smaller L1 cache (on NVIDIA GM204: 384 KB (4 x 4 x 24 KB)) which sits not only on the GPU but even NEARER to its cores!

Plus, there’s another memory which is reserved for input and output data for the GPU Cores: registers or register file. From here the GPU Cores take e.g. two values, calculate them and put the result into a register (which is basically a memory address in the register file):

The results in the registers are then taken and stored back into L1/L2/VRAM to have space for new values in the register file. As a programmer you normally don’t have to worry too much about that stuff.

Why all this hassle? Like mentioned above: It’s all about access times! If you compare the times of an access of e.g. a HDD and the L1 cache there’s a huge huge huge difference! Read about some exact latency numbers in [[a47]](https://gist.github.com/hellerbarde/2843375)

Before the render-party can start, the CPU sets some global values which describe **how** the meshes shall be rendered. This value collection is called **Render State**.

2. Set the Render State

A render state is kind of a global definition of **how** meshes are rendered. It contains information like:

“vertex and pixel shader, texture, material, lighting, transparency, etc. […]” [b01 page 711]


**Important: Each** mesh, which the CPU commands the GPU to draw, will be rendered under these conditions! You can render a stone, a chair or a sword – they all get the same render values assigned (e.g. the material) if you don’t change the render state before rendering the next mesh.

After the preparation is done, the CPU can finally call the GPU and tell it what to draw. This command is known as: **Draw Call**.

3. Draw Call

A draw call is a command to render **one** mesh. It is given by the CPU. It is received by the GPU. The command only points to a mesh which shall be rendered and **doesn’t** contain any material information since these are already defined via the render state. The mesh resides at this point in the memory of your graphic card (VRAM).

After the command is given, the GPU takes the render state values (material, textures, shader, …) and all the vertex data to convert this information via some code magic into (hopefully) beautiful pixels on your screen. This conversion process is also known as **Pipeline**.

4. Pipeline

As i said at the beginning, an asset is more or less just a list of vertex- and texture data. To convert those into a mind blowing image, the Graphic Card has to create triangles out of the vertices, calculate how they are lit, paint texture-pixels on them and a lot more. These actions are called states. Pipeline states.

Depending on where you read, you’ll find that most of the stuff is done by the GPU. But sometimes they say, that for example the triangle creation & fragment creation is done by other parts of the graphic card.

[tweet](https://twitter.com/simonschreibt)or

Here are some example steps the hardware does for **one** triangle:

Rendering is basically doing an immense number of small tasks such as calculate something for thousands of vertices or painting millions of pixels on a screen. At least in (hopefully) 30fps.

It’s necessary to be able to compute a lot of that stuff **at the same time** and not every vertex/pixel one after another. In the good old days, processors had only one core and no graphic acceleration – they could only do one thing at the same time. The games looked … retro. Modern CPUs have 6-8 cores while GPUs have several thousands (they aren’t that complex like CPU-Cores, but perfect for pushing through a lot vertex and pixel data).

Gustav and Christoph refined the core-statements a bit to explain the difference between CPU and GPU core counts:

When data (e.g. a heap of vertices) is put into a pipeline stage, the work of transforming the points/pixels is divided onto several cores, so that a lot of those small elements are formed parallel to a big picture:

Now we know, that the GPU can work on stuff in parallel. But what’s about the communication between CPU and GPU? Does the CPU has to wait until the GPU finished the job before it can receive new commands?

![](../../assets/a52b907d5d9f3010.gif)


Thankfully not! The reason is, that such a communication would create bottlenecks (e.g. when the CPU can’t deliver commands fast enough) and would make parallel working impossible. The solution is a list where commands can be added by the CPU and read by the GPU – independent from each other! This list is called: **Command Buffer**.

The command buffer makes it possible that CPU and GPU can work independent from each other. When the CPU wants something to be rendered, it can push that command into the queue and when the GPU has free resources, it can take the command out of the list and execute it (but the list works as a

[FIFO](http://en.wikipedia.org/wiki/FIFO)– so the GPU can only take the oldest item in the list (which was first/earlier added than all others) and work on that).

By the way: there are different commands possible. One example is a draw call, another would be to change the render state.

That’s it for the first book. Now you should have an overview about asset data during rendering, draw calls, render states and the communication between CPU and GPU.

**The End.**

Finding this series I feel like i struck gold! Thanks a lot mate, really.

Thanks man :) Good to hear!

This is so cool! Finally I understand the whole process, and I love and enjoy your illustrations :D

Keep up the good work!

hehe glad you like them :) mr. gpu is happy to hear that! <3

The Best! Really love this material. Thanks mate!

Thank you :) Glad you like it!

Love this series and these animations ! I always learn something new from your articles.

Keep schreibing dude :D

I’ll try my best. Thank you! <3

Great work! Always good to see tech knowledge spread in a way that helps get more people interested :)

It should probably also be noted that while a GPU and CPU core aren’t comparable, nor are the cores Nvidia and AMD make (or any other GPU maker for that matter). Reading your article, a person might be under the impression that since AMD GPUs have more cores, that makes them inherently better, but really it’s that Nvidia’s cores, like the CPU, are a bit more complex and thus can get more done within a single cycle. The companies merely took slightly different approaches to the same problems, and thus have different instances where they outperform eachother.

Oh cool, thanks for the info! It’s a really interesting detail. :)

OMG, this is so great. Thank you for your all work. I’m really glad to see this series.

Thanks man! Took a long time to put all this together :,D Good to hear that people like it. :)

WOW, it is so amazing!!!!!!!!!!!)))))))))))) Your work is perfect, Thank you very much!!!!)))))

I read this text second time. You are the best)) I’m junior programmer in game dev and for me this material was very very useful

It is so amazing. It helps me advance in game development. Your work is great. Best wish for you guy.

Thanks a lot for your work. It is amazing. But I am still confusing about “buffer”. How many buffers? Where is it in rendering pipeline? and what are these roles?

Again, thank you very much :D

You mean the command buffer? Or are there other mentions of “Buffers” which confuse you?

Really solid stuff. Thanks a lot for the material. :)

Very interesting! Thank you. So clear explanations and funny animations. I’m glad I found this article!

This is 100% golden info – I will be reading and taking notes from this series very carefully. As a self-trained artist with my knowledge of these processes is patchy to say the least, these books will help me feel solid.

Thanks man! :)

This is really great, I’ve never seen something explained so succinctly and clearly. Just one question. I do need clarification on the following:

The textures and mesh data move from [VRAM -> L2 -> L1 -> Register] to get processed by the core correct? This processing is the aforementioned pipeline? And then after the result of that process, they get outputted to the frame buffer/shown and then the textures and mesh data move back to VRAM just in case they are needed again? Basically L2/L1/Register seem unnecessary; they are just there to speed up the process; sort of acting as a filter as data gets inputted?

Thank you! :)

I think so, yes. The pipeline is the copying, processing and of course the final output. If the access to the VRAM would be as fast as on the register, those entities (L2/L1/, …) shouldn’t be necessary – but I can only assume here. I think there’s a lot of smart ideas going into this so that for example the data in the register might stay there if the graphic card still needs them for further processing. But since there’s not that much space, at some point the data has to be switched.

This series is absolute gold. Thank you so much for taking the time to do this. Thanks to any other contributors that helped as well!!

Ah this is such a cool series, Im sorry to find it so late – as now I wonder what might have changed in 5 years

But this visual style of explanation cuts down the stress of quite complex subject!

Love love love it!

Thank you very very very very vertex vertex vertex core core !!!! You are the Human!

I have two question:

1. i see that each vertex taken by separate GPU core in pipeline – so what will happen if there are more vertices in mesh than cores in GPU ?

2. some stages use all vertices (like triangulation) – so which core do it?

Thank you so much for the material. It helped me understand the process better.

THANK YOU SO MUCH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! THIS IS GOLD ♥