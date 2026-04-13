---
title: 'Inside Facebook 3D Photos: Parallax Shaders - Alan Zucconi'
url: https://www.alanzucconi.com/2019/01/01/facebook-3d-photos-2/
author: Alan Zucconi
published: '2019-01-01'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

In the past few months, Facebook has been ~~plagued~~ filled with **3D photos**. If you have not had the chance to see one, 3D photos are images inside a post which gently change perspective as you scroll the page, or as you move your mouse over them.

![](../../assets/ee78126ea3853911.gif)

A few months prior to their introduction, Facebook had been testing a similar feature with 3D models. While it is easy to understand how Facebook can render 3D models and rotates them according to the mouse position, the same might not be as intuitive for 3D photos.

The techniques that Facebook is using to create the illusion of three-dimensionality on two-dimensional pictures is sometimes known as **height map displacement**, and it relies on an optical phenomenon called **parallax**.

This is a two-part series. You can read all the posts here:

- Part 1.
[Inside Facebook 3D Photos](https://www.alanzucconi.com/?p=9493) - Part 2.
[Parallax Shaders & Depth Maps](https://www.alanzucconi.com/?p=10453)

A link to the complete Unity package is available at the end of the tutorial.

## Understanding Parallax

If you have played Super Mario, you know exactly what parallax is. While Mario is running at a certain speed, distant objects in the background appear to be moving slower (below).

![](../../assets/bfc7cdf076f6756b.gif)

This effect creates the illusion that certain elements, like mountains and clouds, are further away. The reason behind its effectiveness comes from the fact that our brain strongly relies on parallax (among other visual clues) to estimate the distance of far objects.

## Parallax As Shifting

If you are familiar with linear algebra, you probably know how tricky and complex the Mathematics of 3D rotations can be. That being said, there is a very easy way to understand parallax which involves nothing more than shifts.

Let’s imagine that we are looking at a cube (below). If we are perfectly aligned to its centre, the front and back faces will appear to our eyes as two squares of different size. That is **perspective** in a nutshell.

![](../../assets/f8d8354d7ff99a6d.png)

However, what happens if we shift the camera down or, equivalently, if we shift the cube up? By applying the same principles, we can see that the front and back faces appear to have shifted from their previous position. More interestingly, they have shifted in respect to each other. The back face, which is further to us, appears to have move less.

![](../../assets/887f9a160997f562.png)

If we want to calculate the actual positions of those cube’s vertices on our projected field of view, we do need to deal with a good amount of trigonometry. However, that is not really necessary. If the movement of the camera is small enough, we can approximate the displacement of the vertices by offsetting them proportionally to their distance.

The only thing we need to establish is a scale. If we move X metre on the right, an object at Y metres from us appears to be shifted by Z metres. As long as X stays small, parallax becomes a problem of **linear interpolation**, not trigonometry. This ultimately means that we can simulate small 3D rotations by simply shifting pixels based on how far they are from the camera.

## Generating Depth Maps

What Facebook does is, at its core, not too dissimilar from what is happening in Super Mario. Given a picture, certain pixels are shifted in the direction of the movement based on their distance from the camera. All that Facebook needs to create a 3D photo is the photo itself, and a map that tells how far each pixel is from the camera. Such a map is called, unsurprisingly, a **depth map**. Depending on the context, it can also be referred to as a **height map**.

While taking pictures is a relatively easy task, generating a reliable depth map is a much more challenging problem. Modern devices rely on various techniques. The most common one involves the use of two cameras; each one takes a picture of the same subject, but from a slightly different perspective. This is the principle behind **stereoscopic vision**, which is another way in which humans are able to perceive depth on a short to medium range. The picture below shows how an iPhone 7 is able to create depth maps from two very close images.

![](../../assets/ad896caf3c403808.png)

The details of how such a reconstruction is done are explained in [Instant 3D Photography](http://visual.cs.ucl.ac.uk/pubs/instant3d/), a paper that [Peter Hedman](http://phogzone.com/) and [Johannes Kopf](https://twitter.com/JPKopf) have presented at SIGGRAPH2018.

Once a reliable depth map is available, simulating the three-dimensionality of an image becomes almost a trivial task. The real limitation of this technique comes from the fact that even if a rough 3D model can be reconstructed, there is lacking information on how to render the parts that were occluded in the original photos. This problem, at the moment, cannot be solved and it is why all the deformations seen in 3D photos are rather mild.

## What’s Next…

This post introduced the concept of 3D photos, briefly explaining how modern smartphones are able to capture them. The next tutorial in this online course will show how to use those very same techniques to implement 3D photos in Unity using shaders.

![](../../assets/9f5519082519a5fe.gif)

This is a two-part series. You can read all the posts here:

- Part 1.
[Inside Facebook 3D Photos](https://www.alanzucconi.com/?p=9493) - Part 2.
[Parallax Shaders & Depth Maps](https://www.alanzucconi.com/?p=10453)

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the full Unity Project for this download on [Patreon](https://www.patreon.com/posts/23680800).

Credits for the picture of the cat and its depth map goes to [Dennis Hotson](https://twitter.com/dennishotson)‘s [Pickle cat](https://dn.ht/picklecat/) project.

## Leave a Reply Cancel reply