---
title: A few details on Imagination's PowerVR GPU with Caustic Graphics hardware ray
  tracing
url: http://raytracey.blogspot.com/2011/09/few-details-on-imaginations-powervr-gpu.html
author: Sam Lapere
published: '2011-09-27'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A few days ago, an article appeared on the Japanese website 4gamer.net about an in-development PowerVR GPU, the PowerVR RTX, which is said to have integrated ray tracing hardware from Caustic Graphics (acquired by Imagination Technologies in December 2010). The article is in Japanese, and the Google translated version is barely understandable:


[http://translate.google.com/translate?hl=en&sl=auto&tl=en&u=http%3A%2F%2Fwww.4gamer.net%2Fgames%2F017%2FG001762%2F20110920023%2F](http://translate.google.com/translate?hl=en&sl=auto&tl=en&u=http%3A%2F%2Fwww.4gamer.net%2Fgames%2F017%2FG001762%2F20110920023%2F)

## 6 comments:

i never understood what Caustic hardware was.

Neither have I, they are very shady about their patented hardware. Apparently it does some kind of sorting of incoherent rays into more or less coherent batches and feeds those to the GPU for shading. They also invented a novel efficient-to-rebuild acceleration structure for dynamic ray tracing, but it's not clear how fast ray traversal is.


If the Caustic hardware ever becomes reality, it's going to be interesting to compare performance of Brazil 3.0 against state-of-the-art GPU path tracers like Octane on the GPUs of that time. As far as I've read on the Splutterfish forums, even with biased rendering Brazil 3.0 is going to be slower than unbiased GPU path tracers.

Apparently Sega has already signed this chip for forthcoming arcade board and console -


http://s3gal3aks.wordpress.com/

You should not believe a thing written on Segaleaks. The author is making up articles using snippets from scientific ray tracing papers, see


http://raytracey.blogspot.com/2011/02/some-details-about-new-powervr-gpu-with.html

I think that Japanese site is a bit unreliable. I think it was fooled by the whole "RTX" name that was spread around by Zach Morris and his many different account names.



I never seen anywhere else where the name "RTX" has been mentioned.

Another issue: Zach is famous for stealing things off other sites. Hell, he copied a bunch of forum posts and posted it as a "opinion peice" and left the word "Jewtendo" at the end. Shows what kind of person this Zach "person" really is.

Thanks for pointing this out. I think I've learned my lesson now, never trust any news about Caustic Graphics or GPUs incorporating Caustic products. According to Caustic, the CausticTwo should have been out last year, but it has just vanished into thin air.

Post a Comment