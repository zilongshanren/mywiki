---
title: 'Nick Levine’s cl-log rocks… :: nklein software'
url: http://nklein.com/2012/12/nick-levines-cl-log-rocks/
author: Pat
published: '2012-12-10'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

Whenever I need logging in my Common Lisp applications, I use Nick Levine’s [cl-log](http://www.nicklevine.org/cl-log/) library. For many applications, spending the time to run `CL:FORMAT`

during runtime is unreasonable. It is often much better to log something in a raw form and do any formatting/presentation offline rather than online. The cl-log library is the only one that I know of which supports binary logging readily.

Additionally, Nick is incredibly responsive. I found an oversight in a corner-case of cl-log last Friday at 1am. I emailed him about it at 1:19am. In under 5 hours, I had email back pointing me to a new release with that case corrected.

I hope to do a more complete comparison of the existing log libraries at some point. At this point, know that I’ve tried all of the ones on the Cliki which had obvious documentation or examples, and I’ll be using cl-log.