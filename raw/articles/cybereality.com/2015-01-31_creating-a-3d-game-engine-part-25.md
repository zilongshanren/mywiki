---
title: Creating a 3D Game Engine (Part 25)
url: https://cybereality.com/creating-a-3d-game-engine-part-25/
author: Cybereality
published: '2015-01-31'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/4ccb6d9211e3c4d9.jpg)


So it comes with great reluctance but I think I will have to suspend development on my 3D game engine, at least for the near future. Surely this will be a disappointment to anyone following the progress and I did not make the decision lightly. After spending some time thinking about it, I think it’s the right move. It’s just really hard to justify the amount of time and effort put into this when there are much better solutions available off-the-shelf.

In the little less than 2 years I’ve worked on this project, I think I have made decent strides. Honestly, I was not working on it full-time. Just on weekends mostly or maybe here and there when I had time after work. My initial goal was to have something functional in about 6 months to a year. It took a little longer, but I guess eventually I did have the basic features of an engine somewhat working. I will list what was implemented below, but it was enough to load in some textured models and fly a camera around. Not ground-breaking work by any means, but I built nearly everything myself so I was happy about that. There was just an enormous amount of work remaining to get to a state where a game could be produced. Finally, it was too much.

So before I give my personal advice, I’ll break down how I got to this point. First, let’s look at all the books I read as research for this project:

Game Engine Architecture – Jason Gregory

Game Coding Complete, Fourth Edition – Mike McShaffry

Real-Time Rendering, Third Edition – Tomas Akenine-Moller

Game Engine Design And Implementation – Alan Thorn

3D Game Engine Programming – Stefan Zerbst

Game Engine Gems, Volume One – Eric Lengyel

3D Game Engine Architecture – David H. Eberly

3D Game Engine Design – David H. Eberly

3D Math Primer for Graphics and Game Development – Fletcher Dunn

Mathematics for 3D Game Programming and Computer Graphics, Third Edition – Eric Lengyel

Introduction to 3D Game Programming with DirectX 11 – Frank Luna

Practical Rendering and Computation with Direct3D 11 – Jason Zink

Beginning DirectX 11 Game Programming – Allen Sherrod

Game Programming Patterns – Robert Nystrom

Game Physics Engine Development – Ian Millington

Physics for Game Developers – David M Bourg

Physics for Game Programmers – Grant Palmer

Game Physics Pearls – Gino van den Bergen

Shadow Algorithms Data Miner – Andrew Woo

The C++ Programming Language, 4th Edition – Bjarne Stroustrup

C++ Primer (5th Edition) – Stanley B. Lippman

C++ Primer Plus (6th Edition) – Stephen Prata

More Effective C++ – Scott Meyers

If you are considering engine development, please read on, but I believe all the above books are valuable to look at. I’ve also read a variety of sources online, from tutorials to official documentation and more. Looking at that list it seems huge, but I am an avid reader and have read and listened to a number of non-technical books in that time-span as well.

Next, let’s look at what features were actually implemented and working (or mostly working):

- Win32 app template (message pump)
- DirectX 11 based rendering engine
- DirectInput mouse and keyboard controls
- Custom math library (Vector, Point, Matrix, view/projection)
- Node-based hierarchical scene graph
- Frustum culling (sphere and point tests, minimal bounding sphere)
- Generic XML parser (from scratch, kind of hacky and slow)
- COLLADA importer (only basic vertex and UVs)
- Custom binary 3D model format (for speed)
- Camera object (spectator mode)
- Texture mapping and Skybox (cube mapping)
- Directional, ambient, and specular lighting
- Normal and shadow mapping shaders
- Command-line console window logging
- Architectural glue and probably some odds-and-ends.

So what wasn’t finished? Way too much to list. I don’t want to get down on myself too hard, cause I think that I accomplished a little something here. Certainly some of this stuff was not easy and, if anything, it has made me a better coder. Even in the current state I guess you could make a Pong game or a simple walk-through demo or the like. Also keep in mind this was a part-time excursion. If I were dedicated to this fully it probably would only have taken months (not counting research time). While I started with a very clean style and deliberate design, by the end I was kind of hacking things together, and some features (like the shadow mapping) became very intertwined with the core rendering code. Of course, this was very much a learning experience, and I planned to go back and clean things up later (which may or may not ever happen, we’ll see).

OK, so by now you are probably getting the idea. As to my advice, if you are trying to make a game (or game-like interactive experience) don’t bother making a custom engine. Everyone basically told me this from the start, and I didn’t listen. It’s sort of like when you see people doing stunts on TV and they tell you “don’t do this at home.” But they did it, and it made them rich and famous. So maybe I was looking for glory, or hoping finishing a big project like this would take me to another level. I guess in a way it did. I’m just not sure that was the best use of my limited time. What I mean to say is that knowledge is valuable, and I feel I learned a lot. However, unless you are really looking to be an engine programming professional, there is not much reason to try to do this.

The crux of the matter is that all-in-one engines like Unity and Unreal are just too complex and mature to expect to compete with. That’s not to say a small team or a single hero-coder can’t produce something great. They can. However, using a pre-built engine cuts out a *lot* of time and risk. Had I been working on a project for a client, I would have never even contemplated a custom engine. It just doesn’t make sense. Both Unreal and Unity have huge teams of expert engineers working solely on engine development. Unless you work for a huge AAA studio with a monster budget, I just can’t see coming up with something better in any reasonable amount of time. Even some huge companies (like Capcom and Square-Enix) are dropping in-house engine development for Unreal 4. Not a good sign for indies or bedroom coders working on their own engines.

But let’s say those big engines aren’t for you. There are a number of open-source engines and libraries out there to help you along. Something like Torque or C4 look promising (if you want a full-featured solution), or OGRE (if you don’t mind having to cobble together a bunch of different libraries). If you are interested in web publishing there are things like three.js for WebGL. With source access you can add the features you need or fix critical bugs. Really there are too many options to ignore.

For the last few weeks I’ve been playing with Unreal Engine 4, and it basically does everything I need and a whole lot more. At $19/month and a small royalty (if you sell your title) making a AAA looking game has never been more affordable. Unity may still have a leg up on ease-of-use and scalability on different platforms, but for high-end development I think Unreal is probably the one to go with. Having the source-code is a huge boon, and the price makes it attainable to almost anyone. Plus, with the visual scripting, Unreal can even be approachable to artists and designers. I’m still in the early stages of getting acquainted with the engine, but so far I am pleasantly surprised. I plan to follow up with some posts and tutorials in UE4 in the future, so don’t think this is the end of my blogging career or anything of that sort.

With all that said, there are still some things I’d like to see in engines that don’t exist today. You typically can’t use the editor in stereo 3D (assuming the engine even supports 3D natively), motion control support for placing objects is non-existent, image and model editing is usually very rudimentary (you must switch back and forth to other apps), real-time code editing and previewing can be limited. So things can certainly improve, and I guess there could be a case made for making plugins or forks to existing projects. I’m not saying things can’t improve. Just that reinventing the wheel to make incremental improvements may not be the best path.

At this point I don’t think I would say engine development is a “waste of time.” As a learning experience, I think it was fun and rewarding. Certainly I hope I didn’t just waste 2 years of my life. Doing all the work and research has brought me here to this place. So it was somewhat worthwhile. It just pains me to think how far along I might have been had I jumped on Unreal 4 when they first announced the subscription model, or spent more time with Unity over the years. If you actually want to build (and finish) a game, it’s a pretty clear choice to use an off-the-shelf solution. I’m sorry, guys. I wanted to prove everyone wrong, but they were right. Make games, not engines.

Finally, I’m sure the question you’re thinking is “will I release the source.” I’m considering it, but there are some hacked bits in there and I’m not sure it’s a great example to work off of. More likely I will pull out portions or classes from the project and use them for future blog posts highlighting a particular algorithm or technique. The full source itself is probably less useful compared to other stuff that’s out there. In any case, I hope maybe you have learned something after 2 years and 25 posts on this project. If you click the (somewhat hidden) 3 white line icon on the top right of the blog, you can see a list of all the blog updates in this series for a little history (if you weren’t following the whole time). Cheers, and happy coding.