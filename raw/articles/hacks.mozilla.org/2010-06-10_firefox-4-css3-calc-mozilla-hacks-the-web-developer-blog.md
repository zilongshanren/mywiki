---
title: 'Firefox 4: CSS3 calc() – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2010/06/css3-calc/
author: Paul Rouget
published: '2010-06-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This article describes the CSS3 calc() value. This feature hasn’t landed yet in any Firefox tree but work to implement it is underway.*

Firefox will support the CSS `calc()`

value, which lets you compute a length value using an arithmetic expression. This means you can use it to define the sizes of `div`

s, the values of margins, the widths of borders, and so forth.

Here is an example of a layout which would be tricky to setup without the `calc()`

function:

```
/*
* Two divs aligned, split up by a 1em margin
*/
#a {
width:75%;
margin-right: 1em;
}
#b {
width: -moz-calc(25% - 1em);
}
```

This example makes sure an input text field won’t overlap its parent:

```
input {
padding:2px;
border:1px solid black;
display:block;
width: -moz-calc(100% - 2 * 3px);
}
```

One particularly powerful feature of the `calc()`

function that you can combine different units in the same computation:

`width: -moz-calc(3px + 50%/3 - 3em + 1rem);`

The current implementation supports the `+`

,` -`

, `*`

, `/`

, `mod`

, `min`

, and `max`

operators.

We’ll also support the `min()`

and `max()`

functions, which could be used like this:

```
div {
height: -moz-min(36pt, 2em);
width: -moz-max(50%, 18px);
}
```

For more details, see:

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 112 comments

Gary van der MerweJune 10th, 2010 at 05:39iGELJune 10th, 2010 at 05:48DanJune 10th, 2010 at 13:07djmichaelbJune 10th, 2010 at 15:32DavidJune 10th, 2010 at 20:22ChemikkJune 10th, 2010 at 05:49Nicholas WilsonJune 10th, 2010 at 05:50Florent V.June 10th, 2010 at 06:14Florent V.June 10th, 2010 at 06:17Wladimir PalantJune 10th, 2010 at 06:38Marcio B D AJune 10th, 2010 at 06:47John GriffithsJune 10th, 2010 at 07:47Eli GreyJune 10th, 2010 at 08:38LachuJune 10th, 2010 at 09:07LachuJune 10th, 2010 at 09:08PietervJune 10th, 2010 at 09:14Ivan EnderlinJune 10th, 2010 at 09:49IliaJune 10th, 2010 at 10:42J. WeirJune 10th, 2010 at 10:59LachuJune 11th, 2010 at 09:23T RasmussenJuly 19th, 2010 at 07:07BTreeHuggerJune 10th, 2010 at 11:30BrianJune 10th, 2010 at 11:56ChrisJune 10th, 2010 at 13:45RasmusJune 10th, 2010 at 14:31voracityJune 10th, 2010 at 21:51Ms2gerJune 10th, 2010 at 12:18Alishah NovinJune 10th, 2010 at 12:42LachuJune 11th, 2010 at 09:31DavidmoreenJune 10th, 2010 at 12:59Zach BaileyJune 10th, 2010 at 13:21Herberth AmaralJune 10th, 2010 at 13:27Y-LoveJune 10th, 2010 at 13:59badanalogistJune 10th, 2010 at 14:00marioJune 10th, 2010 at 14:21AnonJune 10th, 2010 at 14:24Alex PennyJune 10th, 2010 at 14:40Thierry KoblentzJune 10th, 2010 at 14:58Oscar GodsonJune 10th, 2010 at 15:07Magne AnderssonJune 11th, 2010 at 01:44Matias LarssonJune 11th, 2010 at 04:46Matthew WJune 10th, 2010 at 15:46indieJune 11th, 2010 at 02:24unscriptableJune 10th, 2010 at 16:49Magne AnderssonJune 11th, 2010 at 04:00Sumanth NelluruJune 10th, 2010 at 17:42Erik KallevigJune 10th, 2010 at 17:49Georg SausJune 10th, 2010 at 18:10hovaJune 10th, 2010 at 19:17RobJune 10th, 2010 at 20:01DanielJune 10th, 2010 at 20:16JoshJune 11th, 2010 at 09:00DanielJune 14th, 2010 at 22:54JoshJune 15th, 2010 at 05:40Sam WatkinsJune 10th, 2010 at 20:26Thierry KoblentzJune 10th, 2010 at 21:50KlamsiJune 11th, 2010 at 00:18Russell BishopJune 11th, 2010 at 02:11Frédéric DelormeJune 11th, 2010 at 02:41Marco JardimJune 11th, 2010 at 03:26RobJune 11th, 2010 at 03:30SamJune 11th, 2010 at 04:33Magne AnderssonJune 15th, 2010 at 01:32LindaJune 18th, 2010 at 01:07El_HoyJune 11th, 2010 at 05:12AllanJune 11th, 2010 at 06:33Vladimir CarrerJune 11th, 2010 at 08:06ThanyJune 11th, 2010 at 08:08DavidJune 14th, 2010 at 22:55ThanyJuly 19th, 2010 at 23:49okonomiyaki3000February 15th, 2011 at 21:56Magne AnderssonJune 15th, 2010 at 01:31LachuJune 11th, 2010 at 09:27HBJune 11th, 2010 at 09:44nemoJune 11th, 2010 at 11:03carolJune 13th, 2010 at 08:07Magne AnderssonJune 13th, 2010 at 10:03@acarbackJune 16th, 2010 at 09:50Drum BoomJune 18th, 2010 at 01:15Magne AnderssonJune 18th, 2010 at 02:04Drum BoomJune 18th, 2010 at 08:45Magne AnderssonJune 18th, 2010 at 08:51Drum BoomJune 18th, 2010 at 09:37Magne AnderssonJune 18th, 2010 at 09:51Drum BoomJune 16th, 2010 at 22:14Magne AnderssonJune 18th, 2010 at 02:04ArnoldJune 17th, 2010 at 05:53Magne AnderssonJune 18th, 2010 at 02:02RyanJuly 19th, 2010 at 19:29DanJune 18th, 2010 at 08:01Magne AnderssonJune 18th, 2010 at 08:47DanJune 18th, 2010 at 09:49BorisJune 24th, 2010 at 09:56tbxJune 20th, 2010 at 04:25WitekJune 22nd, 2010 at 06:50nemoJune 23rd, 2010 at 18:46reneJuly 7th, 2010 at 16:08Darrell EstabrookJuly 8th, 2010 at 07:35DanJuly 10th, 2010 at 02:25Ant GrayJuly 11th, 2010 at 00:08StevoSeptember 1st, 2010 at 07:54ivanhoeSeptember 6th, 2010 at 09:38AndySeptember 10th, 2010 at 03:46AndySeptember 10th, 2010 at 21:37josiApril 4th, 2012 at 00:38