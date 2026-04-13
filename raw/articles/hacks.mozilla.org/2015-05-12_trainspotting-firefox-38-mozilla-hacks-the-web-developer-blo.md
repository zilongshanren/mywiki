---
title: 'Trainspotting: Firefox 38 – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/05/trainspotting-firefox-38/
author: Sergi Mansilla
published: '2015-05-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Trainspotting is a series of articles highlighting features in the latest version of Firefox, that are live now in production code, ready for you to use in your work. A new version of Firefox is shipped every six weeks – we at Mozilla call this pattern “release trains.”*

Has it been six weeks already?? Firefox 38 is here, and with it come some snazzy new additions to the Web platform. Here are a few highlights:

*For a full list of changes and additions, take a look at the Firefox 38 release notes.*

## Responsive Image Support

Support for both the `<picture>`

element and `<img srcset>`

are now in a stable Firefox! There are [lots](http://www.smashingmagazine.com/2014/05/14/responsive-images-done-right-guide-picture-srcset/) of [great](http://demosthenes.info/blog/936/Responsive-Images-For-Designers-The-HTML5-picture-element) [articles](http://html5hub.com/html5-picture-element/) available to get you familiar with the new techniques, and a [polyfill](http://scottjehl.github.io/picturefill/) available so you can take advantage of them today! There is one caveat for Firefox 38 – responsive images will *load* using the correct media queries, but presently do not respond to viewport resizing. This bug is being actively worked on and tracked [here](https://bugzilla.mozilla.org/show_bug.cgi?id=1135812), and will be fixed in a near-future version of Firefox.

## You got WebSockets in my Web Worker!

Firefox 38 now allows code running in a Web `Worker`

to open up a `WebSocket`

connection. This is great for games or other collaborative applications, which can now do their multiplayer/realtime logic in a separate thread from the UI.

## HTML5 <ruby> markup support

![Ruby Annotation](../../assets/a3e121b9b27b0f4c.png)


Better typography for Japanese and Chinese language sites is now possible without clunky libraries or extensions by using `<ruby>`

markup.

## BroadcastChannel- postMessage *All* the Windows!

If you’re building a webapp with multiple tabs or windows, keeping them all in sync, apprised of events and state changes can be a pain. BroadcastChannel is a fully client-side message passing API that lets any scripts running on the same origin broadcast messages to their peers.

```
// one tab
var ch = new BroadcastChannel('test');
ch.postMessage('this is a test');
// another tab
ch.addEventListener('message', function (e) {
alert('I got a message!', e.data);
});
// yet another tab
ch.addEventListener('message', function (e) {
alert('Avast! a message!' e.data);
});
```


## Developer Tools

Network requests coming from `XMLHttpRequest`

are now marked in the Web Console:

![XMLHttpRequest requests marked in the Web Console](../../assets/2a3a0cf6d7957f04.png)


Need to grab a value from your page? The special `copy`

method available in the Web Console has you covered:

![consolecopy](../../assets/f3c2e350a74072fc.gif)


## But Wait

There are tons more improvements and bug fixes in Firefox 38 I haven’t covered here – check out the [Firefox 38 release notes](https://www.mozilla.org/en-US/firefox/38.0/releasenotes/), [Developer Release Notes](https://developer.mozilla.org/en-US/Firefox/Releases/38), or even the [list of bugs](https://bugzilla.mozilla.org/buglist.cgi?j_top=OR&f1=target_milestone&o3=equals&v3=Firefox%2038&o1=equals&resolution=FIXED&o2=anyexact&query_format=advanced&f3=target_milestone&f2=cf_status_firefox38&bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&v1=mozilla38&v2=fixed%2Cverified&limit=0) fixed in this release for more information.

Enjoy!

## 10 comments

DaveMay 12th, 2015 at 09:56PotchMay 13th, 2015 at 10:20Fida Hussain GhallooMay 12th, 2015 at 10:21nikomoMay 12th, 2015 at 20:03WyattMay 13th, 2015 at 09:23RubyRubyRubyRubyMay 13th, 2015 at 11:52JohnMay 14th, 2015 at 05:05RubyRubyRubyRubyMay 20th, 2015 at 11:49IlyasFMay 18th, 2015 at 02:52ArneMay 20th, 2015 at 05:16