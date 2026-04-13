---
title: 'Developer Edition 41: View source in a tab, screenshot elements, HAR files,
  and more – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/07/developer-edition-41-view-source-in-a-tab-screenshot-elements-har-files-and-more/
author: Jeff Griffiths
published: '2015-07-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When we introduced the [new Performance tools](https://hacks.mozilla.org/2015/06/new-performance-tools-in-firefox-developer-edition-40/) a few weeks ago, we also talked about how the Firefox Dev Tools team had spent a lot of time focusing on user feedback and what we call ‘polish’ bugs – things reported via [our UserVoice feedback channel](http://mzl.la/devtools) and [Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox&component=Developer%20Tools). Even though the Firefox 41 was a short release cycle for us, this focus on user feedback continues to pay off — several new features that our community had been asking for landed in time for the release. Here’s a closer look:

### Screenshot the selected node in the Inspector

New contributor Léon McGregor implemented an interesting suggestion that was posted in [UserVoice](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/6060256-add-screenshot-of-selected-element-to-inspector). This functionality has been available via the gcli ‘screenshot’ command for quite some time, but is much more discoverable and useful as a context menu item. When the screenshot is created, Firefox copies it to your configured downloads directory.

### View source in tab

Starting with Firefox 41, when you right-click and select **View Page Source**, the html source view will open in a tab instead of a new window. This was a hugely popular request and we would have shipped it earlier but what started out as a seemingly simple change was actually quite involved: See the bug linked below for all the gory details. Importantly, we have also ensured that **View Page Source** provides you with the source of the page as-is from Firefox’s cache – we do not fetch a new version.

### Add Rules button

It’s very convenient to be able to add a new rule to the Inspector as you work, and this is a feature from Firebug that users have requested for some time. During this last cycle, we spent some time polishing our implementation, and provided the convenience of a UI button in addition to the context menu command.

### “Copy as HAR” and “Save all as HAR”

Another feature from Firebug that is particularly popular with Selenium users is the ability to export [HAR archives](https://dvcs.w3.org/hg/webperf/raw-file/tip/specs/HAR/Overview.html) for the current page.

### Other notable changes

In total, 140 Developer Tools bugs have been fixed in Firefox since June 1st. On behalf of the team, I’d like to thank all of the people who reported bugs, tested patches, and spent many hours working to improve this version of Firefox Developer Edition, and especially these contributors that fixed bugs: edoardo.putti, fayolle-florent, 15electronicmotor, veeti.paananen, sr71pav, sjakthol, ntim, MattN, lemcgregor3, and indiasuny000. **Thanks!**.

[Bug 1164210](https://bugzilla.mozilla.org/show_bug.cgi?id=1164210)– $$() should return a true Array[Bug 1077339](https://bugzilla.mozilla.org/show_bug.cgi?id=1077339)– Display keyboard shortcuts when hovering panel tabs[Bug 1163183](https://bugzilla.mozilla.org/show_bug.cgi?id=1163183)– Show HTML5 Forms pseudo elements in the rule view[Bug 1165576](https://bugzilla.mozilla.org/show_bug.cgi?id=1165576)– Netmonitor theme refresh[Bug 1049888](https://bugzilla.mozilla.org/show_bug.cgi?id=1049888)– Make the storage actor work in e10s and Firefox OS[Bug 987365](https://bugzilla.mozilla.org/show_bug.cgi?id=987365)– Add pseudo-class lock options to rule view[Bug 1059882](https://bugzilla.mozilla.org/show_bug.cgi?id=1059882)– Frame selection command button should be visible by default[Bug 1143224](https://bugzilla.mozilla.org/show_bug.cgi?id=1143224)– Opening the netmonitor slows down requests on the page[Bug 1119133](https://bugzilla.mozilla.org/show_bug.cgi?id=1119133)– Keyboard shortcut to toggle devtools docking mode between last two positions[Bug 1024693](https://bugzilla.mozilla.org/show_bug.cgi?id=1024693)– Copy CSS declarations[Bug 1050691](https://bugzilla.mozilla.org/show_bug.cgi?id=1050691)– Click on a function on the console should go to the debugger

[ Download Firefox Developer Edition 41 now](http://mzl.la/1JQwR0o). Let us know what you think and

[what you’d like to see](http://mzl.la/devtools)in future releases. We’re paying attention.

## About
[
Jeff Griffiths ](http://canuckistani.ca/)

Jeff is Product Manager for the Firefox Developer Tools and occasional Open Web hacker, based in Vancouver, BC.

## 10 comments

Jesus PeralesJuly 8th, 2015 at 14:31Adrian@DotcomsecurityJuly 8th, 2015 at 15:09IvanJuly 9th, 2015 at 05:34Jeff GriffithsJuly 9th, 2015 at 11:53IvanJuly 10th, 2015 at 05:08Jeff GriffithsJuly 13th, 2015 at 14:29IvanJuly 13th, 2015 at 19:18Nick FitzgeraldJuly 9th, 2015 at 21:01TobyJuly 14th, 2015 at 12:40TobyJuly 15th, 2015 at 13:22