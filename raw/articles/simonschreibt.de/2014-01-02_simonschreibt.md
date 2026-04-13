---
title: Simonschreibt.
url: https://simonschreibt.de/gat/tomb-raider-laras-hot-secrets/
author: Simon
published: '2014-01-02'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Once more a [Tomb Raider](http://www.tombraider.com) game is starring the beautiful [Lara Croft](http://en.wikipedia.org/wiki/Lara_Croft) – featuring outstanding and huge visuals which make it easy to stare and get lost like watching flames. In fact, this *is* todays hot topic: Flames! Or let’s say: **a** Flame.

Don’t tell Lara but I read in her diary and can proudly present the three hot secrets of Lara Crofts torch:

Hot Secret I

Seamless Fire Animation

**5. March 2013**

Dear diary, today i was in an ancient grave and found a torch! I named it “Mr. Magma” ’cause he has a beautiful flame! I never saw such a lovely fire before…it is made out of a pre-rendered loop-able texture animaton:

![](../../assets/bdf41220c9e2215d.jpg)

[Tomb Raider](http://www.tombraider.com)

It is not easy to create such a texture! The renderer can simulate fire **but** you can’t tell it like “simulate fire in 32 frames but please make the first and last frame fit so i can loop it”. An engraving told me the solution: They took the last frame twice and blended in the new frame with 50% transparency:

![](../../assets/07725d24e64690b4.gif)


– Lara

Hot Secret II

Non-breakable fire stream

**10. March 2013**

Ouch! Today i slipped and was sliding down a hill very fast…but guess what: Mr. Magmas fire **wasn’t** interrupted through the fast movement like when using a standard particle system where not enough particles are generated. Do you remember the great game Silver? I love it! It came in my mind as an example for the fast-torch-movement-with-particles-difficulty:

![](../../assets/c23429d768a842f9.gif)

[Silver](http://en.wikipedia.org/wiki/Silver_%28video_game%29)

Do you see the gaps between the single particles? This doesn’t happen with Mr. Magma because the creators of his fire used a subdivided plane which stretches and deforms when its moved (and is always faces at me, how thoughtful of it!):

![](../../assets/65fa77a2cbc67763.jpg)

[Tomb Raider](http://www.tombraider.com)

See how fast the torch can be moved without breaking the fire stream:

![](https://www.data.simonschreibt.de/gat046/blog_tr_fast_movement_01.gif)

[Tomb Raider](http://www.tombraider.com)

I spent the rest of the day wagging Mr. Magma but now we both have to go to bed and sleep a bit.

– Lara

Hot Secret III

Angle-Independent Fire


Today a guy with hat and whip was staring at me from an upper cliff. At first i thought he was looking at my … necklace but then i realized that he focused on Mr. Magma. He was impressed because normally you see the plane-“fake” very well by looking from above. Here an example! From the famous Company of Heroes:


Source:


**15. March 2013**Today a guy with hat and whip was staring at me from an upper cliff. At first i thought he was looking at my … necklace but then i realized that he focused on Mr. Magma. He was impressed because normally you see the plane-“fake” very well by looking from above. Here an example! From the famous Company of Heroes:

![](../../assets/ece0cecf3cb34f87.gif)

[Company of Heroes](http://www.companyofheroes.com)![](../../assets/fb84dc6d201ab7fc.gif)

*But even if you look directly from above on my magic torch you don’t see any plane. This is because the plane fades out depending on the viewing angle*

Isn’t that beautiful? So much effort for a single torch…oh by the way, i don’t know why but i’ve the feeling that someone is sniffing around in the camp and reads you…i’ll keep an eye on that. You’re my precious!


– Lara

**and**then a standard particle system fades in! If you look closely you can see how the both components get exchanged.Isn’t that beautiful? So much effort for a single torch…oh by the way, i don’t know why but i’ve the feeling that someone is sniffing around in the camp and reads you…i’ll keep an eye on that. You’re my precious!

– Lara

![](../../assets/0b1996542ccfe9d0.gif)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

Thanks. Makes you appreciate the game even more. You can also tell from the animations that they put a lot of love into this game. Like when she walks close to a wall she starts holding her hand against it to support herself. Awesome.

Really? I have to check this! Yeah besides of the NPC-Characters (your team) and some Quicktime Events it was a really great game. Impressive Levels, great Design and cool Weapons :)

Great breakdown, I love these articles! Do observers complain when they watch you play a video game for the first time?

No, not really. :D On the one hand i don’t play too often with observers. On the other hand i recognize most times pretty fast that there’s something special about a detail/fx…i note it down and look deeper into it later. Or people give me hints that some stuff is looking really interesting and then i look deeper into it (when i own the game). But i guess we game-devs look at games differently anyway. I bet all other graphic artists and coders stand sometimes minutes in a corner of a game and looking at some details too :D

really cool. but how did you get the sprite sheet?

There are different ways to get some insight-view. Sometimes i have to use performance analyzing tools, sometimes the data lays (compressed) in the game directories already or sometimes i have to use mod tools to get to the core of the game :D Sometimes it takes really really long time and without the help of other people it’s often not possible to get all infos i need.

loved it.

keep it up :)

Thx man :,)

I just wanted to say thank you for the great compliments on the fire I made for Lara. Your sleuthing skills are pretty incredible I have to say! Its always nice to have your work appreciated, and with such description!

Cheers

Mike

Hi Mike, it’s an honour to have you here! Thanks for your comment! You guys did an awesome job with the new TR-Game. Oh and i would have a question about the fire: In one of the first cutscenes, the fire of the torch touches the cave ceiling and therefore the fire is spreading on/along the ceiling. Was this only made for the cutscene? Because i tried to reprodroduce this effect in the normal game (be holding the torch near the ceiling of a room) and nothing happened.

Oh Fire! The paramount of game effects ;D

I love the blend-out / blend-in particles thing for when looking on top of the flame!

True these animation sheets can look convincing for a moment but actually I’m a fan of simple particle based fire. As it could be much more dynamic. It can go out and be lit anywhere without looking duplicated.

The movement interaction is still a problem tho. Sure real simulation could work in a way but what I thought could work already is emitter attributes dynamic to the motion of the emitter. That is:

* lifetime: max when emitter still – goes down when emitter in motion

* emission rate: low when emitter still – goes up when emitter in motion

* emission dir: tilts towards motion direction

Yes that’s right. With such an dynamic solution it could be posible to hit the sweet spot between great particle fire and performance. By the way, there’s a great PDF about how the burning villa in Uncharted 3 was made. Really interesting read (Slide 70, but the whole thing is just crazy awesome): http://www.gdcvault.com/play/1015898/The-Tricks-Up-Our-Sleeves

This is really cool. I’m still not a fan of that bending, wiggling plane – the stretch effect just looks far too strange, and reminds me of glitching in games – but that top down particle fade is excellent. Gave me a new appreciation for a system I’ve largely been against. Thanks!

I’m happy you like the blending as i do :) Yes the stretching can look strange under extreme conditions but hm … personally i prefer it to a standard particle system where gaps would occur. Have to try it out in real world – how a torch behaves while doing such movements :D Now i write about it i realize, that i never had a real torch in my hands … :,(

Hi Simon, just stumbled upon this site and wanted to say thanks to you and all the participating devs, some very interesting information and techniques are discussed here in impressive detail. Great work! Reading these articles definitely makes you appreciate all the care, attention to detail and clever wizardry put into these awesome games even more. Anyway, keep up the good work and I will surely be following this site actively! Now off to read some more Game Art Tricks:)

Glad to hear you like the site. Thanks for taking the time to write me a comment :) It’s always the best motivation to keep it up. I hope you liked the other GATs too. :)