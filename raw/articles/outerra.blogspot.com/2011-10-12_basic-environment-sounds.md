---
title: Basic environment sounds
url: https://outerra.blogspot.com/2011/10/basic-environmental-sounds.html
author: Outerra
published: '2011-10-12'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The whole system works by sampling coarse level environment data points surrounding the camera, using a 5x5 cornerless grid. Sound emitters are then set up at the places of the points, and each emitter is assigned a sound buffer corresponding to the type of environment.

To hide the grid layout, the emitters are set up to start attenuating the sound only from a distance that is larger than half the grid step. This works almost alright, except that the unattenuated zone also spans upwards, which doesn't feel natural. Later we'll have to implement a custom attenuation function that will handle it.

At the moment there are just 4 environment types - grass, open sea, shoreline and forest. Each emitter of given type can use only one of two sound samples (for now), that are pseudorandomly picked for given location. Locations are identified using a global unique identifier; this identifier is also used to manage the reuse of sound emitters.

Apart from these ground sources there is also another layer of emitters that are used to provide sounds of wind and rustling of tree leaves. They are positioned higher above the ground.

Following video shows it in action. The sound of wind in the last part of the video (in forest) is too loud, especially when the leaves and branches aren't moving yet.

***

In other news, we have started a closed beta testing of our alpha demo (yea, beta of alpha

[announcement](http://www.outerra.com/forum/index.php?topic=464.0)and some info from it.

It goes pretty well, meaning we are getting lots of crash and bug reports and unexpected behavior reports on various combinations of hardware, OS versions and internet settings.

It's keeping us quite busy at the moment.

***

There's also a new truck model with digital camouflage texture, that we want to use for our demo game:

The camouflage is a modern type that is apparently not so well-known, and from the initial reactions it seems that Minecraft has spoiled it for people who didn't know about it before :-)

## 3 comments:

Who's on your list for the beta testing? I would love to be able to try this too :)


@zGuba I don't know what you're talking about but there is already doppler effect thanks to OpenAL, you can hear it in the video :)

@Remi Primarily the seasoned people from our forums who are following it actively for some time already, though sometimes we also admit lurkers.

By lurkers he means me... =]

Post a Comment