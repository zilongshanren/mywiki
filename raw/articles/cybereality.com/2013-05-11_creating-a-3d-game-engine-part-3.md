---
title: Creating a 3D Game Engine (Part 3)
url: https://cybereality.com/creating-a-3d-game-engine-part-3/
author: Cybereality
published: '2013-05-11'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

Last time I recommended some good books for engine creation. Today I will talk a little bit more about what an engine actually is, since it’s rather silly to try to create something that is undefined. What I am defining a 3D game engine as is “a framework or set of tools that abstracts complexity and enables creation of real-time 3D experiences.” It’s important that it deals with “a framework or set of tools” and not just a single tool. Obviously artists might use an image editor to create a texture, but we wouldn’t consider Photoshop to be part of a game engine. However we may have a standalone tool, let’s say a light-mapper, that works in conjunction with the 3D engine. In this case, we may count the tool as part of the engine. One key point is that the 3D game engine should “abstract complexity” and allow for more rapid development than otherwise possible. The whole point of using a game engine in the first place is to make common actions easier and quicker to do. It’s also important that you are not limited to creating games, although I would still call it a “game engine” since that is common terminology. The same engine could be used for virtual reality, or simulations, or data visualizations, or any number of non-gaming applications. The engine could even be used for non-interactive experiences (for example: machinima) but it would still need to be real-time in nature. Clearly a video player would not constitute an engine. So now that we have a clear, if not somewhat broad, definition of an engine, whats next?

Well a lot of people (including myself) would like to say they created their 3D game engine “from scratch.” Now what does that mean exactly? Does it mean not using any 3rd party libraries? How far will you go with this is? I mean, does the C++ standard library apply here? Are you going to re-implement the STL? Write your own C compiler? Clearly this is too far. Unless you are creating your own programming language and compiler in straight machine-code, then you are going to be using someone else’s work somehow. There is no shame here. To make a good high-level application, like a video game, you will need to use a variety of low-level functions that you may not want to code all from scratch. This is a given. Especially if you actually want to have a working application finished within your life-time. Obviously you would be using an API like OpenGL or DirectX. There’s no glory in re-inventing the wheel here. While you could write your own physics engine (and some developers do), there are a number of decent solutions available. There also probably isn’t a big need to write your own PNG decompressor. That’s fine, but I still haven’t explained what “from scratch” means. What I would call “from scratch” is something that started as a blank text file, and that was slowly built up over time to have more features. I think this is fair. Even if 3rd party libraries were integrated, I don’t think this takes away from your original code. It’s still “your creation.”

So I defined my 3D game engine as a “framework,” but what exactly does that entail? Though not exhaustive, some of the things I would expect from this engine are:

- Input processing. Reading state from keyboard, mouse, controller, etc. and exposing a high-level interface (like an action-map).
- A graphical representation of a 3D environment. For example, to be able to set positions and orientations of objects in space, and draw them onto the screen.
- A audio system. Being able to play ambient background music, or one-off sound effects.
- A math library for 3D gaming: vector, matrix, quaternion, collision, intersection, AABB, etc.
- An animation and physics system. The ability to animate objects, either due to dynamic interaction or through scripted animation.
- An event system, which would allow entities to fire events and other entities to listen for events and respond accordingly.
- File management, loading resources, streaming assets, saving configuration, etc.
- A scripting system, that allows for rapid iteration and prototyping without recompiling the application.
- An editor that simplifies scene creation, connecting scripts, parameter setting, asset management and other authoring actions.
- A state machine, that lets objects to have different states. Useful for GUI, AI, etc.
- Possibly networking, if the game is multiplayer.

While this list is not going to include every single element of a 3D game engine, I think I have touched on the most important sub-systems of the framework. Certainly, this is no small task. I realize that there is a long road ahead of me (and I hope you do too, since you’re reading this). I’m aiming to spend about 2 years to make this happen. Granted, I hope to have a MVP (minimum viable product) up and running in a much shorter time-frame, lets say 6 months. But I understand that these things can take time, especially for a lone coder. But I think it will happen. No, it will happen. I will make it happen.