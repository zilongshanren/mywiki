---
title: 'Into notch''s mind: Prelude of the Chambered'
url: https://randomtower.blogspot.com/2011/09/into-notchs-mind-prelude-of-chambered.html
author: Pubblicato da Marte
published: '2011-09-01'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

[Last Ludum Dare](http://www.ludumdare.com/compo/)#21 is an amazing experience to study and learn new way to make videogames. maybe learn from Minecraft's creator notch?

![]() |

But first, who is

[notch](http://notch.tumblr.com/)? It's mind behind

[Minecraft](http://minecraft.net/)and creator of

[Prelude of the Chambered](http://www.ludumdare.com/compo/ludum-dare-21/?action=preview&uid=398)an amazing little game made in only 48 hours!

So let's take a look to his game.

Gameplay

Prelude of the Chambered is a first person-adventure game where player have to escape from a prison and find and exit to surface. Player control this avatar using keyboard and an action key. There is no jump, but it's possible interaction between player and another game element: for example destroying blocks of dungeon, pushing rocks and so on. Player can use offensive weapon (a gun) and other objects to get into new areas.

Prelude game video, SPOILER inside!

So gameplay is easy to understand an master: anyone have played Doom or Wolf3d can play this game. There is also some puzzle to solve in order to unlock new area and combat are fast and brutal: no regeneration, few hit points.. you got the idea.

A weak point (for some people) could be lack of direction: player don't have any clue what have to do or where is important area. Just try, learn and move on: remember Minecraft, right? It's the same, in small scale.

Prelude remember rougelike games in many ways: simple controls, deep mechanics, graphics is not so important. Keep in mind that when you play it.

Tecnology

All is made with Java, and source code can be obtained

[here](https://s3.amazonaws.com/ld48/PoC_source.zip). One thing that at first sight you can miss is that noctch have coded all by himself. No external library, nothing.

Game can be played as java applet and as standalone anyou can notice that game is on

[Amazon s3](http://aws.amazon.com/s3/)service (

[take a look on address bar here](https://s3.amazonaws.com/ld48/index.html)). Put this little game on a cloude service could be a waste of resource, but game is fast to load and many, many people have already played it. It's not so strange to think that notch have made this decision to track some statistics on it, I would have done it, only to understand where people come from, how many played it to the end and so on.

Timelapse

Notch have recorded his work on Prelude on this timelapse. It's hard sometimes to get into his work, but can help you understand how this man work: code, try, code again, try, like everyone else.

Yes, watch this and you are him. Or not?

Some notable things about his timelapse is that everything is done in Eclipse and he define everything using some tilemaps, designing levels using bitmaps. Some nice ideas, right?

Source code

We can learn a lot from Prelude source code, so take a look to some notable points (all IMHO, of course). Order is not so important, just random:

**Assets**: all assets is defined into res directory: textures, sounds, gui, times, levels all defined into png files. A smart idea is to keep levels design fast: just open an editor, draw a color on a certain (x,y) and this color is used to determine what load into actual game. I like this idea! There is no xml or jason file to match positions of resources, just coded into Art and Sound classses, for example, but it's okay for this game.**Main**: every Java program have a starting point and Prelude hava too. EscapeComponent.java have "main" program, keep record time, handle main loop, always render screen object and take care to update (or tick) player class and level class. Nothing strange here, but keep separated rendereing object on screen and their logic is reasonable and needed. So, good foundation here.**Render**: rendering screen is simple and mostly done on Screen.java. Here Prelude render first gui then game using Bitmap3D. This class keep care of player position (camera) and draw all objects on screen from a viewport using it. It's interesting notice that first all game is draw on screen then is postprocessing adjusting pixels brightness. One step at time!**Tick and entities**: every active object into Prelude extends Entity, as seen in type hierarchy![](../../assets/67efa046efc33123.png)

Entity type hierarchy

Again a good foundation is to keep some common logic into an ancestor class and use it into children.

An interesting point is into Entity.java where isFree method located. Here Prelude take care of check for collision between Entity/blocks and Entity/other Entities: key point is invoke a callback collide both entities when collision occours, to notify it. So for example when bat hurt player, both player and bat are notified of it and so on. Simple, powerful and easy to get into your game!

Read for example OgreEntity.tick(): when game ask ogre to act if time is right he shoot a bullet to player!

![]() |

**Player**: player movements is handled into Game.java and then Player.java move position, rotate it and so on. It's better to have a look into it, go get the full idea, trust me!**Levels**: other than entities there are statics block to diplay and update and here, after load from an image-level-definition, building istances of Block.java according to level definition into an array. Then blocks are decorate, for example adding torch's sprite to blocks and so on. Powerful ideas here: level defined into a small image using colors, blocks as container only of basic informations and decorations (aka associate sprite to a block) after load it.![](../../assets/f70d64425b6db696.png)

yes, this is a level defined as image from notch

This is just a small step into notch's mind, but amazing thing is how he works: in just 48 hours made a little gem (remember, it's an hard game!) it incredible! Good work, notch!

What can we learn from this code? Not only write a simple wolf3d-clone is easy in java, but you can do it in 48 hours, using only your creativity and the basic idea: keep your game and your code expandable, be agile. Like in minecraft, right?

Where is the exit? I have to finish this game!! :D lol

## No comments:

## Post a Comment