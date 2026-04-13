---
title: Beyond photographic realism
url: http://c0de517e.blogspot.com/2016/03/beyond-photographic-realism.html
published: '2016-03-12'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*Service Note: if you're using motion-blur, please decouple rotational, translational and moving object amounts. And test the effect on a variety of screen sizes (fields of view).*

*In general, motion blur shouldn't be something you notice, that registers consciously.*

*I've been recently playing Firewatch (*

[really good!](https://www.youtube.com/watch?v=8Jiq56G-d5g)), which is annoyingly blurred when panning the view on my projector, and that's not an uncommon "mistake". The Order suffers from it as well, at least, to my eyes/my setup. When in doubt, provide a slider?
Ok, with that out of the way, I wanted to try to expand on the ideas of artistic control and potential of our medium I

[presented last time](http://c0de517e.blogspot.ca/2016/01/color-grading-and-excuses.html), beyond strict physical simulation with some color-grading slapped on top. But first, allow me another small digression...
This winter I was back in my hometown, visiting Naples with my girlfriend and her parents. It was their first time in Europe, so of course we went to explore some of the history and art of the surroundings (a task for which a lifetime won't be enough, but still).

One of the landmarks we went to visit is the

[Capodimonte art museum](https://en.wikipedia.org/wiki/Museo_di_Capodimonte), which hosts a quite vast collection of western paintings, from the middle ages up to the 18th century.
![]() |

[Cimabue](https://en.wikipedia.org/wiki/Cimabue)).
I've toured this museum a few times with my father in the past, and we always follow a path which illustrates the progress of western art from sacred, symbolic illustrations, where everything is placed according to an hierarchy of importance, to the beginnings of study of the natural world, of

[perspective](https://en.wikipedia.org/wiki/Perspective_(graphical)), sceneries, all the way to commissioned portraits, mythological figures and representation of common objects and people.
![]() |

What is incredibly interesting to me in this journey is to note how long does it take to develop techniques that nowadays we take for granted (the use of perspective, of lighting...), and how a single artist can influence generations of painters after.

![]() |

When is the next wave coming, for realistic realtime rendering? When are we going to discover methods beyond the current strict adhesion to somewhat

[misunderstood, bastardized ideas](http://c0de517e.blogspot.ca/2016/01/color-grading-and-excuses.html)borrowed from photography and cinematography?
Well, first of all, we ought to discuss why this question even matters, why there should be an expectation; couldn't photography be all there is to be in terms of realistic depiction? Maybe that's the best that can be done, and artistic expression should be limited to the kind of scene setups that are possible in such medium.



In my view, there are two very important reasons to consider a language of realistic depiction than transcends physical simulation and physical acquisition devices:

1)

**Perception**- Physical simulation is not enough to create perceived realism when we are constrained to sending a very limited stimuli (typically, LDR monitor output, without stereopsis or tracking). Studying physiology is important, but does not help much. A simple replica of what our vision system would do (or be able to perceive) when exposed to a real-world input is not necessarily perceived as real when such visual artefacts happen on a screen, instead of as part of the visual system. We are able to detect such difference quite easily, we need to trick the brain instead!
![]() |

by the human visual system does not look very realistic.

2)


In other words the impression of seeing a realistic scene is in your brain, reproducing only at the physics of light transport on a monitor is not enough to make your brain fire in the same way as when it's looking at the real world...

**Psychology**- Studying perception in conjunction with the limits of our output media could solve the issue of realism, but why perceptual realism matters in the first place? I'd say it's such a prominent style in games because it's a powerful tool for engagement, immersion. The actual goal is emotional, games are art. We could trick the brain with more powerful tools than what we can achieve by limiting ourselves to strict (perceptual) realism.In other words the impression of seeing a realistic scene is in your brain, reproducing only at the physics of light transport on a monitor is not enough to make your brain fire in the same way as when it's looking at the real world...

So it's this all about art then? Why is this on a rendering technology blog? The truth is, artists are often scientists "in disguise", they discover powerful tools to exploit the human brain, but don't codify them in the language of science... Art and science are not disjointed, we have should understand art, serve it.

I've been very lucky to attend a lecture by professor

Margaret Livingstone recently, it's a must-see.

Classical artists understood the brain, if not in a scientific way, in an intuitive one. Painters don't reproduce a scene measuring it, they paint what it -feels- like to see a given scene.



Analyzing art through the lens of science enquiry can reveal some of these tricks, which is interesting to researchers as they can tell something about how our brain and visual system work, but should be even more interesting for us, if we can codify these artistic shortcuts in the language of science, turning talent into tools.

Perceptual tricks are used in all artistic expressions, not only in painting but in architecture or in sculpture.

[Michlangelo's David](https://en.wikipedia.org/wiki/David_%28Michelangelo%29)has its proportions altered to look pleasing from a top-down viewing angle, enlarging the head and the right hand. And there is an interesting theory according to which Mona Lisa's "enigmatic" smile is a product of[different frequencies and eye motions](http://livingstone.med.harvard.edu/MSL%20publications/2000_November17.%20Livingstone.%20Is%20It%20Warm_%20Is%20it%20Real_%20Or%20Just%20Low%20Spatial%20Frequency_.pdf)(remember that the retina can detect high-frequency details only in a small area near the center...)Analyzing art through the lens of science enquiry can reveal some of these tricks, which is interesting to researchers as they can tell something about how our brain and visual system work, but should be even more interesting for us, if we can codify these artistic shortcuts in the language of science, turning talent into tools.

![]() |

[understood](http://strobist.blogspot.ca/2010/07/beers-with-edward-hopper.html)[light](http://www.artcyclopedia.com/feature-hopper.html). And tone mapping!(painting has a much more limited dynamic range than LCD monitors)

Cinematography has

Moreover, we are an unique blend of science and art, we have talents with very different backgrounds working together on the same product. We should be able to create an incredibly rich language!




James Turrell's installations play with real-world lights and spaces

I think that a lot of it is a reaction, a very understandable and very reasonable reaction, against the chaos that we had before physically-based rendering techniques.


We are just now trying to figure everything we need to know about PBR, and trying to educate our artists to this methodology, and that has been without doubt the single most important visual revolution of the last few years in realtime (and even offline) graphics.

PBR gives us certainty, gives us ways to understand visual problems in quantitative terms, and gives us a language with less degrees of freedom for artists, with parameters that are clearly separated, orthogonal (lights, materials, surfaces...).


This is great, when everything has a given degree of realism by construction, artists don't have to spend time trying just to achieve realism through textures and models, they can actually focus on higher level goal of focusing on -what- to show, of actual design.


But now, as we learn more of the craft of physically based models, now is the time to learn again how and why to programmatically break it! We have to understand that breaking physics is not a problem per se, the problem is breaking physics for no good reason.

For example, let's consider adjusting the "intensity" of global illumination, which is something that is not uncommon in rendering engines, it's often a control that artists ask for. The problem is entirely of math, or correctness, but of intent.



Lighting (softness/bounces) can be a hint of scale

Why are we breaking energy conservation? Is it because we made some mistakes in the math, and artists are correcting? Is it because artists did create worlds with incorrect parameters, for what they are trying to achieve? Or is it because we consciously want to communicate something with that choice, for example, distorting the sense of scale of the scene? The last, is a visual language choice, the former are just errors which should be corrected, finding the root cause instead of adding a needless degree of freedom to our system.


Nothing should be off the table, if we understand why we want certain hacks, the opposite, we should start with physical simulations and find what we can play with, and why.

Non-linear geometric distortions? Funky perspective projections (iirc there were racing games in the far past that did play with that)? Color shifts?


And even more possibilities are open with better displays, with stereopsis, HDR, VR... What if we did sometimes kill, or even invert the stereo projection, for some objects? Or change their color, or shading, across eyes?



3D printed dress by Iris Van Herpen

All other artistic disciplines,


We are still in our infancy, it's understandable, realistic realtime rendering is still young (even if we look at -gameplay- in games, that arguably is much more studied and refined than visuals as an art), but it's time to start being more aware, I'd say, of our limits, start experimenting more.

[its own](https://www.youtube.com/user/everyframeapainting)[tricks](https://www.youtube.com/watch?v=sCTGdhXCSks). Photography, Set design, all arts develop their own specific languages. And real-time rendering has much more potential, because we control the entire pipeline, from scene to physics simulation to image transfer, and we can alter these dynamically, in reaction to player's inputs.Moreover, we are an unique blend of science and art, we have talents with very different backgrounds working together on the same product. We should be able to create an incredibly rich language!

We have full control over the worlds we display, and yet so far we author and control content with tools that simulate what can be done with real cameras, in real sets. And we have full control over the -physics- of the simulations we do, and yet we are very wary of allowing tweaks that break physical laws. Why?The most wonderful thing about working in lighting is the people that you encounter. Scientists and artists; engineers and designers; architects and psychologists; optometrists and ergonomists; are all concerned about how people interact with light. It is a topic that is virtually without boundaries, and it has brought me into contact with an extraordinary variety of people from whom I have gathered so much that I know that I cannot properly acknowledge all of them.- From "Lighting by Design", Christopher Cuttle.

![]() |

We are just now trying to figure everything we need to know about PBR, and trying to educate our artists to this methodology, and that has been without doubt the single most important visual revolution of the last few years in realtime (and even offline) graphics.

PBR gives us certainty, gives us ways to understand visual problems in quantitative terms, and gives us a language with less degrees of freedom for artists, with parameters that are clearly separated, orthogonal (lights, materials, surfaces...).

This is great, when everything has a given degree of realism by construction, artists don't have to spend time trying just to achieve realism through textures and models, they can actually focus on higher level goal of focusing on -what- to show, of actual design.

But now, as we learn more of the craft of physically based models, now is the time to learn again how and why to programmatically break it! We have to understand that breaking physics is not a problem per se, the problem is breaking physics for no good reason.

For example, let's consider adjusting the "intensity" of global illumination, which is something that is not uncommon in rendering engines, it's often a control that artists ask for. The problem is entirely of math, or correctness, but of intent.

![]() |

Nothing should be off the table, if we understand why we want certain hacks, the opposite, we should start with physical simulations and find what we can play with, and why.

Non-linear geometric distortions? Funky perspective projections (iirc there were racing games in the far past that did play with that)? Color shifts?

[Bending](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.446.7600&rep=rep1&type=pdf)[light](https://diglib.eg.org/handle/10.2312/CGF.v29i4pp1451-1459)[rays](https://www.researchgate.net/profile/Nicolas_Mellado/publication/273908385_Light_Transport_Editing_with_Ray_Portals/links/559249a908ae15962d8e5691.pdf)?And even more possibilities are open with better displays, with stereopsis, HDR, VR... What if we did sometimes kill, or even invert the stereo projection, for some objects? Or change their color, or shading, across eyes?

![]() |

[from](http://showstudio.com/project/visions_couture/gareth_pugh_3d_scan)[fashion](http://www.irisvanherpen.com/)to[architecture](http://www.grasshopper3d.com/), rush at new[technologies](https://news.artnet.com/art-world/anish-kapoor-adds-new-super-black-to-his-palette-111382), new tools, trying to understand how they can be employed, hacked,[bent](http://www.michaelbach.de/ot/sze_reverspective/), for new effects.We are still in our infancy, it's understandable, realistic realtime rendering is still young (even if we look at -gameplay- in games, that arguably is much more studied and refined than visuals as an art), but it's time to start being more aware, I'd say, of our limits, start experimenting more.

## 2 comments:

Just a side-note: artistic perspective was actually well-developed in antiquity, mostly among the Greeks. The (common) misconception appears to be related to thematic scaling in Christian art--which was itself by far the most common kind in the western world--in the Middle Ages.

You're right, the lack of interest in the study of perspective in early medieval art was certainly not an accident, the paintings were meant to convey a message, the figure proportion and arrangement have symbolic meanings. That said, you can trace the evolution of western art from medieval time through renaissance and note how long it took to "recover" from a symbolic use of space to an interest to perspective, to fully a developed geometrical theory of it.



That said, early greek and roman painters as was the case for early renaissance painters in the 14th century, didn't have a solid grasp of geometrical perspective, but more often an understanding of perspective at an intuitive level, as it's evident by the mistakes in perspective lines in the art of such eras.

Post a Comment