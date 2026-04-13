---
title: 'Firefox 4 Beta: Latest Update is Here – Experimenting With Multi-touch – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2010/08/firefox4-beta3/
author: Paul Rouget
published: '2010-08-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*The latest Firefox 4 Beta has just been released (get it here). This beta comes with hundreds of bug fixes, improvements and multi-touch support for Windows 7 (see the release notes here). This article is about multi-touch support.*

[Felipe Gomes](http://felipe.wordpress.com/) is working on bringing [multi-touch support to web content](http://hacks.mozilla.org/category/multi-touch/). In this latest beta, we are experimenting with this new feature.

**Playing with MultiTouch, HTML5 and CSS3:**


*This video is hosted by YouTube and uses the HTML5 video tag if you have enabled it ( see here). YouTube video here.*

## Multi-touch Events

If you have a multi-touch capable display, [touch events](https://developer.mozilla.org/en/DOM/Touch_events) are sent to your web page, more or less like mouse events. Each input (created using your fingers) generates its own events:

`MozTouchDown:`

Sent when the user begins a screen touch action.`MozTouchMove:`

Sent when the user moves his finger on the touch screen.`MozTouchUp:`

Sent when the user lifts his finger off the screen.

## Touch information

Touch events provide several useful properties.

`event.streamId:`

don’t forget, it’s**multi**-touch, which means that you have to deal with several events from several sources. So each event comes with an**id**to identify the input.`event.mozInputSource:`

the type of device used (mouse, pen, or finger, if the hardware supports it). This is a property of mouse events.`event.clientX/Y`

: the coordinates.

## Designing a touch UI

You might want to have a specific UI for multi-touch capable devices. You can use the `:-moz-system-metric(touch-enabled)`

pseudo class or the `-moz-touch-enabled`

media query to design a more finger friendly UI.

**Note: **For now, this feature only works with Windows 7. If you don’t have hardware that supports multi-touch, you can try Hernan’s [multi-touch simulator](https://addons.mozilla.org/en-US/firefox/addon/214783/).

## More joy:

(This video is made by Felipe, see more [here](http://vimeo.com/13991139)).

At the beginning of the video, you see how a webpage can get data about multi-touch input, correctly track points of contact and differentiate between touch input and pen input.

At the second part, you see a visual application of multi-touch input on a fluid simulator, where each point of contact adds a particle source, and the movement adds forces to the field.

Both parts use HTML5’s canvas element to render their content.

**Like it?**

**Edit:** If you want more details, take a look at [Felipe’s latest blog post](http://felipe.wordpress.com/2010/08/11/multitouch-in-firefox4/).

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 31 comments

SirquiniAugust 11th, 2010 at 20:09Ivan EnderlinAugust 12th, 2010 at 00:10AliAugust 12th, 2010 at 00:36Paul NeaveAugust 12th, 2010 at 03:35AnonAugust 12th, 2010 at 06:00SamAugust 19th, 2010 at 08:43Derek KAugust 12th, 2010 at 06:49Cody RussellAugust 12th, 2010 at 12:02PaulAugust 13th, 2010 at 02:19Marco PivettaAugust 12th, 2010 at 14:13Jamie BrightmoreAugust 13th, 2010 at 02:23noneAugust 13th, 2010 at 09:58DavidAugust 16th, 2010 at 06:51Bhupesh PranamiAugust 16th, 2010 at 23:30Hans Bernhard LungAugust 21st, 2010 at 16:10Joachim ThomasAugust 29th, 2010 at 04:56MithunSeptember 3rd, 2010 at 12:41PHANTOMIASSeptember 10th, 2010 at 05:25James CarringtonSeptember 23rd, 2010 at 11:13Lars KnudsenOctober 15th, 2010 at 08:39Chris KilgoreOctober 2nd, 2010 at 09:23bernhardOctober 17th, 2010 at 11:35bungaNovember 8th, 2010 at 19:18Ashley SheridanMarch 29th, 2011 at 02:46petrikMarch 11th, 2011 at 20:06BrianApril 22nd, 2011 at 08:41Dilan From Sri LankaMay 2nd, 2011 at 22:51ArtemSeptember 20th, 2011 at 11:51Luca BishopOctober 18th, 2011 at 00:50FedericoDecember 5th, 2011 at 07:41StevenOctober 4th, 2012 at 11:43