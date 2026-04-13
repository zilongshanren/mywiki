---
title: First Beta release of Mozilla Persona – Login without Passwords – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2012/09/first-beta-release-of-mozilla-persona-login-without-passwords/
author: Ben Adida
published: '2012-09-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

For the past year, we’ve been rapidly improving [Mozilla Persona](https://persona.org) (previously BrowserID). Our goal is simple: we want to eliminate passwords on the Web. Today, after many iterations based on community implementation feedback, Persona enters Beta. This first beta means:

- we’ve produced and are committing to a
[much improved API](https://developer.mozilla.org/Persona) - the
[first-user experience](http://identity.mozilla.com/post/27914354400/improvements-to-the-first-time-sign-up-flow)is significantly improved and streamlined: it’s actually hard to get lost - critical new features, including support for showing your site’s
[name and logo](http://identity.mozilla.com/post/27122712140/new-feature-adding-your-websites-name-and-logo-to-the), as well as[terms of service and privacy policy](http://identity.mozilla.com/post/23038368841/streamlining-login-with-privacy-policy-and-terms-of), are live

Since the beginning, Mozilla Persona was designed to work across browsers. Our commitment to this continues: Persona Beta 1 supports [all major mobile, tablet, and desktop browsers](https://developer.mozilla.org/en-US/docs/persona/Browser_compatibility). In fact, we’re working to build an extensive library of automated regression tests across all browser platforms to ensure that this support remains rock solid as we continue to add features.

Persona is not just a great product, it’s also designed with the [Mozilla Values](http://www.mozilla.org/about/manifesto.en.html) in mind. When you deploy Persona on your web site (in an afternoon or, sometimes, only 15 minutes), you’re showing respect for your users and their data. You’re only asking for the data needed to log them in, and users know they’re only sharing exactly what’s shown on the screen.

The technology behind Persona is interesting in its own right. We’ve built and scaled Mozilla’s first serious [node.js](http://nodejs.org)-based service. We’ll be writing a few more posts on the specifics of our technology in the weeks and months to come. In the meantime, check out our [source code](https://github.com/mozilla/browserid), and join us on [email](https://lists.mozilla.org/listinfo/dev-identity) or [irc](irc://irc.mozilla.org:6667/identity).

And if you’re building or upgrading a web site, don’t forget to add Persona login support! Our [quick setup guide](https://developer.mozilla.org/en-US/docs/Persona/Quick_Setup) should help you get off the ground in minutes.

## 9 comments

louisremiSeptember 28th, 2012 at 02:54louisremiSeptember 28th, 2012 at 02:55nadimSeptember 30th, 2012 at 10:28Ben AdidaSeptember 30th, 2012 at 19:58NadimOctober 1st, 2012 at 01:31Ben AdidaOctober 1st, 2012 at 06:42thinsoldierOctober 1st, 2012 at 13:19LoriOctober 10th, 2012 at 20:33Robert NymanOctober 11th, 2012 at 03:51