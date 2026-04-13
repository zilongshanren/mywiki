---
title: Randomizing terrain with Houdini to shape player goals in Pacific Drive
url: https://www.gamedeveloper.com/art/the-exceptionally-cool-ways-pacific-drive-used-randomized-terrain-to-shape-player-goals
author: Bryant Francis
published: '2024-02-21'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Randomizing terrain with Houdini to shape player goals in Pacific Drive

The tiny team making the spooky survival sedan driving game Pacific Drive explains how their procedural terrain tech supercharged the game's artist and level designers.

![A wrecked car in Pacific Drive. A wrecked car in Pacific Drive.](../../assets/3077ad866600ae3a.jpg)

## At a Glance

- Ironwood Studios' Pacific Run uses a run-based structure with randomized levels to keep the game fresh for players.
- The game's ever-shifting spooky landscape makes use of a Houdini-based pipeline that lets it visually punch above its weight.

Ironwood Studios lead technical artist Karl Kohlman has been using visual effects software Houdini for a long time. He began his career in the trenches of the film industry's VFX pipeline, pumping out shots on films like Tron: Legacy and the Michael Bay-directed Transformers flicks.

His jump to video games began with a stint on Halo 5: Guardians and a series of freelance contracts, on one of which he'd team up with Ironwood Studios founder and fellow 3D animator Alex Dracott.

Dracott, who knew enough about Houdini to know what he didn't know, pitched Kohlman on a game he was cooking up: Pacific Drive. He wanted to make a first-person driving game where players trekked around the dense forests of the Olympic Peninsula. He knew Houdini's integration with tools like Unreal Engine had expanded over the last few years, but he didn't know how to wisely integrate it in the process.

Kohlman took the gig. It would be the first time as a VFX artist that he would work hand-in-hand with the lead creatives on a project. Even during his time at Laika Studios, he and his colleagues worked in one building while the stop-motion artists worked in another.

The creative collaboration cracked open a compelling case study of how mid-sized studios can use procedural generation technology to generate meaningful terrain. Kohlman's breakdown of his process shone a light on how randomized terrain and hand-crafted design can go hand-in-hand.

In Pacific Drive, that process helps the world feel like something random and chaotic while still guiding players to the right objectives. Here's a taste of what Kohlman and his colleagues cooked up:

## Rules for reliable randomization using Houdini

The Houdini-based terrain pipeline for Pacific Drive runs on rules, rules, rules. Kohlman described how Dracott first showed him a "Houdini doodle" where he took a sample of mountain terrain, hit a "simulate" button, and watched as the software generated ravines running naturally down the soft hills.

"It also barfs out all of these maps," he added. With that information the user can see where water is flowing, observe the slope of different hills, and so on.

With those basic building blocks, could a developer just tell the software how to build a natural forest all on its own? Maybe—if they can cook up the right rules. "There were there was a whole lot of time that was just spent asking 'what rules can we make?'"

![Forest_Gen.gif Forest_Gen.gif](../../assets/00e7cd933185a78a.gif)


The answer: "clusters." One method for generating these kinds of forests would be to tell the software to spawn trees around the flow of a river. A more useful method for Pacific Drive was to create layering terrain spawning rules that started with tree placement but spread outward to encompass rocks, smaller trees, and other flora—and even how all of those objects interact with natural erosion.

An example of this flow in action: large trees influence the spawning of rocks, but rocks do not influence the position of large trees. Flowers or bushes might spawn around those rocks but only interact with each other based on what the system determines.

Every rule added to the cluster system just led to more rules. To diversify terrain, the folks at Ironwood began cooking up "ecosystems" so that Houdini could differentiate between forests, glens, areas near roads, areas near rivers, far from rivers, etc.

Ah, right, the roads. Pacific Drive is a driving game and not only can players drive on roads, they're likely to fling their station wagon off-road in pursuit of loot or while fleeing the deadly supernatural storm. The ramshackle movement of the car introduced interesting new variables into the process, and highlighted how this random terrain can be used to guide the player.

## Random terrain still respects the rules of the road in Pacific Drive

Randomized terrain is great. If the player can't navigate around it, however, all you've made is a cool forest generator.

Dracott (creative director on Pacific Drive, with Seth Rosen acting as game director) tapped in to explain how this terrain flows into the randomized map design.

Every map players load into on Pacific Drive is assembled out of "fixed elements." But after those features are set, Dracott explains, the goal of Ironwood Studios is to disguise them. "I've put in just an absolute ton of hours in our game and it's still surprising me," he said.

The design process goes a bit like this: level designers at Ironwood start with a high-level idea for a game map and set firm rules about the setting, because it will impact the rulesets generated by Houdini.

After creating a rough sculpt of the zone, it's run through the procedural terrain process to do a pass on environment generation, creating the trees that generate rocks that generate flowers, and so on. Then, the level designer takes the map back and refines it, and the iterating continues through playtesting and beyond.

![LevelCreate1.gif LevelCreate1.gif](../../assets/22a0f8f79ca79f77.gif)


Like any process in game development, it's not one where the developer can just "set and forget" the environment design. But Kohlman was pleased to say this process doesn't impose many technical restrictions on what content designers want to create.

"Once we figured out the maximum size for our maps it was pretty easy to start putting ceilings on the procedural tools so someone couldn't accidentally scatter a million trees," he said (though he admitted that early on it was something artists could accidentally do).

A unique challenge in this stage of implementing the terrain system is grappling with which objects will and won't interfere with the movement of the player's car. Pacific Drive places a lot of deliberate friction on its traversal system because it's selling the fantasy of scrappy survival, not sleek speedways.

It's important for players to know what objects will interfere with their path so they can spot them coming while, say, furiously trying to crank up the window or get the windshield wipers working.

It can be a big problem if the game generates foliage that conceals objects that will bring the car screeching to a halt, like a rock or a sizable tree. "We don't want players to be surprised by a stop like that," Kohlman said. Sometimes, those surprise crashes are fun, but in many instances, they aren't, and that means establishing dedicated rules to make it clear when players are and aren't about to have to file an insurance claim.

## Improvements to Houdini could make this process easier for all developers

In a conversation like this, it can be easy to become lost in what a tool like Houdini is doing so well for a game like Pacific Drive. But there are pain points in integrating any tool into your engine. If Kohlman was going through this process again, he says, he'd want better support from Houdini for the compositing software in the program.

![LevelCreate2.gif LevelCreate2.gif](../../assets/c8ef2528617cad91.gif)


He implied that it doesn't integrate as nicely with the rest of the tool's various branches—which is a problem if you, like Kohlman, appreciate that Houdini's best trait is being a set of animation tools that interact with each other to produce beautiful results. "it's a part of Houdini that doesn't get a whole lot of love and hasn't seen a whole lot of development in recent cycles," he observed.

Dracott (who again, was the one who roped Kohlman in, knowing a Houdini expert could punch up the environment art of Pacific Drive) would love improvements from Unreal's developers to improve file integration management from external tools.

"We ended up building a handful of our own tools in Unreal just to speed up and safety buffer our own pipelines just because we couldn't run an automated Houdini process having artists go in and click the 'import' button over and over again."

![WeatherLevelVariety.gif WeatherLevelVariety.gif](../../assets/60828172f630466c.gif)


"Anything that could be done to lower the barrier there...it's going to pay dividends in terms of what that means for any other team trying to make any systems close to ours."

The potency of Ironwood Studios' environmental pipeline sounds like it will play perfectly well for a game where a player is making multiple runs through an eerie, ever-shifting zone that can't be firmly mapped. It's a neat payoff to something Kohlman described about his shift from film to video games: because he sits more closely to the creatives making the game itself, it seems a bit of their creative logic for world generation could inform how he made their tools.