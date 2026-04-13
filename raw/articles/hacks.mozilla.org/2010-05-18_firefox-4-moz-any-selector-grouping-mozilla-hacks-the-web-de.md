---
title: 'Firefox 4: -moz-any() selector grouping – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2010/05/moz-any-selector-grouping/
author: Paul Rouget
published: '2010-05-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a re-post from David Baron’s blog. This feature has landed in Mozilla Central (trunk) and only available with a Firefox Nightly Build for the time being.*

Last night I landed support for `:-moz-any()`

selector grouping. This allows providing alternatives between combinators, rather than having to repeat the entire selector for once piece that’s different. For example, it allowed replacing this rule in our user-agent style sheet:

```
/* 3 deep (or more) unordered lists use a square */
ol ol ul, ol ul ul, ol menu ul, ol dir ul,
ol ol menu, ol ul menu, ol menu menu, ol dir menu,
ol ol dir, ol ul dir, ol menu dir, ol dir dir,
ul ol ul, ul ul ul, ul menu ul, ul dir ul,
ul ol menu, ul ul menu, ul menu menu, ul dir menu,
ul ol dir, ul ul dir, ul menu dir, ul dir dir,
menu ol ul, menu ul ul, menu menu ul, menu dir ul,
menu ol menu, menu ul menu, menu menu menu, menu dir menu,
menu ol dir, menu ul dir, menu menu dir, menu dir dir,
dir ol ul, dir ul ul, dir menu ul, dir dir ul,
dir ol menu, dir ul menu, dir menu menu, dir dir menu,
dir ol dir, dir ul dir, dir menu dir, dir dir dir {
list-style-type: square;
}
```

with this one:

```
/* 3 deep (or more) unordered lists use a square */
:-moz-any(ol, ul, menu, dir) :-moz-any(ol, ul, menu, dir) ul,
:-moz-any(ol, ul, menu, dir) :-moz-any(ol, ul, menu, dir) menu,
:-moz-any(ol, ul, menu, dir) :-moz-any(ol, ul, menu, dir) dir {
list-style-type: square;
}
```

In theory, I could even have used:

```
/* 3 deep (or more) unordered lists use a square */
:-moz-any(ol, ul, menu, dir) :-moz-any(ol, ul, menu, dir) :-moz-any(ul, menu, dir) {
list-style-type: square;
}
```

but this would have been slower since it no longer falls into the [tag bucket](https://developer.mozilla.org/en/Writing_Efficient_CSS). (If `:-moz-any()`

turns out to be popular, we could add extra code so it’s just as fast, but I haven’t done so yet.)

`:-moz-any()`

is allowed to contain selectors with multiple simple selectors (using the css3-selectors definition of simple selectors, not the CSS 2.1 definition), but it is not allowed to contain combinators or pseudo-*elements*. So you can write `:-moz-any(p.warning.new, p.error, div#topnotice)`

or `:-moz-any(:link, :visited).external:-moz-any(:active, :focus)`

, but you can’t put “`div p`

” or “`div > p`

or “`:first-letter`

” inside `:-moz-any()`

.

This has a -moz- prefix for two reasons. First, it’s just a proposal, and hasn’t made its way into any specification. And second, it isn’t quite ready for prime-time, though, since it doesn’t yet [handle specificity correctly].

**Note**: This will be extremely valuable in an HTML5 context when it comes to sections and headings. Since `section`

, `article`

, `aside`

, and `nav`

can be nested, doing something like styling all `h1`

elements at different depths could be extremely complex.

```
/* Level 0 */
h1 {
font-size: 30px;
}
/* Level 1 */
section h1, article h1, aside h1, nav h1 {
font-size: 25px;
}
/* Level 2 */
section section h1, section article h1, section aside h1, section nav h1,
article section h1, article article h1, article aside h1, article nav h1,
aside section h1, aside article h1, aside aside h1, aside nav h1,
nav section h1, nav article h1, nav aside h1, nav nav h1, {
font-size: 20px;
}
/* Level 3 */
/* ... don't even think about it*/
```

With -moz-any():

```
/* Level 0 */
h1 {
font-size: 30px;
}
/* Level 1 */
-moz-any(section, article, aside, nav) h1 {
font-size: 25px;
}
/* Level 2 */
-moz-any(section, article, aside, nav)
-moz-any(section, article, aside, nav) h1 {
font-size: 20px;
}
/* Level 3 */
-moz-any(section, article, aside, nav)
-moz-any(section, article, aside, nav)
-moz-any(section, article, aside, nav) h1 {
font-size: 15px;
}
```

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 27 comments

Warren ParsonsMay 18th, 2010 at 10:07JDMay 18th, 2010 at 10:51Magne AnderssonMay 18th, 2010 at 14:35Magne AnderssonMay 18th, 2010 at 12:38Andy LMay 18th, 2010 at 14:29BarryvanMay 18th, 2010 at 17:01semperMay 19th, 2010 at 03:02voracityMay 19th, 2010 at 04:52voracityMay 19th, 2010 at 04:56CyberSkullJuly 7th, 2010 at 22:11Magne AnderssonMay 19th, 2010 at 08:23zoe somebodyAugust 28th, 2011 at 22:43Paul RougetAugust 29th, 2011 at 02:24semperMay 19th, 2010 at 14:37Magne AnderssonMay 20th, 2010 at 00:59GiorgioMay 19th, 2010 at 15:49MatzipanJune 23rd, 2010 at 10:57ZhouQiJuly 8th, 2010 at 20:47SteveDecember 23rd, 2010 at 09:23Anton AgestamApril 11th, 2011 at 05:19Lars GuntherJune 29th, 2011 at 08:42PoderwacOctober 3rd, 2011 at 06:21DaveNovember 19th, 2011 at 09:57