---
title: Shooting animations in Awesomenauts
url: http://joostdevblog.blogspot.com/2012/09/shooting-animations-in-awesomenauts.html
author: Joost van Dongen
published: '2012-09-08'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com), the player can shoot while walking, standing still, jumping, falling and sliding. How to make animations for this?

![](../../assets/9da8135858467b5e.jpg)

The first idea might be to simply make an animation for each combination. This means animating both walking+shooting, walking+sliding, walking+jumping, etc. This is a lot of work, especially since in the console version of Awesomenauts, characters need to be able to shoot in 5 different directions. That is just a lot of animations.

And that is not even the worst of it. The real issue is that this doesn't actually work. The player can shoot

*at any moment in time*. This means that shooting can start at any point during another animation, not just at the start of an animation. So if the player is already halfway through his current walking animation, then the walking+shooting animation will not connect. Either the shooting has to be delayed until the walking animation has finished, or the feet will shuffle every time the player shoots (which in most games is very often). Both are unacceptable, as shuffling is ugly, and delaying destroys the responsiveness of the controls.

The common solution to this problem, is to split the upper and lower body and animate them separately. However, as I explained in

[last week's blogpost](http://joostdevblog.blogspot.nl/2012/08/making-2d-characters-aim-in-all.html), our character designs were not very fit for that. And since Awesomenauts is a 2D game, we also don't have any bones to do animation blending on parts of the body, as is commonly done in 3D games.

So we had to be more creative. We came up with a combination of a couple of techniques. Our solution is somewhat hacky and weird, but I am pretty happy with the result, and the amount of time it took to make was quite acceptable.

Our solution on console consists of two parts. The most visible part is the shoot effect. Whenever the player shoots, an effect is played at the position of his gun. This effect usually contains a light flash and particles, as is very common when shooting in any game. The trick here is that we exaggerate these shoot effects to compensate for that the character's body itself is not playing an animation when shooting.

From there our artists took this even further: some shoot effects contain body parts that are drawn on top of the character. This essentially means that the gun of a character might be visible double during the shooting, but since it goes so fast, the double is not really noticeable (unless you read this blogpost and start looking for it). The recoil animations this makes possible look much more natural and powerful.

The other part of our solution in the console version of Awesomenauts is that we skew the entire character based on his shooting direction. Skewing is a rather crude effect to apply to an entire character, and looks horrible in slow-motion, but when seen at the speed of the actual game, it actually looks like a recoil effect and looks pretty good. Depending on the shooting direction, we also sometimes squash the character instead of skewing him.

![](../../assets/4ef10af983172be3.gif)

*This video shows how the combination of a shoot effect and a skew works out in the console version of Awesomenauts, both at normal speed and in slow motion.*

This technique works fine for the short burst that each shot is, but doesn't work for some of the longer skill animations. Here we got lucky: most of those don't allow the player to walk while performing them, and many don't have specific aiming either. Clunk's Bite skill is a nice example of this, and was thus pretty straightforward to animate.

The most difficult one here is Lonestar's grenade throw. He can charge this while moving around, and throwing requires an animation in the arm. Luckily, our artists came up with a really simple solution to this: they animated him with his feet of the ground, as if jumping to throw that grenade. This works fine both when Lonestar is in the air, and when he is on the ground. Similarly, Yuri's skills are animated with his jetpack turned on, also resulting in his feet being off the ground. Note that when looking really closely, solutions like this might not look perfect. However, when actually playing, they look totally fine, so I think this was a pretty smart solution from our art team.

*A couple of examples of how some of the longer animations simply use a jumping pose to solve the problem of mixing the animation with free movement.*

While reading this, you might have noticed that I am constantly talking very specifically about the console version of Awesomenauts. This is because on PC, we separated the arms from the body (as I explained in

[last week's blogpost](http://joostdevblog.blogspot.nl/2012/08/making-2d-characters-aim-in-all.html)), and that suddenly makes it a lot easier to do some proper animation while shooting. So on PC, characters have proper recoil in their arms while shooting. Most characters also still have their skewing animations, and the combination of gun recoil, shoot effects and skewing looks great, in my opinion.

*Some examples of shooting animations in the PC version of Awesomenauts, where arms are separate objects and can thus have proper recoil animations.*

For the moment this is the last blogpost in this short series on animation in Awesomenauts. I would like to get back to this topic later, to talk about our tool chain and the way in which our artists create animations, but for the coming weeks I have some much more exciting topics to pester you with. I have some cool footage coming up of a cancelled

[Ronimo](http://www.ronimo-games.com)project (in my opinion a lot cooler than the previously discussed

[Monstertruck VS Zombies](http://joostdevblog.blogspot.nl/2011/11/monster-truck-vs-zombies-cancelled.html)). And, even more exciting:

**next week I will announce the new hobby-project I am working on!**My new hobby project is the weirdest thing I have worked on so far, so be sure to check out it's reveal next week! ^_^

I noticed the change in recoil on the PC after your last post on the changes to aiming on PC; they are really, really well done. The combination of all of these techniques make it look really slick, and it's pretty impressive. You guys are pretty modest!

ReplyDelete"hide it with particles" - haha, I've lost track of the number of times I've come to that conclusion too! I'm loving this series of blog posts. This is the kind of thing people just don't realise goes on, and I love that you're talking about it in this detail. I suspect people would recommend 2D over 3D a lot less if they knew about the kind of hackery they'd need to do to make things look nice :)

ReplyDeleteYeah, I guess in the end the thing is that high quality is always a lot of work, both in 2D and in 3D. However, making something with the kind of detail that Awesomenauts has, would be at least double the work in 3D...

Delete