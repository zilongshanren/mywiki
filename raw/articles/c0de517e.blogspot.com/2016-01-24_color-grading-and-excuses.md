---
title: Color grading and excuses
url: http://c0de517e.blogspot.com/2016/01/color-grading-and-excuses.html
published: '2016-01-24'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I started jotting down some notes for this post a month ago maybe, after watching bridge of spies on a plane to New York. An ok movie if you ask me, with very noticeable, heavy-handed color chocies and for some reasons a heavy barrel distortion in certain scenes.

![]() |

I'm quite curious to understand the reasoning behind said distortion, what it's meant to convey, but this is not going to be a post criticizing the overuse of grading, I think that's already something many people are beginning to notice and hopefully avoid. Also I'm not even entirely sure it's really a "problem", it might be even just

[fatigue](http://www.newyorker.com/culture/cultural-comment/the-turn-against-digital-effects).
For decades we didn't have the technology to reproduce colors accurately, so realistic color depiction was the goal to achieve. With digital technology perfect colors are "easy", so we started experimenting with ways to do more, to tweak them and push them to express certain atmospheres/emotions/intentions, but nowadays we get certain schemes that are repeated over and over so mechanically it becomes stale (at least in my opinion). We'll need something different, break the rules, find another evolutionary step to keep pushing the envelope.

![]() |

[Kinemacolor](http://www.widescreenmuseum.com/oldcolor/oldcolor.htm#menu)
What's more interesting to me is of course the perspective of videogame rendering.


We've been shaping our grading pretty much after the movie pipelines, we like the word "filmic", we strive to reproduce the characteristics and defects of real cameras, lenses, film stocks and so on.

We've been shaping our grading pretty much after the movie pipelines, we like the word "filmic", we strive to reproduce the characteristics and defects of real cameras, lenses, film stocks and so on.

A surprising large number of games, of the most different genres, all run practically identical post-effect pipelines (at least in the broad sense, good implementations are still rare). You'll have your bloom, a "filmic" tone mapping, your color-cube grading, depth of field and motion blur, and maybe vignette and color aberration. Oh, and lens flares, of course... THE question is: why? Why we do what we do?

![]() |

One argument that I hear sometimes is that we adopt these devices because they are good, they have so much history and research behind them that we can't ignore. I'm not... too happy with this line of reasoning.

Sure, I don't doubt that the characteristic curves of modern film emulsions were painstakingly engineered, but still we should't just copy and paste, right? We should know the reasoning that led to these choices, the assumptions made, check if these apply to us.

And I can't believe that these chemical processes fully achieved even the ideal goals their engineers had, real-world cameras have to operate under constraints we don't have.

In fact digital cameras are already quite different than film, and yet if you look at the work of great contemporary photographers, not everybody is rushing to apply film simulation on top of them...

Furthermore, did photography try to emulate paintings? Cross-pollination is -great-, but every media has its own language, its own technical discoveries. We're really the only ones trying so hard to be emulators; Even if you look at CGI animated movies, they seldom employ many effects borrowed from real-world cameras, it's mostly videogames that are obsessed with such techniques.

![]() |

A better reason someone gave me was the following: games are hard enough, artists are comfortable with a given set of tools, the audience is used to a given visual language, so by not reinventing it we get good enough results, good productivity and scenes that are "readable" from the user perspective.



There is some truth behind this, and lots of honesty, it's a reasoning can lead to good results if followed carefully. But it turns out that in a lot of cases, in our industry, we don't even apply this line of thinking. And the truth is that more often than not we just copy "ourselves", we copy what someone else did in the industry without too much regard with the details, ending up in a bastard pipeline that doesn't really resemble film or cameras.

When was the last time you saw a movie and you noticed chromatic aberrations? Heavy handed flares and "bloom" (ok, other than in the infamous J.J.Abrams Star Trek, but hey,

[he apologized](http://www.theverge.com/2013/9/30/4788758/j-j-abrams-apologizes-for-his-overusing-lens-flares)...)? Is the motion blur noticeable? Even film grain is hardly so "in your face", in fact I bet after watching a movie, most of the times, you can't discern if it was[shot on film](http://filmmakermagazine.com/88971-39-movies-released-in-2014-shot-on-35mm)or digitally.
Lots of the defects we simulate are not considered pleasing or artistic, they are





[aberrations](http://www.handprint.com/ASTRO/ae4.html)that camera manufacturers try to get rid of, and they became quite versed at it! Hexagonal-shaped bokeh? Maybe on very cheap lenses...
![]() |

[http://www.cs.ubc.ca/labs/imager/tr/2012/PolynomialOptics/](http://www.cs.ubc.ca/labs/imager/tr/2012/PolynomialOptics/)
On the other hand lots of other features that -do- matter are completely ignored. Lots of a

[lens "character"](http://www.overgaard.dk/pdf/Leica-M-Lenses-Their-Soul-and-Secrets_en.pdf)comes from its point spread function, a lens can have a lower contrast but high resolution or the opposite, field curvature can be interesting, out of focus areas don't have a fixed, uniform shape across the image plane (in general all lens aberrations change across it) and so on. We often even leave the choice of antialiasing filters to the user...
Even on the grading side we are sloppy. Are we really sure that our artists would love to work with a movie grading workflow? And how are movies graded anyways? With a constant, uniform color correction applied over the entire image? Or with the same correction applied per environment? Of course not! The grading is done shot by shot, second by second. It's done with masks and rotoscoping, gradients, non-global filters...

![]() |

Lots of these tools are not even hard to replicate, if we wanted to; We could for example use stencils to replicate masks, to grade differently skin from sky from other parts of the scene.

Other things are harder because we don't have shots (well, other than in cinematic sequences), but we could understand how a colorist would work, what an artist could want to express, and try to invent tools that allow a better range of adjustment. Working in worldspace or clipspace maybe, or looking at material attributes, at lighting, and so on.

Ironically people (including myself sometimes) are sometimes instinctively "against" more creative techniques that would be simple in games on the grounds that they are too "unnatural", too different from what we think it's justified by the real camera argument, that we pass on opportunities to recreate certain effects that would be quite normal in movies instead, just because they are not exactly in the same workflow.

![]() |



**Scene color control vs post-effect grading.**

**I think the endgame though is to find our own ways. Why do we grade and push so much on post effects to begin with? I believe the main reason is because it's so easy, it empowers artists with global control over a scene, and allows to do large changes with minimal effort.**


If that's the case though, could we think of different ways to make the life of our artists easier? Why can't we allow the same workflows, the same speed, to operations on source assets? With the added benefit of not needlessly breaking physical laws, thus achieving control in a a more believable way....

![]() |

[image](http://www.zvork.fr/vls/)in the middle. On the right: warm/cold via grading, on the left a similar effect done editing lights.
Unlike in movies and photography for us it's trivial to

Why did we push everything to the last stage of our graphics pipeline? I believe if in photography or movies there was the possibility of changing the world so cheaply, if they had the opportunities we do have, they would exploit them immediately.


Gregory Crewdson


[change the colors of all the lights](http://blog.maxwellrender.com/tips/multilight-everyones-favorite/)(or even of all the materials). We can manipulate subsets of these, hierarchically, by semantic, locally in specific areas, by painting over the world, interpolating between different variants and so on...Why did we push everything to the last stage of our graphics pipeline? I believe if in photography or movies there was the possibility of changing the world so cheaply, if they had the opportunities we do have, they would exploit them immediately.

![]() |

Many of these changes are "easy" as they won't impact the runtime code, just smarter ways to organize properties. Many pipelines are even pushing towards parametric

[material libraries and composting](http://blog.selfshadow.com/publications/s2013-shading-course/rad/s2013_pbs_rad_notes.pdf)for

[texture](http://quixel.se/dev/ddo)

[authoring](https://www.allegorithmic.com/products/substance-painter), which would make even bulk material edits possible without breaking physical models.







*P.S.*

*A possible concern when thinking of light manipulation is that as the results are more realistic, it might be less appropriate for dynamic changes in game (e.g. transitions between areas). Where grading changes are not perceived as changes in the scene, lighting changes might be, thus potentially creating a more jarring effect.*



*It might seem I'm very critical of our industry, but there are reasons why we are "behind" other medias, I think. Our surface area is huge, engineers and artists have to care about developing their own tools -while using them-, making sure everything works for the player, make sure everything fits in a console... We're great at these things, there's no surprise then that we don't have the same amount of time to spend thinking about game photography. Our core skills are different, the game comes first.*

## 5 comments:

re: distortion


You are thinking too much into Spielberg & Kaminsky's idiosyncrasies. It's just the look ot Hawk anamorphics. Also, a bit of a countar-thesis choice of film to criticize for grading. It is one of the most distinctively stylized films in terms of lighting (that is, stylized in production as opposed to stylized in post) from last year. :)

sorry to say but we will have to continue f0ing with the image quality to simulate cheap cameras because getting the quality rendering needed to make them useless is a long ways off. What I mean is that until we can render images that are of the same quality as a pixar or live action film, we will have to resort to 'cheap' tricks to fool the eye into thinking what they are looking at is 'real'.

cpc: I don't believe that such an evident image effect is accidental, or just a limitation of technology (and if so it could have been easily corrected in post). I've read a bit more, googled a bit, and yeah you're right on the anamorphic lens choice, but apparently it was a conscious choice to use a lens that would produce distortion at the edges. I'll replace "grading" with "color choices" in the text because you're right, I went to fast there and I didn't really pay much attention to which techniques were used in the movie. Even if I personally don't love the "color coding" with cold hues used so literally to highlight a good half of the movie, it wasn't my intention to use it as a prime example of "bad grading", at all. It was literally a movie that I happened to see that made me think again of certain topics and wanted to write the post... If I have to think of movies with horrible grading the first that comes to mind is the expendables (it might have been the second or third even), that almost drove me color-insane :)

Lucas Granito: maybe, that is partially an answer, for example film grain might be good to break the geometric edges (trading aliasing for noise...) and so on. But even if that was the case, we don't need to resort to literal emulation of other medias, we could come up with better ways to introduce stylization or other "distractions", to fool the brain, that are better than just using aberrations from traditional cameras... Moreover, if even we wanted just to copy we're not really doing a great job at it.



But also I don't believe that's always the case, many times, maybe even most, it's just that we don't have a strong -reason- behind the choices we make, and so we just wander adding layers and layers of stuff, just bit by bit until it becomes a monster :) It happens often even in other art forms.

Some time ago there was even a small "colorgate" over Battlefield, with a mod that removed grading (there are many, for most games), that gained enough popularity to almost made EA offer it as an option, IIRC.

Yeah I agree there are many ways.. And that we shouldn't just 'throw' cheap tricks at the image.


RE: Colorgate.. Oh man.. I've fought so many times against grading. Maybe it's a taste thing but most Art Directors I've met love it. I hate how it kills information and makes eyes bleed. But not as much as I hate additive blending without tone-mapping. That's just.. nope.

Post a Comment