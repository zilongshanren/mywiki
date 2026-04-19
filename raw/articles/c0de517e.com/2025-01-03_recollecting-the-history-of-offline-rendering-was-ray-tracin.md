---
title: Recollecting the history of offline rendering.Was ray-tracing "early" and path-tracing
  "late"?
url: https://c0de517e.com/018_rthistory.htm
author: Angelo Pesce
published: '2025-01-03'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

I went a bit on a bend a few days ago trying to dig information about the evolution of offline rendering software. I remember most of it, at least, the stuff you could know outside the secrets of

[proprietary movie studio software](https://www.awn.com/mag/issue2.2/articles/ohmerblue2.2.html) of which my teenage self wasn't privy at the time - but for some reason, I couldn't recall the point when path tracing made it "to the masses". Who started that first?

BTW, this is a bit of a pattern for me (perhaps everyone?). I remember clearly my c64 days as a kid, I remember playing with an 8086 that my uncle had, I bought then an Amiga 600 after playing with one that a cousin of mine had, during a vacation - and I remember my first PC, an original IBM ps/2 486sx. The "sx" there is very important as it precluded me from toying with some 3d software that required a math coprocessor (albeit, there were some software emulators that did work at times).

In general, up to about Windows 9x/nt4 (for a while I was running both, using it for graphics apps and 9x for games) my memory is decent. Past that, it's a blur... I changed so many graphics cards, motherboards, CPUs, OSes, etc - I don't know what was running when and where...

Anyhow - this is what I reconstructed from memory and a bit of research. I posted it initially as a

[journal entry](https://c0de517e.com/JOURNAL/log_003.htm#38), but as it has been confirmed since by a few prominent people in the industry, I moved it to the main blog...

**- The early days.**
In the early days (late eighties, early nineties) of offline rendering raytracing was king, especially in the hobbyist space. I guess this is because RT is relatively simple to implement (albeit a bit annoying when you don't have hardware floats...) but yields incredible results - slowly.

![The iconic "amiga juggler" by Eric Graham.](../../assets/1db9c7ccb52fd5a6.png)

The iconic "amiga juggler" by Eric Graham.
[PovRay](https://www.povray.org/) was the poster child of amateur rendering - but there were many others, all similarly employing a scripting language to model scenes and procedural texturing (I was fond of Vivid myself). It was not uncommon for people to compare PovRay favorably against production renderers - in the misguided way that makes people compare feature lists instead of understanding what are the needs of artists. PovRay is a "toy" renderer, but an incredibly fun one.

![Gilles Tran, PovRay. www.oyonale.com](../../assets/cb79d9261d4c317a.png)

Gilles Tran, PovRay. www.oyonale.com
Some professional 3d software used "scanline" rendering (e.g. the o.g. 3d studio), hybrid (lightwave), or other rasterization methods (notably, Reyes in prman, and later on RenderMan compatible alternatives such as renderdotc, 3delight, aqsis, etc). But even for commercial packages raytracing was common - e.g. Imagine 3D (another favorite of mine...), Real 3D (I toyed with this on the Amiga, but could not understand anything about it), and Cinema 4D were all pure raytracers.

![Work by Eva Fontana, winner of Bit Movie '95. Imagine 3D afaik. Not the best scan, but it took me so long to find. Google and LLMs don't help with content this old!](../../assets/7af8cfee1407425c.png)

Work by Eva Fontana, winner of Bit Movie '95. Imagine 3D afaik. Not the best scan, but it took me so long to find. Google and LLMs don't help with content this old!
Interestingly, whilst the hobbyist raytracers were all about human-writeable scripting languages (e.g. modeling directly by editing the textual scene language), no professional software that I recall, other than prman, separated modeling from rendering. The two worlds did not talk to each other - was not even usual to export from commercial modelers to raytracers like povray - which were much more oriented toward high-level solid primitives than meshes and surfaces.

This might have been an example of how, early in technology cycles, integration is a better choice for the ability to innovate, as you don't want to be slowed down by standards and interfaces.

Notable was Larry Gritz's BMRT (1994 - first public release according to

[bmrt.org](https://web.archive.org/web/20000915084458/http://www.bmrt.org/bmrtstory.html)) which implemented the renderman spec in raytracing, was adopted by Pixar as a ray server for some shots of their movies (A bug's life, Toy Story 2). BMRT became Exluna's Entropy and was infamously killed by

[Pixar's (IMHO outrageously bogus) patent claims](https://www.latimes.com/archives/la-xpm-2003-aug-24-fi-pixar24-story.html).

**- The "radiosity" days.**
The next big step after raytracing was the advent of (indirect) global illumination: late 90ies/early 2000s. This is a time when "radiosity" was used to mean "indirect diffuse GI" or even just "indirect GI" in general (i.e. specular and diffuse) - even if in practice almost nobody was using the radiosity (finite elements) algorithm itself - especially outside architectural rendering software.

![The actual radiosity algorithm. Illustration by Hugo Elias - see www.jmeiners.com/Hugo-Elias-Radiosity/](../../assets/f0a53320e639c7ea.png)

The actual radiosity algorithm. Illustration by Hugo Elias - see www.jmeiners.com/Hugo-Elias-Radiosity/
This is where IMHO the history gets interesting. Because path tracing has been known since... forever. Kajiya's paper is from 86 - radiosity technically came earlier, in 84, but by now they are both old. Heck, the seminal

[thesis by Veach](https://www.reedbeta.com/blog/reading-veach-thesis/) which introduced Metropolis transport, bidirectional tracing, and MIS to the world was from 1997, and everybody read that!

Yet it seems that there were no widespread, public implementations of brute-force path tracing to solve the rendering equation.

The most reasonable assumption is that path tracing was "skipped" simply because it was too computationally expensive - but it is still puzzling, as this did not happen for raytracing which was certainly crazy expensive when it started to flourish in the eighties, on CPUs that did not even do floating point!

![Jensen's book came out in 2001. As influential as "PBRT" (2004)?](../../assets/0c1ee50ad854eaf5.png)

Jensen's book came out in 2001. As influential as "PBRT" (2004)?
I struggled to find early examples of path-tracing software - everyone jumped from recursive/distributed RT directly to biased light transport methods - most commonly photon mapping, final gathering, often with QMC sampling and

[irradiance caching](https://sgvr.kaist.ac.kr/~sungeui/SGA08/course_note/IC.pdf) - a setup that perhaps most famously was employed by MentalRay (Softimage, Maya, 3dsMax...).

Even Povray did the PM/IC combo, first with the popular MegaPov fork/patch, then in the official distribution (and to this day, that's pov's GI). I

[found a pure montecarlo fork](https://web.archive.org/web/20080619083615/http://pagesperso-orange.fr/fidos/MCPov/MCPov.html) of MegaPov from 2008, but I don't think it was ever popular. BTW - did you know that Marcos Fajardo also made

[a povray fork, back in the days?](https://web.archive.org/web/20021218103506/http://www.geocities.com/TimesSquare/2143/povafx10.html)
Timeline-wise, MentalRay's history starts in 1989 - around the same time BMRT was starting to be conceived - but the first big adopter was Softimage 3D in 1992 with v2.52 - and I don't know when it implemented GI. Keller's QMC papers were from 94 - and IIRC these were directly implemented in MentalRay - so it wouldn't be surprising if around that time MentalRay had GI.

Because GI was a big selling point at this time, it's actually not trivial to find the exact techniques the various software employed, they were kept often secret and touted as magical. This was a time when rendering software exploded, and everybody competed on their GI solution - most just called it "GI" or "radiosity".

Some examples of this were:

- Brazil R/s (2007? - photonmapping/qmc). Died after the acquisition by Caustic Graphics, one of the first companies making hardware accelerated raytracing, later acquired by PowerVR...

- Cebas FinalRender (2004?).

- VRay (also pm/QMC apparently) - still exists and is a widely used renderer today.

- Pantaleoni's Lightflow (~2000).

- Worley's FPrime (interactive/progressive rendering).

[This is a great list I remember browsing back in the days](https://www.pointzero.nl/renderers/), it's still online today (took me a while to find...). You can use the internet archive to see its evolution in time.

Notable also in 2002 is Parthenon https://cs.uwaterloo.ca/~thachisu/tdf2017.pdf - which did PM on the GPU!

It's not that unbiased methods were not actively being researched - even I was somewhat invested in trying to improve state-of-the-art (my master's thesis was on unbiased GI) - but IIRC the consensus at the time was that unbiased methods were mostly important to push forward academically as you could always add bias "later" to make them more practical.

And it didn't help I guess that academics were not publishing source code... In fact, behind the scenes, people were also cheating a bit - not all the "unbiased" images were truly so (I guess this is true today as well FWIW).

**- Unbiased Path Tracing.**
The final chapter is the path-tracing era, and it's the one we're currently in today for offline rendering today.

A bit component back then of the push towards path tracing was, in my recollection, the issues you had with "tuning" biased methods. For all its merits, it was not that trivial to get great images out of photon mapping/irradiance caching, and artists needed to fiddle with many parameters (of course, progressive photon mapping was not a thing then).

Even more frustrating - nothing was incremental and interactive - so you saw that the image was not right only at the end of the process, during the final gathering step.

The push towards "unbiased" could even be seen as the first step in what will become the push towards physically based rendering in the industry: removing hacks, unnecessary knobs, and tunables to both simplify art production, make content "universal" (e.g. decoupling materials from lighting) and being able to understand what rendering algorithms were doing right and wrong.

This will be a road walked together by real-time rendering (videogames -

[example...](https://c0de517e.blogspot.com/2011/09/fight-night-champion-gdc.html)) and offline (movies), btw, learning from each other.

As "radiosity" was a grossly misused term before, now "unbiased" will - everyone will start declaring to have "truly unbiased GI" - and chances are, nobody really is - nor should be. Unbiased is not per se good, same "physically-based", they are not objectives (at least, not outside academic pursuits) - better artists' workflows are.

![Sponza, via Indigo Renderer, 2006.](../../assets/b5eb810d5aaa9b25.png)

Sponza, via Indigo Renderer, 2006.
History-wise, this is what I found re. earliest and notable "public" path tracers:

-

[Arnold](https://sushideathrobots.github.io/) - was at least "known" in ~1999 (see

[here](https://www.3dluvr.com/marcosss/raditests.html) and

[here](https://news.povray.org/povray.general/thread/%3CiH08OXoMzWCbJzKLMsEe%3Dvx2H3Vr%404ax.com%3E/)) - but it feels much more contemporary because only in 2004 it got adopted (and then forked) by Sony and even later it started to become available to the general public and licensed to various 3D software.

- Indigo,

[2006, I think](https://www.flipcode.com/archives/12-13-2004_nc.shtml), was the first public release (free, and

[with an exporter for Blender!](https://web.archive.org/web/20060415155201/http://homepages.paradise.net.nz/nickamy/indigo.html)), but development, like with Arnold, started in the late 90ies.

- Maxwell Render, ~2004 using MLT, perhaps the first one to popularize/use in marketing the "unbiased" term and still considered one of the "most physically based" renderers.

-

[Sunflow, ~2005](https://sourceforge.net/projects/sunflow/) (java, opensource). The source code was quite easy to navigate, and it definitely inspired many.

-

[Phos, ~2004](https://web.archive.org/web/20040608032756/http://users.ntua.gr/jpanta/Phos/). Was notable as it implemented all kinds of monte-carlo light transport (i.e. bidirectional, MLT, etc) algorithms. It later became known as

[kerkythea](https://kerkythea.net/) and now "Thea".

-

[WinOSI, ~2001](https://web.archive.org/web/20160618132753/http://www.winosi.onlinehome.de/) (opensource). Famous for being extremely slow but also quite "accurate", it invented its own, kinda weird, light transport algorithms. Sort of a photon map, but with infinitesimal photons.

- PBRT (yes, the book...), ~2004. Won an Oscar, enough said :)

-

[Metropolight, 2004](https://web.archive.org/web/20040603111748/http://www.3dvirtualight.com/mlt/). This free experimental renderer, from the author of VirtuaLight, is a good example of what I wrote before. The "serious" VirtualLight was photonmapping and irradiance caching!

- Fryrender, ~2006 did path-tracing on the GPU!

I'm not sure who "wins" (i.e. was first) in this list - I can see that path tracing was being actively experimented with, even by some hobbyists or academic researchers publishing code, in the early 2000s. But at that point it seemed already "demystified" - the practice (implementations) were quite a bit behind the theory (academia).

It's truly interesting that we had people shooting rays randomly in the scene a decade prior - in photonmapping renderers - but it will take so long to start moving towards pure MC. I guess a combination of both having hardware that was finally powerful enough, starting to appreciate "time to first pixel" more than "time to final image", and the development of certain key tricks that were ignored or not widely publicized in papers, but were key to make the technique practical (e.g. clamping to avoid fireflies, denoising, variance reduction/IS, etc).

Note - the

["Path to Path-traced movies"](https://graphics.pixar.com/library/PathTracedMovies/paper.pdf) course also helps to reconstruct some history (albeit lots of the early development in movies happened in private, so it doesn't count towards our history here).

**- Conclusions.**
IMHO:

1) Raytracing came "early" (before it was realistically practical), path-tracing came "late" (could have been implemented "in public" earlier but was not) - even later than real-time raytracing in fact - e.g.

[Heaven Seven by Exceed](https://www.pouet.net/prod.php?which=5) was in 2000, and that was

[far from being the first RTR demo](https://realtimeradiosity.com/demos/)!

2) Everything comes and goes in waves - hype cycles.

This is good and bad. It's good that the hype makes a lot of people compete on an idea - which gets rapid development, and bad - when the idea is past diminishing returns but we don't go "wide" exploring other avenues.

True radiosity might have held back MC with the promise of computing a view-independent diffuse GI solution and the illusion that it would be better than working from the perspective of a single view. We probably wrote more primitive-based raytracers than "needed", definitely irradiance caching overstayed its welcome - but even the "unbiased" and "PBR" trends one can argue were pushed past their practical usefulness.

And only recently we went all-in on denoising (bring back the bias!), temporal reprojection (for real-time and previews), and now "path guiding" (which we knew at least since Jensen's "importons" but had not really been developed for decades).

Next, we're going to realize that we don't need to sample everything per every pixel, and we can interpolate instead? :)