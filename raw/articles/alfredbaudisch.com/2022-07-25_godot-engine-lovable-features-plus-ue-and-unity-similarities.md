---
title: Godot Engine Lovable Features (plus UE and Unity similarities)
url: https://alfredbaudisch.com/godot-engine/godot-engine-lovable-features-and-characteristics/
author: Alfred Reinold Baudisch
published: '2022-07-25'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

Godot makes my heart feel warm, even if it **frustrates me sometimes** ([as I have previously described in a post](https://alfredbaudisch.com/blog/gamedev/godot-engine/godots-3d-confusing-workflow-inconsistencies-conflicting-behaviours-and-annoyances/)), but most of the time it makes **me love it due to the reasons I am going to list in this article**.

Isn't it strange to declare "love" for a software or tool? **I'm a big advocate of considering any piece of software (or tech) just as tools, that have to be discarded when they don't fulfill their purpose for me anymore. But with Godot (and also Blender and Elixir), things feel different.**

Don't be fooled tho, I still don't use it when I find better tools or better alternatives – i.e. in the case of game engines, I simply use Unity or UE for different purposes, when needed, *but with Godot it still feels like love*. **And even if at one point I decide to discard Godot completely, I would keep it in my list of comfort objects.**

Enough talk, let's go to the list of lovable features and comparisons.

Notices before you begin:

- Based from my 4 years with Godot from
**3.1 to 3.4**. - In order to try to keep this
**list as unbiased as possible**and to**help users of other engines feel at home with Godot**, I added**comparisons with features of Unity and Unreal Engine**in some of the points. I know the 3 engines, so I can pinpoint the differences and similarities between them (and I love – and frequently also hate – each of them for different reasons). - I mention
**"my computer specs"**in some situations, especially when there's consideration for performance and speed. Keep that in mind, as each hardware spec may produce different results.**See my specs at the bottom of the page**. - UPDATE:
[most of 3D workflow issues from the previous article are addressed](https://alfredbaudisch.com/blog/gamedev/godot-engine/godots-3d-confusing-workflow-inconsistencies-conflicting-behaviours-and-annoyances/)in a way or another with Godot 4.

## Resources for Data Modeling and Mapping

**All data you see in Godot is a Resource. A game level, the properties of a mesh, the properties of a sprite, a script attached to a Node, etc. As such you have a single simplified way of handling data in Godot.**

As a Database Architect, this is my favorite thing about Godot. You can mix and match so many different ways of dealing with data in Godot due to Resources.

Additional pros:

- Resources are persisted on disk as text, in a human readable way.
- You can create your own Resource types and extend them as needed. For example, in my Dynamic Inventory System project, items and item categories are custom Resources. They are organized in folders, creating a centralized database. Then, items are customized by creating a Resource file that inherits from my Resource type
`InventoryItem`

. And then I can use them just like any other Godot Resource, including usage of the Resource API.

![](../../assets/697ca35f93fe2bc8.png)


![](../../assets/697ca35f93fe2bc8.png)

Comparisons:

- Unity has
[ScriptableObjects](https://docs.unity3d.com/Manual/class-ScriptableObject.html)for data modeling. - Unreal Engine has many different concepts and APIs in order to achieve the same results: higher flexibility for the cost of higher complexity (and sadly everything is a binary file). The options are:
[Data Assets](https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/AssetManagement/),[Data Tables](https://docs.unrealengine.com/4.27/en-US/InteractiveExperiences/DataDriven/),[Struct Blueprints](https://docs.unrealengine.com/4.27/en-US/ProgrammingAndScripting/Blueprints/UserGuide/Variables/Structs/),[raw UObjects](https://docs.unrealengine.com/5.0/en-US/API/Runtime/CoreUObject/UObject/UObject/)([example](https://www.youtube.com/watch?v=HpUhfnHCENQ)) and even exposed properties from any kind of Blueprint.

## GUI System and UI Development, a Viable Alternative to CSS and Javascript (and Qt)

As opposed to most people, Godot's GUI System is what made me fall in absolute love with the engine. But my reasons are very different from almost every other Godot user: it's because I was looking for a JavaScript and CSS alternative to make user interfaces and business software.

The first thing I made with Godot was [a tiny "Grid Maker" software](https://splitpainter.itch.io/grider). Then things escalated very quickly and **I made a clone of Trello with Godot, Godello, which is very popular amongst Godot's users. Yes, I made a clone of the interface of a full blown complex web application that originally requires thousands of lines of CSS and Javascript.**

![Godello Godot Drag and Drop](../../assets/1482ceaa52a4a110.gif)


![Godello Godot Drag and Drop](../../assets/1482ceaa52a4a110.gif)

With Godot, **I made the UI skeleton visually with its intuitive drag and drop WYSIWYG UI tools** (which is also Node, Scene and Resource based), and then I added dynamic behavior with a few hundreds of GDScript lines.

It's complicated to use words such as "easy", because "easy/hard" is relative. But **Godot actually does make it easy to create responsive and scalable user interfaces with its Layout and Container Nodes**.

To make things even better, Godot UI styling is based on cascading hierarchy based theming, with the possibility of granular styling overrides, for example:

- Global Theme
- Scene Level theme with specific overrides from the global theme
- Container level theme with overrides from both the scene level theme and from the global theme
- Component level overrides

Styles, themes and overrides are defined both with the Theme Editor and the inspector, again WYSIWYG. Styles can also be overridden with code.

**It's magical and IT IS a replacement for Javascript and CSS. A viable alternative for React, React Native, Qt and others**. It's important to remember that I'm even [ writing a book about creating Business Applications and User Interfaces with Godot](https://alfredbaudisch.com/projects/education/godots-book-developing-software-tools-business-apps-api-database/), be sure to check it out.

Comparisons:

- Both Unity and Unreal Engine provides WYSIWYG GUI tools, just like Godot.
- Unity has
[many different](https://docs.unity3d.com/Manual/UI-system-compare.html)ways of creating GUI, with the[UI Builder](https://docs.unity3d.com/Manual/UIBuilder.html)being the most powerful GUI builder of all the 3 engines, with the downside of creating the most performance impacting GUI, due to being Web based – the completely opposite of Godot's GUIs at Runtime. - Unreal Engine has three different ways of creating GUI, and while the
[UMG UI Designer](https://docs.unrealengine.com/5.0/en-US/umg-ui-designer-for-unreal-engine/)is not as easy as Godot's, it also provides all the tools and flexibility to create responsive GUI visually. The biggest downside of UMG is the lack of themes, which forces you to repeat styling in every widget.[Common UI](https://docs.unrealengine.com/5.0/en-US/common-ui-plugin-for-advanced-user-interfaces-in-unreal-engine/)solves that, with the cost of additional complexity.

## Version control friendly, everything is text

Since every Godot resource is saved on disk in a human readable text file (excluding binary assets such as images and meshes, of course), consequentially everything in Godot is *extremely* version control friendly (on top of that, everything has a small footprint).

For example, if you re-structure the entities of a level or a menu (both are the same, since both are a Godot's Scene), you are going to see and compare changes in text:

![](../../assets/a0acf8e811b51b5b.png)


![](../../assets/a0acf8e811b51b5b.png)

Comparisons:

In Unreal Engine, I just inverted a single `if`

condition (a tiny change) in a Blueprint, and this is what I see in version control. Not to mention the big disk space footprint when committing binary changes all the time. To be fair, inside the Unreal Editor you have a way to visualize and compare changes in a beautiful way, but still does not change the fact that you will be comitting binary for every little change and addition.

![](../../assets/4300bcd6626b5816.png)


![](../../assets/4300bcd6626b5816.png)

## Coffee, Coins and Thumbs Up

If you like my content or if you learned something from it, [buy me a coffee](https://ko-fi.com/alfredbaudisch) ☕, [be my Patreon](https://www.patreon.com/alfredbaudisch) or simply check [all of my links](https://linktr.ee/alfredbaudisch) 🔗 and follow me/subscribe/star my repositories/whatever you prefer. If you want to learn Godot, be sure to check [my courses](https://alfredbaudisch.com/projects/education/dynamic-inventory-system-and-user-interfaces-with-godot-course/) 📚!

**Or you can simply add my game to your Steam Wishlist – that helps GREATLY and it's easy and free 🙂**

## Component and Hierarchy Clarity with Scenes and Nodes

Since behaviour and functionality in Godot is defined by creating a tree of Nodes and Scenes, there's nothing that makes you go hunting you project structure in search of stacked hidden behaviours.

Everything is crystal clear: if you have a Node, that's the behaviour. You don't have to click the Node to see additional "components" that may have been added to it. It only has additional components if the Node Tree has Nodes for those behaviours.

![](../../assets/cd2c7f6cb03b4b23.png)


![](../../assets/cd2c7f6cb03b4b23.png)

Comparisons:

- Unity has Game Objects, Components, Prefabs and Nested Prefabs. I
[wrote an article about that](https://alfredbaudisch.com/blog/gamedev/from-unity-to-godot-where-are-my-game-objects-and-components/)and how it compares with Godot. Unity's component stacking inside Game Objects make it hard to find which Components are part of a Game Object, you have to investigate each Game Object individually. - Unreal Engine has
[Blueprints](https://docs.unrealengine.com/4.27/en-US/ProgrammingAndScripting/Blueprints/QuickStart/)and Components (in UE, Blueprint is both the Visual Scripting Language and the "Game Objects" you drag onto your scenes, Blueprints are also data containers).- Just like Unity, a UE Blueprint can have many stacked Components, and you have to investigate each one individually.


## Scripts run in the Editor with a Single Keyword (tool)

If you want to make a script work in the editor, in order to either test behaviour or to extend the editor with your script, simply add `tool`

at the top of the script.

For example, if you have a 3D Mesh for a patrolling enemy, in order to test it, you have to playtest the game. But in Godot, if you add `tool`

at the top of the enemy's script, you are going to see him performing his actions around while you are in the Editor's viewport.

This opens the door for many different possibilities, where the main usage is to extend the editor with custom plugins.

Comparisons:

- Unreal Engine provides ways to create Editor plugins both via Blueprints and C++, see
[Scripting the Editor using Blueprints](https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/ScriptingAndAutomation/Blueprints/). Surprisingly enough, UE also has something similar to Godot's`tool`

, which is called "[Call in the Editor](https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/ScriptingAndAutomation/Blueprints/CallInEditor/)" that can be checked in any piece of Blueprint.- Unreal Engine is the one that offers the most flexibility when it comes to Editor customization and extension, it has a ridiculously complete suite of tools and range of
*debugability*, with its "Widget Reflector" inspector that[works like inspecting a web page](https://youtu.be/zg_VstBxDi8?t=1474).

- Unreal Engine is the one that offers the most flexibility when it comes to Editor customization and extension, it has a ridiculously complete suite of tools and range of
- Unreal Engine's way of handling running behaviour while in the editor is even faster than Godot (in UE it's called "Simulate" and you don't have to change a piece of code, you just press "Simulate" and the Viewport goes live, just like playtesting).
- Unity has extensive documentation regarding
[Extending the Editor](https://docs.unity3d.com/Manual/ExtendingTheEditor.html), but it's not as simple as Godot nor UE.

## Viewport Quick Iteration and Zero Reload Time between Changes

By being able to switch between the 2D, 3D and Script viewports in the editor, you can quickly make changes anywhere and see them immediately. It's very satisfying to quickly toggle between all the viewports, **while making changes to both properties in the Scene Tree, in the Inspect and in a Script** and then seeing them being **reflected without any downtime, without any reload**.

Play testing the changes also happens immediately (depending on your computer).

![](../../assets/4c8721e3888e823b.gif)


Comparisons:

**Unreal Engine is also instant for everything**, including playtesting. I would say that playtesting with UE is even faster than Godot. Press ALT+P, done, game available in ms in the Viewport or a new window (called PIE).**Unity is the slowest of them all, causing the biggest amount of downtime between all the 3 engines**. Even a single comma change in a C# script causes a MonoBehaviour reload in Unity which can take from 5 to 10 seconds (I never seem it taking less and my computer is a massive beast). Then, after that, after you click Play, it also takes another 5 to 10 seconds.- So in Unity, every little change consumes from 10 to 20 seconds.
- Doesn't seem like much? Consider that in a single day of work you make hundreds of changes and you need to playtest hundreds of times. Those seconds quickly add up to hours. It's frustrating.


## Almost-Instant Project and Editor Startup

After the initial indexing and caching of assets, re-opening/re-loading a project in Godot is fast, even if the project has thousands of assets. Godot is still a bit slow to process newly added or re-imported assets, but after that, you don't see any load time.

Comparisons:

- Unreal Engine is very hardware dependent. If you have a computer that follows Epic's recommended specifications, Unreal Engine performs the initial loading and caching quite fast and then
**re-opening the project is also _almost_ instant.****On the other hand, if your computer is not within the recommended specs, the initial caching may consume hours**, specially the well known "Compiling Shaders" step, with some users reporting hours of compilation time.- TL;DR; if you don't have a SSD NVMe M.2 and at least a 12-core CPU, don't even think about UE, unless you like waiting. On the other hand, if you have the recommended specs, using UE is a smooth sailing experience.

**Unity is the one that causes the biggest amount of downtime is this regard as well**, no matter your hardware. If you close and re-open the editor, even without changes, expect Unity to do work with your assets and reload the .NET Assemblies, every time. And every time it may take 10 seconds to minutes to HOURS.

![](../../assets/0f95c816522d759e.png)

## Clear and Simple Input System

No packages, no dependencies, no complexities. Create mappings, call [a single line of code](https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html) to get the input. Done.

Comparisons:

**Unreal Engine is as easy as Godot**, almost the same thing: assign actions and keys, call a single line (or Blueprint node), done.**Unity is very complex and messy when dealing with Input.**It has three different input mechanisms, one conflicting with another. And the most recent one, which is the recommended one to be used,[requires extensive tutorials](https://gamedevbeginner.com/input-in-unity-made-easy-complete-guide-to-the-new-system/)before you can understand and use it.

## Tiny Engine Size, No Installs, Runs in any Hardware, Low Footprint

Everyone talks about this. I don't think I have to elaborate.

- A single file download
- No installation process
- The Editor is not hardware dependent to run well. It just works, with a low footprint, in basically every existing computer spec.

![](../../assets/60c6b9a843429aa0.png)


At the same time it's important to note that while the main engine and editor download does not require a installation process and that's only 40MB, when you need to build and export your project, Godot downloads around 500MB of platform runtimes.

## Straight to the Point Documentation

Not much to say. The header says it all. Check [the Documentation](https://docs.godotengine.org/en/stable/).

## Open-Source and Godot's Codebase Clarity

This section was added a few days after I finished writing this article. I wrote about one of my biggest pains (and annoyances with Godot), which was the "[Viewport switching when clicking Nodes while in the Script editor](https://alfredbaudisch.com/blog/gamedev/godot-engine/godots-3d-confusing-workflow-inconsistencies-conflicting-behaviours-and-annoyances/)".

Being disappointed with the fact that strange UX choice is still present in Godot 4, I decided to clone Godot's source-code and try to fix the issue myself. Less than 30 minutes later, I fixed it, due to Godot's architecture being clear, and its C++ source code being very readable. You can see my [Pull Request here](https://github.com/godotengine/godot/pull/63344) and my "fix journey" in this Twitter thread (open the tweet to see the thread with my steps):

BRB I'll try to find this in the codebase 👀 – maybe there's even a flag somewhere "switch viewports when clicking nodes".

[pic.twitter.com/DDqaPW3SKL]— Alfred Reinold Baudisch (@AlfredBaudisch)

[July 23, 2022]

I don't have any problem coding with C++, but normally open-source C++ projects require some on-boarding time due to complexity, specially if they rely heavily on C++ templating. In this case, my on-boarding with Godot took just a few minutes – the code is crystal clear.

In summary: by being open-source, if you have a pain, you can fix it. And if you don't have the knowledge (or the time, or the patience, or the interest) to fix it, you can ask the community – someone eventually will fix the issue you are having.

## Incredibly Awesome and Caring Community

It may sound cliché, since almost everyone that talks about Godot mentions the "awesome community". But wait until you face a problem or complain about Godot – everyone will make sure your issues are covered, either by providing direct help or by addressing it with Godot Proposals and fixes straight into the Engine.

After I posted my article about my [issues and frustrations with 3D in Godot](https://alfredbaudisch.com/blog/gamedev/godot-engine/godots-3d-confusing-workflow-inconsistencies-conflicting-behaviours-and-annoyances/) 3, one week later, 8 of the issues listed (read: all of them) were addressed!

I have seen that with only 2 other open-source projects, which unsurprisingly I also love deeply:

[Blender](https://blender.org)- The
[Elixir language](https://elixir-lang.org/)(the community there is also awesome!).

What an awesome community. The last pending issue from my article has just been submitted as a proposal by

[@patrick_exe][https://t.co/5DYzqALWcl]– be sure to thumbs up the PR for friendlier Shader Input variables![#GodotEngine][https://t.co/hnUKu1NPjY]— Alfred Reinold Baudisch (@AlfredBaudisch)

[July 24, 2022]

## My Computer

I mentioned "my computer" many times during this article. To keep things as transparent as possible, I think it's import to list my specs in order to understand *MY* context, especially when comparing with other engines, since each case is a case – a user with a worse computer may have way different results.

- AMD Ryzen 9 5900X 12-Cores
- 64 GB Ram
- Geforce RTX 3080 Ti, 12GB VRam
- Samsung 980 PRO SSD PCIe 4.0 NVMe M.2
- I think this is the most fundamental piece of hardware that makes or break usage of an engine – it makes all the difference in the world to have 7800MB/s read and write disk speed versus using slower data storages.


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

Other Godot content in my blog:

[Godot's 3D Workflow Issues, Inconsistencies, and Confusion](https://alfredbaudisch.com/blog/gamedev/godot-engine/godots-3d-confusing-workflow-inconsistencies-conflicting-behaviours-and-annoyances/)[From Unity to Godot: Game Objects and Components in Godot?](https://alfredbaudisch.com/blog/gamedev/from-unity-to-godot-where-are-my-game-objects-and-components/)[Dynamic Inventory System for Godot (Open-source Projects)](https://alfredbaudisch.com/projects/open-source/dynamic-inventory-system-for-godot/)[Donkeys and Quick and Dirty UIs with Godot – Update #1 – Book: Godot Software Development (Education Projects)](https://alfredbaudisch.com/project-logs/donkeys-and-quick-and-dirty-uis-with-godot-godot-book-1/)[Book: Godot Software Development (Education Projects)](https://alfredbaudisch.com/projects/education/godots-book-developing-software-tools-business-apps-api-database/)[Godot Course: Dynamic Inventory System and User Interfaces (Education Projects)](https://alfredbaudisch.com/projects/education/dynamic-inventory-system-and-user-interfaces-with-godot-course/)