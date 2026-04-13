---
title: 'Minecraft Modding: Laser Gun - Alan Zucconi'
url: https://www.alanzucconi.com/2021/04/01/minecraft-laser-gun/
author: Alan Zucconi
published: '2021-04-01'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

While guns are not terribly interesting, this tutorial will cover one rather tricky thing to do in Minecraft, which is often associated with guns: **raycasting**. Simply put, this is the process of finding what object we are looking at. No command is sadly able to do that, so we will need to come up with an alternative solution.

- Part 1:
[An Introduction to Minecraft Modding](https://www.alanzucconi.com/?p=13146) - Part 2:
[Minecraft Modding: Throwable Fireballs](https://www.alanzucconi.com/?p=13140) - Part 3:
**Minecraft Modding: Laser Gun**

![](../../assets/ab92bc97757d3d41.gif)


![](../../assets/ab92bc97757d3d41.gif)

## The Plan

If you have followed the second part of this series about Minecraft modding, you should know by know that the first step is usually finding an existing item that closely resembles the interaction that we desire. There are no guns in Minecraft, although the closest thing would be a crossbow. One possible solution to create a gun would be to repurpose the arrows of a crossbow so that they are super fast and unaffected by gravity. Many existing guns are indeed crossbows in disguise.

However, this is not the approach that we will take. No matter how fast, arrows are not as fast as lasers. For this reason, an actual bullet would be undesirable in this situation. A popular option is to rely on an unusual item: a **carrot on a stick**.

So this is the plan:

- We will use the
**scoreboard**to record when a player is first using the carrot on a stick that we gave them. This is possible because we can add an objective that gets incremented every time an item is used. - As soon as the count goes up, we start shooting. This is done using a process called
**raycasting**, which basically calls a function repeatedly, every time moving the position of the executor a tiny bit ahead. - All of the entities that too close to the raycast paths gets killed.
- We keep moving forward until we hit a solid block. At that point, we destroy the block and spawn a few particles.

We will use the following scripts:

![](../../assets/8a19316eff1254bc.png)


![](../../assets/8a19316eff1254bc.png)

An additional one, *uninstall.mcfunction*, could be needed in case a player wants to fully remove this mod (to remove the scoreboard objective added by *load.mcfunction*). However, Minecraft does not offer any way to natively detect when a mod is being disabled.

### Data Pack Structure

The data pack for this mod will have the following structure:

- 📁 .minecraft
- 📁 saves
- 📁 (WORLD NAME)
- 📁 datapacks
- 📁
**Laser Gun**(the*name*of the mod)- 📄 pack.mcmeta
- 📁 data
- 📁 minecraft
- 📁 tags
- 📁 functions
- 📄 tick.json (used to tell Minecraft to run
*tick.mcfunction*every frame)

- 📄 tick.json (used to tell Minecraft to run

- 📁 functions

- 📁 tags
- 📁
**lasergun**(the*namespace*of the mod)- 📁 functions
- 💾
**load.mcfunction**(used to initialise the scoreboard) - 💾
**give.mcfunction**(used to give the laser gun to the players) - 💾
**tick.mcfunction**(used to detect right clicks) - 💾
**shoot.mcfunction**(used to start the raycast) - 💾
**raycast.mcfunction**(used to find where the laser collides) - 💾
**hit_block.mcfunction**(used to destroy the block that was hit) - 💾
**hit_mob.mcfunction**(used to destroy the mob that was hit)

- 💾
- 📁 tags
- 📁 blocks
- 📄
**raycastable.json**(used to decide which blocks the laser can go through)

- 📄
- 📁 entity_types
- 📄
**killable.json**(used to decide which entities can be killed by the laser)

- 📄

- 📁 blocks

- 📁 functions

- 📁 minecraft


- 📁

- 📁 datapacks

- 📁 (WORLD NAME)

- 📁 saves

The file and folder names in bold are the ones that you are free to change for your own mod. All of the other ones needs to remain as they are.

### Resource Pack Structure

Compared to the previous examples that we have seen, this resource pack is much more complex. So let’s break it down, piece by piece.

First, we have the *pack.mcmeta* and *pack.png* used for the description and icon that will appear in the Option menu.

- 📁 .minecraft
- 📁 resourcepacks
- 📁
**Laser Gun**- 📁 assets
- 📄 pack.mcmeta (the name and description of the mod)
- 🖼️ pack.png (the icon of the mod)


- 📁 assets

- 📁

- 📁 resourcepacks

Let’s see what other folders and files we need.

#### Texture

In previous tutorial we replaced the models of snowballs with fire charges. This requires only one file, since the asset that we wanted was already present inside Minecraft. In this case, we want to use a completely different texture. This requires thee files in a slightly more complicated setup:

- 📁 .minecraft
- 📁 resourcepacks
- 📁
**Laser Gun**- 📁 assets
- 📁 minecraft
- 📁 models
- 📁 item
- 📄 carrot_on_a_stick.json (#1: to replace the model; points to
*laser_gun.json*)

- 📄 carrot_on_a_stick.json (#1: to replace the model; points to

- 📁 item

- 📁 models
- 📁
**lasergun**- 📁 models
- 📁 item
- 📄
**laser_gun.json**(#2: information about which texture to use for the model, points to*laser_gun.png*, #2)

- 📄

- 📁 item
- 📁 textures
- 📁 item
- 🖼️
**laser_gun.png**(#3: the texture for the laser gun)

- 🖼️

- 📁 item

- 📁 models

- 📁 minecraft

- 📁 assets

- 📁

- 📁 resourcepacks

The first file, *carrot_on_a_stick.json*, indicates that we want to replace the model for the tagged carrot on a stick with a custom one, defined in *laser_gun.json*.

{ "parent": "item/handheld_rod", "textures": { "layer0": "item/carrot_on_a_stick" }, "overrides": [ { "predicate": { "custom_model_data": 9039965 }, "model": "lasergun:item/laser_gun" } ] }

The file *laser_gun.json* simply indicates a new texture for the item, which is *laser_gun.png*:

{ "parent": "item/generated", "textures": { "layer0": "lasergun:item/laser_gun" } }

### Sound

For this mod, we will also need to add a new sound. To make sure that a sound file gets loaded, we need to add a special file called *sounds.json*.

- 📁 .minecraft
- 📁 resourcepacks
- 📁
**Laser Gun**- 📁 assets
- 📁
**lasergun**- 📄 sounds.json (#1: declares which sounds to load)
- 📁 sounds
- 🔊
**shoot.ogg**(#2: the sound to use when shooting)

- 🔊


- 📁

- 📁 assets

- 📁

- 📁 resourcepacks

The *sounds.json* file provides some metadata for the actual sound:

{ "shoot": { "category": "record", "sounds": [ { "name": "lasergun:shoot", "stream": "false" } ] } }

For this mod, we have used a generic [Laser Gun Sound Effect](https://www.youtube.com/watch?v=FsLkXXOyeRI&ab_channel=Seaguli).

## The Code

### Giving the laser gun to players

The first step is to make sure that players can have access to the laser gun. That is implemented using a **carrot on a stick** which has two important custom NBT tags set: `CustomModelData`

and `lasergun`

:

#> give.mcfunction give @p carrot_on_a_stick{display:{Name:'{"text":"Laser Gun","italic":false}'},CustomModelData:9039965,lasergun:1b} 1

The former is used to make sure that the companion resource pack can alter the model of this specific carrot on a stick, without replacing *all* other carrots on a stick. The latter is used to make sure that we can shoot only when the player is holding this specific laser gun.

### Right Click Detection

Minecraft does not unfortunately offer any way to test for right clicks. One of the most common solutions that is often used in data packs relies on scoreboard objectives. The scoreboard is a complex system that Minecraft uses to store arbitrary data about certain events. It is often used for things like achievements, timers, and even to to perform some basic arithmetic.

In our case, we will use it to create a new objective, called `click`

, which is increased by one every time that a carrot on a stick is used. This is done in the *load.mcfunction* script:

#> load.mcfunction scoreboard objectives add click minecraft.used:minecraft.carrot_on_a_stick

It is important to remember that calling a script *load.mcfunction* is not enough for Minecraft to execute its code. To make sure this is recognised, it needs to be properly tagged inside *load.json*, as briefly described in the section about the data pack structure.

Once the objective is set, we can run a function every frame to target all players which `click`

score is above one. This means that they have used the carrot on a stick. If that is the case, we invoke `lasergun:shoot`

which will start the raycast process. At the end, we reset the score back to zero, so that this does not become a one time use only:

#> tick.mcfunction # Right click detection execute as @a[scores={click=1..},nbt={SelectedItem:{tag:{lasergun:1b}}}] at @s run function lasergun:shoot # Resets the scores scoreboard players reset @a[scores={click=1..}] click

It is important to notice that we also need to test for the value of the `SelectedItem`

NBT tag. This is a tag that gets set when the player selects an item; in our case, we can use it to detect the `lasergun:1b`

tag which identifies the carrot on a stick which we converted into a laser gun.

If you are interested, Zedwiki has a very interesting article which explore much more in details [Using carrot on a sticks as triggers](https://zedwork.co.uk/wiki/Using_carrot_on_a_sticks_as_triggers).

### Raycast

For the ones of you who are working in the field of game development, you might be familiar with the concept of **raycast**. This is the process of projecting an imaginary ray from a point in space, and to extend it until it hits something. You can imagine casting a ray as shooting a laser beam. Many game engines have ample support for raycasts; Unity, for instance, has a method called `Physics.Raycast`

, while Unreal implements a similar functionality through `LineTraceByChannel`

. Sadly, Minecraft offers no support for raycasting.

There are many ways in which raycasting can be performed. In the past, many modders have used invisible armor stands because they are one of the few non-mob entities which react to collisions. In this tutorial we will use a different, cleaner approach, which is based on the concept of **recursion**. Recursion is when a function calls itself, repeating its code until a certain condition is met.

The main idea is simple: starting from the position of the player, we move along its forward direction by a tiny amount. We check which block is present at that position: if it is air, we keep moving forward, until something solid is being hit.

![](../../assets/9945dcce107c6524.png)


![](../../assets/9945dcce107c6524.png)

The function `lasergun:shoot`

will start this process, by invoking the `lasergun:raycast`

function (which is where the recursion will actually take place). Since we want to shoot from the position of the player’s eyes, we can use the sub-command `anchored eyes`

, which will move the **execution position** at the centre of the camera:

#> shoot.mcfunction execute as @p at @s anchored eyes run function lasergun:raycast

The raycast code is simple: if the block where we currently are is empty (i.e.: it is an *air block*), we move forward by a tiny bit and we invoke `lasergun:raycast`

again. We can alter the execution position using the sub-command `positioned`

:

#> raycast.mcfunction # AS player, AT current raycast position execute if block ~ ~ ~ minecraft:air positioned ^ ^ ^0.02 run function lasergun:raycast execute if block ~ ~ ~ minecraft:cave_air positioned ^ ^ ^0.02 run function lasergun:raycast execute if block ~ ~ ~ minecraft:void_air positioned ^ ^ ^0.02 run function lasergun:raycast

In Minecraft there are different types of air blocks. Both *air*, *cave air* and *void air* blocks behave exactly in the same way, and the difference between them is just *technical*, not *practical*.

The raycast process will eventually stop when one of this condition is met:

- A non-air block is found, in which case
`lasergun:raycast`

will not be invoked anymore; - We code reached a position outside the render distance;
- The code has run for too long.

The problem is that right now we have no way of knowing when that is the case. What we need is a sort of *else statement*: a way of also checking if the block at the executor position is *not* air. And if it is not, to destroy is.

The “complimentary” of the sub-command `if block`

is `unless block`

, which executed a command when the block is not of the desired type. But this becomes tricky to do in a single command, when there are three separate conditions that needs to be met. A more elegant solution is to create a **block tag** which groups together all the “raycastable” blocks which the laser can pass through (in our case: air, cave air and void air). We can do this by adding a *raycastable.json* file to the data pack:

- 📁 .minecraft
- 📁 saves
- 📁 WORLD_NAME
- 📁 datapacks
- 📁
**Laser Gun**- 📁 data
- 📁
**lasergun**- 📁 tags
- 📁 blocks
- 📄
**raycastable.json**

- 📄

- 📁 blocks

- 📁 tags

- 📁

- 📁 data

- 📁

- 📁 datapacks

- 📁 WORLD_NAME

- 📁 saves

The file will have the following content, telling Minecraft that from now on `#lasergun:raycastable`

is a new **block type** that matches with air, cave air and void air:

{ "replace": false, "values": [ "minecraft:air", "minecraft:cave_air", "minecraft:void_air" ] }

This approach is very handy because we can also add any other block that we might want the laser to go straight through, such as grass, snow or water.

One thing that might be confusing is that this new tag, `#lasergun:raycastable`

, starts with a hashtag. The symbol is usually used for comments: using it for anything else makes for a weird syntactic choice. One that can sometimes even trick mcfunction syntax highlighters.

With the new tag in place, the code now becomes:

#> raycast.mcfunction # AS player, AT current raycast position # Have we found an empty block (=raycastable)? Then continue! execute if block ~ ~ ~ #lasergun:raycastable positioned ^ ^ ^0.05 run function lasergun:raycast # Have we found a non-raycastable block? execute unless block ~ ~ ~ #lasergun:raycastable run function lasergun:hit_block

Now we can put the code to destroy a block in the *hit_block.mcfunction* file:

#> hit_block.mcfunction # AS @p AT raycast hit position setblock ~ ~ ~ minecraft:air destroy

Using the `destroy`

mode of the `setblock`

command will drop items as if the block was actually being mined. In this case, this makes for a pretty nice mining gun.

#### Particle

We can make much clear that this is a laser gun by leaving a trail of some kind during the raycast process. This can be done by calling the `particle`

command after the raycast. For instance, this will leave a smoke trail:

particle minecraft:smoke ~ ~ ~ 0 0 0 0 0

We can also add a particle effect inside *hit_block.mcfunction*, which is executed when a block has been hit by the laser.

You can find a list of all particles available here on this article: [List of all particles](https://minecraft.gamepedia.com/Particles).

### Killing entities

The current code will only destroy blocks, leaving any entity on its path unaffected. This might not exactly be what you want. The simplest option to overcome this problem is to add a line inside the `lasergun:raycast`

function that also destroys any non-player entity that is too close to the executor position:

kill @e[type=!minecraft:player, distance=..1]

This will leave a trail of destruction along the path of the ray, killing any entity or mob in its way. For the best possible effect, the line should be *placed* before any call to `lasergun:hit_block`

. If it is placed after, it will destroy any item or block dropped by the destroyed block.

![](../../assets/834c316fb97c32ca.gif)


![](../../assets/834c316fb97c32ca.gif)

The main drawback of a solution like this is that it would destroy *all* non-player entities (including item drops!) which might be undesirable. What if we want to only kill mobs? We can create an **entity group**, similarly to what we did when we grouped together all raycastable blocks using tags. All we need is a *killable.json* file:

- 📁 .minecraft
- 📁 saves
- 📁 WORLD_NAME
- 📁 datapacks
- 📁
**Laser Gun**- 📁 data
- 📁
**lasergun**- 📁 tags
- 📁 entity_types
- 📄
**killable.json**

- 📄

- 📁 entity_types

- 📁 tags

- 📁

- 📁 data

- 📁

- 📁 datapacks

- 📁 WORLD_NAME

- 📁 saves

which lists all of the entities that we want to target; namely, all the mobs in the game:

{ "replace": false, "values": [ "minecraft:bat", "minecraft:bee", ... all the mobs ... "minecraft:zombified_piglin", "minecraft:zombie_villager" ] }

You can find the complete list here: [Minecraft Entity List (Java Edition 1.16)](https://www.digminecraft.com/lists/entity_list_pc.php). Since new mobs are constantly being added, we will need to update this file with each new update.

Now that we have a way to indicate *all mobs*, we can update our `execute`

command:

kill @e[type=#lasergun.mobs, distance=..1]

If you need to run something more substantial (for instance playing a sound or spawning particles) you can create a new function (let’s say) `lasergun:hit_mob`

which could be invoked like this:

execute as @e[type=#lasergun:killable, distance=..1] at @s run function lasergun:hit_mob

This command can be safely executed *after* the raycast functions have been called and the particles have been spawned. This way, any change made to to the execution position (`at @s`

) is not going to change the position of the raycast. This is because each function has its own execution context.

## Conclusion

Let’s recap what we have done to create a laser gun:

- We use the
`/give`

command to give to the player a custom carrot on a stick, with two important changes:- A
**custom NBT tag**`lasergun:1b`

to mark it as an actual laser gun - A
**custom model data**connected to a resource pack, to render the custom carrot on a stick as a laser gun

- A
- We create a
**scoreboard objective**that is incremented every time the carrot on a stick is used. - Every frame we check if the scoreboard objective has been incremented; if that is the case, we invoke the shooting function
- This uses
**raycast**to detect which block the laser ray will hit. The blocks the ray can go through are grouped together using a custom block tag`#lasergun:raycastable`

, which includes all types of air blocks (*air*,*cave air*and*void air*). - At every tick, all killable objects on the laser path are destroyed. We grouped all killable objects using the custom entity tag
`#lasergun:killable`

. - Particles effects are created and sounds are played to create a more compelling experience

- This uses

This concludes the tutorial on how to create a laser gun in Minecraft using data packs and resource packs.

- Part 1:
[An Introduction to Minecraft Modding](https://www.alanzucconi.com/?p=13146) - Part 2:
[Minecraft Modding: Throwable Fireballs](https://www.alanzucconi.com/?p=13140) - Part 3:
**Minecraft Modding: Laser Gun**

### Other resources

In this tutorial we have covered how to create a laser gun. However, we have not done much in terms of animating it. A much more professional resource pack is [3D Gun Resource Pack](https://resource-pack.com/3d-gun-resource-pack-1-14-1-15/), which not only turns a crossbow into a gun, but also provide a very nice reloading animation. It is a good starting point for all Minecraft weapons that needs a reloading effect.

![](../../assets/2f22eb76dbc3e583.jpg)


![](../../assets/2f22eb76dbc3e583.jpg)

### Download Minecraft Mod

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

The data packs and resource packs used in this tutorial series to create throwable fireballs and laser guns are available for downloads on [Patreon](https://www.patreon.com/posts/48674330).

## Leave a Reply Cancel reply