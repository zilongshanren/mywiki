---
title: Godot's 3D Workflow Issues, Inconsistencies, and Confusion
url: https://alfredbaudisch.com/godot-engine/godots-3d-confusing-workflow-inconsistencies-conflicting-behaviours-and-annoyances/
author: Alfred Reinold Baudisch
published: '2022-07-21'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

This page lists issues and inconsistencies I've found with Godot's 3D Workflow and 3D Features (some of them apply to 2D as well). They are not bugs, otherwise I'd have reported them, instead they are part of Godot's workflow and defaults.

For the past 4 years I've been using Godot to make all kinds of projects from GUI, to 2D and to 3D and this is how I ended up compiling this list (see my Godot projects and educational content at the bottom of this article).

I think the situation with the Godot Editor and its workflow is just like Blender. Blender pre-2.8 was (and still is) an amazing piece of software, but it was… weird (not to mention Blender 2.4)? And it had a lot of UI inconsistencies, then 2.8 and more recently 3.0 changed everything – Blender is now praised for its UI and its workflow. I think Godot eventually will reach the same status.

The issues here are related from my own usage with Godot 3.*, from 3.1 to 3.5 RC5.

⚠️ *UPDATE 1 (23/07/22): Seven of the issues listed here are gone or partially gone in Godot 4 (using Godot 4 alpha 12)**, of which one of them was fixed by myself, by updating Godot's code.*

## By switching Scene tabs, you lose the Undo tree from the previous tab (2D/3D)

*UPDATE 1: Issue not present in Godot 4.*

In a situation, I made changes to the material of a Mesh in the scene SuvSingleScene:

I went to another scene tab, then went back to the SuvSingleScene and tried to undo the material changes.

Godot only processed the undo action "Switch Scene Tab" and then stated "Nothing to undo", and it just kept jumping between the Switch Tab actions.

![](../../assets/e6402be791d1bb7f.png)


I'm using the example of changing the above Mesh and its materials because it was what I was doing when I decided to write this article, but this situation happens in almost every workflow in Godot.

## Confusion with Mesh Material Assignment and Overrides

**UPDATE 1: Partially solved with Godot 4.**Godot 4 has an "Advanced Mesh Import" dialog where you can choose the material overrides in a single sport.*But***there are still 3 material assignment spots**per Mesh, which is still confusing and unclear.

![](../../assets/9d15597ee415bec6.jpg)

- In Godot we have three different material assignments and/or override spots:
- FIRST: Import a Mesh. In the Mesh Instance,
**the Mesh child Node has a "Surface" property for each material of the Mesh**. - SECOND: In the
**Mesh Instance itself, you also have spots for materials**. - THIRD: Then the
**Mesh Instance also has a GeometryInstance resource where you can also set a MaterialOverride**, but it has only one spot, not one for each surface.

- FIRST: Import a Mesh. In the Mesh Instance,
- During runtime, Godot does not know which material is which, and if you assigned materials to different spots, there will be Material's Z-fighting and flickering.
- I still haven't figured out how to have a custom material in a mesh with multiple materials.

I tried the following: I removed my overrides from "MeshInstance.Material" and placed overrides directly into "Mesh.Surface". In the viewport the Mesh was showing my overrides (i.e. the car does not have the default green material anymore, it has my dirt texture).

Unfortunately, when running the test screen, at runtime, only the mesh's default materials were shown.

It could have been that the inherited scene is defaulting it to the base green material, but unfortunately it was not the case. As a matter of fact I was even trying to override it with the Dirt Texture material in Mesh.Material.

### Expected

Select a mesh, see its list of materials, keep or override materials, done. Single and clear source of truth for materials.

![](../../assets/2493bbdb5c2b485a.png)

## By default, Mesh re-Import resets all of your changes and overrides made in Godot

*UPDATE 1: Godot 4 seems to have this fixed. I didn't face it anymore. See update on the previous item.*

When importing a Mesh in a 3D engine, it's expected that you are going to tweak properties of this mesh to accommodate multiple usages in the game.

By default, Godot's import meshes in such a way, that if you re-import them, let's say when the mesh is updated externally or when you clone the game from the repository again (considering that you already pushed your changes to the repository), all of your changes will be overwritten.

I was working in a small prototype where I had roughly 20 different meshes and in Godot I carefully overrode materials of each of them.

Then every time I changed the meshes on Blender, when going back to Godot, my overrides were reset.

Even by pulling my saved work from Git in order to try to recover my changes, they were still reset, because pulling from the repository is the same as starting fresh with a new `.import`

directory, this way mesh and materials overrides are still lost.

Also by default I get cyclic resource errors when I import and re-import from scratch:

With [a forum post](https://godotforums.org/d/30560-mesh-loses-material-overrides-everytime-it-is-updated-externally-or-re-imported) that I created, I learned that you need to tweak 3 import options in order to preserve overrides across re-imports – so it's a thing to keep in mind:

As a way to avoid confusion, shouldn't **this is the expected behavior by default**?

Unfortunately, changing the import settings solved the issue of custom changes and overrides being lost, but it still **does not solve the conflicting materials issue described before**.

## Coffee, Coins and Thumbs Up

If you like my content or if you learned something from it, [buy me a coffee](https://ko-fi.com/alfredbaudisch) ☕, [be my Patreon](https://www.patreon.com/alfredbaudisch) or simply check [all of my links](https://linktr.ee/alfredbaudisch) 🔗 and follow me/subscribe/star my repositories/whatever you prefer. If you want to learn Godot, be sure to check [my courses](https://alfredbaudisch.com/projects/education/dynamic-inventory-system-and-user-interfaces-with-godot-course/) 📚!

**Or you can simply add my game to your Steam Wishlist – that helps GREATLY and it's easy and free 🙂**

## High GPU usage with simple 3D scenes

**UPDATE 1:** In a similar scene from my original post with Godot 3, Godot 4 reports 0% to 4% GPU usage in the Viewport and less than 20% during runtime.

![](../../assets/c760e45aba0cedbb.jpg)

![](../../assets/7d29e3ed52978a5a.jpg)

While Godot is known for its low footprint and no hardware requirements (it just runs anywhere and the engine is tiny, a 40MB download with no installation), at the same time, for 3D, even in simple scenes, it keeps the GPU burning at 40 to 100% constant usage, with no justification.

I want to point it out, that I always set V-sync on, and going even further, I even try to cap the FPS as well, but it seems that Godot ignores them.

```
Engine.set_target_fps(60)
Engine.set_iterations_per_second(60)
```


In many of my experiments, I simply imported a mesh with a full PBR material, and I couldn't reduce the GPU usage to less than 60% while I was working in the Editor.

Then, to make things worse, when running the game, the usage was constant at 80 to 92%. Why does it use 90% of a RTX 3080Ti in a barebones scene?

On the other hand, with Unreal Engine, I added a scene with all the bells and whistles of UE (Sky, Volumetric Fog, Sky Light, etc) and a mesh, and I even added texture painting during runtime and I managed to keep the GPU at 14% (the Godot's scene that was using 80%+ did not have anything implemented only the mesh).

## Inconsistent Viewport and Script Editor tab switching when clicking Nodes (2D/3D)

*UPDATE 1: Persists with Godot 4. I think this is by design, but it's not an ideal design choice. If I select a Node while in the Script editor, it shouldn't jump to the 2D/3D Viewport, it should stay in the Script editor in order for me to inspect the Node, get references, etc.*

*UPDATE 2: I fixed it myself by adding a new Editor toggeable flag into Godot's source code. I submitted the fix as a Pull Request. If it's not merged officially, I'll end up always compiling Godot from source to have this feature active for my work with Godot.*

**UPDATE 3: ⚠️ The Feature "Don't switch to 2D/3D viewports when selecting nodes while in Script Editor" has been merged and is now available in Godot, starting from Godot 4.0-alpha13 and Godot 3.5RC8.**

This one is especially annoying when making UIs. Because with the kind of UIs I make with Godot (like my clone of Trello and even my Inventory System), you have huge Node Trees where you have to constantly get Node Paths and change things in the Inspector while coding. Then Godot switch viewports every time I click a Node, doesn't matter whether I use the left mouse button (select) or right button (context menu).

- Open the Script Editor
- Click a Node that is still not highlighted in the Scene Tree, because you want to check the Node's properties in the Inspector
- Godot switches to the 2D/3D Viewport
- You have to Switch back to the Script editor
- Now click the same Node in the Scene Tree that you highlighted previously. The tabs won't switch anymore and you are going to stay in the Script editor
- If my active mode is The Script Editor it should stay there, since it's very common to choose Nodes to check properties, Node Paths, etc.

## Confusing and Conflicting Undo and Duplicate behaviors between the Script Editor and the Scene Tree (2D/3D)

*UPDATE 1: Partially solved with Godot 4. When selecting a Node in the Scene Tree, and pressing CTRL+D, the Node gets correctly duplicated, instead of a line of code. Also, CTRL+Z correctly undoes the highlighted widget (Scene Tree or Script).*

- Open the Script Editor
- Click the currently active Node in the Scene Tree (do not click one that is not active because then we run into another issue as previously shown)
- Press CTRL+D to duplicate the Node
- Godot will duplicate a line of Code
- Now double click the currently active Node, rename it
- Press CTRL+Z, Godot will Undo the rename action
- So the inconsistency here is that some hotkeys are captured by the Scene Trees and others by the Script Editor
- You can see in the video below which part is highlighted and which isn't, also notice the lines of code being duplicated even although the Scene tree is focused, but then undoing, it undoes the Node being renamed, it doesn't undo changes in the code.
- This inconsistency happens in multiple situations

## Skinned Mesh animations changed externally are duplicated in Godot upon Mesh re-import

- If you have a Skinned Mesh with animations, for example, a character with a walking animation, import it into Godot, and the Mesh, Skeleton and Animations are correctly imported
- Now, change the walking animation in the 3D package, for example, Blender
- Go back to Godot, the mesh and animations are re-imported
- Instead of updating the animation tracks in use, Godot duplicates the updated animations and it keeps creating duplicates every time you update the animations externally

## Inconsistent Autoplay and Looping animation behaviour (2D/3D)

*UPDATE 1: I found*[bug reports](https://github.com/godotengine/godot/issues/34394)for this, so issue confirmed.**UPDATE 2: With Godot 4′ Import Dialog, when you mark an animation as "Loop Mode: Linear", it loops correctly.**But checking this in the Animation Player still does not work, but that's ok, it's just a bug and Godot 4 is still in Alpha.

![](../../assets/6f41eaa157602e75.png)

- This is a simple one: if you mark an animation as "Autoplay on Load", sometimes it plays, sometimes it doesn't.
- Likewise, if you mark an animation as "Animation Looping", sometimes it loops, sometimes it doesn't.
- The only way to make it consistent is to force playing the animation with code, in a
`_ready`

override. - I don't even have a way to properly report or duplicate this one, because it's random, regardless of the animation type being played.
- Godot 4 update: "Autoplay On Load" seems to be working as expected. But "Animation Looping" loops the animation only while in the editor, not during runtime, so the issue persists (since Godot 4 is in Alpha, this could be a bug).

![](../../assets/a359929cd55db06a.png)

![](../../assets/18453294c17d48c9.png)

## Lack of Camera and Position input data in Shaders

*UPDATE 1: A proposal by @patrick_exe has been created to address this.*

In general, with 3D game engines and 3D packages, when dealing with Shaders provide aliases for common usage input data, such as the Camera and the Object position in world coordinates.

For example, in Unreal Engine, we have many different straight the point Nodes. Three of them as examples:

![](../../assets/436e36b48673efd1.png)


In Godot, we have available some matrices such as: MODEL_MATRIX, INV_VIEW_MATRIX, MODELVIEW_MATRIX and then we have to perform matrix transformations to get the intended input data (for example, to get Absolute World Position or Camera Position in World Space).

Godot's 4.0 documentation was updated recently to [create a naming and math equivalence.](https://github.com/godotengine/godot-docs/pull/5895/commits/e5f23eebf2921763c091f7d3398804d5a8c23f7b) With Godot 3 the names are more unclear, while not providing any friendly way to get those input data.

NOTICE: I'm not saying the matrices should be removed, otherwise Godot's would lack basic data from GLSL, but since the majority of 3D Shaders rely on inputs such as Camera Position, Object Position and others, some name aliases or new default variables would be a welcome and friendly addition.

## My Background with Godot

I have been using Godot for personal projects, experiments and education since 2018. Some of the things I made with it or for it:

- Godello:
[https://github.com/alfredbaudisch/Godello](https://github.com/alfredbaudisch/Godello)a popular Godot-related repository (almost 500 Github stars and thousands of unique page views across all medias) - Dynamic Inventory System and UI for Godot:
[https://github.com/alfredbaudisch/GodotDynamicInventorySystem](https://github.com/alfredbaudisch/GodotDynamicInventorySystem) - Godot Phoenix Channels library:
[https://github.com/alfredbaudisch/GodotPhoenixChannels](https://github.com/alfredbaudisch/GodotPhoenixChannels) - Two 3D games and one 2D game:
[https://itch.io/c/2510992/ludum-dare-games](https://itch.io/c/2510992/ludum-dare-games) - Implementation of a
[texture painting during runtime](https://twitter.com/AlfredBaudisch/status/1547605886499057665)and also[vertex painting in runtime](https://twitter.com/AlfredBaudisch/status/1546028556865642497). - A 10 hour long course:
[https://splitpainter.itch.io/dynamic-inventory-system-and-ui-with-godot-course](https://splitpainter.itch.io/dynamic-inventory-system-and-ui-with-godot-course) - Writing a Book about making software and tools with Godot:
[https://bit.ly/GodotBook](https://bit.ly/GodotBook) - A small "Grid Maker" tool:
[https://splitpainter.itch.io/grider](https://splitpainter.itch.io/grider) - Many small experiments with
[Shaders](https://twitter.com/AlfredBaudisch/status/1546887115350458370)and Particles - Many
[YouTube videos](https://www.youtube.com/watch?v=c3KAhT7Xalo&list=PLqYboeh3Jru6Fds033Q2pdW53qbw-x2Rn&index=1)and a[very popular article](https://twitter.com/AlfredBaudisch/status/1548337776256397312).

I could say that **I touched every aspect of Godot**, from 2D to 3D. Small games, full blown UI use cases, databases and websockets, shaders and more.

While Godot **does some things very elegantly, like the Node Tree, Resources and Small Footprint**, at the same time **the Editor, the Viewports and the basic Workflow still has some inconsistencies, inflexibility, and some weird and conflicting behaviours**.

**Those things keep adding up and up which leads to a lot of wasted time – while they are basic functionality in other engines**.

**I could also just try to fix those myself, as I have more than enough experience and knowledge to be able to investigate where to fix and what to fix – but right now my time and interest are invested in finding the best working tool for my needs instead of trying to fix or re-invent them – I'm finally making a bigger 3D game, with the hopes of launching on Steam by the end of the year.**

For that reason, I contribute to Godot in other ways, [like being their Patreon](https://godotengine.org/donate) and also by creating open-source projects and content for it, as listed above.

Anyway, I will update this topic as I find more issues or if I find solutions (or even if I fix them myself :)).