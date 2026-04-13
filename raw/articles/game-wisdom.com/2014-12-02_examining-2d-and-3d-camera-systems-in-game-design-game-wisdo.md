---
title: Examining 2D and 3D Camera Systems in Game Design - Game Wisdom
url: https://game-wisdom.com/critical/differences-2d-3d-camera-systems-game-design
author: Josh Bycer
published: '2014-12-02'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

The [last time I talked about camera systems](https://game-wisdom.com/critical/camera-systems-game-design), I approach things from a very basic level for people who have never looked at them before. But a comment on the post made a very good point about not talking more about the differences between these two very important and why one should be used over the other. This brings us to today’s post which is a more advanced look at the two schools of camera system design.


## 2D Camera Design:

As I talked about the last time, the main reason why 2D cameras and design are still popular despite the evolution of 3D comes from being able to deliver a “pure experience” and I want to talk more about that.

From a control point of view, the player doesn’t have to consciously think about controlling the camera as they would in a 3D title. Because the camera by default keeps the player in frame at all times, gives the player the best possible viewpoint when playing.

It’s important when designing your camera for a sidescroller that it should keep the player more on the opposite side of the screen based on the direction they’re going. So if they’re moving right, the camera should be showing them more on the left side of the screen. The reason is that you want to give the player as much information about the environment as you can possibly fit onto the screen.

Another important distinction and major design decision is how enemies respond based on the camera. Older games based enemy spawns on where the player/screen was in relation to the level. Meaning going back and forth across a certain area would keep spawning the same enemy. This could create an endless cycle of being pushed back by a strong enemy, killing it and then getting back to the spawn point to have it reappear.

Speaking of enemies, you also need to decide whether or not enemies respond off screen to the player. Enemies that attack with projectiles could attack the player from without any warning and added difficulty to the game. This can be very frustrating in games where the player could be attacked from all sides as nothing is more annoying than having four directions of shots coming in off screen.

When designing levels, it’s important to take into consideration the camera as you want to avoid any “leaps of faith –” where the player must make a jump or go into a direction from off screen without any information to guide them.

This was a common annoyance in older 2D titles and some games got around it via being able to shift the camera up or down or side to side with a push of a button. It’s also vital to understand how the camera position will affect the level designs of your game.

Because the camera is dependent on the player’s position, complicated multi-screen obstacles may not work out due to them not being all on screen at once, leading to the leap of faith issue. Older series like Mega Man would have screen transitions to bring the camera back to a neutral position that showed more of the environmental issues.

Moving on to 3D, with the extra dimension has a host of different issues to deal with when developing your title.

## 3D Camera Design:

### Over the Shoulder Camera:

As we talked about before, there are different variations of 3D cameras based on the viewpoint. This will have a major impact on your title and it’s important to get it right.

The over the shoulder camera is best used for shooters or games where you’re dealing with ranged combat. Because the character will dominate one side of the screen with their model, the view from the character’s shoulder is the closest analog to a first person camera.

This camera is also great for stealth games as you are able to see ahead of the character unlike with a perspective or isometric view. This had a huge impact on the Metal Gear Solid series when they altered the camera for Metal Gear Solid 3 to be over the shoulder.

This camera style does have a big problem and that it’s not good for fighting or platforming gameplay. The reason is that you aren’t able to see depth wise where the character is in relation to the enemies and it’s very easy to swing too far away from the enemy to hit them. Also because of the constrained view, it makes fighting multiple enemies or screen filling enemies difficult to keep within the frame.

![Snake Eater, originally posted on IGN.com game design](../../assets/a05989f50ecb2e87.png)


![Snake Eater, originally posted on IGN.com game design](../../assets/a05989f50ecb2e87.png)

The shift to an over the shoulder camera had a huge impact on the Metal Gear Solid series and how they were played and developed.

With platforming, it’s very hard to make precise jumps due to the lack of depth and not being able to see the character’s feet. This is similar to the first person viewpoint and why platforming is designed with a wide berth for the player.

The main functionality that you want to have with the camera is being able to lock on or track an enemy. This makes it a lot easier to fight them and somewhat gets around the depth of field issue of combat.

One last important detail when talking about over the shoulder cameras, the same functionality and pros and cons can also be applied to titles where the camera is behind the main character while keeping them in the middle of the frame. See the Demon’s Souls series as an example of this.

For when you want to fight in close range or navigate around the environment, a perspective camera is better.

### Perspective Camera:

The Perspective camera doesn’t show the world through the character’s eyes but makes up for it by letting the player see depth of field. This allows them to gauge jumps easier, see where they are in relation to enemies and attack them and fight multiple enemies at once. One of the best examples of this camera at work would be in Super Mario 64 and how it gave the player excellent information to gauge their jumps and platforming by.

But the camera does have drawbacks and is not built for fighting long range battles. Since the camera stays above the player and looks down at them, it’s all but impossible to track ranged enemies from off camera. This is why many action games give the player a secondary “ranged mode” where they will switch to an over the shoulder camera to fight with a ranged weapon.

![God of War, originally posted on Destructoid.com game design](../../assets/a5309b024be1bbbb.png)


![God of War, originally posted on Destructoid.com game design](../../assets/a5309b024be1bbbb.png)

Perspective cameras are best at providing details surrounding the player for either combat or environmental challenges.

Another issue is that you want to avoid the classic “run towards the camera while being chased” levels. The problem is that due to the position of the camera, it makes it impossible to gauge jumps and you don’t want to set up any complicated obstacles in this view.

With perspective based cameras you need to be aware of two issues with using them for any type of game. One is that despite providing a great view of things, you still need to have control functionality such as being able turn it. And second you also need to have something set up for if the camera gets stuck on a wall or an environmental obstacle blocks the view. Many Mario titles simply let the camera see through the object by making it transparent.

Zooming in and out can be important depending on the scale of your characters. Sometimes it’s better to zoom out to see an entire area while other times you want to zoom in for more precise jumping or combat.

## Camera Rolling:

Great camera design is one of those topics where there is a lot to cover and I know that this post didn’t get everything. If there are other topics you would like me to talk about, feel free to mention it in the comments below.