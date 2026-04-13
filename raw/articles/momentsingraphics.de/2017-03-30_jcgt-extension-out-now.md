---
title: JCGT extension out now
url: http://momentsingraphics.de/JCGTAnnouncement.html
published: '2017-03-30'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# JCGT extension out now

**Update 2017-09-04:** Changed the post to reflect availability of [non-linearly quantized moment shadow maps](http://momentsingraphics.de/HPG2017.html).

The invited extension of our i3D 2016 paper is now [published in the Journal of Computer Graphics Techniques](http://www.jcgt.org/published/0006/01/03/). It discusses techniques for real-time soft shadows, single scattering and shadows for translucent occluders with some novel improvements. All of these techniques are based on moment shadow mapping and the paper also introduces improvements to moment shadow mapping itself.

The implementation is discussed in great detail. If you are a graphics developer interested in moment shadow mapping, it will likely be your most valuable source to implement it in your engine. It is not the only source though. Since it may have gotten a little bit confusing, here is an overview of the available resources:

- The
[lecture held at the GDC Europe 2016](http://momentsingraphics.de/GDCEurope2016.html): If you know nothing about moment shadow mapping, this 53 minute lecture is the best place to get started. It accounts for the improvements discussed in the[JCGT paper](http://www.jcgt.org/published/0006/01/03/). - The
[HPG 2017 paper](http://momentsingraphics.de/HPG2017.html): This publication introduces non-linearly quantized moment shadow maps. If you only care about filtered hard shadows, this is the fastest solution you can find. - The
[JCGT paper](http://www.jcgt.org/published/0006/01/03/): If you are planning to implement a technique based on (linear) moment shadow mapping, this paper will offer all the information that you need. In particular, there is Appendix D with specific instructions which shader functions have to be used in which way. Note that you do not need to read the whole paper if you are only interested in one of the applications. Section 2 introduces moment shadow mapping. Once you have read it you can jump to Section 3, 4 or 5 right away. - The
[executable demo with HLSL code](http://momentsingraphics.de/HPG2017Demo.html): This demo incorporates all techniques discussed in the[JCGT paper](http://www.jcgt.org/published/0006/01/03/)and in the[HPG 2017 paper](http://momentsingraphics.de/HPG2017.html)as well as a lot of related work. It comes with extensively documented shader code. Additional usage instructions for most of the shader code can be found in Appendix D of the[JCGT paper](http://www.jcgt.org/published/0006/01/03/). - The
[i3D 2016 paper](http://momentsingraphics.de/I3D2016.html): This is the original publication on the techniques covered by the[JCGT paper](http://www.jcgt.org/published/0006/01/03/). It may be viewed as a convenient short version but it does not include various more recent improvements, so you should no longer refer to it if you mean to implement these techniques. - The
[i3D 2015 paper](http://momentsingraphics.de/I3D2015.html): This paper introduced moment shadow mapping for filtered hard shadows. There is nothing in there about the other applications. It is far more comprehensive than the[JCGT paper](http://www.jcgt.org/published/0006/01/03/)but not all the provided information is relevant for the implementation and it lacks the improvements discussed in the[JCGT paper](http://www.jcgt.org/published/0006/01/03/). Read this, if you want to know more about core principles of moment shadow mapping. [Matt Pettineo's shadow sample](https://mynameismjp.wordpress.com/2015/02/18/shadow-sample-update/): This demo includes moment shadow mapping. It also has cascaded shadow maps (even[sample distribution shadow maps](https://software.intel.com/en-us/articles/sample-distribution-shadow-maps)) and therefore it allows you to test moment shadow mapping on scenes with a larger scale.

A sensible way to review these resources would be to start with the [GDC Europe 2016 lecture](http://momentsingraphics.de/GDCEurope2016.html), play around with [the demo](http://momentsingraphics.de/HPG2017Demo.html) and then, if this has wet your appetite, read the [JCGT paper](http://www.jcgt.org/published/0006/01/03/). As you implement the techniques, you should have [Appendix D](http://www.jcgt.org/published/0006/01/03/) at hand.

Moment shadow mapping and the techniques that build upon it are the result of research that I did with colleagues and undergrads as PhD student at the [University of Bonn](http://cg.cs.uni-bonn.de/en/start/). They are not patented, the shader code is in the public domain and all resources listed above can be downloaded for free. The only thing that I ask you to consider in return is that you let me know if you find use for these techniques in your products or that you make it publicly known. Being able to point at the practical impact of my work helps to keep this research going and of course it is also motivating.

If you have any questions or feedback, please contact me through the comments, on [Twitter](https://twitter.com/MomentsInCG) or via email.

## Comments

**Jonathan**

2017-09-28, 16:39

Sounds great; I hope I'll have some time to work through this soon.

Comments are closed.