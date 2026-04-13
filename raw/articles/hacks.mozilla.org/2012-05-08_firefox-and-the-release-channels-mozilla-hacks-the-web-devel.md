---
title: Firefox and the release channels – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/05/firefox-and-the-release-channels/
author: Robert Nyman
published: '2012-05-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When we meet and talk to people, there are often questions about Firefox, how the release shedule works and what different channels we have for testing. Therefore, I’d like to introduce you to/remind you about them and also let you know where the most important testing is, both for you and for us.

## Firefox release channels

Basically, we have four different Firefox release channels:

[Firefox Release](http://www.mozilla.org/firefox/)- The official release of Firefox.
[Firefox Beta](http://www.mozilla.org/firefox/beta/)- Testing the next version of Firefox befire it becomes the official release.
[Firefox Aurora](http://www.mozilla.org/firefox/aurora/)- For web/platform developers and early adopters.
[Firefox Nightly](http://nightly.mozilla.org/)- Nightly releases that contains experimental features. (covered regularly on Twitter from
[@firefoxnightly](https://twitter.com/firefoxnightly))

## Firefox release timeline

Firefox is released on a six week schedule, meaning that every sixth week there will be new versions of Firefox Release, Firefox Beta and Firefox Aurora. Nightly is, naturally, released every night.

## Running multiple versions of Firefox at the same time

There are many different ways of running multiple versions of Firefox at the same time. What it all comes down to is setting up different profiles that you have per each web browser instance. The easiest way is most likely to use the [Profile Manager, as described on MDN](https://developer.mozilla.org/en/Profile_Manager).

If you are on Mac OS X, it’s easy to use the [automated version of setting up multiple profiles of Firefox](http://gkoberger.net/n/firefoxes).

Another option, in plain code and as outlined in [Multiple Firefox Instances](http://www.callum-macdonald.com/about/faq/multiple-firefox-instances/), is to just launch the Profile manager directly:

```
# On Windows click Start > Run then:
"C:Program FilesMozilla Firefoxfirefox.exe" -no-remote -ProfileManager
# Mac OS X and Linux, in Terminal
firefox -ProfileManager
# Depending on system/setup, you might need to do this from the directory
./firefox -ProfileManager
```

## Testing Firefox Aurora

The version of Firefox that is the best version to test for web developers is [Firefox Aurora](http://www.mozilla.org/firefox/aurora/). It is in a stable enough condition to use, but also has features at their latest stage before they become approved. Therefore, your chance to affect implementations, find bugs, improve features is when it has become Firefox Aurora – likewise, it gives us a better chance to ensure that when Firefox is officially released, all the things are in place in the best possible manner.

Therefore, please take the time to test out Firefox Aurora and new features, so we can together help Firefox and the web better!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 9 comments

frankMay 8th, 2012 at 07:17Robert NymanMay 8th, 2012 at 10:06ManishMay 8th, 2012 at 11:25Robert NymanMay 9th, 2012 at 06:13Jean-Yves PerrierMay 9th, 2012 at 11:51Elliott RichmondMay 9th, 2012 at 02:26Robert NymanMay 9th, 2012 at 06:14DJ-LeithMay 11th, 2012 at 17:01Robert NymanMay 11th, 2012 at 23:20