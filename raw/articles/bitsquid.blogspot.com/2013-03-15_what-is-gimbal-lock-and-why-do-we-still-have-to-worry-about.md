---
title: What is gimbal lock and why do we still have to worry about it?
url: https://bitsquid.blogspot.com/2013/03/what-is-gimbal-lock-and-why-do-we-still.html
author: Niklas
published: '2013-03-15'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

If you have ever worked with rotations and Euler angles you are probably at least somewhat familiar with the phrase *"gimbal lock"*. But like many things concerning rotations, angles and spaces it can be tricky to visualize and get a good grasp of.

Sometimes it feels like every time I need to think about gimbal lock I have forgotten everything about it and have to go back the beginning and ask myself: OK, but what is it *really* that is happening?

Hopefully, this article will take care of that problem.

The [Wikipedia page](http://en.wikipedia.org/wiki/Gimbal_lock) shows how gimbal lock can happen in a mechanical system. But it isn't necessarily self-evident how this translates to the computer game world. In the computer there are no mechanical limitations, we can rotate an object however we like. How can anything be "locked"?

## Euler angles

When we are using [Euler angles](http://en.wikipedia.org/wiki/Euler_angles), we represent an object's orientation as three consecutive rotations around the object's axes. We can choose the axes and the order in which we apply the rotations arbitrarily, and depending on what we choose we get different Euler representations. So XYZ is the Euler representation where the first angle rotates the object around its X-axis, the second around its (new) Y-axis and the third around its (new) Z-axis. YZX gives us a different representation. We can even have representations with repeated axes, such as XZX.

So if we want to talk about the "Euler angles" of an object, we really must also talk about what axes we are rotating around and in what order. Otherwise we have no idea at all what we are talking about. Unfortunately, many articles about Euler angles are pretty sloppy with this and throw around terms like *yaw*, *pitch* and *roll* as if they had completely well-defined and unambiguous meanings. I prefer to use more wordy, but descriptive names, such as *euler_xyz[0]* that unambiguously state the axis rotation order and the index of the angle we are talking about.

An object has three rotational degrees of freedom and it is quite easy to see that the three Euler angles for a particular axis order (XYZ) are enough to define any possible orientation of an object. Note though that the representation is not unique. There are many possible Euler angles that represent the same orientation. For example, adding 360 degrees to any of the three angles will give us a different representation that results in the same object orientation.

So "gimbal lock" doesn't mean that there are rotations that can't be expressed as Euler angles. We can express any rotation in Euler angle form. Given an object, we can convert its orientation to Euler angles, and from that orientation we can rotate the object however we like and convert the new orientation to other Euler angles.

So what exactly is it that is "locked"? It seems we can do whatever we like.

## The "lock" in gimbal lock

The term "gimbal lock" comes from the mechanical world. If the problem had originated in the world of computers, it would probably have been called something less confusing, such as "Euler angle flip" or "coordinate singularity".

Because, in the computer world, there is really nothing that gets "locked". Instead, the problem is this: when the Euler angles have particular values, there are orientations that are very similar to the current orientation which can't be achieved by just making small changes to the Euler angles. In particular, this happens when one of the angles is at 90 degrees, so that two rotation axes coincide.

So even though the orientations are "close" in the real world, they are not close in the Euler representation. In fact, at least one of the Euler angles will have to flip 180 degrees in order for us to represent the new orientation.

So one of the angles have to flip? What is the big deal? Can't we just flip it and get on with our stuff?

We can, as long as the angles only represent instantaneous "snapshots" of the object's orientation. However, if the angles represent key frames in an animation and we want to interpolate between those key frames we run into trouble. If one of the angles flips 180 degrees between two key frames and we interpolate between those values, we will see the the object animating through all those 180 degrees. In the viewport, we will see the object doing a "flip" or "roll" that shouldn't be there.

Note that it is only the interpolation that creates this unwanted behavior. If we just displayed the actual key frames and didn't interpolate between them -- everything would look right. We could work in Euler angles as much as we liked and be as close to the gimbal lock position as we wanted and no-one would ever know.

So the only thing we need to fix to get rid of gimbal lock is the interpolation. If you have done any work with 3D graphics you probably already know the answer -- to use quaternions instead of Euler angles to represent angles. Quaternions don't have the weird singularity points that Euler angles have and we can interpolate between any keyframes by just lerping the quaternions.

It doesn't matter if the animation package is using Euler angles internally, as long as we convert everything to quaternions before we do the interpolation. Note that interpolation in quaternion space is not the same as interpolation in Euler space though, so to get as close as possible to what the animator intended, we probably want to sample the animation at our target frame rate and generate our quaternion key frames from those samples, rather than directly converting the animator's key frames (which may be further apart).

Well, there is one caveat actually. If we have more than 180 degrees of rotation in a single frame we can't represent that nicely with quaternions. Quaternions always lerp the shortest path between two orientations and you can't represent several "laps" of rotation with quaternions as you can do with Euler angles (by setting one of the angles to 9000 degrees, for example). But you can fix that by sampling at a higher frame rate if you need to represent really fast rotations with quaternions.

So with that we can say good bye and good riddance to Euler angles and never have to worry about their sorry gimbal locking asses ever again.

Or so you may think...

## The return of gimbal lock

I certainly thought so, until I started working on the new cutscene animation system for our level editor.

You see, animators really like to work with *curves*. They like to see a visual representation of what the animation will do to an object over time with key points that can be moved and handles that can be adjusted to change the slope of the curve.

![](../../assets/27abf18069657c14.png)


![](../../assets/27abf18069657c14.png)

Curves! Animators love them!

Quaternions are great for interpolation, but they are no good for curve editing.

Sure, you could probably draw some curves that represented a quaternion (the laziest thing would be to just draw the x, y and z components of the quaternion), but those curves wouldn't *mean* anything to an animator, the way the Euler angle curves do. They wouldn't be able to *do* anything with them.

So, animators want curves with keyframe interpolation. Curves need Euler angles. But what happens when we mix Euler angles with keyframe interpolation? Presto! Our old friend the gimbal lock is back again! Haven't we missed him.

That's it. We're stuck. Gimbal lock is here to stay and the animators will just have to work around it.

And we have to add support for all the usual tricks and workarounds that animators use to get around gimbal lock, such as changing the axis order (from XYZ, to XYZ, XZX or another of the twelve possible permutations), converting to quaternion and back again, applying an "Euler filter", etc.

But who said this game engine gig should be easy?

Quaternions actually *can* go the long way due to the double-cover. Here is a video explaining the details: https://mollyrocket.com/837


ReplyDeleteCheers

Julien

True, you can represent up to 720 degrees of rotation with a quaternion and if you take advantage of that you can handle rotations that are "twice as fast" before you need to increase the sampling frequency.

DeleteIsn't the curve issue just a GUI problem?


ReplyDeleteYou could display curves as Euler angles and convert everything to quaternions when exporting the level.

As you say the interpolations won't be exactly the same but it'll probably be forgiveable in 99% of the cases, and if you have some preview of the animation in the editor and they can see the final result, they can detect and work around those edge cases. I guess that's a conversation to be had with a technical animator.

By the way, very interesting blog, keep up the good work.

Cheers

If you mean that we should replace the artist hand-keyed Euler keyframes with quaternions, when we animate, then yes, the interpolation will be smooth, but it will look nothing like the curves the animator has drawn, so it will make the curve editor useless.


DeleteIf you mean that we should sample the Euler curves at 30 Hz and export that as our quaternion keyframes, then our quaternions will pretty faithfully (with some small error) replicate all the gimbal lock flipping problems that the Euler curves have, so nothing solved there either.

Use Quaternions! Lightweight, more precise for rotations and doesn't have the gimbal-lock syndrome! :D

ReplyDeleteAs I say in the article, I prefer quaternions too, but it doesn't work for animators, who want to see the animation data represented as curves.

DeleteWould the Angle-Axis representation have the gimbal lock issue ? If not, they could be used in the curve editor and have some meaning to artists, to be converted to quats for the engine. If yes, then this comment is useless :).

ReplyDeleteThey don't have any gimbal lock issues, but they are not nice to work with in a curve editor, so they are similar to quaternions in that way.

Deletevery interesting post!


ReplyDeletewhat would be involved in applying an "Euler filter"?

How about using spherical coordinates instead of Euler angles?

ReplyDeleteHere is my thought on this: It is entirely possible to avoid the gimbal lock by writing interpolation functions that always find the shortest way around the sphere (i.e. limit instantenous change in any angle to between 90 and -90 degrees). This can mean that "170 - 10 = -20", which can take a while to get used to, but the problem just disappears afterwards.



ReplyDeleteIf you, for some reason, want to sometimes have interpolations happen the long way around, then that information can not be recorded in instantenous angles, no matter what format you use. But it can be recorded by storing "change in angle" - essentially using same old euler angles or quaternions, but allowing them to go beyond 360 degrees, instead giving them an unlimited range in both plus and minus directions. These "delta angles" would not be computed from plain angles, but instead used for editing and running animations (or possibly for very fast spinning objects in physics). Adding a delta angle to a plain angle produces a new angle, but you lose the information about what happens "between frames" if you do that.

Euler angles, quaternions, and matrices are equally powerful for representing orientation, but for some of them it's just more intuitive how to write algorithns that avoid some common problems.

Did you finally find a solution?

ReplyDeleteYour website is really cool and this is a great inspiring article. Best Vlogging Gopro Gimbals Review


ReplyDeleteWOW! I Love it...


ReplyDeleteand i thing thats good for you >>

Life Style รวมเกล็ดความรู้

Thank you!

ฝันว่าตัดผม ดีไหม? หมายความว่าอะไร?"

ReplyDelete



ReplyDeleteแทงบอล 168

เกมใหม่ภาพสวย แจ่ม!!

wtf is "lerp"?

ReplyDeleteHello, we have a game to recommend.



ReplyDeleteทางเข้า ufabet

ufabet kick

รูเล็ตสายฟ้า

แทง บอล ผ่าน มือ ถือ

กา บอล1

Thank you for your interest."

Your tips on productivity were exactly what I needed. I’m feeling more motivated already!

ReplyDelete