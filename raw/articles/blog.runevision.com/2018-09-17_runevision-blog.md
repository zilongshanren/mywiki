---
title: runevision blog
url: https://blog.runevision.com/2018/
published: '2018-09-17'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

Since my [last post](http://blog.runevision.com/2018/07/level-design-workflows.html) in July where I finally got a vision down for the level design in Eye of the Temple, I've been feeling super productive adding new areas and features to the game.

In August I added two new areas and in September I've been revamping the in-game UI and the speedrun mode. Only problem is I haven't kept up with these blog posts. To avoid this post getting too long, I'll cover the new areas here and save the UI work for a later post.

### Creaking Gorge

Creaking Gorge is an area where you move along and into cliff sides and atop wooden scaffolding. It's by far the most vertical area in the game, spanning more than 50 meters vertically.

![](../../assets/5bf0ccf18a08d252.png)


![](../../assets/5bf0ccf18a08d252.png)


Let me talk a bit about my workflows for doing level design in Eye of the Temple since I recently had some progress in that area.

I've been in something akin to a level design writer's block for a long time, being able to rework individual small areas, but unable to start the major world redesign that I've been intending for over a year.

Maybe calling it writer's block is pretentious - the fact is that I've never done this sort of work before, so I may just not have developed the necessary workflows to deal with it. Anyway, I think I might have finally cracked the nut.

I've had plenty of ideas, but fragmented and not crystallized enough to get down on paper. How do you start planning a non-linear world meant to be highly interconnected and interdependent? I can talk about what eventually worked for me.

I've long pondered what type of document could help me get ideas down on paper in a quick way. In addition to text documents (glorified to-do lists) I've been using tilemaps for sketching level designs.

I've been experimenting with using Unity Tilemaps as a digital replacement for pencil level design sketches. Some success so far, although I'm really missing rotation/flipping of selection and proper multi-selection.

— Rune Skovbo Johansen (@runevision)[November 27, 2017]

![](../../assets/b7e6393531c3a394.jpg)


It's time for a new update on the development of Eye of the Temple.

![](../../assets/83a9df296a601a60.gif)

### Events

GDC in March is well behind us and I had a great time there. Among other things, I got to show off Eye of the Temple at the [European Game Showcase](https://soops.net/selected-games-european-game-showcase-2018/) (and saw a lot of other cool games too). This was a private event for specially invited people from the network of the organizers.

Now, Eye of the Temple has been selected for [Yonderplay](http://www.copenhagengamecollective.org/2018/04/15/yonderplay-nominees/), an event that's part of the Nordic Game Conference in Malmö in Sweden and open to everyone at the conference. This will go down on May 25, the last day of the conference. This is the most public showing of the game yet, and I'm very excited about it! If you'll be at Nordic Game Conference yourself, come by and say hi and give the game a try.

![](../../assets/37c9d2b071eb7409.jpg)


Last week I took a dive into the world of PR with Eye of the Temple.

There is a new trailer you can see on the website [eyeofthetemple.com](http://eyeofthetemple.com/) or right here below.

And Eye of the Temple now has a Steam page: [Eye of the Temple on Steam](http://store.steampowered.com/app/589940/Eye_of_the_Temple/)

If you have a Vive or Oculus Rift, and think Eye of the Temple looks interesting, you can totally add it to your wishlist on Steam now! ;)

After that I took my first stab at contacting the press with a press release. The story got picked up by [UploadVR](https://uploadvr.com/eye-of-the-temple-vr-game-requires-room-scale-locomotion/) and a handful of smaller outlets (see list on the [Sanctum Dreams](http://eyeofthetemple.com/sanctumdreams/) website). Considering I'm an unknown small indie developer with no experience with the press, I'm pretty happy with the results.

This week I'm at Game Developers Conference in San Francisco. I'm mostly here with Unity, but I'll also be showing Eye of the Temple at the [European Game Showcase](https://soops.net/selected-games-european-game-showcase-2018/).

Exciting times!


It seems like I didn't blog since July. How scandalous! Well, here's an update on what I worked on for [Eye of the Temple](http://EyeOfTheTemple.com) since then.

Presented as a series of tweets, because that's what I have time for.

**Note:** Add blockers seem to sometimes randomly block some of the embedded tweets for some reason.

### Prettier background environment

The cold snowy mountains didn't give the feeling I was aiming for. Failing to find anything ready-made that fit the bill, I created my own lush, mountainous environment.

What do you think of this new environment art for the backdrop of the temple that we've been working on?

— Eye of the Temple (@eyeofthetemple)[#gamedev][#indiedev][#VR][#HTCvive][pic.twitter.com/ASGxGCeG3p][September 20, 2017]

Another shot of the mountains surrounding the temple.

— Rune Skovbo Johansen (@runevision)[#screenshotsaturday][#gamedev][#indiedev][#VR][#HTCvive][#madewithunity][pic.twitter.com/GmfAwyzPvp][September 23, 2017]

### Failed attempts at mixed reality capture with StereoLabs ZED stereo camera

I think a mixed reality video would be the ideal way to show off Eye of the Temple, so I invested a bit in this. Unfortunately it didn't go well due to a combination of a bad choice of immature tech, and an insufficient green-screen setup. I might revisit this in the future though.

— Rune Skovbo Johansen (@runevision)

[@stereolabs3D]Could you show how this 3D printed mount is meant to be used with a Vive controller and tracker respectively?[pic.twitter.com/UqoEm0E77v][September 16, 2017]

It's designed to hold a Vive controller, a tracker and even an oculus touch.

— Stereolabs (@Stereolabs3D)[pic.twitter.com/yc4fC2J5ZJ][September 16, 2017]

I posted a video here with my troubles. See tracking issue at 8:04. I mailed your support with more details.

— Rune Skovbo Johansen (@runevision)[https://t.co/DCk6KeRO0O][September 23, 2017]

Argh! Mixed reality recording is hard!

— Rune Skovbo Johansen (@runevision)[#VR][#mixedreality][#HTCVive][#indiedev][pic.twitter.com/YWVH6oFgc9][September 26, 2017]

### Glowy light for certain platforms

Any Unity shader experts who might know why I get heavy banding on alpha of frag function output on Windows (but not Mac)?

— Rune Skovbo Johansen (@runevision)[pic.twitter.com/Xrq8CliYNo][October 16, 2017]

I made a spiky glow for this platform. Helps a bit with awareness of edges without having to look down all the time.

— Rune Skovbo Johansen (@runevision)[#VR][#gamedev][#indiedev][pic.twitter.com/I9ScvbmzZL][October 17, 2017]

### New build for testers with whip and other improvements

I finally finished developing the whip and got a build out to the testers.

### Trying to recruit people to test the speedrun mode (never had any luck!)

The speedrun mode is super fun and challenging to me, but nobody else seem interested in it. Besides asking on twitter I also contacted some of the notable VR speedrunners and people who has posted about VR speedrunning on Reddit, but got nothing out of it. If anyone reading this have a Vive and would like to try it, do let me know!

— Rune Skovbo Johansen (@runevision)

[#speedrunning]in[#VR]with[#HTCVive]? Anyone want to give the speedrun mode of[@eyeofthetemple]a go?[https://t.co/6g2WSQ2jnT][pic.twitter.com/MtVtMKdLC0][October 26, 2017]

### Implemented a new type of dangerous rooms for the temple

The reviews for this feature are through the roof.

Watch out! Working on a new type of danger in

— Rune Skovbo Johansen (@runevision)[@eyeofthetemple]...[#screenshotsaturday][#gamedev][#indiedev][#VR][#HTCVive][pic.twitter.com/95uYeL3b86][October 28, 2017]

It's getting tight in here.

— Rune Skovbo Johansen (@runevision)[@eyeofthetemple][#screenshotsaturday][#gamedev][#indiedev][#VR][#HTCVive][pic.twitter.com/Tvrd3OcWk2][October 28, 2017]

"What do you mean I have to get in there!?" New room in

— Rune Skovbo Johansen (@runevision)[@eyeofthetemple][#screenshotsaturday][#gamedev][#indiedev][#VR][#HTCVive][pic.twitter.com/7lE2iqorVD][October 28, 2017]

### Got serious working on the big level design overhaul

Still far from finished with this one.

I've been experimenting with using Unity Tilemaps as a digital replacement for pencil level design sketches. Some success so far, although I'm really missing rotation/flipping of selection and proper multi-selection.

— Rune Skovbo Johansen (@runevision)[pic.twitter.com/jT2PZloAYE][November 27, 2017]

I'm using

— Rune Skovbo Johansen (@runevision)[#unity3d]tilemaps for level design planning of multi-story structures. Moving things around becomes a pain though; having to do it separately for each layer. Any better alternatives?[pic.twitter.com/STSb8AarvB][December 29, 2017]

### Worked on a texture tool "Bricker" to easily create bricks and carved shapes

I've been continuing refining my tool for generating textures+normals from simple color masks. Output quality is getting there...

— Rune Skovbo Johansen (@runevision)[#gamedev][pic.twitter.com/jWzCUdc6Oz][December 11, 2017]

More on that in another post.

### Contracted a few pieces of concept art to get inspiration for improving the visual look of the game

I've had decent progress towards realizing the concept art vision for

— Rune Skovbo Johansen (@runevision)[@eyeofthetemple]. I'll put further work on that on hold for now and focus again on a level design overhaul.[#gamedev][#indiedev][#screenshotsaturday][#VR][#HTCvive][pic.twitter.com/csUc4C5o7p][December 23, 2017]

### And finally, introduced this little birdy

Bird spotted by the temple.

— Rune Skovbo Johansen (@runevision)[#gamedev][#indiedev][#VR][#HTCVive][#birds][pic.twitter.com/x8W7IRm54g][January 15, 2018]

That's it for now. Hope you enjoyed this glimpse into the development, and see you soon. Back to working on the game for me!

Remember you can also follow the development as it happens following [@EyeOfTheTemple](https://twitter.com/EyeOfTheTemple) or [@runevision](https://twitter.com/runevision) on twitter.