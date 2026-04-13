---
title: 'Snapshot: Shuddering-bug - Game Wisdom'
url: https://game-wisdom.com/analysis/snapshot-shuddering-bug
author: Josh Bycer
published: '2013-01-09'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

As we have seen the rise of the Indie market, so has the increased popularity of 2D design. Over the last few years we have seen a wide variety of games that used the genre to go in interesting directions. With [Snapshot ](http://www.retroaffect.com/games/1/snapshot/)we have a game pulling out a unique camera mechanic. However, the term “shaky cam” can be applied here and leads to some unintentional frustration.


## A Developing Situation:

The story of *Snapshot* is about a robot waking up to find itself alone and sets out to explore the world.

As the title implies, the unique mechanic for the game has to do with taking pictures. The robot is armed with a camera that allows it to photograph objects and transport said object in the photograph. The player can have up to three photos taken and once an object is photographed, the player can rotate the picture before setting the object down.

![Snapshot Snapshot](../../assets/362144b69f475330.jpg)


![Snapshot Snapshot](../../assets/362144b69f475330.jpg)

Controlling the scrolling of the screen is tied to aiming with the camera. This can make it difficult to capture moving objects.

Each level of *Snapshot* is broken down into three sections each with their own puzzles for you to solve.

You’ll earn medals for scoring and achievement purposes for finding all the collectibles, getting through the level under a par time and by beating every section.

*Snapshot* reminds me of Portal: in how the player has one mechanic of interaction and the challenge of the game is built into manipulating the environments and objects they run across.

However, *Snapshot’s* biggest problem is ironically its camera, and not the one we’ve been talking about.

## Camera Shy:

*Snapshot’s* camera system, not to be confused by the camera mechanic is your standard 2D camera. Where it will track the player by default and move quickly to keep the player in the center of the screen at all times. However, the game’s challenges consistently clash with the system and make things far more frustrating than they should be.

The problem comes down to how the player’s camera position is tied to the game’s camera. When the camera lens is in the middle of the screen, the camera stays there, but the camera will pan in the direction that you move the in game camera. In order to take pictures of objects, you need to get the entire object within the frame of the camera for it to transfer.

What ends up happening is that if you are moving and want to take a picture of something, the second you move your lens to get over the object, the camera will also move, messing with the shot.

This is made all the more frustrating when you are dealing with larger objects whose height mirrors the width of the camera, making it very easy to not completely capture the item.

But that’s not all; the game also throws in jumping puzzles where you have to drop an object in mid air, under the character so that they can use it as a jumping point.

Now, not only are you dealing with the camera, but you also have to make sure that you aim it to where the character is in mid air while making sure the object is in position to land on it. And good luck if you also have to quickly take a picture of an object while you are in mid air.

What would have helped would be a way to lock the screen in one position or just slow it down while the player is in mid air. This would allow them to properly aim the lens without it messing with the screen’s position.

Rotating objects is also finicky, as the picture rotates in relation to the mouse pointer. Move the pointer too close to the picture and it may snap back into its original position. Some puzzles require you to rotate a spring so that the player can jump off it at an angle. Messing up will usually end with the character falling on spikes and having to repeat the section.

Adding even more frustration is that many sections have areas where the wrong move by the player will leave a puzzle unsolvable, forcing a restart.

There is nothing worse than knowing what has to be done to solve a puzzle and having the game fight you every step of the way. Unfortunately this is how *Snapshot* ends up, which makes it very hard to recommend to all but the most patient plat former fans.