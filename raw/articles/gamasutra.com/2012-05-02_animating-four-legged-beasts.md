---
title: Animating Four-Legged Beasts
url: https://www.gamedeveloper.com/art/animating-four-legged-beasts
published: '2012-05-02'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Animating Four-Legged Beasts

Animator Cathy Feraday Miller shares her techniques for animating quadrapeds in walk and run states, presenting both reference materials and her own animations in various states of completion.

May 2, 2012

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Author: by Cathy Feraday Miller

[Animator [Cathy Feraday Miller](http://www.rocket5studios.com/about/), who has worked on major feature films and video games, shares her techniques for animating quadrapeds in walk and run states, presenting both reference materials and her own animations in various states of completion.]

Animating animals is usually fun, but can often be complicated and technical. Figuring out what to do with all those legs can really trip up an animator. We can animate human-shaped characters a lot easier than multi-legged beasts because we have an intuitive knowledge of the way bipeds move.

It is easy for an animator to act out a motion when the character moves like us; feeling the action 'in the body' helps us understand how to animate it. So what happens when the character is a quadruped and you don't have that intuitive feel at your disposal? How do you make that movement believable? Suitable reference and a sophisticated media player is the place to start.

Luckily for the animation community, there is a wealth of reference material that can help. I'll walk you through my process for animating quadruped locomotion and share classic references that will help you deconstruct the fundamentals of the four gaits: walk, run, trot and gallop. I'll also share an example of my own 3D walk animation and offer technical tips for creating believable quadruped locomotion cycles.

# Getting Started

With a media viewer that can scrub single-frame backwards and forwards, like [QuickTime](http://www.apple.com/quicktime/), you can watch the movement frame by frame. Drawing thumbnail images with directional notes helps you synthesize the information.

There are now lots of websites out there that put up live-action animal footage, such as the [Rhino House](http://www.rhinohouse.com/) human and animal locomotion website, which has a built-in player that can scrub their video reference material (click the image below to check out their website and viewer). Thanks to the internet, finding reference and getting into it to see what is going on is the easy part. The hard part is converting that information into something that makes sense to the animator and for the character that is to be animated.

![](../../assets/3773717e264a5094.img)

[Horse Locomotion Walk 30](http://www.rhinohouse.com/MotionTools.aspx?mode=tools&itemid=1648) courtesy of [www.rhinohouse.com](http://www.rhinohouse.com/)

Following a process speeds up your workflow. Before I get into the creative part of animating, I usually have all of my research done. Gathering and absorbing all of the technical details and reference material beforehand frees me up to get into the creative flow of animating, with easy access to my reference material. My process is something like this:

1. Consider what animal most closely resembles the beast I need to animate.

2. Search for reference material. Here are the sources I find useful:

Life drawing and observation

Video capture


3. Analyze the reference material and find the section of the footage that is most useful

4. Create thumbnail drawings to assist with my animation, including notes on direction and any unusual qualities I can see in footage.

5. Animate

# The Four Gaits

In the course of my career, I've learned that there is a surprising similarity in how quadrupeds move, from species to species. Eadweard Muybridge's photographic works may be a century old, but they are still relevant and extremely useful.

In his introduction to Animal Locomotion, he maintains that most quadrupeds -- be they dogs, cats, horses or rhinoceroses -- follow the same footfall pattern. This is the order in which the hooves or paws strike the ground while moving through the various gaits. Where they differ is in the flexibility of the spine. Visualize a rhino running, as opposed to a cheetah. The exceptions, according to Muybridge, are elephants, and animals like kangaroos.

The four speeds of movement, or the four "gaits", are shared amongst most four-legged animals. Almost every quadruped walks, trots, canters and gallops, and their legs move in the same manner when they do it.

As you can see in the image below, adapted from Muybridge's Animal Locomotion, the gaits have been broken down into symbols illustrating which leg strikes the ground in which order, assuming the animal is facing north with the right legs on the right and the left legs on the left.

For example, with the rotary gallop gait, if you start your cycle with the left rear foot striking the ground first, the next in sequence to hit the ground would be the right rear foot, then the right fore foot, followed by the left fore foot.

As for the transverse and rotary gallops, I've found the rotary gallop more often in reference material than the transverse, which I've mainly seen in horse footage. The canter is the roughest gait, with a lot of up-and-down movement. Elephants don't seem to follow these rules, and should be considered separately.

![](../../assets/9e784890b9462291.img)


image adapted from: Animal Locomotion, [Eadweard Muybridge](http://en.wikipedia.org/wiki/Eadweard_Muybridge), 1887

Once you get the legs moving roughly in the order that is appropriate, you can be creative with the rest of the body.

To save time, you could animate a "vanilla" gait cycle for each gait with the leg movements blocked in on keys and breakdowns only and the body and head having the rough up-and-down motion laid in on those keys. If using a universal rig, this file could then be exported onto any beast (with minimal adjustments, depending on the disparities of beast shape) and be used as a starting point for the animations.

Several different types or speeds of walks could also be created from this base file simply by playing with the amount of frames in the animation and the distance between the legs in the stride position or the distance the beast travels in the 'leap' part of the gallop.

# The Walk

In the case of the walk gait, the rear left foot strikes first, followed by the left foreleg. The rear right leg strikes third, with the right foreleg falling last. The walk is the slowest gait, and is shared by all quadrupeds. Muybridge breaks down this information into a chart for the walk, trot, canter and gallop gaits in the introduction of Animal Locomotion. Converted into a graphic table, a walk cycle would look like this:

![](../../assets/c0b9896fc4083c9f.img)


image adapted from: Animal Locomotion, Eadweard Muybridge, 1887

Horses are great animals to study because their legs are so long and slender, creating an easily legible silhouette. Below is an example of a walk cycle broken down into 8 phases:

![](../../assets/3f46dd9b6c77f97d.img)


Image adapted from [Horse Locomotion Walk 01](http://www.rhinohouse.com/MotionTools.aspx?mode=tools&itemid=1619), courtesy of [www.rhinohouse.com](http://www.rhinohouse.com/) (Click for larger image)

Once you understand what the feet are doing, it becomes easier to understand what to animate next. Think of the quadruped walk as two offset human walk cycles. I wonder how often studios have used two people in a horse costume for motion capture? Preston Blair's iconic walk cycle with the "stride" and "passing" key positions is a great illustration of the basics of a biped walk demonstrating the following: fall into the stride and recover and rise up into the passing position.

![](../../assets/5a4c06d52d67d09a.img)


Adapted from Preston Blair, Animation, 1948

For the quadruped, the hips and chest become two offset "bouncing balls" in the same manner as the hips in a bipedal walk. Consider circled image 23 from the horse walk cycle (below), which shows the forelegs in the "stride" position and the hind legs in the "passing" position. I've added circles to show the up and down motion of the hips and chest in that phase of the movement. The head could then be animated as yet another bouncing ball, offset from the hips and chest (follow-through! overlap!)

![](../../assets/0a75036d8376abde.img)


Image adapted from [Horse Locomotion Walk 01](http://www.rhinohouse.com/MotionTools.aspx?mode=tools&itemid=1619), courtesy of [www.rhinohouse.com](http://www.rhinohouse.com/)

# Animating A Walk

To illustrate this locomotion in 3D animation, I've roughed in a slow 40-frame walk cycle. Cycles must be symmetrical, or there will be a visible hitch in the walk, like a limp, or a hit in the animation.

![](../../assets/b379ede044df381e.img)


JoJo character, courtesy of [Rocket 5 Studios](http://www.rocket5studios.com/). Watch the animation by clicking [here](http://youtu.be/vbnGQYjPEoU).

There are almost as many methods of animating as there are animators, but I prefer to approach posing as I would with 2D, or classical, animation. Posing out the whole character, rather than starting with the hips or isolating the lower body, and working on the entire character at once when creating the four major poses.

Details like toes and tails can be ignored or turned off at this stage. I create the four major keys or poses of the walk: two stride and two passing. I make them as symmetrical as possible, but they don't have to be mathematically the same.

There is an advantage to keying all major elements on the same frame. At this point, the keys can be slid around easily to change the timing of the walk. It is quick and easy to adapt and manipulate your cycle by figuring out your basic timing to the point where you start to add finishing details like overlap and follow-through. Keys arranged in an orderly fashion are really easy to manipulate in your 3D software package (here I am using the dope sheet in Maya 2011).

![](../../assets/ce199d6cd15620b2.img)


Four key poses, JoJo walk, property of [Rocket 5 Studios](http://www.rocket5studios.com/) (Click for larger image)

This is also the break off point where different kinds of walk cycles can be created now that the feet have been appropriately positioned. Variety can be added, like floppy overlap or stealthy sneak. The four basic poses can also be used as a starting point for other walks. You don't have to recreate the four basic key poses; you only have to adapt them to your specific purposes. Use the graph editor or tweak by hand, but remember to have each opposite pose match each other.

![](../../assets/9dbe2c58ee6bf3df.img)


JoJo walk cycle, four keys only, with smooth spline interpolation. Watch the animation by clicking [here](http://youtu.be/zfZpQqNSySk).

It is important that your software has a great graph editor. When animating cycles, I spend a fair amount of time cleaning up the graph to get symmetrical movement. Don't forget to check all channels! The above video has been carefully tweaked to remove all hits and holds. The stage just prior to this revealed a few errors with the arms:

![](../../assets/4bf79d0839578e6b.img)


JoJo with wonky arm movement. Watch the animation by clicking [here](http://youtu.be/R2Eez0lfcWA).

There are several ways to fix errors like this but the easiest for me at this stage is to look at the graph editor and find out where there is a problem with the curve.

![](../../assets/78c7072f8f989955.img)


Note: flat tangents causing slowdown at apex of movement. (Click for larger image)

The highlighted motion trail shows other problems that can be solved by the graph editor, such as the linear movement of the arm in the air. Arcs always look more natural than linear paths of action. The solution for the slowdown in the forward progression of the arm is to fix the curve so that it can cycle smoothly, as seen below.

![](../../assets/f4355011698f0b01.img)


Grab spline handles and move them so that curve looks like it can cycle or repeat. (Click for larger image)

The next step is to flesh in the walk, adding overlap and follow-through, offsetting the head and making sure there is enough weight in the up and down movements of the hips and chest. When you are pretty sure the cycle is working the way you want it to, animate the feet, hands, fingers and toes. I usually animate the tail last, one rotational axis at a time.

![](../../assets/c818d511e4a011d3.img)


JoJo walk from side view, tail and toes added. Watch the animation by clicking [here](http://youtu.be/g8i48TwZGiw).

# Walks and Runs: In Brief

Walks and runs can be considered a controlled fall with a little acceleration happening right after the passing position, which is similar to a push-off. As with all movement cycles, the forward or Z-translation would be non-linear.

The speed of the walk is dictated by the length of the legs and how far apart the feet are planted in the stride position. There isn't really a moment where all four legs are off the ground, as in the other gaits, and the legs can only move so fast without looking "sped up". Conversely, the speed of gallop is largely determined by the shape and unique qualities of the beast. The faster you need the beast to go, the more flexible the spine will have to be, and the greater the squash and stretch. Look for this when watching reference. As the legs bunch up under the beast (the squash) energy is gathered, preparing for a "leap" or "stretch" where the animal can cover as much ground as its form, weight and strength allow. The tighter the squash, the more extended the stretch and the faster the beast can travel.

![](../../assets/0b282fd2a5eea6af.img)

[Gallop cycle](http://www.youtube.com/watch?feature=player_embedded&v=7cQvlIkKayQ) animated by [Paul Capon](http://paulcapon.wordpress.com/) on [Nico](http://www.creativecrash.com/maya/downloads/character-rigs/c/nico)

Variety in the weight or "attitude" of the walk, trot, or gallop can be achieved through the shape and movement in the spine and the amount of overlap and follow-through. The amount of flexibility and motion in the spine is key to defining the differences between a horse, a rhino, and a jungle cat.

Personality, the key ingredient in any good animation, comes not only from the shape of the key poses but also from what is happening in between the poses. How the character gets from stride to passing can define the character. Are they high-stepping? Straight forward and no-nonsense? Whimsical? Are they flopping around like a puppy or are they hard and densely muscled like a pit bull? The overlapping elements that you've added to the animation and their follow-through shows the audience who the character is and what it is made of.

![](../../assets/69313bbe850f62e4.img)


Image adapted from [Tiger Locomotion Gallop 01](http://www.rhinohouse.com/MotionTools.aspx?mode=tools&itemid=449), courtesy of [www.rhinohouse.com](http://www.rhinohouse.com/)

![](../../assets/7fe373b7aef19842.img)


Image adapted from [Horse Locomotion Gallop 05](http://www.rhinohouse.com/MotionTools.aspx?mode=tools&itemid=1551), courtesy of [www.rhinohouse.com](http://www.rhinohouse.com/)