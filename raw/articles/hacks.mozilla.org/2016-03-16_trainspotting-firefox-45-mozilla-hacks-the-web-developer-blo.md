---
title: 'Trainspotting: Firefox 45 – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2016/03/trainspotting-firefox-45/
author: Sergi Mansilla
published: '2016-03-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Trainspotting is a series of posts highlighting what’s new in release versions of Firefox. A new version of Firefox is shipped every six weeks – we at Mozilla call this pattern “release trains.”*

March winds bring April showers, and also the latest and greatest version of Firefox! Let’s take a look at some of the new goodies and other changes in the browser.

## Tab Sync

![Location bar suggestions for tabs open on other devices](../../assets/1cfcdb4ce63c4beb.png)

If you have tabs open in Firefox on another device, those tabs will now appear as suggestions in the [Awesome Bar](https://support.mozilla.org/en-US/kb/awesome-bar-search-firefox-bookmarks-history-tabs). It’s a fast way to pick up where you left off on your phone or work computer. You can also view the full list of tabs open on other devices via [a toolbar button menu](https://support.mozilla.org/en-US/kb/view-synced-tabs-other-devices).

## Developer Tools

![negative filtering of requests in the network panel](../../assets/e66d9727deaa7d45.gif)

You’ve been able to [filter network requests by URL](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor#Filtering_by_URL) since Firefox 40, but now you’re able to filter *out* requests you’re not interested in by pre-pending ‘-‘ to your filter terms. Handy in long-lived single-page webapps where many requests occur over the duration of a page session.

### Animation Panel Enhancements

![animation property break-down](../../assets/0e5fd6103e2cdd22.png)


The animation panel has a few new tricks up its sleeve (sleeves? not sure how many limbs a devtool has). You can now view a list of individual properties being modified by each animation. The expanded view of the timeline also has markers for each keyframe that applies to the specific CSS property.

Also new in Firefox 45 is the ability to adjust the playback rate in the Animation Panel for fine-tuning those complex sequences in slow motion. Should speed up debugging quite a bit.

## Goodbye Tab Groups

![organize your tabs into groups using the Tab Groups extension](../../assets/b6635bc5d5d43298.png)


**Hello Tab Groups!** If you know about the Tab Groups feature in Firefox, there’s a pretty good chance you are a die-hard power user of the feature. That group, however, was a very small percentage of users, and the feature was removed to simplify Firefox’s code base. Never fear! Simultaneously, add-on developer

[Quicksaver](https://addons.mozilla.org/en-US/firefox/user/quicksaver/)stepped up and hosted the Tab Groups code into a Firefox extension! All the visual organizing, drag-n-dropping action is just as it was before. Kudos to Quicksaver for keeping the power-user dream alive!

There’s always more to talk about in a Firefox release than I have words for, and 45 is no exception. Check out [the release notes](https://www-dev.allizom.org/en-US/firefox/45.0/releasenotes/) for a high-level list of changes in the browser, or peruse the [detailed list of developer facing changes](https://developer.mozilla.org/en-US/Firefox/Releases/45) on MDN.

## 2 comments

AsthMarch 21st, 2016 at 05:31Mysterious AndyMarch 22nd, 2016 at 08:02