---
title: Making history with the August Dev Derby – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2011/08/making-history-with-the-august-dev-derby/
author: Chris Heilmann
published: '2011-08-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It is time to announce another month’s [Dev Derby](https://developer.mozilla.org/en-US/demos/devderby) and this August we want you to play with the [History API](https://developer.mozilla.org/en/DOM/Manipulating_the_browser_history). The History API is a much needed piece of the puzzle of creating modern web applications and here is why:

## Links are good, they make the web work

The web is made up from sites linking to each other. You are on some site and read an HTML document, you hit a link or submit a form and the browser redirects you to another page. This is great as it allows for a few things:

- You always get a unique address you can bookmark and send to your friends to see the page you were on
- You can use the browser’s back button when you did something wrong and get back to where you were before
- Search engines love links and following them through your site

## Why load a whole page when only a small bit changes?

Of course there are some annoyances with that, mainly that you need to leave the page and download a full new document and its linked resources every time to perform a simple action. As this took too long even in the dark past of the web we found workarounds like frames which only loaded part of the site rather than the whole document. This broke the bookmarking and going back in history bit for the first time. The other big thing of course was to make Flash sites bookmarkable and allow for using the back button in them (you might remember JavaScript confirm boxes popping up saying “do you really want to leave this page?”).

When AJAX came around we totally killed the bookmarking and history of the browser. This was a problem as our visitors have already been conditioned to hit the back button every time something goes wrong (admit it, you also found yourself reloading or hitting back in GMail one time or another). We needed a fix for that. As far as I remember [Mike Stenhouse was the first to propose a fix in 2005](http://www.contentwithstyle.co.uk/content/fixing-the-back-button-and-enabling-bookmarking-for-ajax-apps/) using the fragment identifier of the URI to store information and a hidden iframe element to seed the history. This fix got wrapped into several libraries like the [YUI history manager](http://developer.yahoo.com/yui/history/) and the [jQuery History plugin](http://plugins.jquery.com/project/history).

## Breaking the web with “hashbang URLs”

The problem of broken links and browsing session histories escalated when some sites like Twitter and Gawker media discarded real URLs for hashbang URLs. So instead of reaching me at [http://twitter.com/codepo8](http://twitter.com/codepo8) clicking my profile in Twitter will get you to [http://twitter.com/#!/codepo8](http://twitter.com/#!/codepo8). As Twitter is an app that uses a lot of JavaScript, it was deemed more efficient to use the latter to navigate – all Twitter does is load the new content of my profile via JavaScript. This saves them a lot of traffic, but also makes the links dependent on JavaScript which means search engines don’t follow them. In Twitter’s case this is not an issue but when Gawker moved all his blogs to a format using hashbangs rather than reloading the page, [a simple JavaScript error in a different script caused a major outage on a lot of blogs](http://blogs.wsj.com/digits/2011/02/07/gawker-outage-causing-twitter-stir/). But Hashbang URLs became something people really wanted to have to create fast loading apps and pages instead of reloading the page over and over.

Hashbang URLs are brittle to say the least and [a lot](http://isolani.co.uk/blog/javascript/BreakingTheWebWithHashBangs) [of people](http://blog.benward.me/post/3231388630) [voiced concerns](http://www.tbray.org/ongoing/When/201x/2011/02/09/Hash-Blecch) about them. Not all user agents on the web have JavaScript enabled, which means your site can’t even be reached by them. This includes search engine spiders which is why [Google set up a proposal how to make Ajax sites crawlable](http://googlewebmastercentral.blogspot.com/2009/10/proposal-for-making-ajax-crawlable.html) even [throwing out a whole spec](http://code.google.com/web/ajaxcrawling/index.html). As an aside, the Facebook vanity URLs also redirect with JavaScript, which is why mine is “document.location.href”.

## The solution: History API and server redirects

So instead of using hashbangs and break the web and very basic browser usage patterns we now have the History API in HTML5. It allows you to dynamically change the URL in the browser toolbar and add to its history without reloading the page. You get the best of both worlds – you do atomic updates in the page and you leave real, working URLs behind for the user to go to, bookmark and send to friends. The History API is in use by quite a few major sites, [Facebook allows for back button use](http://www.facebook.com/note.php?note_id=438532093919) and [Flickr uses it in their lightbox view](http://www.flickr.com/photos/codepo8/5263730274/in/set-72157625604220110/lightbox/). The coolest implementation however is GitHub and their [Tree Slider](https://github.com/blog/760-the-tree-slider):

Isn’t that slick? You navigate the whole page, it loads in milliseconds rather than seconds and you can hit the back button or copy and paste the URL any time you want.

Now it is your turn, show us what you can do with the History API! Here are some resources to read up on.

## Resources:

[History API at Mozilla Developer Network](https://developer.mozilla.org/en/DOM/Manipulating_the_browser_history)[History API explained in detail at Dive into HTML5](http://diveintohtml5.org/history.html)[Detailed specification of the History API at the WHATWG](http://www.whatwg.org/specs/web-apps/current-work/multipage/history.html)[A simple History API demo by Remy Sharp](http://html5demos.com/history/)[How Facebook uses the History API](http://www.facebook.com/note.php?note_id=438532093919)[Syd Lawrence’s jQuery Fancy Box with History support](https://github.com/sydlawrence/fancy-box)[History.js – a polyfill for History API support](https://github.com/balupton/history.js)

Ladies and gentlemen, start your editors and show us how to make History!

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 5 comments

Ryan GroveAugust 2nd, 2011 at 15:48Chris HeilmannAugust 3rd, 2011 at 00:28Niloy MondalAugust 2nd, 2011 at 22:00Chris HeilmannAugust 3rd, 2011 at 00:28Fawad HassanAugust 5th, 2011 at 03:37