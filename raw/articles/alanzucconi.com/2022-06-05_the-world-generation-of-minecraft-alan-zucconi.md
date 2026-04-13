---
title: The World Generation of Minecraft - Alan Zucconi
url: https://www.alanzucconi.com/2022/06/05/minecraft-world-generation/
author: Alan Zucconi
published: '2022-06-05'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is a companion article to the documentary about the world generation of Minecraft, which you can see below. This is a chance to expand on the content, including more information and resources that was not possible to include in the original 45 minutes of the video.

Have you ever wondered how many grains of sand are on this planet? Well …a rough estimate is… over 7 quintillion! That’s a 7 followed by 18 zeros. And yet, that’s not even half the number of the unique words in Minecraft. So how does Minecraft—and other games like it—build such complex, beautifully crafted yet fully procedural worlds? This article will explore how the game generates its worlds: from its tallest mountain, to its deepest cave. Welcome to the World Generation of Minecraft.

## Part 1: Procedural Generation

For many of you watching, Minecraft might be the first—and perhaps the only—game you’ve played

in which worlds are not hand crafted by a level designer, but are instead created procedurally.

And yet, the Guinness World Record for the first game to feature a procedurally generated world goes to “Elite”, originally developed for the BBC Micro in 1984. The great-grandfather of the more recent “Elite: Dangerous” from 2014.

![](../../assets/8034651fe9217e98.gif)


![](../../assets/8034651fe9217e98.gif)

Generating new worlds automatically might appeal to some as a lazy way to create endless content for a game. But actually it’s… quite the opposite! You need to be such a good programmer and such a good level designer …that you can teach a machine what a good level looks like.

The content must be diverse enough to look novel, but not so diverse that it looks atypical. And it must create worlds that are not only interesting to look at, but playable in a way that—regardless of their actual difficulty—feel fair to the player.

Procedural content generation is definitely not for the faint-hearted. But no matter how complex your algorithms are, they’re all powered by one thing only: randomness. And Minecraft is not an exception: each world starts from a seed: which is basically a number used to initialise the terrain generation and everything it will contain.

These algorithms might be random, but they are also deterministic. It means that given the same initial conditions–the same seed–they’ll always produce the same results. And this is why each Minecraft world can be recreated just from its seed. And since the seeds themselves are stored using 64 bits, there are 18.4 quintillion unique values—and unique worlds—that can be created.

No Man’s Sky is also using 64-bit seeds, which explains why–incidentally–there are 18.4 quintillion unique planets in that game too.

### “Rogue” (1980)

But how can random numbers–which is essentially your computer throwing dice–create worlds? Well, perhaps it’s best to start from something slightly smaller than Minecraft. Welcome to the “Dungeons of Doom”.

Originally released in 1980, “[Rogue](https://en.wikipedia.org/wiki/Rogue_(video_game))” is generally credited with being the first graphical adventure game and it served as a major source of inspiration for the thousands of dungeon crawlers which came in the following decades.

Minecraft too shares many of the characteristics that made Rogue so iconic: and generating procedural dungeons for the player to explore is just one of them.

Rogue is generally credited with being the first “graphical” adventure game, and it probably was at least one of the first

So how did Rogue create its “Dungeons of Doom” back in 1980? Each level is divided into a 3 by 3 grid, with a random room placed in each cell.

![](../../assets/4337a464493687bf.jpg)


![](../../assets/4337a464493687bf.jpg)

The algorithm proceeds by selecting a room for the player to spawn in, and marks it as “reachable”. It then iterates through all of the other rooms, connecting them to a previously reached neighbour (if possible) or skipping to the next one. A stair to the next level is then placed in the last room to be connected.

“Rogue” can also feature dead ends, secret doors and even monster rooms! All done in roughly 9.000 lines of code over 300 functions! …307, to be precise! By comparison, Minecraft 1.18 counts over 52.000 functions from approximately 4200 files!

So get your diamond armour and your enchanted sword ready, because we are about to descend into the treacherous depths of Minecraft’s source code.

## Part 2: The History of Minecraft

Regardless of its complexity, it is undeniable that the universe crafted by Mojang is built upon ideas, techniques and algorithms that were pioneered by previous games (and even movies), some of which date from decades ago.

And so, it would really be a disservice to talk about the history of Minecraft without mentioning the actual game that inspired it: “Infiniminer”.

At a first glance, it looks like a mining game where two teams are competing to collect as much ore, gold and diamonds as possible. But “Infinimer” was as much about mining as it was about building; not just your base, but entire stories.

It’s easy to see how this game directly inspired Minecraft; from the blocks, to the pickaxe, from the caves to lava lakes, from the gold to the diamonds, from the sky to the void! Even the TNT! In a parallel universe, this is what Minecraft could have been instead.

While far from being infinite, each “Infiniminer” map is indeed generated procedurally. It all starts with a solid chunk of dirt, in which a number of ore veins are painted. Each one begins at a random position, with each iteration moving the vein in a random direction. This technique is–unsurprisingly–known as “random walk”.

Mountains and caves are created with the exact same technique: the former erected by replacing air with dirt, the latter carved by replacing dirt with air. Diamonds, meanwhile, are randomly scattered towards the bottom part of the level.

While this might sound simple–perhaps too simple–it was not dissimilar to how Minecraft worked for the first nine months of its development. In its very first iteration–known at the time as “Cave Game”–each world was only 256 blocks wide, and 64 tall.

And while “Infiniminer” never really intended to be–well–infinite, it took indeed nine months to finally fulfil the dream of a boundless Minecraft world. And it happened using a very simple trick: every time the player goes too far, a new “chunk” of the world is created.

After that, each world would only be bound in size by software limitations: on a 32-bit system for example, that’s roughly up to 4.3 billion blocks away from the spawn point.

But wait! Before you start packing for the journey, you can’t actually go that far! Players are restricted to a 60,000,000 by 60,000,000 blocks area. Which doesn’t sound like a lot when compared to infinity. But still, that’s seven times bigger than Earth’s surface. Just about half the size of Neptune!

![](../../assets/71b70ba10460f0b8.png)


![](../../assets/71b70ba10460f0b8.png)

| Earth | Minecraft | Neptune | |
|---|---|---|---|
Radius | ![]() | ![]() | ![]() |
Surface area | ![]() | ![]() | ![]() |
Side as square | ![]() | ![]() | ![]() |

And even so, bigger doesn’t necessarily mean better. No version of Minecraft does really offer any new gameplay mechanic at a scale beyond 25.000 blocks. While the world looks rich and diverse up close, a pattern appears the further we zoom out. Eventually, each sufficiently large patch of the world will look indistinguishable from any other. At that scale, Minecraft is isotropic, pretty much like our universe is expected to be at its largest scale. This reveals the “true” scale at which the game was designed to be played. And, consequently, the scale at which its world generation is truly meant to operate. And to be enjoyed.

![](../../assets/9fed101aed479f77.png)


![](../../assets/9fed101aed479f77.png)

![](../../assets/6fd678b5feeb85e2.png)


![](../../assets/6fd678b5feeb85e2.png)

![](../../assets/96f257a3e9e2ec2f.png)


![](../../assets/96f257a3e9e2ec2f.png)

![](../../assets/33d21e8e0f2ca035.png)


![](../../assets/33d21e8e0f2ca035.png)

![](../../assets/527bc2b7a0cb15ba.png)


![](../../assets/527bc2b7a0cb15ba.png)

![](../../assets/60620f53998c43bb.png)


![](../../assets/60620f53998c43bb.png)

You might have noticed by now how all modern Minecraft maps look somewhat “patchy”: this is because each colour represents a different “biome”: a region with distinct geographical features such as vegetation, animals, buildings and climate conditions.

Nine months after the “infinite update”, Alpha 1.2.0–better known as the “Halloween Update”–introduced ten of those biomes.

The way in which the game decided which part of the world belonged to which biome was fairly simple, and relied on so-called “noise maps”. In a nutshell, these are images whose pixels are produced using random numbers. Based on their initial settings and configuration they can be used to generate a variety of different patterns.

Early versions of Minecraft used three of these noise maps. One to determine the terrain height, and two for the temperature and rainfall.

And it was the combination of the last two that ultimately determined the biome of a region.

High temperature and low humidity? Desert biome!

Low temperature and low humidity? Tundra biome!

…and so on.

![](../../assets/891195c18a15437e.png)


![](../../assets/891195c18a15437e.png)

What worked well is that because the temperature and rainfall maps were fairly smooth, so were the transitions between biomes. Meaning that you would have rarely encountered a forest next to–let’s say–a savanna.

But because the biomes were independent from the terrain, you could have them at any height, making for some pretty unusual landscapes.

A big overhaul came with Beta 1.8: the “Adventure Update”.

First, it got rid of the Far Lands. They marked a sort-of point of no-return, after which the world generation simply stopped working properly. They were found at around 12 million blocks in any direction from the spawn point.

But getting rid of the Far Lands was just the side effect of a much deeper change. The “Adventure Update” came with an entirely new terrain generator!

Veteran players might remember that during this era, worlds had a very distinct vibe. They were somewhat “continental”. Big islands separated by an even bigger ocean.

This changed completely with Minecraft 1.7.2–best known as “The Update that Changed the World”. And indeed it changed it quite a lot! Starting by massively reducing the size of the oceans.

Within the course of three years, Mojang had significantly changed the way worlds generate. Twice! And this had quite a profound impact on all those servers that had been around for a long time, such as the infamous 2b2t–Minecrat’s oldest anarchy server. FitMC made a very interesting video showing how something as simple as upgrading to a different version permanently scarred the already distressed landscape of 2b2t.

Despite some other tweaks in the following updates, the world generator introduced in Minecraft 1.7.2 has been pretty much in use for almost 10 years.

And although Minecraft 1.18 somewhat changed that, the worlds that for years you explored, mined, built, loved and lost …they were all crafted by the same algorithm.

So I know why you’re here: you want to know how that actually works.

Sooooo. Minecraft uses congruential generators to seed Perlin noise maps which serve as octaves for fractal Brownian motion noise maps, which are then processed in a layered stack of cellular automaton-like operators to determine the biomes, which ultimately modulate the amplitude of the fractal density map that controls the terrain height.

Ok. Perhaps that was not the most effective way to explain how it works.

So what about if I show you instead?

## Part 3: World Generation

It all starts with the so-called “biome map”: which serves as a template to dictate which type of biome goes in each region of the world. Plains, deserts, mountains and oceans are all examples of possible biomes, and nowadays the Overworld alone counts over 60 of them.

The second phase of the world generation focuses on the terrain, and works in three steps.

The first one creates a basic outline, using the biome map to decide the height each region can have. The result is a solid, barren landscape, entirely made out of stone, where every empty block below ![Rendered by QuickLaTeX.com y=62](../../assets/627cbe81941edd91.png)


The following step replaces all the surface stone blocks with a type appropriate to their biome. Grass for plains, sand for desert, gravel for oceans, and so on. This is also where the bedrock layer is generated. Interestingly enough, in the Java Edition its pattern doesn’t depend on the world seed, and is the same across every Minecraft world.

In the third step, caves and ravines are literally carved out of stone.

Finally, the third phase populates the world with the remaining features. Structures like villages, strongholds and ocean monuments are placed first, followed by decorative elements like trees and grass. This is also when ore veins are added in the world, in a process not dissimilar to the ones used by “Infiniminer”.

Let’s see how each one works in more detail…

### Biome Map

Generating the biome map is the most critical phase, as it serves as the blueprint the rest of the world is built from.

The map is built using a sequence of fairly simple operations, referred to as “layers”, which are stacked on top of each other. Each layer takes the biome map from the previous one, adds some details, and passes it to the next one.

![](../../assets/7f932035c93f221a.png)


![](../../assets/7f932035c93f221a.png)

Minecraft worlds are crafted using not one but four different stacks.

The main one is responsible for the land, while two smaller ones are used to draw the rivers and to give temperatures to the ocean. An additional stack is used to add even more nuances to hills and rivers.

It all starts with a noise map–an image generated randomly—which features only two colours, representing land and ocean in a 1 to 10 proportion. The process is not dissimilar to rolling a D10 for each pixel: if you get a 1, it becomes land, otherwise it becomes an ocean.

Minecraft obviously doesn’t have a D10 at its disposal, but it can nonetheless “roll” random numbers using what is known as a quadratic congruential generator.

Internally, the source code calls this the **Island Layer**, as each individual pixel of this noise map will be the template from which continents will emerge. Each pixel, in fact, corresponds to 4096 in-game blocks.

The deeper we go in the biome stack, the more refined the details added are. This is possible due to a series of scaling layers, which increase by a factor of two the resolution at which the following layers will operate.

For example, if a pixel from the Island layer corresponds to 4096 blocks, each pixel added after the zoom will have an in-game size of 2048 blocks.

Minecraft is using the **Zoom** layers for another important task: adding variation. Instead of scaling the maps perfectly, they sometimes introduce some small changes. They are coded to work more like an old photocopier: adding the occasional mistake and smudging the edges of what would otherwise be some perfectly square islands.

The next layer encountered in the biome stack is designed to expand the existing islands, creating a more connected world.

Every piece of land has a chance of expanding into the corners of nearby shallow waters, but can also be eroded in the process.

If we run this layer over and over again, we can see that it doesn’t always produce the same effect. Even layers introduce randomness!

So perhaps a better way to understand how most of them work, is to see them as stochastic cellular automata. Which is just a fancy way of saying that they’re simple rules that change a pixel based on the colour of the surrounding ones. The “stochastic” part comes into play because some of those rules might be driven by randomness.

Cellular automata look deceptively simple, but they hide an endless universe of complexity. And are one of the most used tools when it comes to procedural content generation in video games. If you want to learn more about them, there’s an entire documentary on my YouTube channel.

Most of the land shape is created by alternating **AddIsland** and **Zoom** layers. This allows the world to have prominent features at various different resolutions.

### Ocean Regions

The ocean, on the other hand, is mostly shaped by these two layers.

The first one was added in the “Adventure Update” to specifically make the word less “continental” and more “connected”. Internally, Minecraft literally calls it **Remove Too Much Ocean**, leaving very little to the imagination.

All ocean regions surrounded by more ocean have a 50% chance of becoming land.

This not only creates more fragmented coasts, but also brings the amount of land versus ocean from barely 27% to over 50%.

The next layer from the main stack marks all ocean regions which are surrounded by more ocean as “deep”. This will later give rise to shallow ocean and deep ocean biomes.

#### Temperatures & Biomes

Up to this point, we have only mentioned two things: land and ocean. As a prelude to biomes, a series of climate layers are responsible for determining the temperature of each region: either **Warm**, **Temperate**, **Cold** or **Freezing**. Later in the stack, this information will determine which biomes these regions can turn into.

First: each piece of land is randomly assigned a temperature: **Warm**, **Cold** or **Freezing**, in proportions of 4, 1 and 1 respectively.

With such a random distribution, you could very well have a desert next to a snowy tundra. To avoid that, the following two layers blend each region’s temperature, ensuring a smoother transition between them.

Any warm land adjacent to a cool or freezing region will turn into a temperate one instead.

And any freezing land adjacent to a warm or temperate region will turn cold.

These temperatures are ultimately the main factor in determining which biome a piece of land will end up being. For example, **Warm** regions have a 50% chance of turning into a **Desert**, 33% into a **Savanna**, and the remaining 17% into **Plains**.

In a similar process, **Temperate**, **Cold** and **Freezing** regions will have certain probabilities of turning into their respective **Temperate**, **Cold** and **Freezing** biomes (such as forests, taigas and ice plains).

#### Biome Variants

Up to this point, the landscape already looks familiar, but lacks variation within the individual biomes. To fix this, this layer has a small chance of converting a biome into its “hilly” variant. For example, it could turn a **Desert** into a **Desert Hill**, a **Forest** into a **Wooded Hill**, or a **Savanna** into a **Plateau**.

This layer also works on ocean regions, and can turn deep oceans into plains or forests. This is what disseminates the ocean with a lot of tiny islands.

The decision on which areas to change comes from an additional noise map which is Generated by a separate stack. When the colour of each pixel is chosen at random and independently from the others–like in this case–we talk about “white noise”. Which is pretty much the same distribution you get when an old TV is not receiving any signal.

Usually, every layer operates on the map locally, ignoring the big picture. And with so many steps it’s hard to guarantee a harmonious blend between biomes.

To avoid any problem, two more layers are tasked with ensuring a gentle transition between different climates and extreme regions exists at all times.

The second one, **Shore**, also adds beaches where land meets shallow oceans.

### Rare Biomes

Rare biomes deserve a special mention, as their generation works in a slightly different way. On top of assigning temperatures, the climate layer has a 1 in 13 chance of tagging a region as “special”.

When the time comes to assign biomes based on temperatures, special regions get a special treatment. **Warm**, **Temperate** and **Cold** climate regions all have their own special biome variants they turn into: badland plateaus, jungles and giant tree taigas.

A different story takes place for the more niche biomes such as **Bamboo Jungles** and **Sunflower Plains**, as the idea is not to have them on their own, but as small patches within much larger regions.

And so, two additional layers are responsible for randomly turning one jungle out of 10 into a **Bamboo Jungle**, and one **Plains** out of 57 into a **Sunflower Plains**.

The somewhat legendary **Mushroom Islands** are created in a similar fashion. With each ocean block surrounded by water having a 1 in 100 chance of turning into a mushroom field. The layer responsible for this is pretty high in the stack, which is why mushroom islands tend to be quite large and uniform.

This is also one of the rarest biomes in Minecraft, and the only one in which hostile mobs don’t naturally spawn.

### River Stack

The main stack focuses mostly on the land, and does nothing to create rivers. They’re generated in a separate stack, which operates on the same noise map used for the hills.

After being scaled several times, the noise map looks quite patchy. The **River Layer** works as a kind-of edge detection algorithm, creating candidate river beds along the seams of those patches.

They are then smoothed to fix any gaps or rough edges with a low-pass filter, and finally feed into the main stack through the **River Mixer Layer**.

That simply carves a river into the land, with the exception of snowy tundra biomes–which get frozen rivers instead–and mushroom fields, which apparently have no rivers at all.

### Ocean Temperature Stack

The last bit involved in the biome generation is the **Ocean Temperature stack**. It adds variety to the oceans which–besides being shallow or deep–would otherwise have no other distinctive features.

The stack creates its own temperature map using a technique known as Perlin noise. That is a very common algorithm for procedural noise maps, which was originally developed in 1982–not for a game–but for the movie “Tron”.

If you create a white noise map by rolling a dice for each pixel–like the first layer was doing–the overall result will look unpleasantly rugged, because nearby pixels will likely have very different values. Perlin noise, instead, is known to create very pleasant, very smooth images.

And it does so by generating random values on a grid much larger than the final image we want to render. All the points in between are then gently interpolated between those random values, resulting in a much smoother finish. There is much more to Perlin noise than this, but that is as far as we will go.

![](../../assets/3c218ad99b8f4b6e.png)


![](../../assets/3c218ad99b8f4b6e.png)

Once ready, the map is scaled up to size and merged into the full stack through the **OceanMixer Layer**. This finally gives a biome to the ocean regions, which can now be warm, lukewarm, cold or frozen.

The very final step–this time for real–is to upscale the map two more times. This is not done using the traditional **Zoom** layers that we have seen before, but it relies on a different technique which breaks up even more the edges between the different biomes.

After this, we are left with the actual biome map, in which each pixel corresponds to an actual in-game block.

![](../../assets/3d683cfeb38370de.png)


![](../../assets/3d683cfeb38370de.png)

We are now ready to move to the next stage!

### Terrain Height

The second phase of the world generation focuses on the terrain, and works in three steps.

In the third step, caves and ravines are literally carved out of stone. This is done with a slightly more sophisticated variant of “random walk”, called “Perlin worms”. But at its core, the idea is the same: gently moving a sphere in random directions, carving long tunnels along its path.

Out of the three steps that Minecraft takes to generate its terrain, the first one definitely needs a bit more explanation.

Minecraft builds a complex and interesting terrain through a technique known as “fractal Brownian motion noise”: yet another type of noise map.

Fractal noise is constructed by adding together several Perlin noise maps, sampled at different scales. Each new one—called an octave—has double the resolution of the previous one, but its contribution is also halved.

Fractal noise is famously good at generating plausible-looking terrains. And it works because it adds different amounts of details at different scales. Exactly what we can see on a real landscape.

Minecraft could have easily sampled a fractal map at every ![Rendered by QuickLaTeX.com \left(x, z\right)](../../assets/6532f1bbee7fc588.png)


So how is Minecraft getting the terrain height? Well, it starts at the very top of the world, at ![Rendered by QuickLaTeX.com y=255](../../assets/7a6f445765cd5512.png)

![Rendered by QuickLaTeX.com \left(x,y,z\right)](../../assets/df808cfdc9f99f4f.png)

![Rendered by QuickLaTeX.com \left(x, z\right)](../../assets/6532f1bbee7fc588.png)


![](../../assets/2fd3945207e4af60.png)


![](../../assets/2fd3945207e4af60.png)

An early devlog described the rationale behind this process saying that we should interpret

“the noise value as the “density”, where anything lower than 0 would be air, and anything higher than or equal to 0 would be ground.”

That very same post also mentioned how computationally expensive this process is. So, as a form of optimisation, this fractal noise map is sampled at a lower resolution, with the world split into “cells” of 4x8x4 blocks each.

To be more precise, Minecraft isn’t using one single fractal noise map: it’s using three of them! The reason is simple: those maps are awesome, but they are also fairly uniform. By using two, initialised with different parameters, and blended according to a third noise map, Minecraft is able to add even more interesting, natural-looking variation to the terrain.

But that’s not all! In earlier versions of Minecraft, the biomes and the terrain height map were independent of each other. But from Beta 1.8 onwards, that is no longer the case, and the biome map directly affects the terrain generation by modulating how tall each biome can be.

It does so via two parameters: “depth” and “scale”. Those values depend on the type of biome, and represent its average height and how much it can vary from that. Having the biome directly linked to the terrain height ultimately results in a more natural looking landscape, preventing bizarre things like …a mountain beach, for example.

![](../../assets/68f6ee8a05b1b8d0.png)


![](../../assets/68f6ee8a05b1b8d0.png)

Technically speaking, there are at least two more noise maps involved in the terrain generation. The “Depth noise” map adds a bit of extra variability to compensate for the fact that the interpolation between cells smooths out the finer details.

And the “Surface noise” which determines how many blocks of stone need to be replaced with the default block in each biome.

And there are probably at least ten more, involved in minor details such as the flower distribution. But we are not going to go that deep in this article!

### World Features

After the biome map and the terrain height, we are pretty much left with a finished landscape, but devoid of any vegetation, animal, structure or even ore.

And yet, no Minecraft world would be truly complete without its dozens of different features: grass, flowers, trees, mushrooms, mineshafts, dungeons, ruined portals, villages and outposts, ore veins, dripstones and amethyst geodes, fossils, ocean monuments, witch huts, jungle and desert temples, icebergs, igloos, shipwrecks, ocean ruins and woodland mansions.

Because each one spawns according to its very own rules, it would be impossible to cover them all in this video. So let’s just focus on the only structures that are really necessary to win the game: strongholds.

These underground dungeons serve as the only way to access The End dimension. Each world contains only 128 of them, which spawn inside 8 concentric rings, the last of which has a radius between 22 and 24 thousand blocks from the origin.

Within each ring, the strongholds are generated at roughly equal angles from the centre.

![](../../assets/63891afc5d7dac33.png)


![](../../assets/63891afc5d7dac33.png)

While the actual strongholds are placed along with other structures in the “Population phase”, their position is calculated even before the terrain generates. Unlike all other features, Strongholds are key to the completion of the game, making them a critical step that the world generation needs to prioritise over cosmetic decorations or other overly abundant features.

Congratulations: you are now a procedural generation expert!

Now let’s take everything you’ve learnt so far, and throw it into the lava.

## Part 4: Minecraft 1.18+

Because with the “Caves & Cliffs Update”, Minecraft 1.18 brings on a completely new terrain generator. While before the landscape was only 128 blocks tall, now it can stretch up to 320 blocks. With so much more vertical space to play with, it is not surprising that one of the biggest changes is mountains, which are now much taller and proportionate to the rest of the world.

![](../../assets/3e980918ad83e9df.png)


![](../../assets/3e980918ad83e9df.png)

And to avoid disasters when playing old worlds in Minecraft 1.18, there is some clever blending going on. This helps the new chunks to seamlessly integrate with the surrounding landscape and biomes.

![](../../assets/41bfc1183962e98c.png)


![](../../assets/41bfc1183962e98c.png)

But what really makes the difference is that Minecraft 1.18 uses a completely new algorithm to generate its biome maps. And this can be seen quite clearly when we compare them to older versions built using the layer stack we have seen before. The slide below shows how a Minecraft world dramatically change from 1.16 (left) to 1.18 (right):

![](../../assets/6649695d3334caec.png)


![](../../assets/6649695d3334caec.png)

![](../../assets/7287e91686ddb890.png)


![](../../assets/7287e91686ddb890.png)

And even more important is the fact that now biomes are–to a certain extent–3D! This allows underground caves to have their own biomes, as the much anticipated lush caves do.

![](../../assets/6e37815810b740c2.png)


![](../../assets/6e37815810b740c2.png)

And this plays an important role in the new cave system too. On top of carving its caves using Perlin worms, Minecraft 1.18 introduces three new types of caves: cheese caves, spaghetti caves and noodle caves. Yes, you heard that right.

![](../../assets/8ea4d152a2b1eeaf.jpg)


![](../../assets/8ea4d152a2b1eeaf.jpg)

![](../../assets/64cabf0a7048cb6a.jpg)


![](../../assets/64cabf0a7048cb6a.jpg)

![](../../assets/c2406eab12160783.jpg)


![](../../assets/c2406eab12160783.jpg)

They all generate the same way: applying a threshold to a 3D perlin noise map to decide which underground areas are going to be carved out of the solid stone. And just by seeding these noise maps with different parameters, they can produce large caves, long tunnels, or a fine network of interconnected passageways. Cheese, spaghetti and noodles.

![](../../assets/3ec8dc77b2a22cb1.png)


![](../../assets/3ec8dc77b2a22cb1.png)

And there is also a new feature that creates pillars inside caves.

The update also ties the cave generation with a new ore distribution, which is supposed to encourage digging and exploration.

![](../../assets/d8f489a31ad26bd4.png)


![](../../assets/d8f489a31ad26bd4.png)

So I know what you’re going to ask. How does Minecraft 1.18 actually work? Well… it’s complicated. And also, given how recent it is, it might be a bit premature to go into the details of a system that is still subject to fixes and changes.

But just to quench your thirst, the biome and terrain are now even more linked together.

If before the landscape was modulated by its biome, now they both depend on a 3D climate map.

![](../../assets/93f1b6295a8c440c.png)


![](../../assets/93f1b6295a8c440c.png)

Each quarter-chunk–an area of 4x4x4 blocks–gets five climate parameters from a noise map: **temperature**, **humidity**, **continentalness**, **erosion** and **weirdness**.

Besides the first obvious two, continentalness controls how far a region is from the coast, and erosion dictates how flat or mountainous the terrain should be. The last one, weirdness, determines biome variants.

Each biome is defined by its own ideal temperature, humidity, continentalness, erosion and weirdness. With each quarter-chunk assigned to the biome that most closely matches those five parameters.

A standard desert, for instance, will have high temperature, continentalness and erosion, while low humidity and weirdness. All regions matching those parameters will become deserts.

![](../../assets/9a1bbedf2ca0675b.png)


![](../../assets/9a1bbedf2ca0675b.png)

It is very curious that this new system works in a similar way to Alpha 1.2.0, but with 5 parameters–or 6 if you include the depth–instead of just 2.

There are obviously so many more features that make Minecraft the charming game that it is today. And almost every one comes with its own noise map. The new version includes over 50 of them just for the terrain.

## Part 5: Conclusion

No documentary about world generation would ever be complete without mentioning the amazing community that is actively conducting research on and with Minecraft.

From the thousands who used distributed computing platforms to find the seed of a lost world from a single image, to the team who discovered the tallest cactus—which, by the way, is 23 blocks!

And how could we not mention [The Generative Design in Minecraft Competition](http://gendesignmc.engineering.nyu.edu/), which every year challenges its contestants to push the procedural generation to its very limits.

In the end, What has made Minecraft so appealing—and what keeps people coming back to it–is that all of its rewarding complexity emerges from the interaction of very simple mechanics. And this is true not just for its gameplay, but for its world generation as well. And condensing over 10 years of that into a single video was …definitely a challenging task! But I hope watching this video was as entertaining as it was for me making it.

And maybe—just maybe—I hope it helped you see your good ol’ worlds with new eyes.

## Leave a Reply Cancel reply