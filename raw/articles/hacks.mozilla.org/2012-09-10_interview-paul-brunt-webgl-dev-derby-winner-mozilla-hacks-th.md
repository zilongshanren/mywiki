---
title: 'Interview: Paul Brunt, WebGL Dev Derby winner – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2012/09/interview-paul-brunt-webgl-dev-derby-winner/
author: John Karahalis
published: '2012-09-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Paul Brunt](http://www.paulbrunt.co.uk/) won the [WebGL Dev Derby](https://developer.mozilla.org/demos/devderby/2012/june) with [SnappyTree](https://developer.mozilla.org/demos/detail/snappytree), his incredibly powerful (and even a little addicting) 3D tree designer. SnappyTree provides a wonderful example of what we can do with the Web today — it even has an export function for using your trees in native applications (move over Blender), not that we will need native 3D applications if progress like this continues.


*Recently, I had the opportunity to learn more about Paul and his work. In our interview, Paul shared thoughts on the past, present, and future of web development and gave advice relevant to developers of all levels of experience.*

## The Interview

### How did you become interested in web development?

I first became interested in web development in the late 90’s when I went on the internet for the first time. After a little bit of browsing around the web I thought I’d have a go at making a site myself. With the free space provided by the ISP and with a little assistance from Frontpage I managed to put together something you might tentatively call a website. Unfortunately that first site was short lived, the result of an accidental deletion. But, the seed had been planted so I built another, then another, then somewhere along the way I ended up doing it for a living.

### Tell us about developing SnappyTree. Was anything especially exciting, challenging, or rewarding?

It had taken a few days of coding before I was in the position to start drawing anything to the screen. So, the most exciting part was seeing something that resembled a tree appear in the browser for the first time; although it wasn’t much to look at, and there were very obviously issues.

Getting skinning working correctly was extremely challenging; there where many horrible branch twisted iterations while trying to get it right, but I’m pretty happy with the end result.

### Can you tell us a little about how SnappyTree works?

Snappy Tree works by taking an initial branch (the trunk) which then splits into two new branches. The direction of these new branches is determined by several user configurable factors symmetry, droopyness, etc. This process is repeated N times to produce the basic tree structure.

After the basic tree has been constructed a skin in generated around the branches before finally adding planes at the ends of the branches which are used for leaves and twigs. The final mesh data is then piped into Webgl for rendering and used to generate the collada or wavefront files for export.

### What makes the web an exciting platform for you?

Increasingly it seems to be getting quicker and easier to develop for the web than any native platform, so I think the current rate of progress is the most exciting part. With so many new technologies emerging seeing how developers use them is always fun and often downright awe inspiring.

### What up-and-coming web technologies are you most excited about?

I think the most exciting thing emerging right now is [WebRTC](https://hacks.mozilla.org/2012/04/webrtc-efforts-underway-at-mozilla/). I’m really looking forward to seeing what uses developers can come up with. I can see a lot of potential outside of the obvious and it’s going the be a lot of fun discovering interesting uses for it.

### If you could change one thing about the web, what would it be?

There are lots of little things I’d love to tweak in [CSS](https://developer.mozilla.org/docs/CSS) and [HTML](https://developer.mozilla.org/docs/HTML); but, if it’s limited to just one thing I think I would change the “www.” convention. It’s difficult to pronounce, takes far too long to say and just sounds horrible.

### What advice would you give to aspiring web developers?

Jump in the deep end and be ambitious. The best way to learn a new technology is to start a project around that technology. Even if you haven’t got a clue what you’re doing when you start you certainly will by the end.

## Further Reading

[Mozilla and Games: Pushing the Limits of What’s Possible](https://hacks.mozilla.org/2012/08/mozilla-and-games-pushing-the-limits-of-whats-possible/)[WebRTC efforts underway at Mozilla!](https://hacks.mozilla.org/2012/04/webrtc-efforts-underway-at-mozilla/)[The Great Dub-Dub-Dub Debate](http://www.codinghorror.com/blog/2008/04/the-great-dub-dub-dub-debate.html)