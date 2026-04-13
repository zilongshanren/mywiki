---
title: Simonschreibt.
url: https://simonschreibt.de/wft/watchdog-problems/
author: Simon
published: '2015-10-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

I don’t know if this is the standard, but when our game stored a screenshot as BMP it had an Alpha-Channel – which was **not** empty! This is how the BMP looks:

![](../../assets/d77b0c6fa65f7d2b.png)


And this is how the **Alpha-Channel** looks. This is some our debug text menu (which can be activated but was disabled while the screenshot was taken) and do you see the lower right square-gradient? This is a part of the Steam overlay (was not visible while taking the screenshot), which tells you that you can press Shift+Tab to enter the full overlay.

![](../../assets/35ac73414fafedd9.png)


Well, this shouldn’t be a problem since the alpha channel isn’t displayed, right? Unfortunately it **is** a problem since a PNGs transparency information is directly displayed and therefore the resulting image looks like this (the little gray squares are Photoshop background and show were transparency happens):

![](../../assets/b7bd99e5a0e12c71.png)


I guess now you can understand why we couldn’t use the PNG directly out of the box and why we had to use the “-alpha off” option during the [conversion process](http://simonschreibt.de/wft/watchdog-convert).

We were able to disable the whole UI **except** the cross-hair. When we finally got the functionality, we’d have to choose the time to disable the cross-hair wisely because all screenshots would change!

![](../../assets/d43bed30da335ee0.png)


You’ll get a lot mail and it’s quite possible that you miss an important difference in this mail avalanche! So better do this over a weekend where nobody changes stuff.

HDR+Eye Adaption or other post effects might change the image over time and if you’re unlucky you get some differences every day. Here’s an example. Do you see how the brightness changes slowly after every jump?:

**Note**: You couldn’t automatically compare such a shot anyway due the fog and random asteroids. It was just a good example for visualizing the effect. :)

Another day when I was getting hundreds of mails was when a new Post FX was tested. Can you guess what effect it is, by looking at this difference shot?

![](../../assets/10830d2d79e961fa.png)


Right, it was a test for movie-grain-filter and we decided to disable the effect at least for the Watchdog.

Sometimes you end up with a screenshot like this:

![](../../assets/68c2629c5e98bb8d.png)


How the heck did this happen? The reason is that data wasn’t loaded fast enough. During “real” gameplay you move slower and even if you fly through a jumpgate it’s possible to pre-load some data because the game assumes that you want to fly into a new cluster. The screenshots script has no clue about that and sometimes it looks like that after a jump:

That’s why we wait some seconds after **every** jump which of course stretches the script duration. The obvious solution here is to start the game from an SSD and reduce the waiting time.

The same problem occurred in our material scene. Like i described [here](http://simonschreibt.de/wft/watchdog-take#additionalNotes), the scene contains **all** materials of our universe and it takes some time to load all the textures:

That’s why we wait **60s** before doing the first shots.

When you do material shots you wanna end up with something like in the image below: Especially for metals you want some reflection from your cubemap but in best case the background of the image itself should be black.

![](../../assets/ca1897d12dea36ac.png)


Of course it doesn’t has to be a black background but even if it would work for opaque materials, it might be hard to separate material and background when it comes to translucent examples:

![](../../assets/66fc893e354d382c.png)


And you don’t want to get a warning mail only because someone changed the position of a star in the background. But turning the whole background black isn’t a solution because not much is left when you take away reflections from a metal or glass material. [Lino](http://linolafett.deviantart.com/) had the idea to just put a black plane behind the geometry and get best of both worlds:

![](../../assets/c4cdcbd92e9ff8dc.png)


Worrying about disk space makes it all a bit harder. For the images which have to be compared, we do **not** store **every** iteration every night. Only when something has **changed**, the image is kept. Otherwise it gets deleted. When the comparisons starts the two newest files are compared:

![](../../assets/c08880ce6de1d3e1.png)


But sometimes **no** new image is created (for example when the game crashed but the Watchdog Script is still continuing its job like converting, comparing, sending mails, …) and then the two latest files are of course different since you **only** store differences!

![](../../assets/d6f3d075979f514a.png)


My solution to this is that I check the date of the newest file and only if this date is the same like today, I start the comparison process. **Careful**: If you start the Watchdog before 12 PM and the image-creation takes e.g. 2 hours it might be that some images are created “yesterday” and this just mentioned check wouldn’t work anymore!

Besides of the storage there’s another reason to use smaller images: We take the screenshots which **don’t** have to be compared in 1280×720 and the ones for comparison only in 640×320. The reason is, that the comparison costs a lot time when the images are too big. As long as they’re binary identical it’s really fast but if there is some pixel difference, you have to wait longer. Here is a comparison between 1280×720 and 640×320:

Our game had nice minefields where the mines would move towards you (and explode) if you come too close. Sometimes, during taking screenshots, a jump ended in such a region. When we started to test the script we **didn’t** set the player ship/camera to indestructible. We were wondering why the screenshot process was aborted and saw what happened when we looked at the last created screenshot (which showed more or less a huge explosion).

Some shaders create random animated patterns and must be excluded from comparison – except you like to receive a warning mail every day.

We even had to exclude some materials **completely** from the whole process because all material geometries lay in **one** scene and the vertex shader stretched the material so far, that it disturbed the screenshots of the nearby materials.

I developed the script on my computer but the daily execution happens of course on the server. When I tested the script on my machine and let it create images with a resolution of 1280×720 and all was perfect. But some day we discovered that the images on the **server** only have **1264**x720. WTF is this??

The reason is somethings most server have: A small monitor!

Our server monitor has a native resolution of 1280×1024 and and the game is started in window mode. And a window normally has a border. Because of this border the game doesn’t run in full 1280 but only in 1264.

![](../../assets/d5af235548f1e204.png)


Until now this wasn’t a problem but it will be at least for one night, when the server gets a bigger screen. Because in that night the new images will be 1280×720 while the old will be 1264×720 and the image comparison doesn’t like different image resolutions at all.

![](../../assets/d22a4d9a4c594b7e.png)


We’re using [CruiseControl](http://cruisecontrol.sourceforge.net/) which is a program “[…] for creating a custom continuous build process”. CruiseControl handles all the stuff and also executes the Watchdog Script. If the Watchdog writes sometimes as output, it will appear in the log of CruiseControl. Once, I wondered why my script always crashes.

This line was the reason:

Console.SetCursorPosition(50, Console.CursorTop);

The line just sets the text-cursor to a fix position to have nice aligned text in your console:

![](../../assets/0ac8e89eb28cebd7.png)


The problem was for me, that the error message let me think that I did something wrong with writing my mail output TXT because it said something about** System.IO**… :D

![](../../assets/721dbbd167e2dd78.png)


The game has a function to safely position the player after a jump if he’s too near to (or **in**) an object. Some screenshots where different every day because an object was placed very near to the position where the Watchdog Script would jump to:

This isn’t a major issue since this screenshots doesn’t get automatically compared anyway (due the random fog/asteroids/…) but this can have an drastic influence on the frame rate (high FPS when no objects is near the camera and low FPS when an object is full size on the shot) which then again might trigger performance alarm mails.

I already explained [here](http://simonschreibt.de/wft/watchdog-take) that we had to use a work-around for shooting the materials in form of **one** scene containing **all** material test-geometries.

![](../../assets/0a3807e39d2e84b7.png)


Exporting this scene took forever because it consists of 800+ separate geometries. The obvious solution was to melt them together to one big geometry (with a huge multi-material) which wasn’t possible because our engine is limited to max. 20 materials per objects. That’s why the MaxScript had to combine only every 20 geometries into one object.

That’s it! You made it! *wuff* The watchdog is happy that read until here and we hope you enjoyed the read. Feel free to let me know any of your experiences, opinions or questions in the comments, [mail](mailto:simon@simonschreibt.de), [twitter](https://twitter.com/simonschreibt) or [facebook](https://www.facebook.com/simonschreibtblog)!

![](../../assets/d7175abd6ce0df70.gif)