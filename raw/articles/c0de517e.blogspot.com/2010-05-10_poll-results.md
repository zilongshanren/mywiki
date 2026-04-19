---
title: Poll results
url: https://c0de517e.blogspot.com/2010/05/poll-results.html
published: '2010-05-10'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

## Poll: Which means of live-editing does your game/project use? Answers: 75


16%: None.

We like to cause pain and waste money. We are too rich or too stupid or both. We live in the continuous pain of having to relaunch the game every time we change a texture or a shader. We can't solve bugs. We can't optimize performances. We're doomed.


41%: File hot-swapping.

41%: File hot-swapping.

We can switch textures and meshes. Probably even shaders. It was relatively simple, just make sure that the file-system does all the resource creation for a given file, and that files are always accessed via handles, and not directly storing pointers to the loaded resources.

Everything works nicely, as long as you don't want to actually... code stuff. Every code change brings back the pain. Rendering engineers love working on shaders, and would kill themselves every time the have to fall back to C++ stuff.

Can't easily navigate the scene, can't select stuff, tweak parameters, tweak materials, display debugging stuff, live-edit... Memory on the platform is limited, the game crashes after some reloads due to fragmentation.

41%: Script hot-swapping.

Like above, but we have a scripting system, probably Lua. We can swap those files too.

29%: Tools, partially replicating game functions. (i.e. Shader editor, Animation editor etc). Tool saves the changes.

Iterations on the consoles is painful. Build times are slow. Memory is limited. Input devices are awkward. Reload times are bad. So? Well, let's build tools for faster iteration! Tools where you can edit things quickly.

In theory it's a nice idea, but instead of solving the original problem, you create a new framework that works well, but it's not the game. Still, every time you have to iterate on the game, you fall back to the ugly slow and painful workflow. Also, now you have to write everything twice, once for the tool and once in game. And you force most people to work in their tool, thus not reviewing and iteration on the final, in game, on platform result.

21%: Tool manages and serializes data, but can send RPC to live-update the game.

Same as above, but now we can see changes in game. At least for some stuff, after some time.

18%: The game/engine is embedded in a tool by static linking/DLLs. The game serializes the changes.

We're smarter than the group above. The game is a module with a small "loader" for the console and a platform specific implementation of basic system services (i.e. filesystem). The tool is a PC environment that loads the same module (i.e. compiled as a DLL) but has a windowing and input system and adds debug functionality and reflection to the various services. The editing functionality is done via components in the editor that can access both to the tool functionalities (windowing) and to the game interfaces.

Great! But still we are not viewing and editing on the target platform. Also if we're not shipping for the PC, we have to maintain an extra platform (the game and the engine have to compile). Also, coding is still slow. C++ is still painful.

9%: Tool, using reflection/RPC/... it communicates with the game. The game serializes the changes.

Everything is done in game! Finally, few members in this group, the elite. The editor has windowing services, and a system to reflect game features, and send message to the game to change its components.

The editor is written in a cool language, like C#, or uses scripting, or both. It's easy to create new editors. Direct manipulation, picking, editing is done by communicating the mouse input to the console, to have mouse support on the console screen. On the PC screen we display only windows with editing widgets and debugging stuff. C++ = pain.

10%: Purely in-game on-platform editing. Game can build with GUI/editing functionality built in. Game serializes.

Everything is done in game! As above, but on-platform only. On consoles, the limited memory is a big problem. C++ = pain.

9%: Code hot-swapping.

We care about ourselves too! Not only game designers and artists. We care about our work! We don't want to suffer. We are the best, fuck the rest. If you have code hot-swapping, everything else does not matter. Because now you can code fast! You can do whatever. Even code all the above in the time they will take to ship a single game. Enjoy.

## 9 comments:

So that's... 194%?

Seems somebody skipped his math classes.

Warning: this blog's articles may require a brain. Either turn yours on or go troll somewhere else. Offending comments will be deleted.

I'm actually quite serious. I can understand that some of the categories could overlap, but others are clearly mutually exclusive, and without any sort of background, or even the original poll to go by, the figures seem pretty useless.

'Overlapping' and 'Mutually exclusive' are not opposites.





Anyway the poll was made to understand how many people do have live-editing (i.e. do not fall in the "none" category) and among those, which means of live-editing were the most popular.

As expected, file swapping (41%) is very popular as it's the easiest.

Most people also have external tools, not integrated with the game or integrated by sending updates to a live game (29%+21%)

No one care about live-coding (9%)

To argue a bit with the blog theme... In the results of the poll I see a prevailing statement that c++ = pain, but if C# (Mono) is supported on all current console architectures, why isn't it used throughout? Guess the language and its runtime implications are not good enough.. I'm just saying :)

C++ is a huge pile of crap, but that's not what I meant in the post. C++ = pain means that with that given solution, the C++ coding part is not taken care of, it's caring only about data iteration and not code iteration.


Mono has still quite a lot of licensing and implementation limits, but how do you know that it isn't used? Surely going from a langauge to another is not something that happens fast, there is still some Fortran and Cobol code around today, but I know quite a few projects and companies that use C# in game, and shipped titles with that.

It sounds very interesting !! Could you share more information/links about the code hot-swapping principles, techniques and gotchas ? Do you use something comparable to IAT hooks, or bridge DLLs ? Cheers, Nicolas.

rotogulp: in theory, code-swapping is not complicated, you can easily reload DLLs or whatever your system supports.




In practice it's an issue of design, and it can't really be implemented late. The problems are dependencies, a module to be hot-swappable has to have well defined interfaces and no other static or runtime dependencies.

You have to keep track of the module state, and have a functionality to serialize and deserialize it (so you can serialize/unload/load/deserialize) and it's best not to share objects across modules (painful if they are not POD types, especially if you have a vtable, that will change after a reload).

In practice there are quite a few gotchas, but the best thing is to design your engine with that goal in mind from the very beginning, and then every problem you'll encounter will be something that with a bit of refactoring can be solved.

Post a Comment