---
title: Siggraph 2015 course
url: https://c0de517e.blogspot.com/2015/08/siggraph-2015-course.html
published: '2015-08-15'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

As some will have noticed,

[Michal Iwanicki](http://miciwan.com/)and I were speakers (well I was much more of a listener, actually) in the[physically based shading course](http://blog.selfshadow.com/publications/s2015-shading-course/)this year (thanks again to both Stephens for organizing and invitingus) presenting a talk on approximate models for rendering, while our Activision colleague and rendering lead of Sledgehammer showed some of his studio's work on real world measurements used in Advanced Warfare.
![]() |

[Before and after :)](https://instagram.com/kenpex/)
If you weren't at Siggraph this year or you missed the course, fear not, we'll publish the course notes soon (I need to do some proof reading and adding bibliography) and the course notes are "the real deal", as in twenty minutes we couldn't do much more than a teaser trailer on stage.

I wanted to write though about the reasons that motivated me to present in the course that material, give some background. Creating approximations might be time consuming sometimes, but it's often not that tricky, per-se I don't think it's the most exciting topic to talk about.

But it is important, and it is important because we are still too often too wrong. Too many times we use models that we don't completely understand, that are exact under assumptions we didn't investigate and for which we don't know what perceptual error they cause.

You can nowadays point your finger at any random real time rendering technique, really look at it closely, compare with ground truth, and you're more likely than not to find fundamental flaws and simple improvements through approximation.

This is a very painful process, but necessary. PBR is like VR, it's an all or nothing technique. You can't just use GGX and call it a day. Your art has to be (perceptually) precise, your shadows, your GI, your post effect, there is a point where everything "snaps" and things just look real, but it's very easy to be just a bit off and ruin the illusion.

Worse, errors propagate non-locally as artists try to compensate for our mistakes in the rendering pipeline by skewing the assets to try to reach as best as they can a local minimum.

Moreover, we are also... not helped I fear by the fact that some of these errors are only ours, we commit them in application, but the theory in many cases is clear. We often got research from the seventies and the eighties that we should just read more carefully.

For decades in computer graphics we rendered images in

[gamma space](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch24.html), but there isn't anything for a researcher to publish about linear spaces, and even today we largely ignore what colorspaces really are and what we should use, for example.
We don't challenge the assumptions we work with.

A second issue I think is sometimes it's just neater to work with assumptions that it is to work on approximations. And it is preferable to derive our math exactly via algebraic simplifications, the problem is that when we simplify by imposing an assumption, its effects should be measured precisely.

If we consider constant illumination, and no bounces, we can define ambient occlusion, and it might be an interesting tool. But in reality it doesn't exist, so when is it a reasonable approximation? Then things don't exactly work great, so we tweak the concept and create

[ambient obscurance](http://graphics.cs.williams.edu/papers/SAOHPG12/), which is better, but to a degree even more arbitrary. Of course this is just an example, but note: we always knew that AO is something odd and arbitrary, it's not a secret, but even in this simple case we don't really know how wrong it is, when it's more wrong, and what could be done to make it measurably better.
You might say that even just finding the errors we are making today and what is needed to bridge the gap, make that final step that separates nice images from actual photorealism, is a non-trivial

[open problem](http://s2015.siggraph.org/attendees/courses/events/open-problems-real-time-rendering)(*).
It's actually much easier to implement a many exciting new rendering features in an engine than to make sure that we got even a very simple and basic renderer is (again perceptually) right. And on the other hand if your goal is photorealism it's surely better to have a very constrained renderer in very constrained environments that is more accurate than a much fancier one used with less care.

I was particularly happy at this Siggraph to see that more and more we are aware of the importance of acquired data and ground truth simulations, the importance of being "correct", and there are many researchers working to tackle these problems that might seem even to a degree less sexy than others, but are

[really important](https://eheitzresearch.wordpress.com/).
In particular right after our presentations

[Brent Burley showed](http://blog.selfshadow.com/publications/s2015-shading-course/burley/s2015_pbs_disney_bsdf_notes.pdf), yet again, a perfect mix of empirical observations, data modelling and analytic approximations in his new version of Disney's BRDF, and[Luca Fascione](http://blog.selfshadow.com/publications/s2015-shading-course/)did a better job I could ever do explaining the importance of knowing your domain, knowing your errors, and the continuum of PBR evolution in the industry.
P.S. If you want to start your

[dive into Siggraph content](http://blog.selfshadow.com/2015/08/15/siggraph-2015-links/)right, start with[Alex](https://twitter.com/mmalex)"[Statix](http://www.pouet.net/groups.php?which=42)" Evans amazingly presentation in the[Advances course](http://advances.realtimerendering.com/): cutting edge technology presented[through a journey](http://c0de517e.blogspot.ca/2015/04/sharing-is-caring.html)of different prototypes and ideas.
Incredibly inspiring, I think also because the technical details were sometimes blurred just enough to let your own imagination run wild (read: I'm not smart enough to understand all the stuff... -sadface-).

Really happy also to see many teams share insights "early" this year, before their games ship, we really are a great community.

P.S. after the course notes you might get a better sense of why I wrote some of my past posts like:

[Area lights](http://c0de517e.blogspot.ca/2013/12/notes-on-epics-area-lights.html).[No bare bulb point lights](http://c0de517e.blogspot.ca/2013/12/never-again-point-lights.html).[Scientific Python 101](http://c0de517e.blogspot.ca/2014/09/scientific-python-101.html)and[Mathematica 101](http://c0de517e.blogspot.ca/2013/10/wolframs-mathematica-101.html).[Cube map errors](http://c0de517e.blogspot.ca/2014/06/oh-envmap-lighting-how-do-we-get-you.html), and[part two](http://c0de517e.blogspot.ca/2015/03/being-more-wrong-parallax-corrected.html).[Visualitazion](http://c0de517e.blogspot.ca/2014/06/stuff-that-every-programmer-should-know.html).

*(*) I loved the open problems course, I think we need it each year and we need to think more at what we really need to solve. This is can be a great communication channel between the industry, the hardware manufactures and the academia. Chose wisely...*

## 4 comments:

I just read a few lines. Just wanna say. If u r good at reading a book. It is a portal. It doesn't need GPU power. It doesn't need good mathematical model. And every game I played... sucked me in. Just like every good book. Nono. I love the improvements GFX made through the years. Just wanted to point out that there are two ways to look at it. Keep up ur good work.

Sure, we don't need photorealism for good storytelling. Actually it's often easier for the player to immerse in an environment that is "blurred" enough, that leaves space to imagination, than a "realistic" environment that is still wrong. But the power of "good" photorealism is I think still underestimated, even with all the progress in rendering, GPUs and so on, we are still far. What could we do if we could play in environments that were just real, indistinguishable from reality. What if we could reach the quality of movies with the full interactivity that games have. I suspect that would also have a great potential for a much more emotional storytelling.

Really love this post, looking forward to see the notes!

Hi, any news on those course notes? :)

Post a Comment