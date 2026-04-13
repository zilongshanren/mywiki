---
title: 'Mozilla and Web Components: Update – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2014/12/mozilla-and-web-components/
author: Anne van Kesteren
published: '2014-12-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s note:** *Mozilla has a long history of participating in standards development. The post below shows a real-time slice of how standards are debated and adopted. The goal is to update developers who are most affected by implementation decisions we make in Firefox. We are particularly interested in getting feedback from JavaScript library and framework developers.*

Mozilla has been [working on Web Components](https://bugzilla.mozilla.org/show_bug.cgi?id=811542) — a technology encompassing HTML imports, custom elements, and shadow DOM — for a while now and testing this approach in [Gaia](https://developer.mozilla.org/en/Firefox_OS/Developing_Gaia), the frontend of Firefox OS. Unfortunately, our feedback into the standards process has not always resulted in the changes required for us to ship Web Components. Therefore we decided to reevaluate our stance with members of the developer community.

We came up with the following tentative plan for shipping Web Components in Firefox and we would really appreciate input from the developer community as we move this forward. Web Components changes a core aspect of the Web Platform and getting it right is important. We believe the way to do that is by having the change be driven by the hard learned lessons from JavaScript library developers.

- Mozilla will not ship an implementation of HTML Imports. We expect that once JavaScript modules — a feature derived from JavaScript libraries written by the developer community — is shipped, the way we look at this problem will have changed. We have also learned from Gaia and others, that lack of HTML Imports is not a problem as the functionality can easily be provided for with a polyfill if desired.
- Mozilla will ship an implementation of custom elements. Exposing the lifecycle is a very important aspect for the creation of components. We will work with the standards community to use
`Symbol`

-named properties for the callbacks to prevent name collisions. We will also ensure the strategy surrounding subclassing is sound with the latest work on that front in JavaScript and that the callbacks are sufficiently capable to describe the lifecycle of elements or can at least be changed in that direction. - Mozilla will ship an implementation of shadow DOM. We think work needs to be done to decouple style isolation from event retargeting to make event delegation possible in frameworks and we would like to ensure distribution is sufficiently extensible beyond Selectors. E.g Gaia would like to see this ability.

Our next steps will be working with the standards community to make these changes happen, making sure there is sufficient test coverage in [web-platform-tests](https://github.com/w3c/web-platform-tests), and making sure the specifications become detailed enough to implement from.

So please let us know what you think here in the comments or directly on the [public-webapps](http://lists.w3.org/Archives/Public/public-webapps/) standards list!

## About
[
Anne van Kesteren ](https://annevankesteren.nl/)

Standards person with an interest in privacy & security boundaries, as well as web platform architecture · he/him

## 49 comments

LaurentjDecember 15th, 2014 at 09:08葉至柔January 1st, 2015 at 10:54Ryan FrederickDecember 15th, 2014 at 09:23dimaDecember 15th, 2014 at 13:07laurentjDecember 15th, 2014 at 14:33IvanDecember 16th, 2014 at 04:21Erik isaksenDecember 17th, 2014 at 02:11AdamDecember 18th, 2014 at 15:44Erik IsaksenDecember 17th, 2014 at 02:06Anne van KesterenDecember 15th, 2014 at 12:00LaurentjDecember 15th, 2014 at 14:24Alex RussellDecember 17th, 2014 at 17:44Joern TurnerDecember 15th, 2014 at 13:18pkozlowski_osDecember 15th, 2014 at 13:58DanDecember 15th, 2014 at 20:27Chuck HortonDecember 16th, 2014 at 04:43Zimon DaiDecember 16th, 2014 at 21:04markgDecember 16th, 2014 at 23:23Erik IsaksenDecember 17th, 2014 at 02:25Anne van KesterenDecember 17th, 2014 at 08:47Erik IsaksenDecember 17th, 2014 at 02:22Anne van KesterenDecember 17th, 2014 at 08:52LaurentjDecember 18th, 2014 at 02:29BrianCDecember 18th, 2014 at 12:08Anne van KesterenDecember 19th, 2014 at 02:27AdamDecember 18th, 2014 at 15:50TylerDecember 29th, 2014 at 08:33Erik IsaksenDecember 18th, 2014 at 02:16Steve AlbersDecember 19th, 2014 at 20:52ShaneDecember 20th, 2014 at 17:15markgDecember 22nd, 2014 at 22:48Brett ZamirDecember 23rd, 2014 at 13:26Jean-YvesDecember 24th, 2014 at 00:55SciDeveloperDecember 24th, 2014 at 03:58Havi Hoffman [Editor]December 24th, 2014 at 11:55markgDecember 28th, 2014 at 19:40danDecember 31st, 2014 at 10:10Anne van KesterenJanuary 5th, 2015 at 00:56danJanuary 5th, 2015 at 07:09MartijnJanuary 5th, 2015 at 08:06Dominic ChambersJanuary 5th, 2015 at 08:11Steve AlbersJanuary 5th, 2015 at 19:35markgJanuary 5th, 2015 at 21:42Ras FredJanuary 5th, 2015 at 23:07PotchJanuary 6th, 2015 at 12:48Ras FredJanuary 5th, 2015 at 23:08Ras FredJanuary 5th, 2015 at 23:13Anne van KesterenJanuary 6th, 2015 at 11:57Havi Hoffman [Editor]January 6th, 2015 at 13:20