---
title: A Brain Dump of What I Worked on for Uncharted 4 | Ming-Lun "Allen" Chou |
  周明倫
url: https://allenchou.net/2016/05/a-brain-dump-of-what-i-worked-on-for-uncharted-4/
author: Allen Chou
published: '2016-05-10'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

![Uncharted 4 logo](../../assets/14a2905199ef08a4.jpg)


This post is part of [My Career Series](http://allenchou.net/my-career/).

本文之中文翻譯[在此](http://allenchou.net/2016/05/a-brain-dump-of-what-i-worked-on-for-uncharted-4-chinese/)

Now that [Uncharted 4](https://en.wikipedia.org/wiki/Uncharted_4:_A_Thief%27s_End) is released, I am able to talk about what I worked on for the project. I mostly worked on AI for single-player buddies and multiplayer sidekicks, as well as some gameplay logic. I’m leaving out things that never went in to the final game and some minor things that are too verbose to elaborate on. So here it goes:


### The Post System

Before I start, I’d like to mention the post system we used for NPCs. I did not work on the core logic of the system; I helped writing some client code that makes use of this system.

Posts are discrete positions within navigable space, mostly generated from tools and some hand-placed by designers. Based on our needs, we created various post selectors that rate posts differently (e.g. stealth post selector, combat post selector), and we pick the highest-rated post to tell an NPC to go to.

![posts](../../assets/6dedd9182817c809.png)


### Buddy Follow

The buddy follow system was derived from [The Last of Us](https://en.wikipedia.org/wiki/The_Last_of_Us).

The basic idea is that buddies pick positions around the player to follow. These potential positions are fanned out from the player, and must satisfy the following linear path clearance tests: player to position, position to a forward-projected position, forward-projected position to the player.

![follow-request](../../assets/b890455102210746.png)


Climbing is something present in Uncharted 4 that is not in The Last of Us. To incorporate climbing into the follow system, we added the climb follow post selector that picks climb posts for buddies to move to when the player is climbing.

![climb-post](../../assets/95a5df91ab76c442.png)


It turned out to be trickier than we thought. Simply telling buddies to use regular follow logic when the player is not climbing, and telling them to use climb posts when the player is climbing, is not enough. If the player quickly switch between climbing and non-climbing states, buddies would oscillate pretty badly between the two states. So we added some hysteresis, where the buddies only switch states when the player has switched states and moved far enough while maintaining in that state. In general, hysteresis is a good idea to avoid behavioral flickering.

### Buddy Lead

In some scenarios in the game, we wanted buddies to lead the way for the player. The lead system is ported over from The Last of Us and updated, where designers used splines to mark down the general paths we wanted buddies to follow while leading the player.

![lead-spline](../../assets/697301b97306856b.png)


In case of multiple lead paths through a level, designers would place multiple splines and turned them on and off via script.

![multiple-lead-splines](../../assets/cf587f16734b9ad5.png)


The player’s position is projected onto the spline, and a lead reference point is placed ahead by a distance adjustable by designers. When this lead reference point passes a spline control point marked as a wait point, the buddy would go to the next wait point. If the player backtracks, the buddy would only backtrack when the lead reference point gets too far away from the furthest wait point passed during last advancement. This, again, is hysteresis added to avoid behavioral flickering.

We also incorporated dynamic movement speed into the lead system. “Speed planes” are placed along the spline, based on the distance between the buddy and the player along the spline. There are three motion types NPCs can move in: walk, run, and sprint. Depending on which speed plane the player hits, the buddy picks an appropriate motion type to maintain distance away from the player. Designers can turn on and off speed planes as they see fit. Also, the buddy’s locomotion animation speed is slightly scaled up or down based on the player’s distance to minimize abrupt movement speed change when switching motion types.

![speed-planes](../../assets/b2458ca4f9d2a405.png)


### Buddy Cover Share

In The Last of Us, the player is able to move past a buddy while both remain in cover. This is called cover share.

![tlou-cover-share](../../assets/5e969b0a21d5efad.png)


In The Last of Us, it makes sense for Joel to reach out to the cover wall over Ellie and Tess, who have smaller profile than Joel. But we thought that it wouldn’t look as good for Nate, Sam, Sully, and Elena, as they all have similar profiles. Plus, Uncharted 4 is much faster-paced, and having Nate reach out his arms while moving in cover would break the fluidity of the movement. So instead, we decided to simply make buddies hunker against the cover wall and have Nate steer slightly around them.

![cover-share](../../assets/5cbac2eb3e009abd.png)


The logic we used is very simple. If the projected player position based on velocity lands within a rectangular boundary around the buddy’s cover post, the buddy aborts current in-cover behavior and quickly hunkers against the cover wall.

![cover-share-debug](../../assets/393d4af64330154f.png)


### Medic Sidekicks

Medic sidekicks in multiplayer required a whole new behavior that is not present in single-player: reviving downed allies and mirroring the player’s cover behaviors.

![medic-revive](../../assets/c134560f2ec08863.png)


Medics try to mimic the player’s cover behavior, and stay as close to the player as possible, so when the player is downed, they are close by to revive the player. If a nearby ally is downed, they would also revive the ally, given that the player is not already downed. If the player is equipped with the RevivePak mod for medics, they would try to throw RevivePaks at revive targets before running to the targets for revival (multiple active revivals reduce revival time); throwing RevivePaks reuses the grenade logic for trajectory clearance test and animation playback, except that grenades were swapped out with RevivePaks.

![medic-revivepak](../../assets/7e7d0dcfb2bf6894.png)


### Stealth Grass

Crouch-moving in stealth grass is also something new in Uncharted 4. For it to work, we need to somehow mark the environment, so that the player gameplay logic knows whether the player is in stealth grass. Originally, we thought about making the background artists responsible of marking collision surfaces as stealth grass in Maya, but found out that necessary communication between artists and designers made iteration time too long. So we arrived at a different approach to mark down stealth grass regions. An extra stealth grass tag is added for designers in the editor, so they could mark the nav polys that they’d like the player to treat as stealth grass, with high precision. With this extra information, we can also rate stealth posts based on whether they are in stealth grass or not. This is useful for buddies moving with the player in stealth.

![stealth-grass](../../assets/1322f88c6e96b313.png)


### Perception

Since we don’t have listen mode in Uncharted 4 like The Last of Us, we needed to do something to make the player aware of imminent threats, so the player doesn’t feel overwhelmed by unknown enemy locations. Using the enemy perception data, we added the colored threat indicators that inform the player when an enemy is about to notice him/her as a distraction (white), to perceive a distraction (yellow), and to acquire full awareness (orange). We also made the threat indicator raise a buzzing background noise to build up tension and set off a loud stinger when an enemy becomes fully aware of the player, similar to The Last of Us.

![threat-colors](../../assets/490d30b3758200dd.png)


### Investigation

This is the last major gameplay feature I took part in on before going gold. I don’t usually go to formal meetings at Naughty Dog, but for the last few months before gold, we had a at least one meeting per week driven by [Bruce Straley](https://twitter.com/bruce_straley?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor) or [Neil Druckmann](https://twitter.com/Neil_Druckmann?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor), focusing on the AI aspect of the game. Almost after every one of these meetings, there was something to be changed and iterated for the investigation system. We went through many iterations before arriving at what we shipped with the final game.

There are two things that create distractions and would cause enemies to investigate: player presence and dead bodies. When an enemy registers a distraction (distraction spotter), he would try to get a nearby ally to investigate with him as a pair. The closer one to the distraction becomes the investigator, and the other becomes the watcher. The distraction spotter can become an investigator or a watcher, and we set up different dialog sets for both scenarios (“There’s something over there. I’ll check it out.” versus “There’s something over there. You go check it out.”).

In order to make the start and end of investigation look more natural, we staggered the timing of enemy movement and the fading of threat indicators, so the investigation pair don’t perform the exact same action at the same time in a mechanical fashion.

![staggered-investigation](../../assets/fe87e870aba418da.png)


If the distraction is a dead body, the investigator would be alerted of player presence and tell everyone else to start searching for the player, irreversibly leaving ambient/unaware state. The dead body discovered would also be highlighted, so the player gets a chance to know what gave him/her away.

![dead-body-highlight](../../assets/832c1327b1bcb78c.png)


Under certain difficulties, consecutive investigations would make enemies investigate more aggressively, having a better chance of spotting the player hidden in stealth grass. In crushing difficulty, enemies always investigate aggressively.

### Dialog Looks

This is also among the last few things I helped out with for this project.

Dialog looks refers to the logic that makes characters react to conversations, such as looking at the other people and hand gestures. Previously in The Last of Us, people spent months annotating all in-game scripted dialogs with looks and gestures by hand. This was something we didn’t want to do again. We had some scripted dialogs that are already annotated by hand, but we needed a default system that handles dialogs that are not annotated. The animators are given parameters to adjust the head turn speed, max head turn angle, look duration, cool down time, etc.

![dialog-look](../../assets/68a8caaa2c56c459.png)


### Jeep Momentum Maintenance

One of the problems we had early on regarding the jeep driving section in the Madagascar city level, is that the player’s jeep can easily spin out and lose momentum after hitting a wall or an enemy vehicle, throwing the player far behind the convoy and failing the level.

My solution was to temporarily cap the angular velocity and change of linear velocity direction upon impact against walls and enemy vehicles. This easy solution turns out pretty effective, making it much harder for players to fail the level due to spin-outs.

![jeep-momentum-maintenance](../../assets/cf147bca10622913.png)


### Vehicle Deaths

Driveable vehicles are first introduced in Uncharted 4. Previously, only NPCs can drive vehicles, and those vehicles are constrained to spline rails. I helped handling vehicle deaths.

There are multiple ways to kill enemy vehicles: kill the driver, shoot the vehicle enough times, bump into an enemy bike with your jeep, and ram your jeep into an enemy jeep to cause a spin-out. Based on various causes of death, a death animation is picked to play for the dead vehicle and all its passengers. The animation blends into physics-controlled ragdolls, so the death animation smoothly transitions into physically simulated wreckage.

![bike-ragdoll](../../assets/7af81a51395245b5.png)


For bumped deaths of enemy bikes, we used the bike’s bounding box on the XZ plane and the contact position to determine which one of the four directional bump death animations to play.

![bike-obb](../../assets/b66a0b69c6d24708.png)


As for jeep spin-outs, the jeep’s rotational deviation from desired driving direction is tested against a spin-out threshold.

![jeep-spin-out](../../assets/3f11139143a66a2a.png)


When playing death animations, there’s a chance that the dead vehicle can penetrate walls. A sphere cast is used, from the vehicle’s ideal position along the rail if it weren’t dead, to where the vehicle’s body actually is. If a contact is generated from the sphere cast, the vehicle is shifted in the direction of the contact normal by a fraction of penetration amount, so the de-penetration happens gradually across multiple frames, avoiding positional pops.

![bike-sphere-cast](../../assets/21bdf96959d5e3fa.png)


We made a special type of vehicle death, called vehicle death hint. They are context-sensitive death animations that interact with environments. Animators and designers place these hints along the spline rail, and specify entry windows on the splines. If a vehicle is killed within an entry window, it starts playing the corresponding special death animation. This feature started off as a tool to implement the specific epic jeep kill in the 2015 E3 demo.

### Bayer Matrix for Dithering

We wanted to eliminate geometry clipping the camera when the camera gets too close to environmental objects, mostly foliage. So we decided to fade out pixels in pixel shaders based on how close the pixels are to the camera. Using transparency was not an option, because transparency is not cheap, and there’s just too much foliage. Instead, we went with [dithering](https://en.wikipedia.org/wiki/Dither), combining a pixel’s distance from the camera and a patterned [Bayer matrix](https://en.wikipedia.org/wiki/Ordered_dithering), some portion of the pixels are fully discarded, creating an illusion of transparency.

![dithering](../../assets/7b23700240b408be.png)


Our original Bayer matrix was an 8×8 matrix shown on [this Wikipedia page](https://en.wikipedia.org/wiki/Ordered_dithering). I thought it was too small and resulted in banding artifacts. I wanted to use a 16×16 Bayer matrix, but it was no where to be found on the internet. So I tried to reverse engineer the pattern of the 8×8 Bayer matrix and noticed a recursive pattern. I would have been able to just use pure inspection to write out a 16×16 matrix by hand, but I wanted to have more fun and wrote a tool that can generate Bayer matrices sized any powers of 2.

![bayer-matrix](../../assets/2141a93601c9f76e.gif)


After switching to the 16×16 Bayer matrix, there was a noticeable improvement on banding artifacts.

![dithering](../../assets/573caf13c350b38a.png)


### Explosion Sound Delay

This is a really minor contribution, but I’d still like to mention it. A couple weeks before the 2015 E3 demo, I pointed out that the tower explosion was seen and heard simultaneously and that didn’t make sense. Nate and Sully are very far away from the tower, they should have seen and explosion first and then heard it shortly after. The art team added a slight delay to the explosion sound into the final demo.

### Traditional Chinese Localization

I didn’t switch to Traditional Chinese text and subtitles until two weeks before we were locking down for gold, and I found some translation errors. Most of the errors were literal translations from English to Traditional Chinese and just did’t work in the contexts. I did not think I would have time to play through the entire game myself and look out for translation errors simultaneously. So I asked multiple people from QA to play through different chapters of the game in Traditional Chinese, and I went over the recorded gameplay videos as they became available. This proved pretty efficient; I managed to log all the translation errors I found, and the localization team was able to correct them before the deadline.

### That’s It

These are pretty much the things I worked on for Uncharted 4 that are worth mentioning. I hope you enjoyed reading it. 🙂

Hi! Thanks for sharing these tips, really interesting to read! I was wondering if you could quickly explain the “desired tension” and “current tension” that we can see in some of the screen printings?

Current tension determines the current player move set and soundtracks. There is an extra desired tension because the game needs to wait for the current soundtrack to reach a valid transition point before switching to the desired tension.

fascinating – thank you for sharing.

I’m glad that I followed you since Flash era, AWESOME!

Awesome stuff. Really great to know all that, I was actually curios about the buddy system while playing the game. Also the best part of the game was stealth using grass, I just loved that new addition to the game, and now that I know how it was implemented it seems even more interesting.

Uff as a beginner game programmer this is mind blowing thanks for sharong this.

Awesome post and awesome work! Thanks!

I remember watching that E3 demo and specifically thinking, “ohman, they even got that sound delay right for the explosion.” It definitely made a difference in impressing me. Great work!

Truly something to be proud of, this game is by far the most polished I’ve ever seen. It’s very interesting to see the thoughts and efforts that contribute to something so epic. Keep up the great work.

Thanks for your hard work on an amazing game.

Thanks for all of your work, and thanks for the very detailed write up. I thoroughly enjoyed it.

Can you go into more detail on the post system? I’m curious how it was auto generated. What sort of criteria was used and how did the AI query it. How did you blend designer placed posts with auto generated ones? Did posts get parented to existing props in a prefab like way?

Thanks in advance.

As a nav mesh is loaded into a level, posts are generated across the nav mesh. There are criteria like path distance, exposure, cover direction, character blockage, etc. An NPC uses a post selector that utilizes a set of criteria to rate posts, and the NPC picks the best-rated post. Designer-placed posts are loaded separately and added to the same pool of posts, and they are treated equally. Posts get parented to the same parent object the corresponding nav mesh is parented to.

Pingback: One Man's Amazing Contribution To Uncharted 4 | News, Games, and Reviews

This is an awesome post, very interesting, thank you!

Amazing read, thx

Not sure if you were involved in these moments but something that been immersion breaking somewhat for me in the scripting sequences are when you swing down using the rope, then the AI member joins you afterward… yet you never throw the rope back in anyway. If you turn the camera quickly enough you do see them do some unnecessary dangerous jump to the stationary rope, and its just kinda silly.

Was there ever a time when nathan had an animation where he got the rope back to the AI guy after swinging?

Sweet Jesus man- you just read a massive article about 3/4 of the things this singular man did for the game and you’re concerned about a slight immersion break (that only occurs if you’re looking for it )? Just enjoy the game bro, and compliment the man for his amazing work.

Cheers.

Thank you for this!

As a big fan of uncharted games, and a Taiwanese, I really admire and envy you can work in this great company. It is encouraging when I read your articles. Thanks for sharing.

Pingback: Here's What Uncharted 4 Looks Like To The Developers | Kotaku Australia

Pingback: An In-Depth Understanding of the Physics of Uncharted 4, Simplified – ASidCast

在 gamasutra 看到這文 :). I’ve noticed that your work seems to cover a wide range of expertise, physics simulation, graphics, AI behavior, animation, etc. Which seems uncommon in a larger studio like naughty dog, is this common in the studio?

Yes. We don’t have specific titles and do whatever is needed.

Hey, thanks for the article, very interesting.

Could you go more implementation specific about use dithering for fade out pixels? Cause I can’t wonder how this works (uses discard operation at the end?).

Thanks in advance.

For a 16×16 Bayer matrix, you have 256 pixels, obtained by populating the pixels with one of each values between 0 and 255 divided by 256, so the matrix is “normalized” (all pixel values are within the [0.0, 1.0) interval).

Define a distance before the camera near plane that you would like to start fading out pixels, say 1.0 meter for convenience, saving the trouble of normalizing pixel distance from the near plane.

For a pixel located at (x, y) in screen space, compute its distance from the camera near plane. If it’s between 0.0 and 1.0 (meter), then compare the distance with the sampled value of the Bayer matrix at (x % 16, y % 16). If the distance is less than the sampled Bayer matrix value, then you discard the pixel.

I hope that answers your question.

Oh I see, thanks for the explanation.

I can’t wait for testing this in-game, hopefully I will on weekend 🙂

This is one of the first things that really caught my eye when playing the scuba section, as I was swimming through the plants. I’ve never seen it done so elegantly. Really great work and inspiring read!

Why transperency is not cheap?

Because transparency involves alpha blending and some form of z-sorting, whereas dithering just involves z-buffer look-up and comparison against a Bayer matrix look-up.

Pingback: A Brain Dump of What I Worked on for Uncharted 4 via /r/gamedev | KyleHarrison.ca

Thanks, really interesting read!

This is some great work. Thanks for sharing!