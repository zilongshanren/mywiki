---
title: Simonschreibt.
url: https://simonschreibt.de/gat/black-flag-waterplane/
author: Simon
published: '2016-12-14'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/3b710fb2ff0e7821.png)


![](../../assets/3b710fb2ff0e7821.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

![](../../assets/f60d71265b66a711.png)

If your game demands for having boats swimming in water you might get interesting problems to solve. Since boat-water-interaction is pretty expensive to simulate, normally the water-plane just cuts through the boat-geometry like in this example:

Today we’ll look at some smart solutions how to hide that artifact from the players eye.

![](../../assets/3c413dc11bf35f5c.png)

Big boats usually don’t have this problem – at least if you’re standing on deck or the camera shows the ship from the outside. In these cases you can’t see into the ships “belly” and wouldn’t notice the water-plane.

But one day I saw this funny bug-video recorded from [Back Flag](http://assassinscreed.ubi.com/de-de/games/assassins-creed-black-flag.aspx) which shows really obvious, that the developers actually pushing the water away below the boat!

So I got the game to investigate this issue and even if the effect is way less drastic, if you look closely you can see how the ships interacts with the water:

Unfortunately I couldn’t find too much detail about this. This is one of the few quotes I got (note that this is from about Assassins Creed **III** [not Blag Flag!]):

Full detailed collision detection with fluid dynamics and rigid body interactions would be impossible in realtime, but it is effectively simulated by the use of multiple partitioned boxes or ‘buoyancy spheres’.


[Assassin’s Creed III: The tech behind (or beneath) the action]

The article came with this picture. But by looking at the bug video and the accurate ship-shaped hole in the water I can’t believe, that the job would be done by only these spheres…

After releasing this article someone (he/she wanted to stay anonymous) brought light into the dark:

“The buoyancy spheres are probes used to measure the velocity of the ship entering the water at that location, it tells the particle splashes when and how big to spawn.


The water is pushed downwards based on a small displacement mask that’s projected onto the water. You’re right about the clipping plane on the small boats.”

– A nice but anonymous developer

Anyway, the engine does an impressive job with that simulation – but something else catched my attention during the investigation. It was the **small** boats in the game.

![](../../assets/b139946858b3cff7.png)

Like explained above, big boats can hide the water-plane by not showing the insides of their “belly” to the player. Smaller boats often don’t have this luxury but as you can see in this evidence-video, somehow the water-plane is not visible even the boat “sticks” in the water:

Before I present my theories about the solution, here is how it looks in some games where this problem wasn’t a big priority:

Sure, if your boats are damaged anyway they are allowed to be filled with water like below. Bot let’s look at solutions to this issue without having to physically simulate all the water!

![](../../assets/53930cca22d269d1.png)

If your game-camera always looks from **above** (like for example in most action-rpgs) a common workaround might be to let the boat just float a bit which shouldn’t be that visible (except the boat drops a shadow on the water). It’s a dirty hack but Mr. Pirate doesn’t care as long as his feet are dry. :D

![](../../assets/e9c991d62d6f05fe.png)

Inspired by the big boats you can add some geometry to the boat to hide the inside of the “belly”. So the water actually **is** in the boat but as long as it is not higher than the added geometry nobody will notice. Job done. Arrrr!

Here you can see exactly that done in Fallout 4:

![](../../assets/0365953f60daba70.png)

Now back to the boat in Black Flag. Clearly the water-plane is high enough so than we *should* see the water in the boat.

The magic seems to be coming from an invisible geometry which is covering the top of the boat like a lid:

At first I thought this plane might be used as a mask/stencil buffer so that the game just would **not** render any water in **front** of this plane but this would be problematic if you would have a big wave like this looking at the boat from the other side:

If you would **not** draw any water, the wave would have a “hole” where the lid-geometry of the boat sits seen from the pirates point of view.

Then [Attila](https://twitter.com/ATTILAM) mentioned a technique called “DepthMask” ([read more about it here](http://wiki.unity3d.com/index.php/DepthMask)) and this seems to be the key:

You first render your terrain, pirate, boat, etc. and then – and this is the secret weapon here – you draw the invisible plane **but you draw it only into the depth buffer!**

If you don’t know what a depth buffer is, I tried to visualize it here. Basically it’s used to store the distance to the camera (per pixel) and is used for sorting. With that you can (but don’t have to) discard pixels behind other pixels before executing the pixel shader:

Now you can render the water-plane which will only be visible in those areas which aren’t already obstructed (based on the information in the depth buffer).

Here you can see this in action:

What’s happening?

- There’s no water and no invisible plane (you can see then inside of the boat in the depth buffer).
- Invisible plane is rendered into depth buffer. Now you can’t see the inside of the boat in the depth buffer. No
**new**pixel below the invisible plane will be rendered anymore. - Water is rendered where no other pixels of the depth buffer obstruct it.

And here comes some evidence for all this:

![](../../assets/91459f463c8095bd.png)

1. Sometimes you see artifacts like in the example from the beginning of this article. When the waves are higher than the lid-geometry you can see this:

![](../../assets/7f31e4778f88c83c.png)

2. Sometimes you can see foam **inside** the boat which leads to the suspicion that the water-plane is still there (even if we can’t see it) and the logic reacts the to player spawning foam.

![](../../assets/235e34f0d9d7f471.png)

3. When we disable the draw call, which draws the magic lid-geometry, it looks like below. Look at this, I guess we’ve found the water!

Isn’t that beautiful?

By the way, while working on this article I remembered another game which might be worth a look:

![](../../assets/cc507fb37a54bba3.png)

In Battlefield 2 you could have these amphibian vehicles where players could sit in the “belly” of the car.

So I wondered how they would cut away the water-plane for those players to avoid that:

This is how it looks when you’re sitting inside this car. As you can see, there’s no water inside which surely makes the soldiers happy.

I tried to investigate this so here’s what I found out. Just to recap, this is our result:

To get there, very early (in my case it was the 13th drawcall of ~280) the geometry of the windows is rendered (here he lower left corner):

Just for better understanding, here’s how this geometry looks like from further away:

Note: Nothing is visible yet! I suspect that this just serves as a **mask** to know what needs to be rendered so that you can discard everthing in the black area:

Then the terrain and water is rendered and the mask seems to keep the water out.

Just a side-node: If you disable the drawcall for the windows-geometry right now, it looks like this:

You may think that everything is fine but wait until they render the foam on the water:

Luckily they render the window-geometry again! This time we even see the geometry (i increased the contrat a bit to make the geometry better visible):

Basically that’s it. Of course the UI is rendered next but this isn’t really important right now. :)

So the truth is that the soldiers having a bath all the time but this is basically done to them:

![](../../assets/1338fd8b1dc17bba.png)

I really hope you like the new article/video and I would love to hear your opinion, tips, ideas, theories and whatever else you want to tell me. Have a nice day!

Links & Resources

[a01][Assassin’s Creed III: The tech behind (or beneath) the action](https://www.fxguide.com/featured/assassins-creed-iii-the-tech-behind-or-beneath-the-action/)

[a02]

[Assassin’s Creed IV: Black Flag Ocean Technology Talk](http://www.gamedev.net/topic/652966-assassins-creed-iv-black-flag-ocean-technology-talk/)

[a03]

[Assassin’s Creed IV: Black Flag Has The Most Beautiful Bug I’ve Seen](http://www.kotaku.com.au/2013/11/assassins-creed-iv-black-flag-has-the-most-beautiful-bug-ive-seen/)

[a04]

[Interactive Water Surfaces](http://jtessen.people.clemson.edu/papers_files/Interactive_Water_Surfaces.pdf)

[a05]

[5 things you need to know about the tech of AC4](https://www.fxguide.com/featured/5-things-you-need-to-know-about-the-tech-of-assassins-creed-iv-black-flag/)

[a06]

[AC4: Black Flag Graphics Tech Explained](http://www.gamersnexus.net/gg/1205-assassins-creed-4-black-flag-graphics-analysis)

[a07]

[Unity 3D Wiki: DepthMask](http://wiki.unity3d.com/index.php/DepthMask)

[a08]

[Wikipedia: Z-buffering/Depth Buffer](https://en.wikipedia.org/wiki/Z-buffering)

[a09]

[A trip through the Graphics Pipeline 2011, part 7](https://fgiesen.wordpress.com/2011/07/08/a-trip-through-the-graphics-pipeline-2011-part-7/)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

Hey :) Nice trick and nice explanation. How does the effect that you see in the AC4 bug video work though?

Someone told me that a small displacement map is used for this. It pushes the vertices downward.

Very nice article!

About the masking of the water in the boat, another approach is the usage of a stencil buffer. Stencil buffer is basically a mask (generally 8bits) that you can read, write, increment and decrement that is often use to create portal effects, masking certain objects or even redner shadows, like in doom 3. If the hidden geometry is writing a value to the stencil buffer, let say 1, and the water is rendered after that everywhere except on the pixels that have a value of 1, then you’re good.

Here is a screenshot of the stencil technique in action : http://www.ignishot.com/localimages/BoatStencil.png

wow, thanks for the screenshot and the explanation! this is awesome :)

But, like in an example at article, in the situation with looking on a ship throught a very high wave wouldn’t you discard nessesary fragments and see a hole in wave?

I made a rather terrible image gallery explaining this depth mask solution for the Minecraft 1.9; http://imgur.com/a/xxOUw

Prior to the 1.9 update, boats in Minecraft had a “hidden belly”, which solved the problem of them flooding, until they got too low and then the problem appeared again.

During the 1.9 update, a preview version had lowered the belly of the boat – which resulted in them becoming permanently flooded. Mojang saw my image gallery and implemented the solution :)

There is another technique as well; portals! A stencil buffer can be used in-place of the depth buffer for masking, however this comes with the limitation of the water needing to be a uniform level (no large waves in-front of the boat). The benefit is that the depth buffer is not modified, which may be important for other effects.

What do you use to step through draw calls like that?

Intel GPA (DirectX) is a good program for that as well as NVidia NSight (OpenGL). GLIntercept as well is a nice tool but doesn’t offer stepping through drawcalls. But it offers (when it works) for example a free debug camera.