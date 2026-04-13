---
title: 'Minecraft Modding: Throwable Fireballs - Alan Zucconi'
url: https://www.alanzucconi.com/2021/04/01/minecraft-throwable-fireballs/
author: Alan Zucconi
published: '2021-04-01'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of the tutorial on **Minecraft modding**; in this article we will create throwable fireballs, using **data packs** and **resource packs**.

- Part 1:
[An Introduction to Minecraft Modding](https://www.alanzucconi.com/?p=13146) - Part 2:
**Minecraft Modding: Throwable Fireballs** - Part 3:
[Minecraft Modding: Laser Gun](https://www.alanzucconi.com/?p=13241)

![](../../assets/5da4dea2da73d486.gif)


![](../../assets/5da4dea2da73d486.gif)

A link to download this mod is available at the end of the page.

In the second part of this tutorial about Minecraft modding, we will see how to create a custom item using data packs and resource packs. More specifically, we will create a throwable fireball. As discussed already in the previous sections, neither data packs not resource packs can *really* create new items. What they can do instead, is customising an existing item by storing some data in its NBT tags, and render that with a custom texture or model. But at its core, the modded item is and remains one of Minecraft’s existing items.

## The Plan

Depending on what weapon or tool you want to create, you should customise one of Minecraft’s existing items. We will see later in this article what are the most commons ones. For now, the plan to create our throwable fireballs is simple:

- Finding an existing item that closely resembles the interaction we want our fireball to have. In our case, that turns out to be a
*snowball*(yes, a snowball!), since it can be hold in the inventory and thrown to inflict damage. - Summoning a fireball (an actual fireball this time) when the custom snowball is thrown.
- Updating the position of the fireball to follow the trajectory of the existing snowball.

We will organise the code in three main functions (`fireball:tick`

, `fireball:throw`

, `fireball:move`

), plus one (`fireball:give`

) to give players the fireballs in their inventory.

![](../../assets/29a795782cb59148.png)


![](../../assets/29a795782cb59148.png)

The mod that is available for download at the end of this tutorial also declares `fireball:load`

, although that is only used to display a message to the players.

![](../../assets/5da4dea2da73d486.gif)

### Data Pack Structure

Our data pack will be called “Fireball”, and will have the following structure:

- 📁 .minecraft
- 📁 saves
- 📁 (WORLD NAME)
- 📁 datapacks
- 📁
**Fireballs**(the*name*of the mod)- 📄
**pack.mcmeta**(contains the name and version of the data pack) - 📁 data
- 📁 minecraft
- 📁 tags
- 📁 functions
- 📄
**tick.json**(used to tell Minecraft to run tick.mcfunction every frame)

- 📄

- 📁 functions

- 📁 tags
- 📁
**fireball**(the*namespace*of the mod, which is used in the code)- 📁 functions
- 💾
**give.mcfunction**(used to give the fireballs to the players) - 💾
**tick.mcfunction**(used to run the fireball code each each frame) - 💾
**throw.mcfunction**(used to instantiate the fireball) - 💾
**move.mcfunction**(used to move the fireball)

- 💾

- 📁 functions

- 📁 minecraft

- 📄

- 📁

- 📁 datapacks

- 📁 (WORLD NAME)

- 📁 saves

The file and folder names in bold are the ones that you are free to change for your own mod. All of the other ones needs to remain as they are.

The file *tick.json* is used to tell Minecraft that the function called `fireball:tick`

will need to be executed every frame (also known as a *tick*). This is its actual content:

{ "values": [ "fireball:tick" ] }

In our case, we will use the function `fireball:tick`

to instantiate the fireballs. Which is why it needs to run every frame.

Minecraft also support a *load.json* file, which can be used to call a function when the data pack is loaded.

### Resource Pack Structure

For our specific asset, this is what we will need:

- 📁 .minecraft
- 📁 resourcepacks
- 📁
**Fireballs**- 📄 pack.mcmeta
- 🖼️ pack.png
- 📁 assets
- 📁 minecraft
- 📁 models
- 📁 item
- 📄 snowball.json (this pack will change the texture of some snowballs)


- 📁 item

- 📁 models

- 📁 minecraft


- 📁

- 📁 resourcepacks

Resource packs are often used to completely replace the original textures and model in the game. As we will see later in this article, we will use snowballs as the “base” item for our fireballs. However, we do not want to replace the texture of *all* snowballs, but only a selected few.

In Minecraft, we can use something called **custom model data** to associate a 7-digit number to an existing item. A resource pack can be made so that it only replaces the graphics of an item with the right *type* and *custom model data*. In our case, we used the (completely arbitrary) number 2538461.

![](../../assets/6eac3def4dc98ca6.png)

![](../../assets/16eaafae14357a5f.png)

The content of the *snowball.json*, below, indicates that we want to replace the model of all snowballs which custom model data is equal to 2538461 with fire charges (which looks more like actual fireballs):

{ "parent": "item/generated", "textures": { "layer0": "item/snowball" }, "overrides": [ { "predicate": {"custom_model_data":2538461}, "model" : "item/fire_charge" } ] }

We will need to make sure that the snowballs that we use have the right custom model data, or their graphics will not be changed. You can pick pretty much any 7-digit number you want for this, although the number must not start with a 0.

A good website to get started with more complex examples is [NovaSkin](https://minecraft.novaskin.me/resourcepacks), which also allows you to draw your own textures and models.

## The Code

While really handy, data packs are subjected to some serious limitations. One above all, is the fact that new items cannot *really* be created. What is possible, instead, is “repurposing” an existing item which closely resembles what we envisioned. This is possible because entities in Minecraft can hold some arbitrary data. This way, we can tag an existing item—such as a sword or a crossbow—and detect every time an item with that tag is being used.

![](../../assets/51a1abfbf503f4f0.png)

![](../../assets/37bda080eac58b39.png)

![](../../assets/c6f321022642c663.png)

![](../../assets/033753b3af812645.png)

![](../../assets/6eac3def4dc98ca6.png)

However, things are not that easy. Right now, Minecraft data packs lack the ability to properly detect events, such as objects being created, used or even simple collisions. The modding community has nonetheless found some very ingenious ways to get around this, even though some might sound very counterintuitive. For instance…

- Detecting right click: carrot on a stick
- Dropping an item: spawn egg / armour stand
- Launching item with charging: bow
- Launching item with reload: crossbow
- Launching item with right click, no charging: snowball

Possibly the most obvious item that we could repurpose to throw fireballs is a bow. A bow could be repurposed as a magic staff, which throws fireballs instead of arrow. However, turning bows and crossbows into guns comes with some additional complexities. This is because while we can tag a a bow to distinguish from the unmodded ones, the arrows that it spawns do not inherit its tags. The problem them becomes detecting when the player shoots an arrow, which is non trivial.

An easier alternative is to use a snowball instead. This is because throwing a snowball does creates a completely new entity, like a bow does. The snowball you are holding is the one that is being thrown, meaning that all of its tags and properties attached while it was in the inventory are preserved when it manifests as a moving entity in the world. Consequently, for this tutorial we will used tagged snowballs to create fireballs.

The YouTube channel Timber Forge has made a very helpful video explaining which item you should start from, depending on what action you want to detect.

### Giving snowballs to players

In Minecraft, players usually obtain new items by crafting. While it is possible to create custom crafting recipes, we will start with a much simple approach. We can simply receive a desired item using the `/give`

command. This can be done using a *command block* inside the game, or typing the command directly in the chat.

[MCStacker](https://mcstacker.net/) is a very handy online tool which allows to easily generate commands. We can use the “/give” section to give one snowball, which has a custom **NBT tag** called `fireball`

with value `1`

:

# CustomTags "fireball:1b" give @p minecraft:snowball{display:{Name:'{"text":"Fireball"}'},CustomModelData:2538461,fireball:1b} 1

By all means, this is a normal snowball, which behaves exactly like all of the other ones. The only difference is that we have changed its name in the inventory to “Fireball” and added some extra bits of information to it. We have also added the **custom model data** necessary to make this snowball appear as a fire charge, as discussed in the previous section about resource packs.

![](../../assets/328bd3cc772a397b.gif)

Normally, Minecraft prevents you from seeing the “real” name of an object. However, you can press `F3`+`H` on your keyboard to enable the NBT tooltips.

## Creating a Fireball

As it turns out, Minecraft actually has a fireball entity that we can use. The ghasts in the Nether dimension are known for throwing them at players. Fireball entities are called `minecraft:fireball`

, and the `/summon`

command will instantiate one at the executor position. This makes things much easier for us, because we do not need to actually create any new item.

![](../../assets/7f6cbb483348bebe.gif)

Since a tagged snowball is available in the player’s inventory, all we need to do is to wait for it to be thrown. Minecraft does not offer any native mechanism to get notified when such an event occurred. For this reason, what we need to do is to run a custom function every frame, to check if a snowballed with an NBT tag `fireball:1b`

has appeared in the game as an entity.

We can now put some code in the “tick.mcfunction” file, searching for all snowballs with the an NBT tag `fireball:1b`

. Once that is found, we can actually summon a fireball where the snowball is. The summoning is conditional to presence of a snowball, and need to happen at the position of the snowball. To do this, we need to use the `execute`

command to change the executor location to the position of the snowball:

# Summon a fireballs at the exact position of each tagged snowball execute as @e[type=minecraft.snowball, nbt={Item:{tag:{fireball:1b}}}] at @s run summon minecraft:fireball ~ ~ ~ # ❌ This will create a trail of fireballs!

If we run this in a command block set on Repeat, our snowballs will leave a rather spectacular trail of fireballs. Really cool, but not what we are here for.

![](../../assets/5524d27f59ac77ef.gif)

If you want to customise the fireball, you can use the “/summon” section of MCStacker.

### Create a companion fireball for each snowball

What we really want is to create only one fireball per tagged snowball. The easiest way to do this is to create a fireball, and the to add another tag the snowball—let’s call it `processed`

. We can change the previous command so that it only operates on snowballs that do not have the `processed`

tag (possible using the `!processed`

syntax).

In order for all of this to work, we need to execute not one but two commands (summoning the fireball and tagging the snowball). This is not really possible in a single `execute ... run`

command. What we can do, however, is to call a function (`fireball:throw`

, in the example below):

#> tick.mcfunction # Invoked every frame execute as @e[type=minecraft:snowball, nbt={Item:{tag:{fireball:1b}}}, tag=!processed] at @s run function fireball:throw

Functions in data packs are just text files with the “mcfunction” extension. This is what throw.mcfunction looks like:

#> throw.mcfunction # AS AT snowball # Creates a fireball where the snowball is # Adds the "player" tag to show it is thrown by the player summon minecraft:fireball ~ ~ ~ {NoGravity:1b,Fire:0,ExplosionPower:1,Tags:["player"],CustomName:'{"text":"Fireball","color":"red"}'} # Adds the processed tag # so that we do not create fire every time tag @s add processed

Since the function is invoked by an `execute`

command, `@s`

will refer to the snowball being processed. We also add the `player`

tag to the fireball, to distinguish it from the ones that are spawned by ghasts.

### Playing the fireball sound

One small—yet effective—addition to the *throw.mcfunction* script would be sound. We can play a sound using the `playsound`

command. Since the fireball model comes from the ghasts, it makes sense to also use the same sound, which is called `entity.ghast.shoot`

:

playsound entity.ghast.shoot player @p

The keyword `player`

inside the command indicates what type of sound this is.

### Move the fireball to the position of the snowball

The really important bit is to make sure that the fireball will always follow the trajectory of the snowball. One way to do that, is to invoke a function (let’s call it `fireball:move`

) every frame, on every special snowball with a companion fireball instantiated (that is, a snowball with the `processed`

tag).

#> tick.mcfunction # Invoked every tick # If the snowball h as been processed, # then we have already created a fireball on top of it # All we need to do is to find that fireball, and update its position execute as @e[type=minecraft:snowball, nbt={Item:{tag:{fireball:1b}}}, tag=processed] at @s run function fireball:move

The most obvious way to move the fireball would be to teleport it to the position of its closest snowball. For instance, by doing the following:

#> move.mcfunction # AS AT snowball # Teleport the fireball to the snowball tp @e[type=minecraft:fireball,tag=player,sort=nearest,limit=1] @s # ❌ Does not work! It only moves at integer positions!

Unfortunately, it appears that this solution does not work as intended. If we try, the fireball will only move at integer positions, basically “lagging” behind the snowball.

![](../../assets/3399f7a04750b86f.gif)


![](../../assets/3399f7a04750b86f.gif)

So, the alternative is to copy the position and velocity of the snowball into the fireball. We can do this using the `data modify entity`

command on the `Pos`

and `Motion`

properties, which every entity has.

#> move.mcfunction # AS AT snowball # Copies the position from the snowball (@s) to its closest fireball data modify entity @e[type=minecraft:fireball,tag=player,sort=nearest,limit=1] Pos set from entity @s Pos data modify entity @e[type=minecraft:fireball,tag=player,sort=nearest,limit=1] Motion set from entity @s Motion

This finally allows us to create a real, throwable fireball!

![](../../assets/5da4dea2da73d486.gif)

### Destroying orphaned fireballs

There is one last thing that we need to take care of. The fireball and the snowball are overlapping, but they technically are different entities. This means that, although unlikely, there is a change that one might die while the other survives.

Unfortunately, there is no way to check if or when an entity gets destroyed. The best we can do it is to destroy all fireballs that do not have a sufficiently close snowball. This can be done using the sub-command `unless entity`

of the `execute`

command. It works as a “complement” to the `if entity`

sub-command, allowing to run a function only when there are no entities of a certain types around. In this case, the target selector is looking for at least one snowball within 1 block away form the fireball. If none is found (= `unless entity`

) then the fireball is destroyed:

#> tick.mcfunction #> Destroy orphaned fireballs # Destroys all fireballs if their closest snowball has been destroyed. # # For every fireball (@s), # IF there are zero snowballs nearby (= UNLESS there is at least one snowball in a radius of 1block) # THEN delete that fireball (@s) execute as @e[type=minecraft:fireball,tag=player] at @s unless entity @e[type=minecraft:snowball, nbt={Item:{tag:{fireball:1b}}}, distance=..1, limit=1] run kill @s

In the command above, we used `limit=1`

because we only need to find one snowball, not to run this code for all snowballs.

If you are familiar with C# and LINQ, that command is loosely equivalent to the following snippet:

// Destroys all fireballs which do not have a snowball nearby // execute as @e[type=minecraft:fireball,tag=player] at @s unless entity @e[type=minecraft:snowball, nbt={Item:{tag:{fireball:1b}}}, distance=..1, limit=1] run kill @s // execute as @e[type=minecraft:fireball,tag=player] at @s ... foreach (Entity fireball in EntityList .HasType("minecraft:fireball") .HasTag("player")) { SetExecutor(fireball); // as @e SetLocation(fireball); // as @s // ... @e[type=minecraft:snowball, nbt={Item:{tag:{fireball:1b}}}, distance=..1, limit=1] bool anySnowballNearby= EntityList .HasType("minecraft:snowball") .HasTag("fireball") .DistanceBetween(0f, 1f) .Any(); // unless entity ... run kill @s if (! anySnowballNearby) Kill(fireball); }

We can test that this works simply by killing all snowballs `/kill @e[type=minecraft.snowball]`

and see that the fireballs are destroyed as well.

If needed, we could also add another condition to destroy all special snowballs which do not have a special fireball nearby.

## What’s Next…

Let’s recap what we have done to create a throwable fireball.

- We use the
`/give`

command to give to the player a custom snowball, with two important changes:- A
**custom NBT tag**`fireball:1b`

to mark it as an actual fireball - A
**custom model data**connected to a resource pack, to render the custom snowball as a fire charge

- A
- We run the
`fireball:tick`

function every frame, to do the following:- For every snowball with the custom NBT tag
`fireball:1b`

which has not been processed yet, a “companion” fireball is summoned; the snowball also received the tag`processed`


- For every snowball with the custom NBT tag
`fireball:1b`

which has been processed, we find the closest fireball and place it at the same position - Every summoned fireball which is not close enough to a snowball, gets destroyed

- For every snowball with the custom NBT tag

This concludes the tutorial on how to create throwable fireballs in Minecraft using data packs and resource packs.

- Part 1:
[An Introduction to Minecraft Modding](https://www.alanzucconi.com/?p=13146) - Part 2:
**Minecraft Modding: Throwable Fireballs** - Part 3:
[Minecraft Modding: Laser Gun](https://www.alanzucconi.com/?p=13241)

### Other resources

This was possibly the easiest way to make throwable fireballs in Minecraft. If you are interested, there are many other resource online which have taken somewhat different approaches.

### Download Minecraft Mod

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

The data packs and resource packs used in this tutorial series to create throwable fireballs and laser guns are available for downloads on [Patreon](https://www.patreon.com/posts/48674330).

## Leave a Reply Cancel reply