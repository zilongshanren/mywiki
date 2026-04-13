---
title: Best practices using the PS4 Dualshock controller speaker
url: https://www.gamedeveloper.com/audio/best-practices-using-the-ps4-dualshock-controller-speaker
author: Rev Dr Bradley Meyer
published: '2015-04-06'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Best practices using the PS4 Dualshock controller speaker

The controller speaker in the Playstation Dualshock 4 can be an effective way to communicate information to the player. Rev. Dr. Bradley Meyer, audio director at Sucker Punch, provides some tips and tricks to make it work well.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

The controller speaker in the Dualshock 4 is pretty damn cool, though it's by no means the first of its kind. The Wii Remote famously had a speaker in it which was used occasionally. The archery and fishing sounds from Twilight Princess were the first time I really noticed its use. In the Wii version of Spider-man Web of Shadows we played Spider-man's web flings out of it. It was a fun novelty, but not the best quality speaker. The Wii U has not one, but two speakers! Stereo sound on a controller. Now that's awesome! (or possibly overkill). The PS4 DualShock controller has a single speaker, but it's a nice quality one (the same as the Vita speakers). In my time playing with it, I've come up with a set of best practices I would like to share. I think these concepts apply to the Nintendo controller speakers as well, and probably any environment where you have a "special" speaker close to the player, yet separate from the normal sound field:

Mind the (Latent) Gap

The Dualshock 4 controller connects via bluetooth and with bluetooth comes inherent latency. For this reason, you really shouldn't try synching the controller speaker with the game speakers. It just won't work consistently well. Maybe it will one time out of a hundred, but every other time, it's going to be off by some amount, which can be a little disorienting. The discrepancy between the timing of the controller speaker and game speakers is fine for more amorphous sounds, but for anything the player needs sample accurate cognition of (like critical dialogue) choose one or the other. There are some really cool techniques you can do with dialogue, which I'll touch on further down.

Treat it like an LFE

The LFE channel of a surround system is commonly known as the subwoofer (the speaker it plays out of), but LFE itself stands for Low Frequency Effect. The key word here being "Effect." If you're constantly hitting the sub with sounds, not only does the mix start to feel muddy and fatiguing, but you also dilute the power of the LFE's intended purpose: to emphasize key, special moments or events. I strongly believe the controller speaker should be used in the same manner. Make sure what you're sending through it has purpose and reason. Generally speaking the best sounds to send through it are UI/notification sounds and "first person" sounds, or those that make sense to the player when they emanate directly in front of him/her instead of in the landscape of the room speakers. By no means are these the only categories of sounds you can use the speaker controller for, but it's good practice to ensure you're not breaking immersion through its use (unless of course that's your intention).

Avoid using it for critical sounds

As designers, there are a lot of unknown factors we need to consider when deciding what to pump through the controller speaker. Listening environments vary greatly and sometimes the noise of a child crying, a dishwasher running, or a friend yammering endlessly about how awesome they are can completely overshadow the sounds coming through the controller speaker. Furthermore, users can adjust the speaker volume in the system menu, and while there are now ways to query that volume and ideally use that information to determine whether to route a sound through the controller speaker or the main mix, it bears considering that sounds you want to emanate from the controller speaker may not be heard by the player. For this reason, I recommend not using it for any critical sounds that the player absolutely must hear. Whether or not you follow this advice, always design a contingency plan for any controller sounds you want to ensure the player hears. If they're using headphones, if the controller is turned down, etc. In a perfect world, the PS4 would know via its HDMI connection what the audio setup of the user currently is (headphones, stereo, 5.1, etc.), and with a microphone attached to the system, we could be sampling the ambient noise of the room and adjusting the mix dynamically [as Rob Bridgett suggested in his recent GDC talk on adaptive loudness.](http://issuu.com/newbayeurope/docs/ami_march_2015_digital/17) If these two concepts were achieved, the engine could determine when to send your controller sounds to the controller speaker and when they need to be diverted to the main mix instead. But until we get there, have a plan in place for controller sounds the user must absolutely hear.

![](http://2e130c55e0c2763c8a20-c7a4d0feffd26319b59c92c4aecae366.r18.cf1.rackcdn.com/61db506ce32f7bbf7fb9a358e0f6ac856e86479b.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Be creative!

The speaker controller is a fun tool and can really add an extra level of immersion beyond the normal mix. We received a lot of positive feedback for our use of it in inFAMOUS Second Son: from the ball shakes of the graffiti can to the way we used it for draining powers (the drain sound started at the source of the power in the world and slowly moved into the controller speaker as Delsin absorbed the power), and there's tons of other developers out there doing neat stuff with it. I loved how Transistor played the narrator's voice through it (only if you select to use the speaker in the options menu), but still sent the reverb sends to the main mix. It created a fantastic sense of your sword intimately talking to you, but still being in the world (and by only having the dry mix go through either the mains or the controller they avoided the sync issues of sending the VO through both). The Last of Us Remaster did a similar feature with their audio logs. Shadow of Mordor had a great example of a first person notification in playing a bush rustle sound whenever the player would enter high grass. It helped communicate to the player that they were in cover using an in-world sound rather than a possibly-immersion-breaking UI sound. The bush rustle sound also brings up one last point: while it is a decent quality speaker, it's still a small speaker in a plastic housing, best to keep it relegated primarily to mid and higher frequencies.

Perhaps we need to give the speaker controller a fancy acronym akin to LFE to help explain its best uses, something like Personal Mid-to-High-Frequency Effect (PMtHFE). Although that's more syllables than "speaker controller," so let's just remember to use it wisely.