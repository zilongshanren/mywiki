---
title: A Prefab Primer
url: https://www.gamedeveloper.com/audio/a-prefab-primer
author: Nathan Cheever
published: '2018-06-18'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# A Prefab Primer

Grouping objects for repeat use is a way to manage them remotely as well as letting others work on the same scene together. If you've never heard of Prefabs or want to know how to make them more powerful, give this a look!

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![](../../assets/17430bf8c24c4322.img)


Prefabs are not a new topic to game developers. These will be referenced in future articles of mine, so here's an overview to a concept for mastering massive content.

# Introduction

If you’ve ever had to deal with tons of objects across multiple scenes, you’ll inevitably wish you could group similar or exact copies together for quicker management. If you’ve added a desk lamp to 30 different office rooms in 15 different scenes, wouldn't it be nice to turn up the that light's intensity once instead of 450 times?

That’s the power of prefabs.

So, what exactly is a prefab? It's a collection of game objects used in multiple places across the game.


A Prefab should be a Scene. The only thing that should make a prefab different than a scene (a level, map, environment, etc.) is it exists inside a scene. A large city scene can have several small prefab neighborhoods and those in turn can have repeatable prefab houses inside of each.

Some game engines develop prefabs as a unique feature, separate from a scene's format. By developing a prefab as an extension of a classic scene means they inherit all features and power scene editing has!

Any feature that exists for a scene should exist for a prefab:

A collection of models (a bench, a bus stop sign, a garbage can).

A building with AI navigation and interaction nodes.

An enemy with a unique change (BadGuy_Type_4 with dual pistols).

A complex script sequence (depending on project's script file handling).

A skybox with all associated FX and animation.

A Security Door (a door model & logic, security palm switch & logic, emergency lighting & logic, surrounded by cover nodes & path volumes).


## Advantages

Repeat occurrences only have to be created once. When the original prefab is modified, all instances are updated.


Multiple people can work on the same scene by partitioning the scene into prefabs. Each user works on their individual prefab, testing their work in the master scene.


## Game Usage

Prefabs should be created in the editor as a new scene or from a selection within an existing scene. The most common type is a Static Prefab. They can be saved to the game library for reuse later. When the game is built and run, all static prefabs are ungrouped (sometimes called exploded). All parts should have their name prefixed to the prefab's unique name for reference. All game logic now points to unique items maintaining unique scripting.

In the editor they can also be exploded into an existing scene to creating unique, free roaming objects, no longer connected to its source.

Aside from static prefabs, Dynamic Prefabs are another option. These are used to stream in content. If done right, prefabs can be the primary means all content is contained and streamed into the game.

With procedural systems like Houdini, you could even extend prefabs into becoming Smart Prefabs. These feature a set of rules to decide what, where, and when to place a variety objects at different times. This article is only about the core prefab concept though.

# The Concept

Every scene can be made with a number of prefabs. Take a look at the following diagram as an example:

![](../../assets/878fd97a33be2395.img)


Now let's see how prefabs let several people work on the scene:

![](../../assets/b0da0362841e2de7.img)


The Art Team works on the Ground Terrain A location:

Artist 1 models Building D with indoor lighting to be used in 2 locations.

Artist 2 models Building C to be used in 4 locations.

Artist 3 models Building B to be used in 3 locations.

Artist 4 models Building A with indoor lighting to be used in 4 locations.


Artist 5 is lighting the whole scene. Some lighting features on-off logic with Gameplay.

The Audio department is working on ambient Sound for the scene, mixed with Gameplay.

The Design Team is providing gameplay to the Ground Terrain B location:

Designer 3 is creating a generic prefab for assigning AI and stats for a Train Event.

Designer 2 is creating City Tower logic to be used in 4 separate places in Ground B.


And lastly, Designer 1 is providing gameplay for the overall scene in the Master Scene.

When any person is finished, they check their prefab into Source Control to share with the rest of the team. When the master scene is opened again, any existing prefab is updated with the latest changes. When new content ready, the user should be able to pick them from the Resource Browser to add to the scene without restarting the editor.

## Example Scene

Let's group areas in a scene into prefabs, allowing several people to work on each area:


A Designer takes a city block and creates a series of prefabs from it:

Each building is named appropriately and saved as a prefab.

A city block of prefabs is saved as one sector (optional).

The master scene is now a framework of roads, game logic, prefabs, and sectors.


Original Scene | Scene cut into 3 Game Sectors |

Artists individually open each prefab building to edit it:

They can replace the stand-in model with a final version.

They can even add new objects like doors, windows, lamps, lights, etc.

They can open the sector to understand relations between each building prefab.


When a Designer re-opens the scene, all prefabs are updated with changes the Artists have made.

# Slicing Up Scenes

How do you set up scenes to use sectors? How do you work on them? How should logic be arranged in them? Before we talk about sectors, we need to understand how the scene played in the game (the Master, Main, or Persistent scene) is organized. Each scene consists of four basic components:

![](../../assets/8cdc383256ee5f33.img)


Applying this concept to sectors, we can create a framework for maximum flexibility to add (or remove) parts of the master scene without impacting the master scene itself. Each component can become a prefab for each sector.

![](../../assets/e7fa1931367a59b8.img)


Some prefabs don't have to be exclusive to a sector; they can span several sectors. This allows one person to check out a prefab to have access to the whole scene. The disadvantage is when sectors are move around in the master scene requiring contents to be moved manually to their new position.

![](../../assets/fc3ec13d55e69d5a.img)


## Editing Prefabs

Two methods of prefab editing should exist:

Edit the prefab in a new scene.

Edit the prefab in the current scene.


Editing prefab “A” in a new scene isolated from original scene.

Editing prefab “A” within the scene for instant feedback how it affects the scene.

(The fences will need to be modified.)

By editing the prefab within the current scene, it removes switching back and forth between scenes to see your changes.

# Deltas

By their nature, prefabs placed in scenes are instances of the original prefab. If changes are made to the prefab, those changes propagate to all copies in every scene. This can be helpful for example, if you want to change a texture or a light across a hundred copies. You might however only want one small change. You need a way to remember those individual changes, instead of creating a new prefab for each change, exponentially increasing the number in the game library.

This can be solved by tagging any differences and re-applying those differences after changes to the original is made. Technically speaking, values unique to any type of object are stored in the parent prefab or scene file to override its original values. When a change to the original is made, all copies reflect that change unless the value has been overridden on the instance.

An “Allow Deltas” action provides a way to maintain these overrides. With a prefab selected and “Allow Deltas” on (set to true), unique values will be accepted and maintained. If “Allow Deltas” is turned off, all values are reset to their default.

![](../../assets/b97f14b25aabbb54.img)


Without Deltas, editing one prefab edits all of them.

![](../../assets/bad951ebae514bc6.img)


With Deltas, unique edits remain while

any unchanged values inherit changes.

To prevent the need to open prefabs, another option is enabling Child-picking. This ignores prefab containers and directly picks any object in view, no matter how deep they're nested. Normal editing of prefabs should be outlined in red to indicate changing this one instance will change all instances of it. With Deltas on, objects inside prefabs should be outlined in cyan, letting you know any changes will only be applied to the selected object.

# Conclusion

Today’s games involve thousands, if not millions, of objects. Managing all that content, making quick changes, and sharing team efforts, becomes a massive burden without a prefab system in place. If you want to spend more time discovering what’s exciting about your game and less time playing 52,000 card pickup, then take the time to invest in a proper prefab feature.

You can find more posts like this on my website at [CuriousConstructs.com](https://www.curiousconstructs.com).