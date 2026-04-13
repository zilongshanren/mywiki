---
title: Implementing Fog of War for RTS games in Unity 1/2
url: https://blog.gemserk.com/2018/08/27/implementing-fog-of-war-for-rts-games-in-unity-1-2/
published: '2018-08-27'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

For the last 3 years, I’ve been working on [Iron Marines](https://www.ironmarines.com/) at Ironhide Game Studio, a Real time Strategy Game for mobile devices. During its development, we created a Fog of War solution that works pretty well for the game but it lacks some of the common features other RTS games have, and how to improve that is something I wanted to learn at some point in my life.

Recently, after reading a [Riot Games Engineering blog post about Fog of War in League of Legends](https://engineering.riotgames.com/news/story-fog-and-war), I got motivated and started prototyping a new implementation.

In this blog post I will explain Iron Marines’ Fog of War solution in detail and then I will write another blog post about the new solution and explain why I consider it is better than the first one.

# Fog of War in Strategy Games

It normally represents the missing information about the battle, for example, not knowing how the terrain is yet, or outdated information, for example, the old position of an enemy base. Player units and buildings provide vision that removes Fog during the game revealing information about the terrain and the current location and state of the enemies.

![](../../assets/cf4353539eecb76f.gif)


Example: Dune 2 and its Fog of War representing the unknown territory (by the way, you can [play Dune 2 online](https://epicport.com/en/dune2)).

![](../../assets/646ca5a7480350bd.png)


Example: Warcraft: Orcs and Humans' Fog of War (it seems you can play [Warcraft online too](https://www.myabandonware.com/game/warcraft-orcs-humans-250/play-250)).

The concept of Fog of War is being used in strategy games since more than 20 years now, which is a lot for video games.

# Process

We started by researching other games and deciding what we wanted before start implementing anything.

After that, we decided to target a similar solution to Starcraft (by the way, it is free to play now, just download Battle.net and create an account). In that game, units and buildings have a range of vision that provide vision to the Player. Unexplored territory is covered with full opacity black fog while previously explored territory is covered by half opacity fog, revealing what the Player know about it, information that doesn’t change during the game.

![](../../assets/00417f5ca3da2098.png)


Enemy units and buildings are visible only if they are inside Player’s vision but buildings leave over a last known location after they are not visible anymore. I believe the main reason for that they can’t normally move (with the exception of some Terran buildings) so it is logical to assume they will stay in that position after losing vision and might be vital information about the battle.

![](../../assets/c177db069b953179.png)


# Iron Marines

Given those rules, we created mock images to see how we wanted it to look in our game before started implementing anything.

![](../../assets/9ee6993190b79879.png)


Mock Image 1: Testing terrain with different kind of Fog in one of the stages of Iron Marines.

![](../../assets/526afc44fc306374.png)


Mock Image 2: Testing now with enemy units to see when they should be visible or not.

![](../../assets/a5e160784d6e1d59.png)


We started by prototyping the logic to see if it works for our game or not and how we should adapt it.

For that, we used an int matrix representing a discrete version of the game world where the Player’s vision is. A matrix’s entry with value 0 means the Player has no vision at that position and a value of 1 or greater means it has.

![](../../assets/3a8b72baaa45c4ef.png)


Image: in this matrix there are 3 visions, and one has greater range.

Units and buildings’ visions will increment 1 to the value of all entries that represent world positions inside their vision range. Each time they move, we first decrease 1 from its previous position and then we increment 1 in the new position.

We have a matrix for each Player that is used for showing or hiding enemy units and buildings and for auto targeting abilities that can’t fire outside Player’s vision.

To determine if an enemy unit or building is visible or not, we first get the corresponding entry of the matrix by transforming its world position and check if the stored value is greater than 0 or not. If not, we change its GameObject layer to one that is [culled from the main camera](https://docs.unity3d.com/ScriptReference/Camera-cullingMask.html) to avoid rendering it, we named that layer “hidden”. If it is visible, we change it back to the default layer, so it starts being rendered again.

![](../../assets/3a194a5f53fc29b8.png)


Image: shows how enemy units are not rendered in the Game view. I explain later why buildings are rendered even outside the Player’s vision.

## Visuals

We started by just rendering a black or grey color quad over the game world for each matrix’s entry, here is an image showing how it looks like (it is the only one I found in the chest of memories):

![](../../assets/96a68695a4dec40f.png)


This allowed us to prototype and decide some features we didn’t want. In particular, we avoided blocking vision by obstacles like mountains or trees since we preferred to avoid the feeling of confinement and also we don’t have multiple levels of terrain like other games do. I will talk more about that feature in the next blog post.

After we knew what we wanted, and tested in the game for a while, we decided to start improving the visual solution.

The improved version consists in rendering a texture with the Fog of War over the entire game world, similar to what we did when we created the visual mocks.

For that, we created a GameObject with a MeshRenderer and scaled it to cover the game world. That mesh renders a texture named FogTexture, which contains the Fog information, using a Shader that considers pixels’ colors as an inverted alpha channel, from White color as full transparent to Black color as full opaque.

Now, in order to fill the FogTexture, we created a separated Camera, named FogCamera, that renders to the texture using a RenderTexture. For each object that provides vision in the game world, we created a corresponding GameObject inside the FogCamera by transforming its position accordingly and scaling it based on the vision’s range. We use a separated Unity’s Layer that is culled from other cameras to only render those GameObjects in the FogCamera.

To complete the process, each of those objects have a SpriteRenderer with a small white Ellipse texture to render white pixels inside the RenderTexture.

*Note: we use an Ellipse instead of a Circle to simulate the game perspective.*

![](../../assets/c0f97670bfcf4aea.png)


Image: This is the texture used for each vision, it is a white Ellipse with transparency (I had to make the transparency opaque so the reader can see it).

![](../../assets/43ae8c10f5b55da5.png)


Image: this is an example of the GameObjects and the FogCamera.

In order to make the FogTexture look smooth over the game, we applied a small blur to the FogCamera when rendering to the RenderTexture. We tested different blur shaders and different configurations until we found one that worked fine on multiple mobile devices. Here is how it looks like:

![](../../assets/af418d26c4041c75.png)


And here is how the Fog looks like in the game, without and with blur:![](../../assets/48488668fa08c9fa.png)


![](../../assets/bd4f940bcaf3cc4c.png)


For the purpose of rendering previously revealed territory, we had to add a previous step to the process. In this step, we configured another camera, named PreviousFogCamera, using a RenderTexture too, named PreviousVisionTexture, and we first render the visions there (using the same procedure). The main difference is that the camera is configured to not clear the buffer by using the “Don’t Clear” clear flag, so we can keep the data from previous frames.

After that, we render both the PreviousVisionTexture in gray color and the vision’s GameObjects in the FogTexture using the FogCamera. The final result looks like this:

![](../../assets/f13b3ba890de584a.png)


Image: it shows the revealed territory in the FogCamera.

![](../../assets/2e0b7e7129180bd6.png)


Image: and here is an example of how the Fog with previous revealed territory looks in the game.

## Buildings

Since buildings in Iron Marines are big and they don’t move like Starcraft, we wanted to follow a similar solution.

In order to do that, we identified buildings we wanted to show below the Fog by adding a Component and configuring they were going to be rendered when not inside the Player’s vision.

Then, there is a System that, when a GameObject with that Component enters the Player’s vision for the first time, it creates another GameObject and configures it accordingly. That GameObject is automatically turned on when the building is not inside the Player’s vision anymore and turned off when the building is inside vision. If, by some reason the building was destroyed while not in inside vision, the GameObject doesn’t disappear until the Player discovers its new state.

We added a small easing when entering and leaving the Player’s vision to make it look a bit smoother. Here is a video showing how it looks like:

# Conclusion

Our solution lacks some of the common Fog of War features but it works perfectly for our game and looks really nice. It also performed pretty well on mobile devices, which is our main target, and if not done properly it could have affected the game negatively. We are really proud and happy with what we achieved developing Iron Marines.

That was, in great part, how we implemented Fog of War for Iron Marines. I hope you liked both the solution and the article. In the next blog post I will talk more about the new solution which includes more features.

Thanks for reading!