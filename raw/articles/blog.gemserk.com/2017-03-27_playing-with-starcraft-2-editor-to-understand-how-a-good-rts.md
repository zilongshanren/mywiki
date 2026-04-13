---
title: Playing with Starcraft 2 Editor to understand how a good RTS is made
url: https://blog.gemserk.com/2017/03/27/playing-with-starcraft-2-editor-to-understand-how-a-good-rts-is-made/
published: '2017-03-27'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

When working on Iron Marines engine at work we did some research on other RTS games in order to have more knowledge on how they did some stuff and why. In this post, in particular, I want to share a bit of my research on the SC2 Editor which helped a lot when making our own editor.

The objective was to see what a Game Designer could do or not with the SC2 Editor in order to understand some decisions about the editor and the engine itself.

Obviously, by taking a look at the game mods/maps available it is clear that you could build entire games over the SC2 engine, but I wanted to see the basics, how to define and control the game logic.

As a side note, I love RTS games since I was a child, I played a lot of Dune 2 and Warcraft 1. I remember playing with the editors of [Command & Conquer](https://www.youtube.com/watch?v=nRe39UyYFjU) and [Warcraft 2](https://www.youtube.com/watch?v=1C_m682LRsw) also, it was really cool, so much power 😉 and fun. With one of my brothers, each one had to make a map and the other had to play and beat it (we did the same with Doom and Duke Nukem 3d editors).

# SC2 Editor

SC2 maps are built with Triggers which are composed by Events, Conditions and Actions to define parts of the game logic. There are a lot of other elements as well that I will talk a bit after explaining the basics.

Here is an image of the SC2 Editor with an advanced map:

![](../../assets/e18b5863fb7de913.jpg)


## Trigger logic

The Triggers are where the general map logic is defined. They are triggered by Events and say which Actions should be performed if given Conditions are met. Even though behind the scenes the logic is C/C++ code and it is calling functions with similar names, the Editor shows it in a natural language like “Is Any Unit of Player1 Alive?” which helps for quick reading and understanding.

This is an example of a Trigger logic of a SC2 campaign map:

![](../../assets/8e0fc8edf5ca14fc.png)


### Events

Events are a way to Trigger the Trigger logic, in other words, when an event happens the logic is executed. Here is an example of an event triggered when the unit “SpecialMarine” enters the region “Region 001”:

![](../../assets/6c47220cefe82189.png)


### Conditions

Conditions are evaluated in order to execute the actions or not. Here is an example of a condition checking if unit “BadGuy” is alive or not:

![](../../assets/54931514dbbb6b5b.png)


### Actions

Actions are executed when the event happened and the conditions are met. They could be anything supported by the editor, from ordering a structure to build a unit to showing a mission objective update on screen, among other things.

This example shows an action that enqueues to unit “BadGuy” an attack order with unit “SpecialMarine” as target, replacing existing enqueued orders in that unit. There is another action after that which turns off the Trigger in order to avoid processing its logic again.

![](../../assets/10eaa56437e131e0.png)


The idea with this approach is to build the logic in a descriptive way, the Game Designer has tools to fulfill what he needs in terms of game experience. For example, he needs to make it hard to save a special unit when you reach its location, then he sends a wave of enemies to that point.

I said before that the editor generates C/C++ code behind the scenes, so, for my example:

![](../../assets/72474da407b2b631.png)


The code generated behind the scenes is this one:

![](../../assets/f3e4542f892fdab7.png)


Here is a screenshot of the example I did, the red guy is the SpecialMarine (controlled by the player) and the blue one is the BadGuy (controlled by the map logic), if you move your unit inside the blue region, BadGuy comes in and attack SpecialMarine:

![](../../assets/5234db4a56faa7af.jpg)


Even though it is really basic, download [my example](https://www.dropbox.com/s/0p0xqe01yx2kbsr/Map.SC2Map?dl=0) if you want to test it 😛 .

## Parameters

In order to make the Triggers work, they need some values to check against, for example, Region1, is a region previously defined, or “Any Unit of Player1”. Most of the functions for Events, Conditions and Actions have parameters of a given Type, and the Editor allow the user to pick an object of that Type from different sources: a function, a preset, a variable, a value or even custom code:

![](../../assets/a6aa6bf153eb863b.png)


![](../../assets/daea51addee7e9ca.png)


This allows the Game Designer to adapt, in part, the logic to what is happening in the game while keeping the main structure of the logic. For example, I need to make the structures of Player2 explode when any Unit of Player1 is in Region1, I don’t care which unit I only care it is from Player1.

## Game design helper elements

There are different elements that help the Game Designer when creating the map: Regions, Points, Paths and Unit Groups, among others. These elements are normally not visible by the Player but are really useful to the Game Designer to have more control over the logic.

As said before, the SC2 Editor is pretty complete, it allows you to do a lot of stuff, from creating custom cutscenes to override game data to create new units, abilities, and more but that’s food for another post.

# Our Editor v0.1

The first try of creating some kind of editor for our game wasn’t so successful. Without the core of the game clearly defined we tried to create an editor with a lot of the SC2 Editor features. We spent some days defining a lot of stuff in abstract but in the end we aimed too far for a first iteration.

So, after that, we decided to start small. We starting by making a way to detect events over the “being defined core” at that point. An event could be for example: “when units enter an area” or “when a resource spot was captured by a player”.

Here are some of the events of one of our maps:

![](../../assets/8c3e4c76de41780b.png)


Note: Even though they are Events we named them Triggers (dunno why), so AreaTrigger is an empty Trigger in terms of SC2 Editor with just an Event.

Events were the only thing in the editor, all the corresponding logic was done in code in one class, corresponding to that map, which captures all events and checks conditions for taking some actions, normally, sending enemies to attack some area.

Here is an example code for some of the previous defined events:

![](../../assets/dac958a164167767.png)


It wasn’t a bad solution but had some problems:

- The actions were separated from the level design which played against the iteration cycle (at some point our project needed between 10 and 15 seconds to compile in the Unity Editor).
- Since it needs code to work, it requires programming knowledge and our team Game Designers aren’t so good with code.

# Our Editor v0.2

The second (and current) version is more Game Designer friendly, and tends to be more similar to SC2 Editor. Most of the logic is defined in the editor within multiple triggers. Each Trigger is defined as a hierarchy of GameObjects with specific components to define the Events, Conditions and Actions.

Here is an example of a map using the new system:

![](../../assets/8756b1f56c7f1e76.png)


This declares for example a trigger logic that is activated by time, it has no conditions (so it executes always given the event) and it sends some enemies in sequence and deactivates itself at the end.

We also created a custom Editor window in order to help creating the trigger hierarchy and to simplify looking for the engine Events, Conditions and Actions. Here is part of the editor showing some of the elements we have:

![](../../assets/4547b9c8952b01a8.png)


![](../../assets/b4f2577a515d0100.png)


![](../../assets/a8305cf64e96b421.png)


All those buttons automatically create the corresponding GameObject hierarchy with the proper Components in order to make everything work *according to plan*. Since most of them need parameters, we are using the Unity built-in feature of linking elements given a type (a Component), so for example, for the action of forcing capture a Capturable element by team Soldiers, we have:

![](../../assets/abefd6f122db1e02.png)


Unity allow us to pick a Capturable element (CapturableScript in this case) from the scene. This simplifies a lot the job of configuring the map logic.

Some common conditions could be to check if a resource spot is controlled by a given player or if a structure is alive. Common actions could be, send a wave of enemy units to a given area or deactivate a trigger.

The base code is pretty simple, it mainly defines the API while the real value of this solution is in the custom Events, Conditions and Actions.

## Pros

- Visual, and more Game Designer friendly (it is easier for Programmers too).
- Faster iteration speed, now we can change things in Editor directly,
*even in runtime!* - Easily extensible by adding more Events, Conditions and Actions, and transparent to the Game Designers since they are automatically shown in our Custom Editor.
- Take advantage of Unity Editor for configuring stuff.
- Easy to disable/enable some logic by turning on/off the corresponding GameObject, which is good for testing something or disable one logic for a while (for example, during ingame cinematics).
- More control to the Game Designer, they can test and prototype stuff without asking programming team.
- Simplified workflow for our ingame cinematics.
- Compatible with our first version, both can run at the same time.

## Cons

- Merge the stage is harder now that it is serialized with the Unity scene, with code we didn’t have merge problems or at least it was easier to fix. One of the ideas to simplify this is to break the logic in parts and use prefabs for those parts, but it breaks when having links with scene instances (which is a common case).
- A lot of programming responsibility is transferred to the scripting team which in this case is the Game Design team, that means possibly bad code (for example, duplicated logic), bugs (forget to turn off a trigger after processing the actions) and even performance.

# Conclusion

When designing (and coding) a game, it is really important to have a good iteration cycle in each aspect of the game. Having switched to a more visual solution with all the elements at hand and avoiding code as much as we could, helped a lot with that goal.

Since what we end up doing looks similar to a scripting engine, why didn’t we go with a solution like [uScript](https://www.assetstore.unity3d.com/en/#!/content/1808) or similar in the first place? the real answer is I didn’t try in depth other Unity scripting solutions out there (not so happy with that), each time I tried them a bit they gave me the feeling it was too much for what we needed and I was unsure how they perform on mobile devices (never tested that). Also, I wasn’t aware we would end up need a scripting layer, so I prefered to evolve over our needs, from small to big.

Taking some time to research other games and play with the SC2 Editor helped me a lot when defining how our engine should work and/or why we should go in some direction. There are more aspects of our game that were influenced in some way by how other RTS games do it, which I may share or not in the future, who knows.

I love RTS games, did I mention that before?