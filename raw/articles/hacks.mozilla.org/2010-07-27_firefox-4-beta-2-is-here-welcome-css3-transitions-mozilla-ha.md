---
title: Firefox 4 Beta 2 is here – Welcome CSS3 transitions – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2010/07/firefox4-beta2/
author: Paul Rouget
published: '2010-07-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As we have [explained before](https://hacks.mozilla.org/2010/07/firefox-4-beta-1-is-here-whats-in-it-for-web-developers/), Mozilla is now making more frequent updates to our beta program. So here it is, [Firefox Beta 2](http://www.mozilla.com/en-US/firefox/beta/) has just been released, 3 weeks after Beta 1.

Firefox 4 Beta 1 already brought a large amount of new features ([see the Beta 1 feature list](https://hacks.mozilla.org/2010/07/firefox-4-beta-1-is-here-whats-in-it-for-web-developers/)). So what’s new for web developers in this beta?

## Performance & CSS3 Transitions

The two major features for web developers with this release are **Performance improvements and CSS3 Transitions on CSS3 Transforms**.

*This video is hosted by Youtube and uses the HTML5 video tag if you have enabled it ( see here). Youtube video here.*

**Performance: **In this new Beta, Firefox comes with a new page building mechanism: [Retained Layers](http://weblogs.mozillazine.org/roc/archives/2010/07/retained_layers.html). This mechanism provides noticeable faster speed for web pages with dynamic content, and scrolling is much smoother. Also, we’re still experimenting with hardware acceleration: using the GPU to render and build some parts of the web page.

**CSS3 Transitions on transforms:** The major change for web developers is probably CSS3 Transitions on CSS3 Transformations.

CSS3 Transitions provide a way to animate changes to CSS properties, instead of having the changes take effect instantly. [See the documentation](https://developer.mozilla.org/en/CSS/CSS_transitions) for details.

This feature was available in Firefox 4 Beta 1, but in this new Beta, you can use Transitions on Transformation.

A CSS3 Transformation allows you to define a Transformation (scale, translate, skew) on any HTML element. And you can animate this transformation with the transitions.

`transform: rotate(5deg);`

will transform `transform: rotate(350deg) scale(1.4) rotate(-30deg);`

through a smooth animation.
```
#victim {
background-color: yellow;
color: black;
transition-duration: 1s;
transform: rotate(10deg);
/* Prefixes */
-moz-transition-duration: 1s;
-moz-transform: rotate(5deg);
-webkit-transition-duration: 1s;
-webkit-transform: rotate(10deg);
-o-transition-duration: 1s;
-o-transform: rotate(10deg);
}
#victim:hover {
background-color: red;
color: white;
transform: rotate(350deg) scale(1.4) rotate(-30deg);
/* Prefixes */
-moz-transform: rotate(350deg) scale(1.4) rotate(-30deg);
-webkit-transform: rotate(350deg) scale(1.4) rotate(-30deg);
-o-transform: rotate(350deg) scale(1.4) rotate(-30deg);
}
```

CSS 3 Transitions are supported by Webkit-based browsers (Safari and Chrome), Opera and now Firefox as well. Degradation (if not supported) is graceful (no animation, but the style is still applied). Therefore, you can start using it right away.

## Demos

I’ve written a couple of demos to show both CSS3 Transitions on Transforms and hardware acceleration (See the video above for screencasts).

**Credits**

**Creative Commons videos:**

[Ian Broyles](http://www.flickr.com/photos/ianbroyles/4498340824/)[Spoony Mushroom](http://www.flickr.com/photos/transcendent/4024024153/)- Mark Sebastian:
[[1]](http://www.flickr.com/photos/markjsebastian/3727252404/)[[2]](http://www.flickr.com/photos/markjsebastian/3528096655/) [Swanky](http://www.flickr.com/photos/swanky-hsiao/4036499457/)[Spiral Production](http://spiralproductions.com/)

**The multicolor cloud effect (MIT License)**

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 61 comments

RichJuly 27th, 2010 at 13:32Paul RougetJuly 27th, 2010 at 13:42MichaëlJuly 27th, 2010 at 14:04Magne AnderssonJuly 27th, 2010 at 14:05Michael FienenJuly 27th, 2010 at 14:07RichJuly 27th, 2010 at 14:27Matt WiebeJuly 27th, 2010 at 21:54CraigOctober 9th, 2010 at 00:00RichJuly 27th, 2010 at 14:28Ege ÖzcanJuly 27th, 2010 at 15:00Adam LuikartJuly 27th, 2010 at 15:50Tim DawsonJuly 27th, 2010 at 15:59Paul RougetJuly 28th, 2010 at 07:34factlickerJuly 27th, 2010 at 16:14RickJuly 27th, 2010 at 16:42J.B. Nicholson-OwensJuly 27th, 2010 at 18:50Paul RougetJuly 28th, 2010 at 03:42SethJuly 27th, 2010 at 21:01JoshJuly 28th, 2010 at 03:04Paul RougetJuly 28th, 2010 at 03:26DenJuly 28th, 2010 at 02:49MaxJuly 28th, 2010 at 05:13Paul RougetJuly 28th, 2010 at 07:35Komrade KilljoyJuly 28th, 2010 at 05:45Komrade KilljoyJuly 28th, 2010 at 05:50Paul RougetJuly 28th, 2010 at 07:36Cristóferson BuenoJuly 28th, 2010 at 06:09Paul RougetJuly 28th, 2010 at 07:36Bruno simioniNovember 16th, 2010 at 06:34Roger ErensJanuary 20th, 2011 at 16:48Mark CurtisJuly 28th, 2010 at 06:39Daniel84July 28th, 2010 at 08:13voracityJuly 28th, 2010 at 23:13TéAugust 1st, 2010 at 14:22Daniel HendrycksJuly 28th, 2010 at 07:44Christopher BlizzardAugust 15th, 2010 at 10:57sugandaJuly 28th, 2010 at 08:57Bart K.July 28th, 2010 at 10:14ChrisJuly 28th, 2010 at 14:25discoleoJuly 28th, 2010 at 14:30discoleoJuly 28th, 2010 at 14:31Paul RougetJuly 29th, 2010 at 01:56VictorJuly 29th, 2010 at 10:20mathis the aznas ownerJuly 29th, 2010 at 16:18Anthony CalzadillaJuly 29th, 2010 at 21:59Christopher BlizzardAugust 15th, 2010 at 11:00Komrade KilljoyJuly 29th, 2010 at 23:17nemoJuly 30th, 2010 at 11:48Ingo RautenbergJuly 30th, 2010 at 13:56Peter GeilJuly 31st, 2010 at 08:49CharlesAugust 1st, 2010 at 15:20ThiagoAugust 25th, 2010 at 04:17marcAugust 28th, 2010 at 20:47mOctober 15th, 2010 at 09:59Gamal El-shalOctober 21st, 2010 at 10:46MarkDecember 13th, 2010 at 08:20thinsoldierDecember 22nd, 2010 at 13:54quixoteJanuary 19th, 2011 at 13:24evalicaApril 5th, 2011 at 11:00m lyakhovskyNovember 29th, 2012 at 11:36m lyakhovskyNovember 29th, 2012 at 11:40