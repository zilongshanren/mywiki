---
title: Mozilla developer preview (Gecko 1.9.3a1) available for download – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/02/mozilla-developer-preview-gecko-1-9-3a1-available-for-download/
author: Alix Franquet
published: '2010-02-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Editor’s note: Today, Mozilla released a preview of the Gecko 1.9.3 platform for developers and testers. Check out the Mozilla Developer News announcement reposted below.*

A Mozilla Developer Preview of improvements in the Gecko layout engine is now available for download. This is a pre-release version of the Gecko 1.9.3 platform, which forms the core of rich Internet applications such as Firefox. **Please note that this release is intended for developers and testers only.** As always, we appreciate any [feedback](http://hendrix.mozilla.org/) you may have and encourage users to help us by [filing bugs](http://developer.mozilla.org/en/docs/Bug_writing_guidelines).

This developer preview introduces several new features, including:

- Support for
[CSS Transitions](http://www.w3.org/TR/css3-transitions/). This support is not quite complete: support for animation of transforms and gradients has not yet been implemented. - Support for SMIL Animation in SVG. Support for animating some SVG attributes is still under development and the
`animateMotion`

element isn’t supported yet. - Support for
[WebGL](https://developer.mozilla.org/en/WebGL), which is disabled by default but can be enabled by changing a preference. See[this blog post](http://hacks.mozilla.org/2009/09/webgl-for-firefox/)and[this blog post](http://hacks.mozilla.org/2009/12/webgl-draft-released-today/)for more details. - Support for the
`getClientRects`

and`getBoundingClientRect`

methods on`Range`

objects. See[bug 396392](https://bugzilla.mozilla.org/show_bug.cgi?id=396392)for details. - Support for the
`setCapture`

and`releaseCapture`

methods on DOM elements. See[bug 503943](https://bugzilla.mozilla.org/show_bug.cgi?id=503943)for details. - Support for the
[HTML5](https://developer.mozilla.org/en/DOM/Manipulating_the_browser_history#Adding_and_modifying_history_entries). See`History.pushState()`

and`History.replaceState()`

methods and the`popstate`

event[bug 500328](https://bugzilla.mozilla.org/show_bug.cgi?id=500328)for details. - Support for the
`-moz-image-rect()`

value for`<a href="https://developer.mozilla.org/en/CSS/background-image">background-image</a>`

. See[bug 113577](https://bugzilla.mozilla.org/show_bug.cgi?id=113577)for more details.

and several other significant changes, including:

- On Mac OS X, we render text using Core Text rather than ATSUI.
- We rewrote major parts of the code for handling scrolling. See
[bug 526394](https://bugzilla.mozilla.org/show_bug.cgi?id=526394)for details. - We rewrote the way a snapshot of a document is taken in order to print or print preview. See
[bug 487667](https://bugzilla.mozilla.org/show_bug.cgi?id=487667)for details. - We made significant changes to table border handling. See
[bug 452319](https://bugzilla.mozilla.org/show_bug.cgi?id=452319)and[bug 43178](https://bugzilla.mozilla.org/show_bug.cgi?id=43178)for details. - We made various architectural changes to improve Web page performance.

More information on these changes is in the [release notes](http://www.mozilla.org/projects/firefox/3.7a1/releasenotes/), as well as the [Upcoming Firefox features for developers](https://developer.mozilla.org/en/Upcoming_Firefox_features_for_developers) article on the [Mozilla Developer Center](https://developer.mozilla.org/).

Please use the following links when downloading this Mozilla Developer Preview:

## 9 comments

James John MalcolmFebruary 10th, 2010 at 16:43BorisFebruary 10th, 2010 at 17:19Brett ZamirFebruary 10th, 2010 at 21:43WesFebruary 13th, 2010 at 09:20Benjamin MeyerFebruary 16th, 2010 at 23:14Dan WelshMarch 2nd, 2010 at 06:50sn123March 13th, 2010 at 09:07