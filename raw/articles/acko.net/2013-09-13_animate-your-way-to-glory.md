---
title: Animate Your Way to Glory
url: https://acko.net/blog/animate-your-way-to-glory/
author: Steven Wittens
published: '2013-09-13'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![Animate Your Way to Glory](../../assets/9c73d31024cb84d8.jpg)

# Animate Your Way to Glory

## Math and Physics in Motion

“The last time that I stood here was seven years ago.”

“Seven years ago! How little do you mortals understand time.

Must you be so linear, Jean-Luc?”

*Note: This article is significantly longer than previous instalments. It features 4 interactive slideshows, each introducing a new tool as well as related concepts around it. In one way, it's just another math guide, but going much deeper. In another, it's a thesis on everything I know about animating. Their intersection is a handbook for anyone who wants to make things move with code, but I hope it's an interesting read even if that's not your goal.*

Developers have a tough job these days. A seamless experience is mandatory, polish is expected. On touch devices, they are expected to become magicians. The trick is to make an electronic screen look and feel like something you can physically manipulate. Animation is the key to all of this.

Not just any animation though. Flash intros were hated for a reason. The `<blink>`

tag is not your friend, and flashing banner ads only annoy rather than invite. If elaborately designed effects distract from the content, or worse, ruin smoothness and performance, it'll turn people off rather than endear. Animation can only add value when its fast and fluid enough to be responsive.

It's not mere polish either, a finishing touch. Animation–and UI in general—should always be an additional conversation with the user, not a representation of internal software or hardware state. When we press Play in a streaming music app, the app should respond immediately by showing a Pause control, even if the music won't actually start playing for another second. When we enable Airplane Mode on our phones, we don't care that it'll take a few seconds to say good bye to the cell tower and turn off the radio. The UI is there to respond to our wishes: it should act like a personal assistant, not a reluctant helper, or worse, a demanding master.

Hence animation is visual language and communicates both explicitly and implicitly. It establishes an unspoken trust and confidence between designer and user: we promise nothing will appear, change or disappear without explanation. It can show where to find things, like an application that minimizes into place in the dock, or a picture sliding into a thumbnail strip. It can tell miniature stories, like a Download button turning into a progress bar turning into a checkmark. More simply just the act of scrolling around a live document, creating the illusion of viewing an infinite canvas, persisting in space and time. Here, page layout is the use of placement and style to denote hierarchy and meaning in a 2D space.

As with any conversation, tone matters, in this case expressed through choreography. Items can fade into the background or pop to demand our attention, expressing calm or assertiveness. Elements can complement or oppose, creating harmony or dissonance. Animations can be minimalist or baroque, ordered or parallel, independent or layered. The proper term for this is *staging*, and research shows that it can significantly increase our understanding of diagrams and graphs when applied carefully. Whenever elements transition, preferably one at a time, it is easier to gauge changes in color, size, shape and position than when we are only shown a before and after shot.

This is important everywhere, but especially so for abstract topics like data visualization and mathematics. When we have no natural mental model of something, we build our understanding based on the interface we use to examine it. The more those interfaces act like real objects, the less surprising they are.

In doing so, we replace explicit explanations with implicit metaphors from the natural world: distance, direction, scale, shadow, color, contrast. These are the cues our brains evolved to be excellent at interpreting. By imbuing virtual objects with these properties, we make them more realistic and thus more understandable. Mind you, this is not a call for *skeuomorphism*, far from it. The properties we are seeking to mimic are far more basic, far more important, than some faux leather and stitching.

The clearest example of this has to be inertial scrolling. Compared to an ordinary mouse wheel, scrolling on a tablet is actually much more complicated. We can flick and grab, go as fast or slow as we want. When skimming through a list, often we never wait for the page to stop moving, in theory requiring more effort to read. Yet everyone who's seen a toddler with an iPad can attest to its uncanny ease of use and efficiency, offering improved control and comprehension. Our brains are very good at tracking and manipulating objects in motion, particularly when they obey the laws of physics: moving with *consistent inertia and force*.

Which brings me to the actual topic of this post: how animation works on a fundamental level. I'd like to teach a mental model based on physics and math, and how to precisely control it. Along the way, we'll come to understand why Apple built a physics engine into iOS 7's UI, reveal some secrets of the demoscene, compose fluid keyframe animations, and defeat the final boss: seamless rotation in 3D. In doing so, we'll also go beyond just visual animation. The techniques described here work equally well for manipulating audio, processing data or driving meatspace devices. In a world of data, animation is just a different word for *precise control*.

## A Matter of Time

An animation is something that *changes over time*. As it so happens, these three humble words are a veritable Pandora's box of mathematics. They open up to the strange world of the continuously and infinitely dividable, also known as *calculus*.

In a [previous article](https://acko.net/blog/to-infinity-and-beyond/), I covered the origins of calculus and how to approach the concept of infinity. In what follows, we won't be needing it much though. We'll be working with finite steps throughout, with *discrete* time. This makes it vastly easier to understand, and is an eminently useful stepping stone to the true theory of continuous motion, which you can find in any good physics textbook.

Math class hates it when we just punch numbers into our calculator instead of deducing the exact result: a decimal number is meaningless on its own. On that, I can agree. But when we punch in a couple thousand numbers and look at them in aggregate, it can tell us just as much. This page will be your calculator.

We've seen how to examine an animation at multiple levels of change: position, velocity, acceleration. Differences approximate *derivatives* and let us to dissect our way down the chain. Accumulators approximate *integration* and let us construct higher levels from lower ones. Thus we can manipulate an animation at any level. By plugging in correct physical laws or arbitrary formulas, we can produce behavior that is as physical or unphysical as we like.

## Customer is King

Everything we've done so far has been independent animation, without interaction. Even inertial scrolling has this luxury: whenever the user is touching, there is no inertia and the animation system is inactive. It's only when you let go that the surface coasts.

In many cases, this is not enough: animations need to be scheduled and executed while retaining full interactivity. Often the animation needs to continue despite its target changing midway. In order to handle such situations, we need to build adaptive models that remain continuous and smooth, no matter what.

We'll also need to drop the assumption that the frame rate—the time step—is constant. In the real world, the frame rate might drop here or there, or be variable altogether. In either case, we'd prefer it if the effect of this was minimal. If we're adding music to an animation, this is essential to prevent desynchronization. It will also have some nasty consequences for our physics engine, and we need to level it up significantly.

By manipulating time, we've managed to eliminate frame rate issues altogether, even make it work to our advantage. We've discovered more accurate physics engines, so we don't have to waste time simulating tiny steps. We've also created interruptible animations and turned them into filters. We can choose their easing curves and use feedback systems to remove the need for any manual interruptions altogether.

Here, *linear time-invariant* systems are very useful building blocks: they are simple to implement, but eminently customizable. Both IIR and FIR filters are simple in their basic form. We can also combine feedback systems with other physical or unphysical forces: we can move the target any way we like, perhaps superimposing variation onto existing curves. If we broaden our horizons a bit, we can find applications outside of animation: data analysis, audio manipulation, image processing, and much, much more.

Of course, there are plenty of non-linear and/or non-time-invariant systems too, too many to cover. When dealing with animation though, we'll prefer systems based on physics. They're just the trick to turn a bunch of artificial data into something that feels slick and natural. That said, physics itself is sometimes non-linear: fluids like water, smoke or fire are perfect examples. Solving those particular boondoggles requires the kind of calculus that frightens most adults and large children, so we won't go into that here. It's the same thing though: you simulate it finitely with a couple of clever tricks and the awesome power of raw number crunching.

*Continued in part two.*