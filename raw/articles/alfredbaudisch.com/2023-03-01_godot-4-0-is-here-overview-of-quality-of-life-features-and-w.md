---
title: Godot 4.0 is here! Overview of Quality of Life Features and Workflow Enhancements
url: https://alfredbaudisch.com/blog/godot-4-0-is-here-release-overview-quality-of-life-features/
author: Alfred Reinold Baudisch
published: '2023-03-01'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

No more waiting for Godot 4.0! You can finally [download](https://godotengine.org/download) [Godot 4.0 stable](https://github.com/godotengine/godot/releases/tag/4.0-stable). After **more than 3 years of an impressive community-driven effort with thousands of developers and almost 22000 contributions, Godot 4.0 is finally here**!

It's a completely new engine while keeping familiar elements from Godot 3. The core has been rewritten from scratch, and Godot is now better than ever for 2D and 3D games, as well applications.

![](../../assets/7c04bb8a6a31adac.png)


![](../../assets/7c04bb8a6a31adac.png)

While there are [hundreds of changes and features](https://godotengine.org/article/godot-4-0-sets-sail/) to be [listed and covered for this release](https://github.com/godotengine/godot/blob/master/CHANGELOG.md), including massive changes such as the addition of the Vulkan renderer, instead, **the focus of this article is in the fundamental workflow and quality of life changes, additions and enhancements brought to Godot 4.0**.

*Thumb background island scene: Tropical Island Scene in Godot 4 (Alpha 8) – Terrain, Water & Placement by Wojtek Pe*.

## Do you prefer video?

This article is also available as a video.

## A brand-new 3D Asset Pipeline

### Fine-Tuned 3D Importing Workflow

Apart from the Vulkan renderer, the **Advanced Import Settings** dialog is probably one of the most important additions in Godot 4.0 for 3D game developers, with preview and customization options for every aspect of imported 3D meshes and animations, their materials and physical properties. It gives all the importing tools that are missing in Godot 3.

You can now fine tune every aspect of a 3D file being imported: meshes, materials, animations, collisions and more.

![](../../assets/6aa2a3b12707c46b.png)


![](../../assets/6aa2a3b12707c46b.png)

### Animation Libraries

You can now create re-usable animation libraries, sharing animation data between different meshes and even different purpose [Animation Players](https://docs.godotengine.org/en/latest/classes/class_animationplayer.html) (not only for 3D).

For example, you can now have a [set of character animations](https://www.youtube.com/watch?v=NBukd3NmK88) such as run, walk, jump and re-use them between different characters, without importing separate animation assets.

![](../../assets/95b751bc8d5cf31e.png)


![](../../assets/95b751bc8d5cf31e.png)

Just like everything else in Godot, [Animation Libraries are also Resources](https://github.com/godotengine/godot-proposals/issues/4296).

### Animation Retargeting

"Retargeting" is the workflow to apply animations between different models. Godot now has proper built-in [Animation Retargeting](https://godotengine.org/article/animation-retargeting-in-godot-4-0/) with the addition of `BoneMap`

and `SkeletonProfileHumanoid`

.

With Animation Retargeting alongside Animation Libraries, you can now have a single source of truth for animations, without having to duplicate or manually remap animations.

### Blender Import Support

You can now import [Blender's](https://www.blender.org/) **.blend* files directly into Godot, thanks to a new Blender importer integration. This makes it easy to create a 2-way flow, allowing you to save changes in Blender and see them reflected in Godot, without the need to export to an intermediate format such as GLTF.

## Scripting is better in every aspect

### GDScript 2.0

Godot's own scripting language, GDScript, has been revamped and is now [GDScript 2.0](https://godotengine.org/article/gdscript-progress-report-feature-complete-40/). Between the many improvements, the most important ones are:

- Typed arrays.
- Functions as first-class citizens. You can now assign functions to variables, pass them as arguments and more (lambdas and Callables). With this, GDScript now also has proper functional capabilities, such as map and reduce.
- Signal connection using function references as well
[Callables](https://docs.godotengine.org/en/latest/classes/class_callable.html#class-callable). - Proper await syntax.
- Faster runtime.

![](../../assets/a7ed1d86bef606ac.png)


![](../../assets/a7ed1d86bef606ac.png)

![](../../assets/f41a45055c6da012.png)

Notice that there are fundamental syntax changes, so be sure to check the new [GDScript guide](https://docs.godotengine.org/en/latest/tutorials/scripting/gdscript/gdscript_basics.html).

#### GDScript 2.0 Exports

There are now [dozens of different export directives](https://docs.godotengine.org/en/latest/tutorials/scripting/gdscript/gdscript_exports.html), making scripts more streamlined with the Inspector, as well making it easier to build custom inspector and tools.

For example, you can now group variables by category:

![](../../assets/61fab039be27aa54.png)


There are different ways to export and retrieve Nodes:

![](../../assets/8b41138424646695.png)


And many more. Be sure to check [GDScript exports](https://docs.godotengine.org/en/latest/tutorials/scripting/gdscript/gdscript_exports.html) in the docs.

### Script Editor Enhancements

The Script Editor now has support to drag and drop as well quality of life enhancements:

- Drag and drop Nodes from the Scene Tree into a script.
- Drag and drop Resources from the File System into a script.
[Multi-carets](https://godotengine.org/article/dev-snapshot-godot-4-0-beta-3/)(ALT+click) and[multi-selection](https://github.com/godotengine/godot/pull/67644)(CTRL+D), similarly to VS Code and JetBrains IDEs (works in any TextEdit container in Godot). By the way, the multi-selection feature was[implemented by me](https://github.com/godotengine/godot/pull/67644)(*although it wouldn't be possible for me to implement it if it weren't for the*) 🙂[great work Paulb23 did](https://github.com/godotengine/godot/pull/61902)with his multi-caret implementation- Support for JSON, YAML and more.

### Exported Custom Resources

The [number one requested feature](https://github.com/godotengine/godot-proposals/issues/18) for Godot is [available](https://godotengine.org/article/dev-snapshot-godot-4-0-beta-2/) in Godot 4.0: [export custom resources](https://github.com/godotengine/godot/pull/62411). It's now possible to assign custom resource files in the Inspector. And thanks to GDScript 2.0 Typed Arrays, it's also possible to assign custom resources into arrays.

### Automatic Documentation

Documentation is now generated on the fly for GDScript code by writing comments on top of classes, methods and members.

It's as easy as writing comments (with support to BB Code), hitting Save and finding the class docs in the built-in documentation browser (F1).

### C#10 and .NET6

For C# users, the port to .NET6 opens up all the features of C#10. Engine extensions can now be written in C# where only lower level languages could be used in the past. In addition, the engine now relies on source generators for better performance and error reporting. Be sure to check the post [What's new in C# for Godot 4.0](https://godotengine.org/article/whats-new-in-csharp-for-godot-4-0/).

## Improved UI and UI design

The whole UI system was revamped, and since the Godot Editor is built with Godot, the 4.0's editor itself benefits from these improvements.

### Visual Layout Options

Aligning and anchoring UI elements and containers is now straightforward due to the added layout options and presets.

### Multiple Window Support

In Godot 4.0 the root node is now [Window](https://docs.godotengine.org/en/latest/classes/class_window.html) which inherits from Viewport (in Godot 3.0 the root node inherits from Viewport).

It's now possible to make games and applications [with multiple windows](https://twitter.com/reduzio/status/1617943360324669441). In the Godot 4.0 editor itself, you can detach some of the dockers into separate windows and even move them to different monitors.

### Improved Sub-resource Editing

Opening and keep tracking of [nested sub-resources](https://godotengine.org/article/editor-improvements-godot-40/) in the inspector is now easier due to color shifting that highlights and adds a border to all the different resources.

![](../../assets/1dbd112da139ac73.png)

## Godot UI Masterclass Course 60% Off

My course ** Godot Engine Course: Data Driven Inventory System and Complex UIs** is a masterclass about Godot's concepts, mostly important on GUI and Godot Resources in-depth. No Godot and GDScript knowledge required. With the course, you are going to learn how to create extensible user interfaces with Godot, but mostly important dynamic data driven systems, check the trailer below.

Available on [Itch](https://bit.ly/GodotUI) or [Skillshare](https://skl.sh/35VyvE1) (one month free).

**To celebrate the launch of Godot 4, the course is going to be 60% off for two weeks!** The course is made with Godot 3, but the update for Godot 4.0 has started and **by buying now, you are going to get the 4.0 Update** when it's ready!

## Extend the Engine with GDExtension

GDExtension is [GDNative's successor](https://godotengine.org/article/introducing-gd-extensions/), that allows us to adapt and extend the engine to specific use cases. GDExtension makes it possible to **write custom engine modules with C, C++ or Rust without ever having to recompile Godot**.

And as opposed to GDNative, writing GDExtension modules is quite straightforward, as it can be seen in [the official guide](https://docs.godotengine.org/en/latest/tutorials/scripting/gdextension/gdextension_cpp_example.html).

## Additional Enhancements

### Consistent Node Names

Godot node names are now unified and consistent. For example, in Godot 3, 2D nodes inherit from Node2D, while 3D nodes inherit from Spatial.

In Godot 4, 2D nodes are still called Node2D, while 3D nodes are now Node3D. See more in [Upgrading from Godot 3 to Godot 4](https://docs.godotengine.org/en/latest/tutorials/migrating/upgrading_to_godot_4.html#automatically-renamed-nodes-and-resources).

### Toggeable Editor Features and Profiles

It's now possible to customize the editor by toggling features from the Editor and the Engine. For example, if you are making a 2D game, you may want to disable all 3D features.

![](../../assets/82a603234f0df240.png)

### Improved Localization

Control (GUI) nodes now include Localization settings. To make localization even simpler, the context-aware translation system now supports plurals and generates translation files directly from project scenes and scripts.

![](../../assets/d142250150beb336.png)


### Git by Default

The Godot Project Manager automatically adds the required Git metadata to set up a new Godot project as a Git repository.

![](../../assets/133a1c7b6773f75c.png)


## Where to go next?

This is just the tip of the iceberg. Godot 4.0 is massive, if you want to learn more about the new features and changes, these are my recommendations:

- Read the official 4.0 Press Release below.
- Check the
[official MASSIVE release post](https://godotengine.org/article/godot-4-0-sets-sail/). - Check the
[official changelog](https://github.com/godotengine/godot/blob/master/CHANGELOG.md). - Check the
[changelog grouped by contributor name](https://downloads.tuxfamily.org/godotengine/4.0/Godot_v4.0-stable_changelog_authors.txt). - The
[Beta 1 release post](https://godotengine.org/article/dev-snapshot-godot-4-0-beta-1/)contains an extensive list of new features. [Upgrading from Godot 3 to Godot 4](https://docs.godotengine.org/en/4.0/tutorials/migrating/upgrading_to_godot_4.html)[All the function renames in Godot 4](https://github.com/godotengine/godot/blob/master/editor/renames_map_3_to_4.cpp)- Check the
[other posts and videos](https://godotengine.org/blog/)from the community about the launch of 4.0. Each post and video created for the 4.0 release is unique, so be sure to check them all! - And of course,
[download Godot 4.0](https://godotengine.org/download/)and play with it by yourself! There's no reason to wait anymore! - Check my
[Godot course](https://splitpainter.itch.io/dynamic-inventory-system-and-ui-with-godot-course)(60% off during Godot 4.0 launch) and[open-source projects](https://alfredbaudisch.com/projects/open-source/my-godot-projects-and-contributions/).

## Press Release

**The new release boasts Vulkan and OpenGL renderers, a game-specific physics engine, boosted graphics and VFX, drastically improved 3D, 2D, multiplayer and XR workflows, as well as wider localization, accessibility, and platform support.**

In an example of community-driven software development gone right, the increasingly popular free and open source game engine has truly leaned into its ability to leverage user input. For the past 3 years, Godot has been quietly undergoing an ambitious overhaul capitalizing on the experience of its numerous contributors and the feedback of its growing user base.

The result: A powerful new release that sees the game engine reviewed from the ground up, improving what worked well and closing the gap on frequently requested features. All while remaining under MIT license, free and open-source forever.

The engine core was rewritten from scratch to build a more robust foundation for evolution. Godot 4.0 now targets developers and gamers who have access to high performance hardware while maintaining and further extending support for users who rely on less powerful devices.

Like its predecessors, the new release is compatible with Windows, Linux and MacOS, but it also runs in and exports to the web browser and Android devices.

There's a quantum leap in visual performance with the new Vulkan backend and support for FSR 1.0, [AMD's Fidelity FX Super Resolution 1.0](https://github.com/godotengine/godot/pull/51679). This is in addition to OpenGL renderers for devices that are not Vulkan compatible.

For 3D game developers who previously found Godot better suited for 2D development, this might be the right time to reconsider. Shadows have significantly improved, and the introduction of new real-time global illumination techniques makes it a breeze to achieve great lighting for both large open worlds and smaller or closed environments. This is in addition to multiple new occlusion culling and LOD methods to optimize rendering, as well as a variety of mid and post-processing options including realistic light units.

VFX and shader support have also level up. Several atmospheric effects are available out of the box such as Volumetric Fog and Sky Shaders, while decals make it easier than ever to project materials and textures. The shader language has been extended and the visual shader editor is more intuitive.

For 2D game makers, Godot 4.0's brand new tile editor is a real game changer. It's effectively a full-fledged level-editing software that brings a plethora of practical additions such as: layers, terrain auto-tiling, a randomized painting system, a tool to copy, stamp, and save selections for reuse, to name just a few.

Godot 4.0 makes importing 2D and 3D assets very straightforward with preview and customization options for every part of the imported asset, its materials and physical properties.

For multiplayer game development, Godot 4.0 networking has become much more reliable with more stable connections, less hanging, and the option to set timeouts and limit network bandwidth. Peer-to-peer networking is available and scene replication is easier than ever. Godot 4.0 can also run in headless mode for server hosting and testing.

With OpenXR, no plugin is necessary to build XR projects and all major Windows and Linux SteamVR headsets are supported out-of-the-box, including the Oculus and Monado. A dedicated XR toolkit and a project template make it easy to get started and WebXR is also supported for browser games.

Godot Physics, the new game-specific physics engine replaces Bullet with major stability improvements, better performance through broadphase optimization and multithreading, as well as a more intuitive workflow and simplified scripting.

Godot 4.0's new server-based navigation system supports fully dynamic environments and on-the-fly navigation mesh baking. Any physics body can be marked as an obstacle for automatic collision avoidance and AI agents can use navigation links for complex pathfinding requiring crossing over gaps, walking onto moving platforms, climbing ladders, etc.

![](../../assets/6fb41527ab1633d6.png)


![](../../assets/6fb41527ab1633d6.png)

With Navigation Links, AI pathfinding is greatly improved. AI agents can navigate to any point of interest in 2D or 3D scenes, crossing over gaps, walking onto moving platforms, climbing ladders and more.

Speaking of scripting, documentation can be automatically generated from script comments and the script editor offers better syntax highlighting, multiple cursor support, drag and drop interaction with the editor and support for various text-based data files, such as JSON, YAML, and more.

Godot's own language, GDScript, has also been revamped for a better coding experience. It features improved syntax, more robust typing, first-class functions and signals, support for unicode characters and faster runtime.

For C# users, the port to .NET6 opens up all the features of C#10. Engine extensions can now be written in C# where only lower level languages could be used in the past. In addition, the engine now relies on source generators for better performance and error reporting.

For companies, studios and developers who need to adapt the engine to their specific use cases, the introduction of GDExtension makes it possible to write custom engine modules using high performance languages such as C, C++ or Rust without ever having to recompile Godot.

UI design is noticeably easier in Godot 4.0 with a new theme editor, multiple window support, more visual layout options, finer control of components and improved text rendering with text wrapping/trimming and access to ligatures and right-to-left languages. Godot 4.0's editor itself benefits from these improvements.

To make localization even simpler, the context-aware translation system now supports plurals and generates translation files directly from project scenes and scripts.

One great example of the editor's many new features, widgets and docks, is the new movie maker mode which makes it possible to render scenes and record videos or trailer footage directly in the engine.

Audio in Godot 4.0 is revised for quality and sound cleanliness. It now features a smart track importing system. Sounds are easier to superimpose to create SFX. Most importantly, text-to-speech is available to support and encourage accessibility in games and apps.

Another game-changing improvement in Godot 4.0 is on the animation front. Reuse greatly speeds up the workflow with the addition of animation libraries and a new animation retargeting system. Blending systems have been rewritten from scratch and the animation tree editor now provides much more control and better flexibility to set up advanced animation graphs and complex state machines.

Console portability is always a point of contention between Godot users and critics. It comes down to Godot's commitment to remain open-source. Any extension of console support would require incorporating console manufacturer's devkits which are hardly ever open source.

This said, [W4 Games](https://w4games.com/), a new company created by Godot Engine veterans is developing a free and easy solution for console ports. According to Godot Lead developer Juan Linietsky, beta access is coming soon.

Godot 4.0 is free to [download](https://godotengine.org/download/), use and modify.