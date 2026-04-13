---
title: 'Opinion: Animations Without An Animator'
url: https://www.gamedeveloper.com/art/opinion-animations-without-an-animator
author: Szymon Swistun
published: '2011-08-30'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

[In this reprinted [#altdevblogaday](http://altdevblogaday.com/)-opinion piece, November Software co-founder Szymon Swistun shares how his studio created a motion capture setup for under $1,500, using PS Eye Cameras and iPi Desktop MC.] We needed to author around 70 animation sequences for 4 characters without an animator. I watched a bunch of character key frame animation video tutorials, and found out quickly that manually authoring human motion is a lot of work. So, we looked into motion capture to help generate the base foundation of our animations. We wanted to have the flexibility of authoring our own unique motions and were not happy with the quality of using motion databases. Another option was to record our own motions using other studios, but the cost was too high. After hitting many walls, we finally stumbled upon iPi Desktop Motion Capture software. Trial Run After downloading the free version, we setup a trial run and purchased the following:

3 PlayStation Eye cameras @ $30 each

3 Camera tripods @ $30 each

1 USB2 hub @ $10

2 USB2 10 ft. extensions @ $6 each

1 Maglite Mini for calibration @ $20

Tape @ $0, used some from home


![](http://gamesetwatch.com/jonas-kick-mocap.jpg?width=1280&auto=webp&quality=80&disable=upscale)


iPi Mocap Jonas Kick Test

Results were pretty good, not great. You can see how the motion is represented but not perfectly. Calibration process takes a bit of processing time, but it is mostly automatic. Once calibrated, we captured a bunch of video of motions that are then taken to be tracked with their studio software. Tracking quality was okay and missed around faster, more complex motions, but they provide a nice ability to pause the tracking, pose, fit, and track backwards from a known pose state and fix up most issues.

![](http://gamesetwatch.com/iPi-Studio-Calibration-Results-1024x337.jpg?width=1280&auto=webp&quality=80&disable=upscale)


iPi Studio Calibration and Kick Test Result

3DS Max Work Once we had the motions tracked well, we applied jitter removal to smooth them out, and exported them into 3DS Max. After applying the motion on our rigs, thus getting re-targeted, basic fix-up was required to get working well in game. Those include:

Set the timeline to intended animation frequency; we use 60 frames per second.

Manually delete keys around foot plants and set plant keys; instead lock the feet to the ground/

Add a layer animation for head tracking, matching captured video.

Fix up hands to work with intended props either manually, or using a layer.

Also, accent the animation with a layer for any specific styles, fix-ups, or exaggerations, and to match the video capture motions more accurately if needed.

For cyclic animations, use the Mixer / Motion Flow to create a cyclic transition to the same animation. Some manual work here required to get the right cycle working. Clip the animation to the intended boundaries.

For movement-less actions, delete X and Z root key frames. Recently, we moved this step to our own internal export and retain the root motion to move our physics representation in game instead.


Final Setup The results worked seamlessly in game, and we decided to upgrade to the standard package and get a six-camera 360 degree studio setup to improve capture quality and get more range of motion. We use a quad core Intel i5 with a nVidia 480 GTX, and it works fine with a six PS Eye camera setup as long as you have three separate USB2 controllers each that can take two USB2 PS Eye cameras plugged in at full performance. We additionally purchased:

Standard Edition iPi Desktop Motion Capture software for $995

3 more PS Eye cameras @ $30 each

Two 3-meter-tall light stands instead of tripods for 2 cameras to get them higher @ $30 each

4 PS3 USB2.0 4.7-meter-long repeaters @ $10 each

1 more USB2.0 hub @ $10

$15 table and two $10 dollar chairs for some added comfort.


![](http://www.gamesetwatch.com/110829-mc-1.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Yes, the software is marker-less, but we found we got much better results the funkier we dressed ;). Also, having one or two people there to help critique the motions, run the machine, and provide endless jokes is super helpful. With the new machine setup, we can capture a session of motions in around 15 minutes, and it usually takes about out hour to track and fix up around six motions with a session. Then each motion takes another 30 minutes to an hour to refine in 3DS Max and get working in-game. The total amount we spent for doing our motion capture, including the wacky clothes from Target, is $1,462. Keep in mind we already had 3DS Max and a computer built to handle the capture and processing efficiently. The end result is that we have been able to author all of our crazy motions and sequences using our actual physical actions, and stylize them them in 3DS Max without too much hassle. It would be great to hear from others with experience in animation workflows and motion capture processing with 3DS Max and Motion Builder. Feature Requests for iPi

Head tracking

More then one person capture

Faster calibration and tracking ( consider SLI / CrossFire support ), ideally real-time

Improved tracking quality, fine if more markers on actors would help

Improved Studio controls like Maya camera movement, better timeline snapping, better rotation widgets, and import custom models with rigs into display

Direct connect real-time motion capture viewing into 3DS Max and Motion Builder

Virtual Camera tracking rig

Face expression tracking rig


[This piece was reprinted from [#AltDevBlogADay](http://altdevblogaday.com/), a shared blog initiative started by [@mike_acton](http://www.twitter.com/mike_acton) devoted to giving game developers of all disciplines a place to motivate each other to write regularly about their personal game development passions.]