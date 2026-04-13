---
title: Why do mirrors reverse right and left but not up and down?
url: https://divisbyzero.com/2010/02/04/why-do-mirrors-reverse-right-and-left-but-not-up-and-down-2/
author: Dave Richeson
published: '2010-02-04'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

[I apologize to those of you who have been reading my blog for more than a year. I’m reposting [something I wrote last year at this time](https://divisbyzero.com/2009/01/24/why-do-mirrors-reverse-right-and-left-but-not-up-and-down/). I was then, and am now, teaching Calculus III, and we just finished discussing the cross product. I ended the conversation by telling my classes how the cross product helps us answer the question: why do mirrors reverse right and left but not up and down?]

Stand in front of a mirror and hold up your right hand. The person standing in the mirror holds up her left hand. Why is that? Why does a mirror reverse left and right? After all, it does not reverse up and down.

Before we answer that question, we have to ask a more basic one: what is “the right”?

Looking for an answer, I turned to the venerable [Oxford English Dictionary](http://dictionary.oed.com/) (subscription required). I was disappointed to discover that the OED does not give a definition of the term “right”! Instead it gives the circular path shown below.


Right

17.a.=[RIGHT HAND]2.

Right hand

2. a.The right side.b.The direction towards the right. =[RIGHT]n.1

“Right” and “left” are a slippery concepts that are hard to define. In fact, you need to know other things about an object before you can determine its right and left. For example, if I handed you a blob-like sea creature and asked you which side is its right side, you may not be able to answer me. If I told you where the top and front sides of the critter were, then you could quickly identify the right side.

Here’s a mathematical explanation of what you would be doing mentally. Take the coordinate axes shown below, point the z-axis out of the top of the creature and the y-axis out its front, then the x-axis will point to its right.

If you are familiar with vector operations in ![coordsys coordsys](../../assets/2932c600a69f2d6b.jpg)


.


“**Right equals front cross top**“

The three directions, top, front, and right are mutually perpendicular and that if you know two of them, you know the third. For a person, a car, an animal, etc, the top and the front are unambiguous and intuitive. Then we use them to determine which side is the right side.

Now let us go back to the mirror. What does it really reverse? If you raise your arm, your reflection raises her arm. If you stick your right arm out to the side, the reflection sticks an arm out in that same direction. However, if you point **at** the mirror, then the reflection points in the opposite direction—she points back at you. In other words, **the mirror reverses front and back**!

Here’s where things start going wrong. Your brain does not have to do any work to recognize the top and front sides of your reflected image. Then it uses them to calculate your reflection’s right side. More specifically, your reflection’s z-axis points in the same direction as yours, but her y-axis points in the opposite direction (yours points into the mirror and hers points out). Consequently, if we use the xyz-coordinate system above, her x-axis points in the opposite direction as yours. Thus your right arm corresponds to her left arm, and we perceive the mirror reversing left and right.

Here another way to describe what is happening. The xyz-coordinate system shown above is often called a *right-handed coordinate system* because if you take your right hand, point your fingers in the x-direction and curl them in the y-direction, then your thumb will be pointing in the z-direction. What a mirror truly does is changes a right-handed coordinate system into a left-handed one—that is to say, the reflection of a right-handed system is a left-handed system. When we look into a mirror, our brain, which is accustomed to using a right-handed coordinate system to tell right from left, errs because the mirror world actually has a left-handed coordinate system.

When we see words in a mirror, they look like they are written from right to left, but that is because we are imposing our right-handed coordinate system on a left-handed mirror world.

I’ll end this post with some assorted thoughts about the left and the right.

- One thing that occurred to me while writing this post is that we treat different objects differently. Suppose I was holding a piece of paper out in front of me with my two hands and you were facing me. If I told you to point to the right hand side of the paper, then to point to my right hand, you would point to two opposite sides of the paper! There are certain objects (people, animals, cars, boats, etc.) in which right and left refer to the right and left sides
**from the objects’ perspective**. However, there are other objects (pieces of paper, buildings, etc.) in which you use**your right and left side**to reference it. I assume this has to do with whether we can mentally substitute ourselves in place of the object—we can do that with other living things or with vehicles in which we can ride, but not inanimate objects like a piece of paper. - Perspective is important. As a child, I was always confused about where right field was on a baseball diamond. Is it on the batter’s right or on the fielders’ right?
- It is no wonder that so many people confuse their right and their left. They have to compute a cross product in their head each time.
- It is a good thing that right and left are relative quantities, otherwise cars driving in opposite directions on a two-way road, both driving on the right-hand side would be in the same lane!
- I just came across these
[two](http://www.sciam.com/blog/60-second-science/post.cfm?id=drivers-med-rearview-mirror-sans-bl-2009-01-19)[articles](http://www.philly.com/inquirer/health_science/weekly/20090112_A_nice_reflection.html)about[Andrew Hicks’](http://www.drexel.edu/coas/math/people.asp?lname=Hicks&fname=R.)work with mirrors.

“After all, it does not reverse up and down.”

I like to point out that a mirror on the ceiling (or floor) *does* reverse up and down.

Yes, good point. But such a mirror doesn’t reverse front and back. Thus it still reverses right (= front x top).

Yes — is there a way to orient a mirror that reverses top and front and not right/left?

What a mirror is doing is reflecting light with respect to the surface normal at the point the photon hit it (the surface normal is the cross product of the two vectors that describe the plane of the mirror). Since we have depth perception we will see the reflected light as coming from beyond the mirror, even though it is coming from behind us. The mirror really does just invert the viewing frustum. Nothing is different. Nothing is on a different side.

So if it doesn’t actually reverse left and right, why does our brain think it does? We see a person in the mirror and our brain assumes its another person looking at us. That’s when one’s mind’s sense of depth perception plays tricks on one’s sense of direction. Since our brain is saying that person is looking at us, we think that left and right directions are different when they’re not. In other words, we just confuse ourselves because we’re not used to mirrors! Our visual system never evolved to take a mirror into account. So we have to learn it. That’s why when we’re driving and some one puts on a turn signal and we see it in the mirror, we know that they are still turning in the same direction as the side of the car their turn signal was blinking. It’s the same psychology that makes driving a car backwards awkward at first.

Then why do images and letterings appear backwards? I’m glad you asked. When one looks at the writing in a mirror one expects its orientation to change just like one thinks a person (who is mostly symmetric, while text is not) is facing the other direction. Automatically, one reads it backwards. Normally, the text’s right is on one’s left. If one is holding the text so they are facing the same way, it will appear backwards.

It’s the same reason everything on a storefront window display looks backwards once one is inside the store. If you were out side the store and looking in and there was a mirror inside reflecting the writing in the window, it would be perfectly readable to you in the mirror as well as in the window. If you were in between the window and the mirror, you could read the writing in the mirror, but the writing in the window would be backwards to you. “Ambulance” is written out backwards, not just so that one can read it in you rear view mirror, but so that if the ambulance were transparent you could read the “backwards writing” in its front from behind the vehicle with the text oriented the right way.

Aren’t mirror’s wonderful!?

The mirror does not reverse front and back. The mirror presents a two dimensional image. Not having any third dimension, it does not have a front or a back.

A mirror does not reverse anything, our minds do this assuming the image is that of another person in front to us.

@DerekSmith A mirror may practically be 2d dimensional, but it reflects light that encodes three dimensional information. That’s why one can look in a mirror and still focus on objects as though they were much further in front of oneself (even though in reality they’re behind you).

@Dave Richeson I wrote you back on your comment @ my blog entry. Sorry for not being clear with that last statement. I was just augmenting your point.

A mirror doesn’t reverse anything imagewise.

You see “left” and “right” based on where the photons come from in relation to each other and your eye.

The photons from your right hand still come from the right. The photons from your left hand still come from the left.

It’s when a human stands between you and the mirror, then

turns aroundto face you, that their hands reverse and the photons from their right hand come from your left, and so forth. If the human instead stood on their head to face you, then they would be reversing up and down. But a mirror, which reverses nothing, doesn’t do that.Or write something on a transparency. Hold it up so you can read it directly, then do the same thing standing in front of a mirror. You can read it directly in the mirror. It hasn’t been reversed at all. Now reverse it so it “faces” the mirror. You will see it backwards in the mirror, now, because you reversed it.

addendum: …or flip the transparency forward, so it faces the mirror. Now you see it upside down, because you turned it upside down.

Is there a simple answer to the question “Why do mirrors reverse right and left but not up and down?” that everyone could understand without having to go to an online dictionary every two seconds?

I am grateful for the serendipity that brought me to your website. My son had realized that his image in our mirror was not the one other people saw. And wondered if there were ‘true reflection’ mirrors. Thany you for carrying the ‘Light of Truth’, Mathematics. Arne Leon

There’s no mind tricks involved really, I guess the light just stays in the same direction.

The image may flip, but you have to think about how we actually get to see reflections in mirrors in the first place…

Light travels from somewhere and hits your face.

Now imagine that your face has been ‘imprinted’ on that wave of light.

That light bounces off your face, then into the mirror, then back to your eyes.

As it comes back, the image is still the same way around as it was when it first ‘imprinted’ your face.

This image is what you see, reflecting back.

There’s more scientific ways of describing it, but that is essentially all that happens :)

I came here for an extra school question last year. Oh if only John Mirren had posted then.

This is very well explained but again confuses making use of the “right handed” coordinate system.

It can be either a left-handed one or a right-handed one. But, the same type is to be used in both the instances.

So, the conclusion is that whatever hand you use for defining the cross product, use the same all over!!

just turn the mirror upside down duh!