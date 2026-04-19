---
title: Creating a 3D Game Engine (Part 23)
url: https://cybereality.com/creating-a-3d-game-engine-part-23/
author: Cybereality
published: '2014-07-18'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![engine_zero_08](../../assets/9b3ca83d787106b2.jpg)

While I implemented frustum culling a little while ago, I never actually coded a proper bounding volume. For the bounding test I was using a sphere, but I just set the radius to some hard-coded value. This was fine when I just had a bunch of similar sized cubes on screen, however it broke apart once I started getting varied models imported. This week I decided to do something about it.

After a quick Google search for bounding spheres, I ended up [on Wikipedia](https://en.wikipedia.org/wiki/Bounding_sphere). There was some good information there regarding minimal bounding spheres (also known as smallest enclosing ball or minimal enclosing ball), and I was given a few options for different algorithms. After reading the whole page I become very interested in the “bouncing bubble” algorithm, especially due to the spiffy gif animation showing it in action. The brief explanation seemed easy to follow compared to the other methods, and the error percentage was only around 1-2% which is much lower than Ritter’s algorithm (which can be as high as 20%). So far so good.

Unfortunately I found next to nothing on the internet describing the method. What I did find is [a post from last year on StackOverflow](http://stackoverflow.com/questions/17331203/bouncing-bubble-algorithm-for-smallest-enclosing-sphere) by someone in the same situation as me. This lead me to the original paper describing the method, which was [for sale for $18 on Grin.com](http://www.grin.com/en/e-book/204869/bouncing-bubble-a-fast-algorithm-for-minimal-enclosing-ball-problem). Honestly I don’t mind paying the money for quality information if it’s going to help improve my engine. The article was fairly easy to follow, and provided just enough information to base the implementation on. At first I was disappointed that no source-code was given, but I managed to pull it together using the pseudo-code. All in all I think I spent about 4 hours on it (including research) so I’m happy to have got it working so quickly.

Below is my bouncing bubble implementation. Keep in mind I have not profiled this code, it’s possible it’s not fully optimized. However, I’m only doing the calculation when a 3D model is loaded, so it shouldn’t effect performance at all really.

BoundSphere RenderCore::calculateBoundSphere(vector vertices){ Vector3D center = vertices[0].position; float radius = 0.0001f; Vector3D pos, diff; float len, alpha, alphaSq; vector::iterator it; for (int i = 0; i < 3; i++){ for (it = vertices.begin(); it != vertices.end(); it++){ pos = it->position; diff = pos - center; len = diff.length(); if (len > radius){ if (i < 2){ alpha = len / radius; alphaSq = alpha * alpha; radius = 0.5f * (alpha + 1 / alpha) * radius; center = 0.5f * ((1 + 1 / alphaSq) * center + (1 - 1 / alphaSq) * pos); } else { radius = (radius + len) / 2.0f; center = center + ((len - radius) / len * diff); } } } } return BoundSphere(center, radius); }

Also, I should remind myself to do benchmarks more often. After I added all the normal mapping and shadow stuff performance has taken a big it. Before I was getting likely over 2400fps, now I’m only getting around 1600fps. Still acceptable, but maybe could be better with such a simple scene. The culling definitely helps, but I may have to look into other optimizations like batching and instancing if I want to get the speeds I need for my project. I’ll probably get started with the physics engine aspect soon and then optimize later if I can’t meet my 120fps target. Cheers.