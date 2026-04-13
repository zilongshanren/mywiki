---
title: Aurora 16 is out — Unprefixing time ! – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/07/aurora-16-is-out/
author: Jean-Yves Perrier
published: '2012-07-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Web developers, it is time to celebrate! In the upcoming Firefox 16, which reached the Aurora status today, a major enhancement is the unprefixing of several stable CSS features. Other notable features of interest to Web developers include several more HTML5-related APIs, better accessibility on Mac OS, and improvements to Firefox Developer Tools.


**So which CSS features are unprefixed?**

| Specification | Properties, functional notations, and at-rules | More information |
|---|---|---|
| CSS3 Animations | `animation` , `animation-name` , `animation-duration` , `animation-delay` , `animation-timing-function` , `animation-iteration-count` , `animation-direction` , `animation-play-state` , `animation-fill-mode` , `@keyframes` |
|

`transition`

, `transition-property`

, `transition-delay`

, `transition-duration`

, `transition-timing-function`

[Using CSS Transitions](https://developer.mozilla.org/En/CSS/CSS_transitions)`transform`

, `transform-origin`

, `transform-style`

, `backface-visibility`

, `perspective`

, `perspective-origin`

[Using CSS Transforms](https://developer.mozilla.org/En/CSS/Using_CSS_transforms)`linear-gradient()`

, `radial-gradient()`

, `repeating-linear-gradient()`

, `repeating-linear-gradient()`

[Using CSS Gradients](https://developer.mozilla.org/en/CSS/Using_CSS_gradients)`<a title="The CSS calc() function" href="https://developer.mozilla.org/en/CSS/calc">calc</a>()`

### Pay attention to the gradient syntax

While the syntax of CSS animations, transitions and transforms has not changed lately, that is not the case of the CSS gradients syntax, which is significantly different than in most prefixed implementations.

The definitive syntax for [linear gradients](https://developer.mozilla.org/en/CSS/linear-gradient) is :

`<linear-gradient> = linear-gradient(`

`[ [ <angle> | to <side-or-corner> ] ,]? <color-stop>[, <color-stop>]+ )`

`<side-or-corner> = [left | right] || [top | bottom]`


If we break it down, its structure is :

`linear-gradient( <em>direction</em> , <em>color-stop</em> )`


As the *color-stop* syntax hasn’t evolved lately, the *direction* parameter is where most of the latest changes happened.

The *direction* parameter can be defined either using a CSS [ <angle>](https://developer.mozilla.org/en/CSS/angle), or using the

`to`

keyword followed by one or two keywords describing the side or the corner.That’s the major change! This `to`

keyword wasn’t there before and it reverses the direction that was use previously: `-prefix-linear-gradient( top left )`

becomes `linear-gradient( to bottom right )`

.

Also the <angle> changed: before, `0deg`

pointed to the right; now it points, consistently with other angles in the CSS spec, to the top. Like this:

So here again, you need to change `-prefix-linear-gradient(0deg)`

to `linear-gradient(90deg)`

. Failure to adapt the angle will lead to the gradient to be oriented differently, like this:

![An horizontal blue-white gradient will suddenly become... An horizontal gradient, blue at the far left, white at the far right.](https://developer.mozilla.org/@api/deki/files/3951/=basic_linear_blueleft.png)

![... an vertical blue-white gradient A vertical gradient, blue at the top, white at the bottom](https://developer.mozilla.org/@api/deki/files/3950/=basic_linear_bluetop.png)


Similar changes have been made to the radial gradient syntax, with a newly introduced `at`

keyword.

**More HTML5 & friends goodies**

Unprefixing mature CSS features is not the only improvement in the area of supporting standards:

**IndexedDB**has reached Candidate Recommendation status and has been unprefixed too. This is amazing.- Support for the HTML5
landed.**Microdata API** - Support for the HTML5
element landed.`<strong><meter></strong>`

- We unprefixed the
.**Battery API** - We unprefixed the
.**Vibration API** - We improved our media queries support by adding support for the
`dppx`

unit. - The CSS properties
`height`

and`width`

are now animatable. - The CSS animations can be “
[reversed](https://developer.mozilla.org/en/CSS/animation-direction)“: the`reverse`

and`alternate-reverse`

keywords have been added. - Our implementation of JavaScript improved with several new features in Harmony (the maybe future EcmaScript 6):
- Support for
[direct proxies](http://wiki.ecmascript.org/doku.php?id=harmony:direct_proxies) - Support for the
`Array`

‘soperator`spread`

- Improvement of
, supporting now`Number`

`toInteger()`

,`isInteger()`

and`isFinite()`


- Support for
- Improvement of
`Keyboard`

(still prefixed as`mozKeyboard`

), now supporting`setSelectedOption()`

,`setValue()`

and`onfocuschange()`

.

### Accessiblity

A giant step has been done in making Firefox more accessible. Support for [ VoiceOver](http://www.apple.com/accessibility/voiceover/) on

**Mac OS**has landed. It was the last platform where our accessibility features where severely behind. This is very exciting for all people needing such features on the Mac.

[More information](http://www.marcozehe.de/2012/04/30/initial-voiceover-support-now-in-firefox-nightly-builds-for-mac-os-x/).

### Developers Tools

Last but not least, we continued to improved our developer tools!

Now you can toggle a developer toolbar: go to Tools > Web Developer > Developer Toolbar, or press Shift-F2. The toolbar itself looks like this:

The toolbar has a command line interface and also nice buttons to the right to quickly reach useful tools. The command line interface is easy to expand and more commands are expected in the future. Typing help in it displays the supported commands.

The Web Console also has been improved and displays now a nifty error count.

Finally our Scratchpad gained a list of recently opened files. Always convenient.

### Other notable changes

- We slightly
[changed](https://bugzilla.mozilla.org/show_bug.cgi?id=728831)our UA string not to display the 3rd digit of our versioning system. - Incremental GC, a major part in our effort to revamp our Garbage Collector, is now
[enabled by default](http://blog.mozilla.org/dmandelin/2012/07/20/incremental-gc-now-in-firefox-aurora/). - Opus, a low-latency codec aimed at real-time communication, is
[enabled by default](https://bugzilla.mozilla.org/show_bug.cgi?id=772341). - By default, we
[do not accept anymore](https://bugzilla.mozilla.org/show_bug.cgi?id=650355)MD5 hashes in X.509 certificates. `about:memory`

is now displaying[memory usage ‘per tab’](http://blog.mozilla.org/nnethercote/2012/07/11/memshrink-progress-week-55-56/).- We
[tweaked the context menu](http://msujaws.wordpress.com/2012/07/23/applying-hicks-law-to-the-firefox-context-menus/), removing the ‘Send link…’ item and combining the ‘Stop’ and ‘Reload’ ones.

See more details in the [release notes](http://www.mozilla.org/en-US/firefox/16.0a2/auroranotes/) and in [Firefox 16 for developers](https://developer-new.mozilla.org/en-US/docs/Firefox_16_for_developers).

### Conclusion

Firefox 16 is on the way to being a very strong release for Web developers, both on the support of standards, and with the nice improvements in our tools, maturing quickly. In the future, Web sites will be easier to do and more powerful!

## About Jean-Yves Perrier

Jean-Yves is a program manager in the Developer Outreach team at Mozilla. Previous he was an MDN Technical Writer specialized in Web platform technologies (HTML, CSS, APIs), and for several years the MDN Content Lead.

## 39 comments

Michael BeckwithJuly 20th, 2012 at 23:36WebUserJuly 21st, 2012 at 12:23Jean-Yves PerrierJuly 21st, 2012 at 12:41WebUserJuly 21st, 2012 at 13:36Jean-Yves PerrierJuly 21st, 2012 at 13:38pdJuly 22nd, 2012 at 00:58Jean-Yves PerrierJuly 22nd, 2012 at 01:02jonJuly 22nd, 2012 at 15:20Thomas S.July 23rd, 2012 at 07:30Jean-Yves PerrierJuly 23rd, 2012 at 07:35Jason NgJuly 23rd, 2012 at 09:40Jean-Yves PerrierJuly 23rd, 2012 at 09:53BinyaminJuly 23rd, 2012 at 13:08Jean-Yves PerrierJuly 23rd, 2012 at 13:52BinyaminJuly 23rd, 2012 at 14:03Jean-Yves PerrierJuly 23rd, 2012 at 14:23BinyaminJuly 23rd, 2012 at 22:52Jean-Yves PerrierJuly 23rd, 2012 at 22:55MonkeyHiteOctober 12th, 2012 at 10:29Jean-Yves PerrierOctober 12th, 2012 at 10:35BinyaminOctober 13th, 2012 at 14:20BinyaminOctober 13th, 2012 at 15:14BinyaminJuly 23rd, 2012 at 14:03Jason NgJuly 23rd, 2012 at 15:28Jean-Yves PerrierJuly 23rd, 2012 at 15:39Ishan Oshadi JayawardeneJuly 24th, 2012 at 06:40FJuly 24th, 2012 at 10:38Janet SwisherJuly 24th, 2012 at 10:47kiziJuly 26th, 2012 at 15:17Jean-Yves PerrierJuly 26th, 2012 at 21:05PeterJuly 29th, 2012 at 01:16Jean-Yves PerrierJuly 29th, 2012 at 01:17CiNiTriQsJuly 29th, 2012 at 03:11Pikadude No. 1August 14th, 2012 at 00:16Jean-Yves PerrierAugust 14th, 2012 at 00:26Pray For RainSeptember 28th, 2012 at 23:16Jean-Yves PerrierSeptember 29th, 2012 at 00:03alexNovember 20th, 2012 at 18:28Jean-Yves PerrierNovember 21st, 2012 at 00:29