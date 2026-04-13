---
title: WebSocket disabled in Firefox 4 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/12/websockets-disabled-in-firefox-4/
author: Chris Heilmann
published: '2010-12-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Recent discoveries found that the protocol that Websocket works with is vulnerable to attacks. Adam Barth [demonstrated some serious attacks against the protocol](http://www.ietf.org/mail-archive/web/hybi/current/msg04744.html) that could be used by an attacker to poison caches that sit in between the browser and the Internet.

This is a serious threat to the Internet and Websocket and not a browser specific issue. The protocol vulnerabilities also affect Java and Flash solutions. In a web environment that could for example mean that a widely used JavaScript file – like Google analytics – could be replaced on a cache you go through with a malware file. Google would not be to blame and it would be hard for you to trace where the file is from as it will not be on your server. To avoid a lot of malware showing up without being easily traceable we need to fix the protocol.

## No Websocket support in Firefox 4 and Opera until the security issues are fixed

That’s why we’ve decided to [disable support for WebSocket in Firefox 4](https://bugzilla.mozilla.org/show_bug.cgi?id=616733), starting with beta 8 due to a protocol-level security issue. Beta 7 of Firefox has support for the -76 version of the protocol, the same version that’s included with Chrome and Safari. Beta 8 of Firefox 4 will remove that support. Anne van Kesteren of Opera [also announced that Opera are dropping Websocket support](http://annevankesteren.nl/2010/12/websocket-protocol-vulnerability). We are confident that other browser developers will follow.

## What does this mean for developers?

Right now, your Websocket solutions will not work in Firefox 4 final. Once we have a version of the protocol that we feel is secure and stable, we will include it in a release of Firefox – even a minor update release. The code will remain in the tree to help development, but will only be activated when a developer sets a hidden preference in Firefox (the same applies to Opera).

If your code does proper object detection nothing should go wrong – when a user doesn’t have Websocket enabled the `window.WebSocket`

property will not be available.

## Working on a fix

Mozilla is still excited about what WebSocket offers and we’re working hard with the IETF on a new WebSocket protocol.

Right now we are pushing the boundaries of what browsers can do for their users – this is what HTML5 is about.

Whenever you push the boundaries of any technology you will run into issues. The great thing about our situation right now is that we can react quickly and swiftly to any issues arising and fix them before our end users are the ones who suffer. Making the whole world upgrade and patch a final browser is almost impossible which is why it makes sense to test and patch in betas and nightlies.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 47 comments

Matt RanneyDecember 8th, 2010 at 18:00John HaugelandDecember 8th, 2010 at 19:19WulfTheSaxonDecember 9th, 2010 at 00:20Henri SivonenDecember 9th, 2010 at 02:47BillyDecember 16th, 2010 at 14:29Sasha AickinDecember 8th, 2010 at 21:38Sasha AickinDecember 8th, 2010 at 21:41Kyle KDecember 8th, 2010 at 21:54Unni V ManaJanuary 3rd, 2011 at 22:30Marco PivettaDecember 9th, 2010 at 01:08wduDecember 9th, 2010 at 02:42Ruud PoutsmaDecember 9th, 2010 at 03:17lapc506January 8th, 2011 at 10:04MontanaFebruary 7th, 2011 at 07:06Michael C.June 22nd, 2011 at 19:16hmmmDecember 9th, 2010 at 03:25Danny MoulesDecember 9th, 2010 at 06:17Mark RoggenkampDecember 9th, 2010 at 06:39Daniel EnnisDecember 9th, 2010 at 07:19Martyn LoughranDecember 9th, 2010 at 08:09Jon NealDecember 9th, 2010 at 08:23qweDecember 9th, 2010 at 14:04dssDecember 9th, 2010 at 14:59Yuri AgenniDecember 9th, 2010 at 17:16ben porterDecember 9th, 2010 at 18:33MRKDecember 10th, 2010 at 08:35Ruhsen KahramanDecember 11th, 2010 at 03:09jonathan ChetwyndDecember 12th, 2010 at 14:29Olav KolbuDecember 14th, 2010 at 07:01TJ VanderpoelJanuary 11th, 2011 at 13:52WulfTheSaxonJanuary 11th, 2011 at 16:25James BJanuary 23rd, 2011 at 12:38James BJanuary 23rd, 2011 at 12:40QuizoriFebruary 21st, 2011 at 03:07the futureFebruary 28th, 2011 at 16:55ZequezMarch 23rd, 2011 at 19:24whatdoesitwantMarch 30th, 2011 at 12:00WulfTheSaxonMarch 31st, 2011 at 08:36whatdoesitwantApril 1st, 2011 at 07:30AikarApril 1st, 2011 at 15:30mcApril 19th, 2011 at 14:29DAlDoApril 23rd, 2011 at 15:35KristjanMay 10th, 2011 at 06:22José Angel YánezJune 13th, 2011 at 16:50viktorJuly 1st, 2011 at 04:52TomAugust 20th, 2011 at 11:41sagaAugust 31st, 2011 at 14:42