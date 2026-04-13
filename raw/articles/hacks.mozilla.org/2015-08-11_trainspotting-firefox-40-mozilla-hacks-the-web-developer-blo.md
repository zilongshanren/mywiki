---
title: 'Trainspotting: Firefox 40 – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/08/trainspotting-firefox-40/
author: Sergi Mansilla
published: '2015-08-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Trainspotting* is a series of articles highlighting features in the lastest version of Firefox. A new version of Firefox is shipped every six weeks – we at Mozilla call this pattern “release trains.”

Firefox keeps on shippin' shippin' shippin' /


Into the future…

—Steve Miller Band, probably

Like a big ol’ jet airliner, a new version of Firefox has been cleared for takeoff! Let’s take a look at some of the snazzy new things in store for both users and developers.

*For a full list of changes and additions, take a look at the Firefox 40 release notes.*

## Developer Tools

Find what you’re looking for in the Inspector, but don’t know where it is on the page? You can now scroll an element into view via the Markup View in the Inspector:

![scroll-into-view](../../assets/8c797bb18b248057.gif)


Sift through complex stylesheets more easily by filtering CSS rules:

![](https://mdn.mozillademos.org/files/11197/css-filtered.png)


You can now toggle how colors are represented by Shift+clicking on them in the Rules view:

![color-rotate](../../assets/e1ac88ffebf55acc.gif)


The Web Console will now warn of code that is unreachable because it comes after a `return`

statement:

![unreachable](../../assets/69d93f1af51382ef.png)


The Developer Tools have also gained a powerful new set of Performance analysis tools, which are demonstrated along with all the other Firefox 40 Developer Tools changes in this [in-depth blog post](https://hacks.mozilla.org/2015/06/new-performance-tools-in-firefox-developer-edition-40/).

## Signed Add-ons

![extension-warning](../../assets/5bb632766d3bc0fe.png)


Malicious extensions are a growing problem in all browsers. Because Firefox Add-ons have tremendous power, there needs to be a better way to protect users from malicious code running wild. Starting in Firefox 42, all Firefox add-ons will be *required* to be signed in order to be able to be installed by end-users. In Firefox 40, users will be warned about un-signed extensions, but can opt to install them anyway. You can read more about [why extension signing is needed](https://blog.mozilla.org/addons/2015/04/15/the-case-for-extension-signing/), and also check out the [overall plan](https://wiki.mozilla.org/Addons/Extension_Signing) for the roll-out of signed extensions.

## Event `offsetX`

and `offsetY`


Sometimes a good idea is a good idea, even if it takes [14 years](https://bugzilla.mozilla.org/show_bug.cgi?id=69787)! Firefox now supports the [ offsetX](https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/offsetX) and

[properties for](https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/offsetX)

`offsetY`

[MouseEvents](https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent). This makes it much easier for code to track mouse events on an element within a page, without needing to know where in the page the element is. As always, perform capability checks to ensure that your code works across browsers:

```
el.addEventListener(function (e) {
var x, y;
if ('offsetX' in e) {
x = e.offsetX;
y = e.offsetY;
} else {
// addition needed for every offsetParent up the chain
x = e.clientX + e.target.offsetLeft /* ... */;
y = e.clientY + e.target.offsetTop /* ... */;
}
addGlitterMouseTrails(x, y);
}
```


## But Wait, There’s More!

Every new version of Firefox has dozens of bug fixes and changes to make browsing and web development better- I’ve only touched upon a few. Finally, it’s well worth noting that [ 55 developers contributed their first code change](https://blog.mozilla.org/community/2015/08/10/firefox-40-new-contributors/) to Firefox in this release, and 49 of them were brand new volunteers. Shipping would not be the same without these awesome contributions!

**Thank you!**

For all the rest of the details, check out the [Developer Release Notes](https://developer.mozilla.org/en-US/Firefox/Releases/40) or even [the full list of fixed bugs](https://bugzilla.mozilla.org/buglist.cgi?j_top=OR&f1=target_milestone&o3=equals&v3=Firefox%2040&o1=equals&resolution=FIXED&o2=anyexact&query_format=advanced&f3=target_milestone&f2=cf_status_firefox40&bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&v1=mozilla40&v2=fixed%2Cverified&limit=0). Happy Browsing!

## 8 comments

Minh NguyễnAugust 11th, 2015 at 21:34PotchAugust 11th, 2015 at 22:43Jean HominalAugust 12th, 2015 at 00:31Havi Hoffman [Editor]August 12th, 2015 at 07:24AlbertAugust 12th, 2015 at 04:37George8211August 12th, 2015 at 04:46Havi Hoffman [Editor]August 12th, 2015 at 07:23roodiAugust 12th, 2015 at 06:24