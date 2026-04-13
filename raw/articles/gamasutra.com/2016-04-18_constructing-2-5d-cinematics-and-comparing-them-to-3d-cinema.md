---
title: Constructing 2.5D cinematics and comparing them to 3D cinematics
url: https://www.gamedeveloper.com/art/constructing-2-5d-cinematics-and-comparing-them-to-3d-cinematics
author: Kaj Driesen
published: '2016-04-18'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Constructing 2.5D cinematics and comparing them to 3D cinematics

In this post I discuss my research on the topic of 2.5D and 3D cinematics and walk you through my process of creating them.

![Game Developer Game Developer logo in a gray background | Game Developer](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/bltba62518415cda0e2/652fe6ddbc479f8697ef691f/default-cubic.png?width=1280&auto=webp&quality=80&format=jpg&disable=upscale)

In this article I’ll be making a quick comparison between 2.5D and 3D cinematics after which I’ll talk about my research to delve deeper into this topic. Additionally, I’ll be showing the method I used for the creation of 2.5D cinematics.

When I talk about cinematics, I’m talking about short videos relating in any way to the story or promotion of a game. Cinematics can include story cut scenes, teasers, trailers, and any other supplemental videos that support a game’s story or background.

I will be comparing:

pre-rendered CGI cinematics (which focus on high levels of detail, high quality rendering, and semi- or fully-realistic lighting and materials)


to

painterly 2.5D cinematics (which use a combination of 3D techniques and 2D paintings to create something similar to an animated comic).


![](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blt2fc766103deccf0b/650e9a3bf631d51892308ee4/LotV_Screenshot.png/?width=604&auto=webp&quality=80&disable=upscale)


![](../../assets/5ad0d199ee11800b.img)


The styles will be compared on two main parameters:

Audience reception

Production cost


By doing this I hope to be able to give direction as to when the use of a certain style is advisable for certain games or developers.

Investigating audience reception

Views | Likes/Dislikes | |
Mists of Pandaria (3D) | 16,805,764 | 99,029/11,017 |
Burdens of Shaohao (2.5D) | 558,697 | 5,808/98 |
Warlords of Draenor (3D) | 19,124,708 | 84,784/2,512 |
Lords of War (2.5D) | 1,970,853 | 15,483/149 |







By looking at Blizzard Entertainment’s channel on YouTube, we can get a first idea of how audiences respond to the two styles. A vast difference can be seen when looking at the view counts for “[Warlords of Draenor](http://www.youtube.com/watch?v=TLzhlsEFcVQ)”, a 3D intro cinematic, and comparing it to the first video of “[Lords of War](http://www.youtube.com/watch?v=LG3RVCEwCPg)”, an accompanying 2.5D series. While the former has almost 20 million views, the later has only 2 million (on 11/4/2016). When comparing the viewer ratings, however, a different story can be seen. “Warlords of Draenor” has close to a 33/1 positive to negative ratio, while “Lords of War” has a ratio closer to 107/1. A comparison of the “[Mists of Pandaria](http://www.youtube.com/watch?v=wvYXoyxLv64)” 3D cinematic and its accompanying “[Burdens of Shaohao](http://www.youtube.com/watch?v=afpRzcAAZVM)” 2.5D series shows a similar pattern.

These numbers give us a good first impression, but there are too many variables at play to get a definite conclusion. Because of this, I decided further research would be valuable.

I decided to eliminate as many variables as possible and then conduct a survey with deeper questioning than simply “like” or “dislike”. The surveys starts with the viewing of a cinematic in one of the two styles. It will be either the 3D rendered style, or the painterly 2.5D style.

The cinematic I’ll be showing is “Warcraft III - Reign of Chaos - Arthas' Betrayal” by Blizzard Entertainment. For some in the original version, and for others in a 2.5D version created by me. I’m using the “same” cinematic to try and minimize any difference in story, audio, subject or context as much as possible. I also chose a relatively older 3D cinematic to make up for the possible lack in quality of the cinematic that I was able to produce.

Creating the 2.5D Cinematic

There are several different ways to go about the creation of a 2.5D cinematic. Below I will be outlining the method I used, as well as some of the issues I faced along the way.

By choosing to remake an existing cinematic most of the preproduction work was done for me: it was not necessary to do any concepts, color keys or storyboards, as these would all be copied from the original cinematic. As such, I could immediately jump into the technical aspects of development.

![](http://kajdriesen.com/S07_Layered_GIF.gif?etag=%2260f1f-57114bea%22&width=553&auto=webp&quality=80&disable=upscale)


The pipeline starts with making a painting for the shot you are working on. When making this painting, it is important to already start planning out which elements will be furthest from the camera, and which will be closer, so you can paint the layers accordingly. Additionally, any elements that will be moving must also be painted on a separate layer. Lastly, key frames must be painted for any large movements.

![](../../assets/024f2cbf32f23748.img)


For the next step, the images will be projected onto 3D layers. The painting is brought into Maya, or an equivalent 3D program, and the geometry is constructed upon which the painted layers will be projected. In many cases these are simple planes, but sometimes more complicated geometry is needed for the right result. Both a projection and an animation camera are added to the scene, after which the first test renders are made.

![](../../assets/2cd88d8d8bfea822.img)


Once the geometry and camera are in place, we move to compositing software. In this case I chose Nuke because the free version was sufficient for my purposes. Here we import all our geometry, cameras and textures once again. In Nuke, we can more easily look for any problems that were missed than we can in Maya. This step is also where particle effects are added. Once everything looks correct, the shot is rendered out and saved.

![](../../assets/cc236568eee0780b.img)


This process is repeated for each shot in the cinematic, after which all of the separate shots are brought into video editing software. For this pipeline, Adobe Premiere was used. The shots are all stitched together, and any necessary transition effects are added. In this stage the audio is also added, and any mistimed shots are adjusted. As a last step, the video is exported and appropriately compressed.

Production Cost

By going through this process, I can already hypothesize that the production of 2.5D cinematics will be lower than those of 3D cinematics. I am currently attempting to contact and interview others who have worked on cinematics in a studio environment to get more confirmation on the topic of production costs and will publish my findings when I complete this process.

Future Plans

The next step in my research is conducting the survey I created and drawing my conclusions for the results.

This is where I ask for your help:

I hope that reading through this article has made you as interested in this topic as I am and that you will be willing to spend some time viewing the results of my labor and filling in the questionnaire. It should not take you any longer than 5 minutes. Please click [this](https://docs.google.com/forms/d/1kSjxTHC3abCEUsApBOiWcUza_blqzv-NGBv2nzfBr7c/viewform) link to join in. If you really don’t want to do the survey, but would still like to see the finished 2.5D cinematic you can do so [here](https://youtu.be/KrHmIGtEayQ).

Lastly, I would like to thank you for reading and invite you to contact me on contact(at)kajdriesen(dot)com if you have any further questions or suggestions concerning my work or this topic.