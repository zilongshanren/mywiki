---
title: Creating a 3D Game Engine (Part 20)
url: https://cybereality.com/creating-a-3d-game-engine-part-20/
author: Cybereality
published: '2014-06-01'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

Spent the last couple days adding in skybox support into the engine. Currently it’s a little hard-coded, but it does seem to be working well. I also bumped the field of view (FOV) up to 90 (from 45) so you can see more of the sky. I wanted to make sure I was only using my own artwork for this engine demo. Unfortunately, it would have been rather difficult to take panoramic photos myself. So I generated the sky texture using Terragen. Somewhat of a cheat, but I did technically “create” it myself, so I can live with that.

Ran into one issue that had me stumped for about a day. Basically, I was following a tutorial for implementing the skybox. It seemed like I followed everything well, but I was getting this wild fish-eye type of distortion on the sky. As it turned out, it was my custom matrix transpose function that was at fault. The tutorial used “XMMatrixTranspose()” but I re-implemented this myself. The trouble was, I was swapping around the values without creating a temporary copy first. Meaning, I was doing something like this:

m12 = m21; ... m21 = m12;

Clearly that won’t work. The interesting part is that I got stuck on it one night and couldn’t figure out what was wrong. I knew it had something to with the matrix math, but I wasn’t sure what. So I left it alone and went about my day. Then, while in the bathroom washing my face, I had a “eurika!” moment and the answer came to me. Not sure how that works, if it’s like a sub-process in my mind or something cracking away at problems. But I’m glad I finally caught the error.

There are a few things I’d like to try next. First off, the lighting model could be improved great. Right now it’s just a hard-coded ambient and directional light. I’d like to have a more flexible system to add any type of light into the scene graph and have the shader support it. Support for normal mapping would be cool, as well as specular and emissive textures. I’d also like to do some initial experiments in building a physics system, or at least learn more about compute shaders and how they integrate into the pipeline. Plus, better artwork. Stay tuned.