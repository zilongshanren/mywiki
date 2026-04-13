---
title: My dissertation is available now
url: http://momentsingraphics.de/DissertationAnnouncement.html
published: '2017-12-31'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# My dissertation is available now

My dissertation has been published digitially and is now available in its entirety as a [free download](http://hss.ulb.uni-bonn.de/2017/4918/4918.htm). Most results have been published before through my papers at [i3D 2015](http://momentsingraphics.de/I3D2015.html), [SIGGRAPH Asia 2015](http://momentsingraphics.de/SiggraphAsia2015.html) and [JCGT](http://momentsingraphics.de/JCGT2017.html). Though, there is some entirely new material. Since I spent a lot of time writing it, there better be somebody to read parts of it. Below I'll try to wet your appetite.

## What's new?

Most of the new material deals with moment shadow mapping itself and its foundation in the theory of moments.

- Introduction to the theory of moments (Chapter 2)
- The dissertation starts with a brief and pragmatic introduction to the theory of moments. It focuses on the basics but does have some simple algorithms. At the end there are pointers to the many different moment problems and algorithms discussed throughout the dissertation. If you face a problem that might benefit from the theory of moments, this might be a good place to get started.
- An errata to moment shadow mapping (Section 3.4)
- The
[original paper on moment shadow mapping](http://momentsingraphics.de/I3D2015.html)did not just introduce moment shadow mapping, it compared it to 66045 alternative candidate techniques. When I revisited this part for the writeup, I found a flaw. The comparison relies on linear programming and the used solvers have small numerical tolerances. These tolerances essentially introduce light leaking, much like the biasing used in moment shadow mapping. Then the results of the comparison largely just measure how robust the various techniques are to this kind of errors. This is interesting by itself but not what was originally intended. The good news is that I reran the experiment with substantitally smaller tolerances and that the new data supports the original conclusions even better than the original data. The key observation is that 15000 out of 66045 candidates realize the top performance and that moment shadow mapping is one of them. - A new interpretation of biasing (Section 4.1.3)
- The dissertation offers an interesting new view on what it means to apply biasing. Through linear programming, it is possible to incorporate rounding errors into the reconstruction explicitly. You can ask for a sharp lower bound if you only know that the moments lie in a small hybercube defined by rounding errors. It turns out that the results resemble those obtained with biasing very closely. This is neat, because the biasing is simple and efficient but still manages to give you something similar to the best thing you could ask for with the available information.
- Details on the derivation of biasing strategies (Appendix B.1)
- The
[JCGT paper](http://momentsingraphics.de/JCGT2017.html)introduces a biasing strategy that is optimal in the worst case, thus improving robustness. The dissertation provides a lot of detail on how this can actually be computed. - Integrating over the maximum entropy spectral estimate (Sections 8.2.3 and 8.4.4)
- For fast transient imaging, I have used trigonometric moments among with a reconstruction optimizing the Burg-entropy. This reconstruction algorithm is very efficient and elegant but it only computes a density function. In the dissertation I show how to compute the corresponding cumulative distribution function. The most tricky step is computation of polynomial roots, so it is a closed form for up to four trigonometric moments which gets you quite far. Even if you are not interested in transient imaging at all, you might want to take a look. It is essentially a generic replacement for inverse Fourier transforms of positive functions with many benefits.

## Outlook

While the dissertation deals with fairly diverse problems, its red thread is the transfer of solutions to moment problems from mathematics literature to computer graphics practice. This is a generic set of tools that I have thrown at a handful of problems I encountered in the past years. I am convinced that much more can be done with it and encourage everybody to give it a try. With all the material I have published, the tools have been packed into pretty robust black boxes. You put moments of a signal in and get a reconstruction of the signal out. In my experience, people still have some trouble getting into the right mode of thinking to use these boxes. With my dissertation (especially Chapter 2) I am hoping to change this.