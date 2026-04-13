---
title: People of HTML5 – Bruce Lawson – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/01/people-of-html5-bruce-lawson/
author: Chris Heilmann
published: '2011-01-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 needs spokespeople to work. There are a lot of people out there who took on this role, and here at Mozilla we thought it is a good idea to introduce some of them to you with a series of interviews and short videos. The format is simple – we send the experts 10 questions to answer and then do a quick video interview to let them introduce themselves and ask for more detail on some of their answers.

The first person to feature is ![fowd-london-18-19.05.2010_5761](../../assets/b71f30b88d559f66.jpg)


[Bruce Lawson](http://brucelawson.co.uk)of Opera, co-author of

[Introducing HTML5](http://introducinghtml5.com/)and one of the curators of

[HTML5 Doctor](http://www.html5doctor.com).

Bruce works from home somewhere in the darker and unknown regions of England, and if you haven’t had the chance to see him speak, make sure to catch one of his talks. Also, despite his disturbing fetish for cheesy cam effects, he really knows his stuff and is a very funny man to boot.

You can find Bruce on Twitter as [@brucel](http://twitter.com/brucel).

## The video interview

[Watch the video on YouTube](http://www.youtube.com/watch?v=IhkUe_KryGY) or Download it from [Archive.org](http://www.archive.org/details/PeopleOfHtml5-BruceLawsonwebmVersion) as [WebM (45MB)](http://www.archive.org/download/PeopleOfHtml5-BruceLawsonwebmVersion/PeopleOfHtml5-BruceLawson.webm), [OGG (70 MB)](http://www.archive.org/download/PeopleOfHtml5-BruceLawsonwebmVersion/PeopleOfHtml5-BruceLawson.ogv) or [MP4 (70 MB)](http://www.archive.org/download/PeopleOfHtml5-BruceLawsonwebmVersion/PeopleOfHtml5-BruceLawson_512kb.mp4)

## Ten questions about HTML5 for Bruce Lawson

### 1) What, in your view, is HTML5 and what does it mean for web development as a whole?

It’s the language for web applications: it makes writing apps more robust, more interoperable and expands the capabilities of browsers so the web can come closer to native apps.

### 2) How did you get involved in the HTML5 world? What is your background and even more importantly, what drives you?

My background is in accessibility and writing markup. So getting involved in the development of the new language for the Web was too exciting to pass over, and because Opera (my employer) was so closely associated with the genesis of HTML5, it was easy to persuade my boss to let me have the time!

### 3) What do you consider the most exciting of the new technologies?

HTML5, of course — and also [DAP](http://www.w3.org/2009/dap/) (“Device APIs and Policy Working Group”). This thrillingly-named set of specifications is further extending the capabilities of the Web by specifying APIs that allow access to device features like camera, contact books and calendar — much like Geolocation gives browsers access to the device’s GPS capabilities. Like HTML5, the DAP are adapting existing proprietary APIs that have been road-tested, and other manufacturers have committed to supporting the specifications.

### 4) You’ve co-authored “Introducing HTML5” — what was the most frustrating part about writing an HTML5 book? Isn’t HTML5 still a bit of a moving target?

Apart from the freakishly anachronistic processes behind dead-tree publishing (everything to be submitted in Microsoft Word!) the hardest part was the fact that the spec kept moving from under us. The chapter on video had just been proofread and indexed when the webM format was announced and we had to rewrite. But we were pretty sure that most of the stuff that was ready to use was pretty stable — and in a short Introductory book, we weren’t trying to cover the more esoteric areas, anyway.

### 5) You’ve been advocating using the term “NEWT” instead of talking about HTML5, what does that mean and why not HTML5 as an umbrella term?

Clients and journalists will use “HTML5” to mean CSS 3/video-that-runs-on-iThings/Geo-enabled applications. It’s the new “Web 2.0”. But we practitioners need to get our nomenclature straight. There are no HTML5 image transitions, just as there are no CSS semantics — and to say there are shows that you didn’t get the 2001 memo about separating style and content.

If we need an over-all term to encompass DAP, CSS 3, HTML5, Geolocation, SVG, WebGL, then let’s call it the Open Web Stack. But, because people seem to like easy-to-pronounce acronyms and cute logos, I proposed [NEWT](http://www.brucelawson.co.uk/2010/meet-newt-new-exciting-web-technologies) as a tongue-in-cheek way to highlight the jargon abuse I see happening.

### 6) What is in your opinion the biggest obstacle to mainstream HTML5 adoption?

Developer ignorance: “I can’t use it because it’s not finished” and “I can’t use it because I still have to support IE6” are the main stumbling blocks. “It’s not finished” annoys me the most. Perhaps we should stop using the English language because it’s “not finished yet” and move to French, as that was apparently finished in 1799.

Then there’s the IE6 fallacy. The HTML5 Shim allows you to style HTML5 elements in IE6, as long as you have JavaScript. If a visitor is surfing the Web with IE6 and JS turned off, their experience of the whole Web will be pretty dreadful and your site won’t be any worse.

And, of course, it’s not The Law that you *must* use HTML5; it’s really for Web applications. HTML4 and XHTML 1 will continue to work fine for documents.

### 7) There are a lot of fixes right now available to make HTML5 degrade gracefully on older browsers and IE6. If you look, for example, at the HTML5 boilerplate, this seems a lot of work and extra code and files. Is this worth it? What is your stance on so called “polyfills”?

All you really need is Remy’s [HTML5 Shim](http://code.google.com/p/html5shim/) so you can style your new HTML5 elements. Depending on your project you choose individual polyfills. is it a lot of work? Perhaps — but is linking to a pre-written polyfill that fakes WebSockets in old browsers harder work than writing that functionality from scratch and making it work in IE6 to 8?

Polyfills come with built-in obsolescence. They’re only needed for old browsers, and by definition, that’s a dwindling number of installs. Newer browsers don’t even know of their existence. It ain’t pretty, but feature detection and polyfilling are better than browser sniffing or locking out users.

### 8) Is there something in the HTML5 recommendations and specs that ails you? Are they taking a direction you don’t agree with?

I wish that accessibility aspects of canvas had been specified long ago, so that they were in browsers now. People are already abusing canvas to make User Interfaces, and it’s going to be the biggest problem, I think. I also think it’s silly that you can’t use CITE around the name of a person, which is one of the few instances of breaking backwards compatibility with HTML4.

### 9) If I wanted to learn about HTML5, where would you say is the best place to start?

There’s a wonderful book that introduces HTML5. The title escapes me for a moment… Mark Pilgrim [has an online book](http://diveintohtml5.org/), too, which is pretty good. I co-curate a site called [HTML5 Doctor](http://html5doctor.com/) which has a lot of beginner’s articles in tasty morsels. There are, unfortunately, so-called schools sites with out-of-date information and even published books based on archaic versions of the spec.

### 10) HTML5 takes a much more lenient approach to markup than HTML4.01 strict or XHTML. You can for example mix upper and lowercase tags and omit the quotes around attributes. Isn’t that a step back in terms of code quality?

Nope. It should be easy for people to move their sites from XHTML 1 or HTML4, and browsers never cared about syntax (when served text/html), so why impose an arbitrary rule forbidding lower case, or upper case, or requiring trailing slashes? Authors should pick a style that works for them and stick to it. Sites like [HTML Lint](http://lint.brihten.com/html/) offer the ability to opt-in to “lifestyle” syntactical choices like quoting attributes, lower case, etc. and I expect authoring tools to do the same.

The real test of quality is the DOM that the browser constructs from the code, and when browsers have HTML5 parsers, they’ll construct identical DOMs even from invalid code, which is a fantastic win for the interoperable Web.

### Bonus: What’s next? What do you consider the next big issue we need to fix to make the web a better place and easier to build for it?

We need a CSS layout mechanism that can be understood by mere mortals, some real accessibility for canvas and webGL, and more [pictures of nude Open Standards evangelists](http://www.flickr.com/photos/24374884@N08/4793141518/in/set-72157605968816582/).

Do you know anyone I should interview for “People of HTML5”? Tell me on Twitter: [@codepo8](http://twitter.com/codepo8)

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 21 comments

IanJanuary 6th, 2011 at 04:41Russell BishopJanuary 6th, 2011 at 04:47Benoit JacobJanuary 6th, 2011 at 06:00bruceJanuary 6th, 2011 at 08:14SkouaJanuary 6th, 2011 at 10:50bruceJanuary 6th, 2011 at 11:19SkouaJanuary 6th, 2011 at 11:33Tarjei VassbotnJanuary 6th, 2011 at 17:49GregJanuary 7th, 2011 at 01:21SkouaJanuary 7th, 2011 at 09:57DrClueJanuary 7th, 2011 at 04:34bruceJanuary 7th, 2011 at 10:34Tom – 大肚腩January 10th, 2011 at 18:35Axel RauschmayerJanuary 7th, 2011 at 15:04SkouaJanuary 7th, 2011 at 17:01Tarjei VassbotnJanuary 8th, 2011 at 02:59LaurentJanuary 7th, 2011 at 16:08StephenJanuary 8th, 2011 at 15:13TheoJanuary 16th, 2011 at 04:16IanJuly 27th, 2011 at 08:55JimFebruary 17th, 2012 at 09:13