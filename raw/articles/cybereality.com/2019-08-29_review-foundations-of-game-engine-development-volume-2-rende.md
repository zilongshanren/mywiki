---
title: 'Review: Foundations of Game Engine Development, Volume 2: Rendering by Eric
  Lengyel'
url: https://cybereality.com/review-foundations-of-game-engine-development-volume-2-rendering-by-eric-lengyel/
author: Cybereality
published: '2019-08-29'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/9c1bc9159a8e7ac8.jpg)

This is the second book in the new game engine development series by acclaimed author and engine developer, Eric Lengyel. Though it is not strictly necessary to read in order, it is basically one book cut into sections, so you may want to get the first one, as well as the upcoming continuations of the series, to get the most out of it.

I found Volume 2 of Foundations of Game Engine Development to be a solid resource and a compelling sequel to the first book. Please keep in mind that this is a foundation series, which builds a solid breadth of knowledge for building a 3d game engine. It is not a state-of-the-art cookbook, and much of the coverage is of techniques that are relatively old (say from 10 years ago or more). I would not say it’s a beginner’s book, it’s more of an intermediate level introduction. You will still need to be able to read the math and code snippets, though Lengyel does well explaining things.

I’ll give a brief survey of what’s in the 400 some odd pages (clocking in at twice the length of the first volume). The author dives into color science, gamma correction, coordinate spaces, and the basics of the graphics pipeline. Then he deals with projection matrices, really basic lighting models, normal and parallax mapping, as well as light sources and shadows (including stencil shadows, which I found interesting, despite being an antiquated technique). The next chapter focuses on visibility and occlusion and the book is worth reading for this chapter alone. Here we see polygon clipping, bounding volumes (spheres and boxes), frustum culling, portal systems, and occluders. This has got to be one of the best explanations of these methods I have seen in one text, the writing is clear and the diagrams are perfect. I especially like that the whole book is in color, and all the diagrams take advantage of this and are easy to understand. Finally, the book concludes with some “advanced” techniques, like decals, billboards, volumetric light, ambient occlusion, motion blur, and god rays. Gotta have those god rays.

I really enjoyed the whole book, and I found it to be helpful, even though I might have had some understanding of most of the topics already. Going in, you should know these are not state-of-the-art techniques, nor is it a shader code cookbook. For that you are better off with a GPU Pro or GPU Zen type of book. This is a foundations book, for people wishing to code their own game engine. There are not a whole lot of books that cover this topic, I have read most of them, and this is one of the best. Many books tie themselves to one API or framework version and are quickly obsolete. While here, in Foundations of Game Engine Development, you have tried and true methods that have been incorporated into practically any engine written in the last 10 – 15 years. The engine code is in C++, and the shader code is in a high level language, but the author thankfully does not mix in any API code so all the techniques are applicable to whatever API you prefer.

Overall this book is great, as long as you know what you are getting into. It’ll probably be mostly a refresher for game engine pros, though for people starting out I think this would be a godsend. I should preface this with saying I’m still not 100% sure writing your own engine today is a good idea. If you asked me honestly, I’d probably say use Unreal or Unity and call it a day. However, if you do want to go down this path, you really can’t go wrong with this series. Recommended.