---
title: 'A VR Primer, via Prototype: Building Bouncing Babies VR in 72 hours'
url: https://www.gamedeveloper.com/audio/a-vr-primer-via-prototype-building-bouncing-babies-vr-in-72-hours
author: Charlie Deck
published: '2016-04-18'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# A VR Primer, via Prototype: Building Bouncing Babies VR in 72 hours

In preparation for this weekend's NYC VR Jam (and Ludum Dare), I cooked up a quick prototype that hit on several core VR game design issues. Here's what I learned building Bouncing Babies VR.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

### There has been a fire at the downtown children's hospital and the rooftop (why?) nursery is at risk! Catch the falling babies before they hit the asphalt in Bouncing Babies VR!

![](http://giant.gfycat.com/HarshAccomplishedKestrel.gif?width=600&auto=webp&quality=80&disable=upscale)


I finally got my HTC Vive and I couldn't wait to test out some VR concepts I saw at GDC. I chose this concept because it hits a number of core virtual reality game design issues:

Depth perception as a central game mechanic (catching falling babies)

Leveraging hand-eye coordination (throwing babies into ambulances)

Encouraging room-scale movement (scrambling around to catch babies)

Interacting with physical, diagetic mechanisms (difficulty slider, bat)

Eschewing HUD for diagetic data representations

A familiar, but not-uncanny self-consistent 360-degree environment including audio cues


![](../../assets/13e2bf0cb21aeaff.png)


Before getting into interaction issues, it's important to acknowledge that VR is demanding in terms of production values. The immersive effect of the headset makes presentation even more impactful than usual in gaming -- for better or worse. Self-consistency is central to making sure the environment is supporting the gameplay and not distracting from it.

Sound effects need to be placed in space. (No more audio sources on the main camera.) Things like reverb and attenuation are much more noticeable. The fire engine's rumble grows as you step towards it. The crackling fire is clearly in front of you. The babies have an audible ..waaAAAAAAA!!!! as they fall into your (capable) hands.

Uncanny valley effects are amplified in VR. Mixing high-end and low-poly objects is going to feel palpably weird. And motion characterizes your mobs. Body language seems to speak louder in VR. Even my simple box characters looked creepy when they weren't moving at all. They were still a little creepy in an idle state, just staring forward. Having the NPCs stare up at the fireman on the roof just barely crosses into plausibility. (Better would have been some varied behaviors, scratching of noses and heads, shaking head, turning to chat with neighbor.)

![](http://giant.gfycat.com/DistortedClassicAmethystsunbird.gif?width=600&auto=webp&quality=80&disable=upscale)


Physics is something that have to be up to snuff even more than usual. Making a difficulty slider that you could grab is pretty straightforward as long as you have your linear algebra is straight. Making babies fall as rigidbodies, and then attach to a glove, and then release as thrown, with plausible linear and angular momentum isn't too complex, but any bugs in that flow made the game feel horrible.


![](http://giant.gfycat.com/PeacefulSatisfiedBongo.gif?width=600&auto=webp&quality=80&disable=upscale)


HUD no more. My [last few](http://wordfireworks.com) [big projects](http://gradinggame.com) were super heavy on UI. Now, the UI is the world. There's no Iron Man HUD in Bouncing Babies. You're just there, in the street. But this is still a computer game. You can't shout up to the rooftop fireman to start. So in my game about catching babies thrown from rooftop fireman, you start the game by looking up at the fireman, thereby signalling you're ready. The fireman also shouts down instructions to you as the countdown progresses. It's a natural way to receive direction without asking someone wearing a headset to read a text popup.

I could have taken that principle further -- the "Look at the fireman to start the game!" could have been eliminated. Maybe a nearby NPC could urge the player to look up if they hadn't yet.


![](http://giant.gfycat.com/ImmaculateRealisticAmericanrobin.gif?width=600&auto=webp&quality=80&disable=upscale)


Instead of a score readout glued to the inside of your eyelid, there's a stadium scoreboard set up on the sidewalk. (I haven't quite figured out the narrative justification for that..) It features a stadium buzzer when you run out of time. That sound is an important touch - it clearly reads "game" and disarms some of the gross-out horribleness of, y'know, "bouncing" babies.


![](http://fat.gfycat.com/BlackSameDassie.gif?width=600&auto=webp&quality=80&disable=upscale)


In the few places where I felt text instructions were useful, they're placed in the world. So your eyes don't have to refocus on the point of interest. (Props to Riho Kroll of Crytek for bringing this up at GDC16.) I found that making them hover up and down slightly helped (for lack of a better term) naturalize them to the environment. It was clear that they weren't a structural element, but rather an informational graphic thing, like a projection.

A lesson from Job Simulator: disappear the controller-hand when manipulating an object. At GDC I got the impression that the reason for that was because it was difficult to create plausible animations of the hand representation griping a given object. Now I think it's because there's a mismatch between the expected orientation of an gripped object and the natural way the player holds the controller. It was natural enough for babies to land in your glove, but that same orientation didn't work for the other objects you can carry in the game. (I have no idea who put that baseball bat and sword in the street..)

One place I get into trouble with this game is physical safety. It's very tempting to push the bounds of your room-scale VR jail to reach for that baby. It's a good way to smack into a bookshelf or TV. And you'd better have your wrist straps on when you try to toss that baby into an ever-receding ambulance. Replacing that Vive controller isn't going to happen for a [i]long[/i] time (never mind your broken window.)

(Also, consumer room-scale VR is basically closet-scale VR. Isn't the smallest room-scale environment ~4 by 6 feet? You're not playing in the street, you're playing on one square of sidewalk pavement.)

Having non-VR control solution is crucial for testing. In the static screenshot above you can see that in action -- when active, it plays as a mouselook FPS. The mouse buttons made the hands grasp, and you could throw things around with your momentum by moving with WASD. I didn't have a great way to keep the two control rigs synced up 100%, but the aggravation was worth not constantly putting on the headset to iterate.

Also, as usual in Unity, you'll probably have to use some third-party tech of UI/text. In lieu of the currently-popular TextMesh Pro, I actually used NGUI -- it took a little hacking to cajole it into placing its elements into world space conviently -- but once done it was a cinch to whip up some dynamic graphical text and UX elements, such as the scoreboard, the starting countdown widget with circular progress bar, the text on the difficulty slider, and the rising notifications out of rescued (or...not rescued) babies.


![](../../assets/3d24d6c2ae2354a1.gif)


And of course this was a tribute to the 1984 MSDOS classic of the same name.

I'm still not sold that VR is that fun a thing to do more than a few minutes. So this game takes about three minutes per round. It's a great thing to pass around between friends. It is novel and you get a big wow and big laughs.

I feel good about how I spent the past few days. It's pretty fun and it looks OK! As someone who felt restricted to doing abstract programmer graphics a mere few years ago, I'm happy that I was able to repurpose some Asset Store goodies and combine with my own authored assets with my own to make a plausibly cohesive environment.

Whew. Now I'm ready for NYCVR Jam/Ludum Dare this weekend. Say hi if you see me at Sketchfab.

When Babies Collide...

![](http://giant.gfycat.com/MistyJoyousGrayreefshark.gif?width=600&auto=webp&quality=80&disable=upscale)


Full playthrough video:

Questions - comments welcome ~

bigblueboo[http://twitter.com/bigblueboo](http://twitter.com/bigblueboo)

and don't forget my [gif-a-day blog.](http://bigblueboo.tumblr.com)