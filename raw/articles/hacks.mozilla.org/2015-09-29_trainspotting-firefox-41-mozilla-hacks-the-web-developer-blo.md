---
title: 'Trainspotting: Firefox 41 – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/09/trainspotting-firefox-41/
author: Sergi Mansilla
published: '2015-09-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Trainspotting* is a series of articles highlighting features in the lastest version of Firefox. A new version of Firefox is shipped every six weeks – we at Mozilla call this pattern “release trains.”

Firefox 41 (the Fire-y-est Fox to date) brings a bevy of new and improved features for browser users and web developer audiences. Let’s take a look at some highlights.

*For a full list of changes and additions, check out the Firefox 41 release notes.*

## Screenshot a single element

Need to capture just one bit of a web page? Using the Inspector panel, you can now screenshot the area of a page contained by a single element:

![Right click on a node in the markup view.](../../assets/1d3eb2895633fde6.gif)


The result is a snapshot cropped to perfection:

![Resulting Screenshot of an element on the page.](../../assets/9cfcdcf73028bc98.png)


## Connection status

The `navigator.onLine`

API, historically, wasn’t all that useful. Pages could only inquire whether Firefox itself was in a specific “Work Offline” state, regardless of whether the computer had any network connection. Now, `navigator.onLine`

uses system network information to mirror the state of the device’s Internet connection!

See the Pen [QjGoRP](http://codepen.io/potch/pen/QjGoRP/) by Potch ([@potch](http://codepen.io/potch)) on [CodePen](http://codepen.io).

## Clipboard management

Copying text on behalf of the user used to be *the hardest problem in computer science*. Web developers would have to embed a Flash widget on the page just to put some text in the user’s clipboard. No more! Developers can now copy text to a users’ clipboard programmatically directly in JavaScript, provided the user takes an explicit action such as clicking a button.

Read the [Hacks Post](https://hacks.mozilla.org/2015/09/flash-free-clipboard-for-the-web/) on clipboard manipulation for more details.

## Network Panel HAR exports

We should rename the Network Panel to Hagar, because it’s now [HAR-able](https://en.wikipedia.org/wiki/H%C3%A4gar_the_Horrible)! HAR is a network request archive format used by many performance and request analysis tools, and it’s now possible to export HAR information from the Network panel from the context menu.

![The location of the Save As HAR option in the context menu.](../../assets/4b7cd7748ce57ce9.png)


## <picture> perfect

In a [previous edition of Trainspotting](https://hacks.mozilla.org/2015/05/trainspotting-firefox-38/#toc_1), I provided the following caveat about responsive image support in Firefox:

Responsive images will load using the correct media queries, but presently do not respond to viewport resizing. This bug is being actively worked on and tracked here, and will be fixed in a near-future version of Firefox.


Well, that *near-future* version is this *now-present* version! Responsive images will now respond to post-load changes to the page’s viewport. Isn’t it nice when a plan comes together!

## There couldn’t possibly be more…

…But there most definitely is. There’s plenty of additional information in the [Developer Release Notes](https://developer.mozilla.org/en-US/Firefox/Releases/41) or, for large <table> enthusiasts, [the full list of fixed bugs](https://bugzilla.mozilla.org/buglist.cgi?j_top=OR&f1=target_milestone&o3=equals&v3=Firefox%2041&o1=equals&resolution=FIXED&o2=anyexact&query_format=advanced&f3=target_milestone&f2=cf_status_firefox41&bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&v1=mozilla41&v2=fixed%2Cverified&limit=0).

Keep on rocking the Free Web!

## 17 comments

Fabio BenedittoSeptember 29th, 2015 at 09:20MTSeptember 29th, 2015 at 10:44PotchSeptember 29th, 2015 at 15:12MTSeptember 29th, 2015 at 15:19Joe ZimSeptember 30th, 2015 at 06:53en45masaoOctober 1st, 2015 at 03:41HervéSeptember 30th, 2015 at 02:08jtSeptember 30th, 2015 at 09:00IvanSeptember 30th, 2015 at 16:20VinayOctober 1st, 2015 at 00:26JacopoOctober 1st, 2015 at 02:53NutamaticOctober 1st, 2015 at 04:50Francis KimOctober 1st, 2015 at 05:10DDOctober 1st, 2015 at 07:06DuminduOctober 3rd, 2015 at 00:39MikePOctober 5th, 2015 at 12:40MTOctober 5th, 2015 at 14:15