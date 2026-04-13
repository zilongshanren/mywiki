---
title: Runtime editor-console connection in The Witcher 2
url: https://bartwronski.com/2014/05/13/runtime-editor-console-connection-in-the-witcher-2/
published: '2014-05-13'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

During Digital Dragons and tons of inspiring talks and discussions I’ve been asked by one Polish game developer (he and his team are doing quite cool early-access Steam economy/strategy game about space exploration programmes that you can check out [here](http://store.steampowered.com/app/257930/)) to write a bit more about the tools we had for connectivity between game editor and final game running on a console on The Witcher 2. As increasing productivity and minimizing iteration times is one of my small obsessions, (I believe that fast iteration times, big productivity and efficient and robust pipelines are much much more important than adding tons of shiny features) I agreed that it is quite cool topic to write about. 🙂 While I realize that probably lots of other studios have similar pipelines, it is still a cool topic to talk about and multiple other (especially smaller) developers can benefit from it. As I don’t like sweeping problems under the carpet, I will discuss disadvantages and limitations of the solution we had at CD Projekt RED at that time.

**Early motivation**

Xbox 360 version of The Witcher 2 was first console game done 100% internally by CD Projekt RED. At that time X360 was already almost 7 years old and far behind the capabilities of modern PCs, for which we developed the game in the beginning. Whole studio – artists, designers and programmers were aware that we will need to cut down and change really lots of stuff to make game running on consoles – but have to do wisely not to sacrifice the high quality of players experience that our game was known for. Therefore programmers team apart from porting and optimizing had to design and implement multiple tools to aid the porting process.

Among multiple different tools, a need for connection between game editor and consoles appeared. There were 2 specific topics that made us consider doing such tools:

### Performance profiling and real-time tweaking on console

PC version sometimes had insane amounts of localized lights. If you look at following scene – one of game opening scenes, at specific camera angles it had up to 40 smaller or bigger localized deferred lights on a PC – and there were even heavier lit scenes in our game!

![the_witcher_2_geralt_dungeon](../../assets/15a313c7d47a4038.png)


Yeah, crazy, but how was it even possible?

Well, our engine didn’t have any kind of Global Illumination or baking solution, one of early design decisions was that we wanted to have everything dynamic, switchable, changeable (quite important for such nonlinear game – most locations had many “states” that depended on game progress and player’s decision), animated.

Therefore, GI was faked by our lighting and environment artists by placing many lights of various kinds – additive, modulative, diffuse-only, specular-only, character or env-only with different falloffs, gobo lights, different types of animation on both light brightness and position (for shadow-casting lights it gives this awesome-looking torches and candles!) etc. Especially interesting ones were “modulative” lights that were subtracting energy from the scene to fake large radius AO / shadows – doing such small radius modulative light will be cheaper than rendering a shadowmap and gives nice, soft light occlusion.

All of this is totally against current trend of doing everything “physically-correct” and while I see almost only benefits of PBR approach and believe in coherency etc, I also trust great artists and believe they can also achieve very interesting results when crossing those physical boundaries and have “advanced mode” magical knobs and tweaks for special cases – just like painters and other artists that are only inspired by reality.

Anyway, having 40+ lights on screen (very often overlapping and causing massive lighting overdraw) was definitely a no-go on X360, even after we optimized our lighting shaders and pipelines a lot. It was hard for our artists to decide which lights should be removed, which ones add significant cost (large overdraw / covered area). Furthermore, they wanted to be able to decide in which specific camera takes big lighting costs were acceptable – even 12ms of lighting is acceptable if whole scene mesh rendering took under 10ms – to make game as beautiful as possible we had flexible and scene-dependent budgets.

All of this would be IMHO impossible to simulate with any offline tools – visualizing light overdraw is easy, but seeing final cost together with the scene drawing cost is not. Therefore we decided that artists need a way to tweak, add, remove, move and change lights in the runtime and see changes in performance immediately on screen and to create tools that support it.

### Color precision and differences

Because of many performance considerations on x360 we went with RGBA 1010102 lighting buffer (with some exp bias to move it to “similar range” like on PC). We also changed our color grading algorithms, added filmic tone mapping curve and adapted gamma curves for TV display. All of this had simply devastating effect on our existing color precision – especially moving from 16bit lighting to 10 bit and having multiple lighting, fog and particle passes – as you might expect, the difference was huge. Also our artist wanted to have some estimate of how the game will look on TVs, with different and more limited color range etc. – on a PC version most of them used high quality, calibrated monitors to achieve consistency of texturing and color work in the whole studio. To both have a preview of this look on TV **while** tweaking color grading values and to fight the banding, again they wanted to have live preview of all of their tweaks and changes in the runtime. I think it was easier way to go (both in terms of implementation and code maintenance time), than trying to simulate looks of x360 code path in the PC rendering path.

Obviously, we ended up with many more benefits that I will try to summarize.

**Implementation and functionality**

To implement this runtime console-editor connection, we wrote a simple custom command-based network protocol.

Our engine and editor already had support for network-based debugging for scripting system. We had a custom, internally written C-like scripting system (that automatically extended the RTTI, had access to all of the RTTI types, was aware of game saving/loading and had a built-in support for state machines – in general quite amazing piece of code and well-designed system, probably worth some more write-up). This scripting system had even its own small IDE, debugger with breakpoints and a sampling profiler system.

Gameplay programmers and script designers would connect with this IDE to running editor or game, could debug anything or even hot-reload all of the scripts and see the property grid layout change in the editor if they added/removed or renamed a dynamic property! Side note: everyone experienced with complex systems maintenance can guess how often those features got broken or crashed the editor after even minor changes… Which is unfortunate – as it discouraged gameplay scripters from using those features, so we got less bug reports and worked on repairing it even less frequently… Lesson learned is as simple as my advice – if you don’t have a huge team to maintain every single feature, KISS.

Having already such network protocol with support for commands sent both ways, it was super-easy to open another listener on another port and start listening to different types of messages!

To get it running and get first couple of commands implemented I remember it took only around one day. 🙂

So let’s see what kinds of commands we had:

### Camera control and override

Extremely simple – a command that hijacked in-game camera. After the connection from editor and enabling camera control, every in-editor camera move was just sent with all the the camera properties (position, rotation, near/far planes and FOV) and got serialized through the network.

Benefits from this feature were that it not only made easier working with all the remaining features – it also allowed debugging streaming, checking which objects were not present in final build (and why) and in general our cooking/exporting system debugging. If something was not present on the screen in final console build, artist or level designer could analyze why – whether it is also not present in the editor, does it have proper culling flags, is it assigned to a proper streaming layer etc. – and either fix it, or assign a systemic bug to programmers team.

### Loading streaming groups / layers

Simple command that send a list of layers or layer groups to load or unload (while they got un/loaded in the editor), passed directly to the streaming system. Again allowed performance debugging and profiling of the streaming and memory cost – to optimize CPU culling efficiency, minimizing memory cost of loaded objects that were not visible etc.

While in theory something cool and helpful, I must admit that this feature didn’t work 100% as expected and wasn’t very useful and used commonly in practice for those goals. It was mostly because lots of our streaming was affected by hiding/unhiding layers by various gameplay conditions. As I mentioned, we had very non-linear game and streaming was also used for achiving some gameplay goals. I think that it was kind of a misconception and bad design of our entity system (lack of proper separation of objects logic and visual representation), but we couldn’t change it for Xbox 360 version of Witcher 2 easily.

### Lights control and spawning

Another simple feature. We could spawn in the runtime new lights, move existing ones and modify most of their properties – radius, decay exponent, brightness, color, “enabled” flag etc. Every time a property of a light was modified or new light component was added to a game world, we sent a command over network that replicated such event on console.

A disadvantage of such simple replication was that if we restarted the game running on console, we would lose all those changes. 😦 In such case either save + re-export (so cooking whole level again) or redoing those changes was necessary.

### Simple mesh moving

Very similar to the previous one. We had many “simple” meshes in our game (that didn’t have any gameplay logic attached to them) that got exported to a special, compressed list, to avoid memory overhead of storing whole entities and entity templates and they could be moved without the need of re-exporting whole level. As we used [dynamic occlusion culling and scene hierarchy structure – a beam-tree](http://www.flipcode.com/harmless/issue01.htm), therefore we didn’t need to recompute anything, it just worked.

### Environment presets control

The most complex feature. Our “environment system” was a container for multiple time-of-day control curves for all post-effects, sun and ambient lighting, light groups (under certain mood dynamic lights had different colors), fog, color grading etc. It was very complex as it supported not only dynamic time of day, but multiple presets being active with different priorities and overriding specific values only per environment area. To be able to control final color precision on x360 it was extremely important to allow editing them in the runtime. IIRC when we started editing them while in the console connection mode, whole environment system on console got turned off and we interpolated and passed all parameters directly from the editor.

### Reloading post-process (hlsl file based) shaders

Obvious, simple and I believe that almost every engine has it implemented. For me it is obligatory to be able to work productively, therefore I understand how important it is to deliver similar functionalities to teams other than graphics programmers. 🙂

## What kind of useful features we lacked

While our system was very beneficial for the project and seeing its benefits in every next project in any company I will opt for something similar, we didn’t implement many other features that would be as helpful.

### Changing and adding pre-compiled objects

Our system didn’t support adding or modifying any objects that got pre-compiled during export – mostly meshes and textures. It could be useful to quickly swap textures or meshes in the runtime (never-ending problems with dense foliage performance anyone? 🙂 so far the biggest perf problem on **any** project I worked on), but our mesh and texture caches were static. It would require partial dynamism of those cache files and system + adding more support for export in editor (for exporting we didn’t use the editor, but a separate “cooker” process).

### Changing artist-authored materials

While we supported recompiling hlsl based shaders used for post-effects, our system didn’t support swapping artist-authored particle or material shaders. Quite similar to the previous one – we would need to add more dynamism to the shader cache system… Wouldn’t be very hard to add if we weren’t already late in “game shipping” mode.

### Changing navmesh and collision

While we were able to move some “simple” static objects, the navmesh and gameplay collision didn’t change. It wasn’t a very big deal – artists almost never played on those modified levels – but it could make life of level and quest designers much easier – just imagine when having a “blocker” or wrong collision on a playthrough quick connection with editor, moving it and immediately checking the result – without the need to restart whole complex quest or starting it in the editor. 🙂

### Modifying particle effects

I think that being able to change particle system behaviors, curves and properties in the runtime would be really useful for FX artists. Effects are often hard to balance – there is a very thin line of compromise between the quality and performance due to multiple factors – resolution of the effect (half vs full res), resolution of flipbook textures, overdraw, alpha value and alpha testing etc. Being able to tweak such properties on a paused game during for instance explosion could be a miracle cure for frame timing spikes during explosions, smoke or spell effects. Still, we didn’t do anything about it due to complexity of particle systems in general and multiple factors to take into account… I was thinking about simply serializing all the properties, replicating them over the network and deserializing them – would work out of the box – but there was no time and we had many other, more important tasks to do.

### Anything related to dynamic objects

While our system worked great on environment objects, we didn’t have anything for the dynamic objects like characters. To be honest, I’m not really sure if it would be possible to implement easily without doing a major refactor on many elements. There are many different systems that interact with each other, many global managers (which may not be the best “object-oriented” design strategy, but often are useful to create acceleration structures and a part of data/structure oriented design), many objects that need to have state captured, serialized and then recreated after reloading some properties – definitely not an easy task, especially under console memory constraints. Nasty side effect of this lack was something that I mentioned – problems with modifying semi-dynamic/semi-static objects like doors, gameplay torches etc.

### Reloading scripts on console

While our whole network debugging code was designed in the first place to enable scripts reloading between the editor and a scripting IDE, it was impossible to do it on console the way it was implemented. Console version of the game had simplified and stripped RTTI system that didn’t support (almost) any dynamism and moving there some editor code would mean de-optimizing runtime performance. It could be a part of a “special” debug build, but the point of our dynamic console connection system was to be able to connect it simply to any running game. Also again capturing state while RTTI gets reinitialized + scripts code reloaded could be more difficult due to memory constraints. Still, this topic quite fascinates me and would be kind of ultimate challenge and goal for such connection system.

## Summary

While our system was lacking multiple useful features, it was extremely easy and fast to implement (couple days total?). Having an editor-console live connection is very useful and I’m sure that time spent developing it paid off multiple times. It provides much more “natural” and artist-friendly interface than any in-game debug menus, allows for faster work and implementing much more complex debug/live editing features. It not only aids debugging as well as optimization, but if it was a bit more complex, it could even accelerate the actual development process. When your iteration times on various game aspects get shorter, you will be able to do more iterations on everything – which gives you not only more content in the same time/for the same cost, but also much more polished, bug-free and fun to play game! 🙂

You must be logged in to post a comment.