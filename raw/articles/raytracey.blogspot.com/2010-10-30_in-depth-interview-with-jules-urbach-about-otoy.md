---
title: In-depth interview with Jules Urbach about OTOY
url: http://raytracey.blogspot.com/2010/10/in-depth-interview-with-jules-urbach.html
author: Sam Lapere
published: '2010-10-30'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

An anonymous reader of my blog, called RC, (yes, there are actually people who read my blog ;-) pointed me to this very interesting interview with Jules Urbach conducted by Research 2.0:

Many thanks for this, RC!


Some very interesting excerpts from the interview:


The greater efficiency for rendering games in the cloud when using ray tracing could be the killer argument to start using ray tracing instead of rasterization (besides the simplicity of the code and the greater realism)!


OTOY's patnership with AMD, Nvidia and Intel:


and about unbiased rendering:


[http://www.research2zero.com/Resources/Documents/R2%20Thought%20Leader%20Interview%20OTOY%20Sept%202010.pdf](http://www.research2zero.com/Resources/Documents/R2%20Thought%20Leader%20Interview%20OTOY%20Sept%202010.pdf)Many thanks for this, RC!

Some very interesting excerpts from the interview:

We can run 48 first person shooters at 60 fps on a single 1U server through ORBX. That is with legacy games that have not been optimized for our service (i.e. games that we run out of the box, without any modifications). When developers target our platform (through tools such as our raytracing pipeline), concurrent usage gets closer to 100 users per GPU. That is before you factor in local rendering power offloaded on the client.

The greater efficiency for rendering games in the cloud when using ray tracing could be the killer argument to start using ray tracing instead of rasterization (besides the simplicity of the code and the greater realism)!

OTOY's patnership with AMD, Nvidia and Intel:

SW: OTOY has been working closely with AMD. What are the major advantages of AMD’s technology relative to Nvidia and Intel?

JU: We were very deliberate in choosing to go down this path with AMD. We tested early versions of ORBX on Nvidia GPUs, x86 CPUs, and AMD GPUs. We settled on CAL as our core development platform (CAL is AMD‟s low level computing language). It was very challenging to program a GPU using CAL, which is not officially supported by AMD. But we were seeing amazing speeds which we could not replicate on other architectures.

As our company has evolved, so have our relationships with other major hardware vendors. This year, we‟ve added Intel and Nvidia as partners. More will follow. We announced Intel this summer. Obviously, we need CPUs on our servers as well as GPUs. And, in that respect, Intel has a very compelling offering. Intel is also developing hardware cards made from densely packed x86 cores which we may use in the future.

We are officially announcing our partnership with Nvidia in a few weeks. We have been working with them on a version of ORBX that will be deployed on Nvidia hardware in 2011. This is not trivial, given that ORBX‟s speed has, up until now, come from functionality that is specific to AMD hardware. But, from a practical perspective, we would be ignoring a significant portion of the professional graphics market if we didn‟t support CUDA applications. Adobe Photoshop, CS5, and countless other apps only support CUDA.

and about unbiased rendering:

Just as I see rendering moving towards an unbiased model that becomes as simple as photography, I can imagine high performance computing and software development becoming equally democratized.

## 2 comments:

Yes, of course you have readers! Here's another one. Had it translated from Hungarian, but the slides are English:



http://translate.google.ca/translate?u=http%3A%2F%2Fprohardver.hu%2Fhir%2F2014-re_minden_szamitasigenyes_program_felhoben_fu.html&sl=hu&tl=en&hl=&ie=UTF-8

RC - stands for Ray as well, but didn't want to confuse people. C is for Canada if you're wondering.

Thanks for the link Ray!


Just in case, my real name isn't Ray Tracey, it's just a pseudonym that I thought was funny for a blog about real-time ray tracing.

Post a Comment