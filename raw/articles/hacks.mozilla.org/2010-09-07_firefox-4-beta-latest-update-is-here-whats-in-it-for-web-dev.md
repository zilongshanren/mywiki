---
title: 'Firefox 4 Beta: Latest update is here — what’s in it for web developers? –
  Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2010/09/firefox4beta5/
author: Paul Rouget
published: '2010-09-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [latest Firefox 4 Beta](http://firefox.com/beta) has just been released. Here is a quick overview of the new features for web developers.

**Hardware acceleration for Windows Vista/7 (via Direct2D) has been activated.**[Demo and explanations are in a previous post](https://hacks.mozilla.org/2010/09/hardware-acceleration/)(see screencast below).**The**[Audio Data API](https://wiki.mozilla.org/Audio_Data_API)is now available. See[David’s blog post](http://vocamus.net/dave/?p=1148)(see screencast below) and[try the audio demo](http://videos.mozilla.org/serv/blizzard/audio-slideshow/)(better if[WebGL activated](http://learningwebgl.com/blog/?p=11)).- Firefox 3.6.9 and Firefox 4 will support
`X-FRAME-OPTIONS`

(a HTTP header to declare the web page as non-embeddable in an iframe).[Read the details.](http://michael-coates.blogspot.com/2010/08/x-frame-option-support-in-firefox.html) - You can use another HTTP header,
`Strict-Transport-Security`

, to force your website to use HTTPS.[I’ve talked about this feature before.](https://hacks.mozilla.org/2010/08/firefox-4-http-strict-transport-security-force-https/) - We now allow calling
`click()`

on a`input type="file"`

(from a user action, like a click on another button).[See the related Bugzilla ticket](https://bugzilla.mozilla.org/show_bug.cgi?id=36619). - We also significantly improved our support of HTML5 WebForms: more inputs types (email, url, tel, search) new attributes (placeholder, autofocus), decoupled forms and different validation mechanisms.
*Details coming soon.*

David’s Audio API demo:


([try the audio demo ](http://videos.mozilla.org/serv/blizzard/audio-slideshow/))

Myself about Hardware acceleration:


([try the hardware acceleration demo ](https://developer.mozilla.org/media/uploads/demos/p/a/paulrouget/8bfba7f0b6c62d877a2b82dd5e10931e/hacksmozillaorg-achi_1334270447_demo_package/HWACCEL/))

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 10 comments

RyanSeptember 7th, 2010 at 18:24Anthony RicaudSeptember 8th, 2010 at 04:52Martin KliehmSeptember 7th, 2010 at 23:04jswisherSeptember 8th, 2010 at 15:06Wladimir PalantSeptember 8th, 2010 at 03:29Paul RougetSeptember 8th, 2010 at 03:58voracitySeptember 8th, 2010 at 05:18voracitySeptember 8th, 2010 at 05:29Christopher BlizzardSeptember 9th, 2010 at 09:02vinayOctober 11th, 2010 at 06:51