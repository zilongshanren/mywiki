---
title: Our Tool Architecture
url: https://bitsquid.blogspot.com/2010/04/our-tool-architecture.html
author: Niklas
published: '2010-04-23'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

- Tools should use the "real" engine for visualization.
- Tools should not be directly linked or otherwise strongly coupled to the engine.

Using the real engine for visualization means that everything will look and behave exactly the same in the tools as it does in-game. It also saves us the work of having to write a completely separate "tool visualizer" as well as the nightmare of trying to keep it in sync with changes to the engine.

By decoupling the tools from the engine we achieve freedom and flexibility, both in the design of the tools and in the design of the engine. The tools can be written in any language (C#, Ruby, Java, Lisp, Lua, Python, C++, etc), using any methodology and design philosophy. The engine can be optimized and the runtime data formats changed without affecting the tools.

What we envision is a Unix-like environment with a plethora of special purpose tools (particle editor, animation editor, level editor, material editor, profiler, lua debugger, etc) rather than a single monolithic Mega-Editor. We want it to be easy for our licensees to supplement our standard tool set with their own in-house tools, custom written to fit the requirements of their particular games. For example, a top-down 2D game may have a custom written

*tile editor*. Another programmer may want to hack together a simple batch script that drops a MIP-step from all vegetation textures.

At first glance, our two design goals may appear conflicting. How can we make our tools use the engine for all visualization without strongly coupling the tools to the engine? Our solution is shown in the image below:

Note that there is no direct linkage between the tool and the engine. The tool only talks to the engine through the network. All messages on the network connection are simple JSON structs, such as:

{

"type" : "message",

"level" : "info",

"system" : "D3DRenderDevice",

"message" : "Resizing swap chain: 1626 1051"

}

This applies for all tools. When the lua debugger wants to set a breakpoint, it sends a message to the engine with the lua file and line number. When the breakpoint is hit, the engine sends a message back. (So you can easily swap in your own lua debugger integrated with your favorite editor, by simply receiving and sending these messages.) When the engine has gathered a bunch of profiling data, it sends a profiler message. Et cetera.

For visualization, the tool creates a window where it wants the engine to render and sends the window handle to the engine. The engine then creates a swap chain for that window and renders into it.

(In the future we may also add support for a VNC-like mode where we instead let the engine send the content of the frame buffer over the network. This would allow the tools to work directly against consoles, letting the artists see, directly in their editors, how everything will look on the lead platform.)

A tool typically boots the engine in a special mode where it runs a custom lua script designed to collaborate with that particular tool. For example, the particle editor boots the engine with

*particle_editor_slave.lua*which sets up a default scene for viewing particle effects with a camera, skydome, lights, etc. The tool then sends script commands over the network connection that tells the engine what to do, for example to display a particular effect:

{

type = "script",

script = "ParticleEditorSlave:test_effect('fx/grenade/explosion')"

}

These commands are handled by the slave script. The slave script can also send messages back if the tool is requesting information.

The slave scripts are usually quite simple. The particle editor slave script is just 120 lines of lua code.

To make the tools independent of the engine data formats we have separated the data into human-readable, extensible and backwards compatible

*generic data*and fast, efficient, platform specific

*runtime data*. The tools always work with the generic data, which is pretty much all in JSON (exceptions are textures and WAVs). Thus, they never need to care about how the engine represents its runtime data and the engine is free to change and optimize the runtime format however it likes.

When the tool has changed some data and wants to see the change in-engine, it launches the

*data compiler*to generate the runtime data. (The data compiler is in fact just the regular Win32 engine started with a

*-compile*flag, so the engine and the data compiler are always in sync. Any change of the runtime formats triggers a recompile.) The data compiler is clever about just compiling the data that has actually changed.

When the compile is done, the tool sends a network message to the engine, telling it to reload the changed data file at which point you will see the changes in-game. All this happens nearly instantaneously allowing very quick tweaking of content and gameplay (by reloading lua files).

This system has worked out really well for us. The decoupling has allowed for fast development of both the tools and the engine. Today we have about ten different tools that use this system and we have been able to make many optimizations to the engine and the runtime formats without affecting the tools or the generic data.

Nice post, this is a fascinating subject. The key point for me was "All this happens nearly instantaneously". I wonder if that might become a development bottleneck at some point. What if transforming super-generic data into ultra-optimized data is no longer near-instantaneous? Would you provide/support multiple compile modes, with different speed/efficiency trade-offs?

ReplyDeleteI am all with you on this, but how do you plan on minimizing the clicking a user needs to do if they for example want to edit some material features when doing some level editing?



ReplyDeleteIf you have many separate tools I guess it will be a lot of different clicking and windows open?

Cheers,

Otto

Jurie: We in fact already have two different modes. One "regular" where the compiled data is stored as individual files in the file system, and one "bundled" which uses the same compile settings but puts all the data in a single file ordered by access and compresses it with gzip. This allows the data to be read without disk seeking but building the bundle takes some time.




ReplyDeleteFor data that takes long to build (two examples: lightmaps, ai nav meshes), there are two options. Either different compile modes (as you suggest) or a manual build step.

By a manual build step I mean that nav meshes (for instance) are not recompiled automatically, they are regenerated only when the level designer presses [Build NavMesh] in the editor. This runs the expensive computation and saves the new nav meshes. The nav meshes would then still be saved in a generic format, but with all the data that is expensive to compute included, so that they could quickly be converted to the runtime format.

Which method is better can be discussed, but personally I'm leaning against the latter method. Introducing more compile modes increases complexity. It also means that what you see when you have compiled the game with the "low" setting doesn't match the performance you would get when you do the final game build which is a really bad thing. I think it is crucial that the performance and visual quality that the artists see when they iterate over the game data match the performance and quality of the final game as closely as possible.

Otto: Good point! For looser integration one tool could just launch another, as you say. The user would see this as a window opening. So there would be some extra windows and mouse clicks, but not that much different from a monolithic editor which would also open a new window or a new tab in such cases.



ReplyDeleteIn some cases a tighter integration is desired. One example is between the particle editor and the material editor, since each particle effect will typically use its own material. Our plan there is to integrate a material editor, specifically adapted for editing particle materials directly in the particle editor.

To do this we might decide to share some code between the material editor and the particle editor, or we may decide not to if that makes more sense. We are still in a better position than with a monolithic editor since we decide exactly when and where we want to share code and we only introduce dependencies when we actually want them.

I've been experimenting with similar approach for my home projects and it seems to work nicely. One thing I wasn't so sure about was how would it work for applications where perfect time synchronization is crucial, like animation editors for example. Didn't you guys encounter any problems here?

ReplyDeleteRainbow Studios' engine and toolchain for Deadly Creatures worked a lot like this, although in their case the "tool" was in large part 3DSMAX. Their system allowed you to launch and edit the world in 3DSMAX and see it updating live on the target, which was pretty cool if you ask me.



ReplyDeleteThe engine at my current place of employ also works similarly, despite different choices in technology. We can drive the engine with Python running on the host computer, and have implemented a fairly substantial suite of tests for the engine among other uses. It's been pretty helpful to maintain a baseline of functionality as the technology develops.

I'm not a fan of allowing the game to build the data, though. IMHO the game should only see built data (although being able to load out of packfiles or free files is a necessary convenience), and it should always be another application that does the build. This is desirable so that you don't accidentally have unprocessed data getting shipped, and so that you can't be lazy and leave "unoptimized" formats around to suck minutes out of every person's every launch of the game.

MaciejS: I don't see the issue. In our animation editor all animations are run in the engine on the engine's clock. They don't have to be synced with any clock in the editor.

ReplyDeleteTom: I agree with your concerns, and we have explicitly structured our code to prevent that from happening. In pseudo-code, our main() is something like: (excuse the terrible formatting of code in these comments)



ReplyDelete#if defined(WIN32) && defined(DEVELOPMENT)

....if (flags.compile()) {

........compile(generic_data_folder, runtime_data_folder);

....exit();

....}

#end

run(runtime_data_folder);

Once the engine is in run() it never sees the generic data folder so it can't "cheat" and read anything there. Also, the compilation code is only included in the Win32 development build, not in release builds or console builds.

Very interesting ideas! I've never seen such approach before. I think most companies do the Single Almighty Big Editor.

ReplyDeleteWe use a similar approach (but XML instead of JSON), but in our case the engine creates the window for itself. Is there a reason why you chose to create the render window in the tool?

ReplyDeleteBalázs: Sorry, my post was a bit confusing on that point. What actually happens is that the tool creates a parent window and passes the parent window handle to the engine. The engine in turn creates its own child window to that parent and uses that for rendering.


ReplyDeleteSo the engine creates its own window, but as a child to a tool window (so that it can appear "inside" the tool with menu bars, tool bars etc from the tool).

The idea is nice, thanks for sharing. Looks like your current tool chain is Windows oriented, right?(though you mentioned you were going to add support for VNC alike communication and this way make it possible to use any platform for engine running in server mode).

ReplyDeleteNi tar det här med att ha löst kopplade komponenter ett steg längre. Utvecklingsmöjligheterna i detta är ju enorma! Jag blir sugen att se mer detaljerat hur ni bygger! En häftig idé jag fick var att det inte borde vara några problem att i HTML5 göra ett fullfjädrat webbaserat toolset med rendering till canvas-taggen och kommunikationen via ajaxanrop med i sjson. Mycket intressant!

ReplyDeleteThanks for a wonderful article, you've inspired me to write some tools of my own. They are browser based and use HTML5 and websockets, and I kinda ripped off the profiler you've had in the old profiler screenshot. Check it out - https://github.com/hyp/gamedevwebtools .


ReplyDeletegoogle 4009

ReplyDeletegoogle 4010

google 4011

google 4012

google 4013

Nice work, truly valuable to me.


ReplyDeleteI hope you keep it up.

We are offering best offshore development services,

Visit here:

Iyrix Technologies

Remote Software Developers

Software Development Services

Check Developers Rates

대구출장샵


ReplyDelete대전출장샵

부산출장샵

울산출장샵

정선출장샵

울산출장샵

대구출장샵

부산출장샵

속초출장안마



ReplyDelete청도출장안마

용인출장안마

속초출장안마

동해출장안마

고령출장안마

파주출장안마

파주출장안마

I love how you always provide practical and actionable advice.

ReplyDelete