---
title: Notes on vr development
url: https://www.executionunit.com/blog/2019/05/10/notes-on-vr-development/
published: '2019-05-10'
source_blog: Blog | Execution Unit
source_site: http://www.executionunit.com/blog/
category: game programming
fetched: '2026-04-13'
---

Prompted by [a question](https://www.reddit.com/r/gamedev/comments/bmnleb/how_is_developing_for_vr_different_than_a/) on reddit’s gamedev subreddit here is a slightly more fleshed out answer to

How is developing for VR different than a standard 3D dev cycle?


In 01/2018 we worked on a VR prototype of [Smith and Winston](http://www.smithandwinston.com), ultimately we abandoned it because we couldn’t attract enough investment to take it forward. Here is what we learned, hopefully this is useful to anyone else embarking on a VR project even though this was learned over a year ago.

## Interaction

One of the first things you’ll experience in VR is that some types of interaction that are rewarding in a 3D or 2D game are so different that they are completely useless or make you vomit.

Things that are annoying like “Press triangle to continue” are a PITA in the real world and if you can’t see the controller it’s impossible to remember where triangle is anyway. The solution of placing the controller in the scene, something we did for Smith and Winston demo, doesn’t work in all games. Astrobot does this really well by making the controller an integral part of the players experience.

![Smith and Winston putting the controller in the scene.](../../assets/57b2a07f963dd6f5.jpg)


*Putting the controller in the scene helps but not always*

The sheer act of looking around in a 3D game is interesting but it can be completely absorbing in a VR game. Even beyond the trivial first contact with VR the act of being in a game is intensely rewarding to the player.

So if you bring a traditional game, like we did with Smith and Winston, you quickly find a lot of what you’ve learned, implemented and become accustomed to is no longer useful.

## Sound Design

Sound design is the ugly step child in game development. Everyone knows it’s there but no one pays enough attention to it. In VR the minimum requirements are much much higher. I’d go as far as to say potentially two to four times more costly for an indie. For the AAA guys, they are already doing full surround sound 7.1 Dolby mega THX tastic stuff that people play out of their crappy PC speakers. For them, the audience may actually hear their lovely work. For indies, you need to step up your game.

In VR, because the players head is IN the game (and thus their ears are in the game) and because nearly all VR is played with headphones, the potential for sound design is much greater but also what is needed is much greater. The player can pinpoint exactly where the sound is coming from relative to them and they will look at the sound source.

![Smith and Winston Chalk and Flowers Secret Level](../../assets/459b2ca8dd492a98.jpg)


*this image is from the 3D (non vr) version of the game*

In Smith and Winston we had a very low pace puzzle level as a break from the destruction. The sound design for this level is a very light wind, the occasional Cicada chirp and a single bird call (that can play from five or so different locations). That is all that is needed. The player gets it, it’s restful.

However in VR the bird call was annoying as you can never see the bird despite being able to locate the invisible sound source pretty well. We’re all used to not being able to locate the Cicada sound but we expect to be able to see the bird.

There is so much potential for immersive sound design in VR but there is also so much that can be subtly wrong that disconnects the player from the scene.

## Textures will all need work

The actual displays for each eye are very low resolution and the image you send to the headset is very distorted. This tends to exaggerate any slight movement of pixels and noise within textures. The “small voxel” art style in Smith and Winston naturally creates a very high frequency image and when distorted the middle distance shimmered and looked terrible. We toned all of our colours down to compensate for this. It’s basically was not possible to take all of the levels we’d already designed and just explore them in VR.

The level of detail in the scene dramatically affects how the brain reacts to motion. So games like Rez with limited detail can get away with extreme speed/direction change where as doom can make you spew in 30 seconds. It takes a lot of time to find the sweet spot for your game and art style.

## Implicit design.

There are very many things about playing a game that you don’t need to explicitly tell players. Everyone knows how the analog controllers work for example. In VR those tropes haven’t been established yet. As time goes by this will be fixed and stand out titles like Astrobot are setting standards for people to follow. We’re not there yet though.

## Captivated

In games like Astrobot, Moss and in our demo players are totally captivated by tiny life forms that they can bend over and look at. It’s a deeply rewarding and weirdly emotional experience for players and it can change your game completely. When the robots in Astrobot look at you it is a very intense experience that cannot be replicated in 3D (nor in movies I would add).

![Smith and Winston looking in a hole](../../assets/b542b4d496aa6398.jpg)


*I couldn’t find a picture of looking at Smith or Winston but here is a pick up the player uncovered*

## Time challenges

The tweak/test cycle is a LOT longer. It takes time to put the headset on/off and you need to rest your eyes/brain a lot more for VR work. It’s easy to work too long and get car-sick.

## Budgeting

A lot of the recent indie/small studio boom has been enabled by the off the shelf engines. This has dramatically lowered costs and risk. In VR those gains are partially lost. The increased sound design and slower design/tweak/test cycle increase costs and risk. This new risk/cost profile has to be balanced with the smaller market that VR currently offers. Again, over time this will hopefully change as VR grows. A lot of publishers are not willing to take on the increased risks at the moment so the actual designs they will consider are more limited.

Anyway, hope this helps someone who is researching doing a VR game.

## Comments