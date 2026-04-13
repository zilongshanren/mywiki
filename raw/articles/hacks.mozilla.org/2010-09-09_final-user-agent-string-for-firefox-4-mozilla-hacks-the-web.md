---
title: Final User Agent String for Firefox 4 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/09/final-user-agent-string-for-firefox-4/
author: Dan Witte
published: '2010-09-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

With a title like that, you just know this is going to be fun. (No, seriously.)

The user agent string is one of those wonderfully eclectic things, a balance of modernity and antiquity. Except mostly skewed toward antiquity. It’s grown, piece by piece, over the years; because everyone has their own special way of parsing it, it’s a notoriously sensitive beast. Adding to it is relatively simple, but removing or rearranging bits is not.

If you’re a web developer and you rely on bits in the UA string, this post is definitely for you. As it so happens, the UA string for [Internet Explorer 9](http://blogs.msdn.com/b/ie/archive/2010/03/23/introducing-ie9-s-user-agent-string.aspx) has undergone some revision, and Microsoft has recently announced the string for [IE Mobile](http://blogs.msdn.com/b/iemobile/archive/2010/03/25/ladies-and-gentlemen-please-welcome-the-ie-mobile-user-agent-string.aspx). This makes the time ripe for a revision so that web developers can make the necessary changes to sniffer code all at once.

This is what the User Agent string will look like for Firefox 4 on 32-bit Windows:

![User Agent string](../../assets/4b92cb7f5bc816f7.png)


**Note that this string will change depending on the user environment, platform and architecture.** It’s particularly important to understand that the string can change quite a bit depending on if you’re on a phone, on Windows, Windows 64 bit, a Mac or any variety of Linux-based devices.

In addition, Gecko, the underlying browser platform used by Firefox, is used as a basis for a number of other products. Those products will likely produce Firefox-like strings, and you should be prepared to handle them and treat them much like Firefox. (See below for more details.) **If you’re sniffing the UA string, you should consider carefully** what you’re trying to achieve, and whether you can feature-sniff instead. See [this excellent article](http://articles.sitepoint.com/article/dhtml-utopia-modern-web-design/4) for some suggestions on how you can do this.

For a complete reference, see the [Gecko User Agent String Reference](https://developer.mozilla.org/En/Gecko_User_Agent_String_Reference). There’s also a [text file](http://people.mozilla.com/~dwitte/ua.txt) you can test against, with a large set of UA strings for new and old versions of Firefox and other Gecko-based browsers.

Here’s a list of what’s changed since Firefox 3.6:

1) The locale (e.g. “en-US;”) is gone. The locale of the browser is not always the same as the locale the user prefers to view content in — the HTTP Accept header is the recommended source of this information.

2) The “U;” is gone. Back in the day, this was used to denote browsers with strong encryption from those without. Nowadays, no browser ships with weak encryption. This means that if you’re sniffing for “U;”, you should stop doing so, or — if you must — sniff for the lack of strong encryption (“I;” or “N;”).

3) The “Windows;” prefix is gone from the (surprise!) Windows-specific string. Note that the number of semicolon-delimited fields within the platform token varies between different platforms!

4) Browsers running on the Nokia mobile Maemo (and Meego) platforms will now report themselves as “(Maemo; Linux armv7l; …)”. This is in keeping with the Android mobile string “(Android; Linux armv7l; …)”, and we will continue to add different strings here as more Linux platforms come into play.

5) A rather minor detail, but worth noting — for Linux i686 builds running on an x86_64 platform, the platform-specific part will now read “(X11; Linux i686 on x86_64; rv:…)”. This changed from “(X11; Linux i686 (x86_64); rv:…)”. (Nested parentheses are a bad idea!)

6) The Gecko build date in the “Gecko/yyyymmdd” token **has been frozen to 20100101 for Firefox releases**. This means:

**If you want to detect whether the browser is genuine Gecko**, search for the strings “Gecko” and “rv:”. The presence of these two strings will distinguish Gecko from browsers who state they are “like Gecko” in the UA string.**If you want to determine the Gecko version**, first — as noted above — consider carefully whether you can[feature-sniff instead](http://articles.sitepoint.com/article/dhtml-utopia-modern-web-design/4). If you must, obtain it from the “rv:x.y.z” string.

**If you are presently using the build date or otherwise depending on the exact format of the **“Gecko/yyyymmdd”** token, stop!** In the next major release of Gecko, this will be replaced by the string “Gecko/”. If you rely on the fact that this will be followed by a date string, you will break.

For testing purposes, the unfrozen build date is still included in nightly builds of Firefox, but it will be removed in future nightly builds.

7) For Gecko-based browsers other than Firefox, the way they identify themselves has changed. For instance, this is what it’ll look like for Fennec, the mobile version of Firefox:

![Fennec User Agent string](../../assets/7725e50ef68ddb4d.png)


**Firefox token**. This is a compatibility token that*some*Gecko-based browsers will use; for instance Fennec — and Camino (for Mac) — wish to appear like Firefox for maximum compatibility with websites. (The version portion of the string will generally represent the Firefox version corresponding to the given release of Gecko.) Now, this is an optional token that some Gecko-based browsers may not opt into. For this reason, sniffers should be looking for Gecko — not Firefox! For Firefox itself and other browsers that don’t opt in, this token will not appear, since it’s taken care of by:**Application**. This will be something like “Firefox/4.0.1” for Firefox itself, or “Fennec/2.0.1”, or “Camino/2.1.1”. In addition, testing builds of Firefox (Minefield nightlies and prerelease builds) will now identify themselves as Firefox rather than Minefield.

It’s also worth noting why we *didn’t* change some things. The “X11” part of the Linux string may appear redundant, but it’s actually not: desktop machines are almost exclusively running X11, but Android phones are not, and Maemo (while X11-based) should be differentiated. For reasons like this, the various platform-specific parts of the string are important to know: there are different tokens for Windows 64 on x64, or WoW64 (a 32-bit browser on a 64-bit Windows); PPC or Intel on Mac OS X; and the various environments and architectures for Linux. Here are some examples of various Gecko-based browsers on various platforms:

Mozilla/5.0 (Windows NT 5.2; rv:2.0.1) Gecko/20100101 Firefox/4.0.1

Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1

Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1

Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1

Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1

Mozilla/5.0 (Windows NT 6.0; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre


Mozilla/5.0 (Macintosh; Intel Mac OS X 10.5; rv:2.0.1) Gecko/20100101 Firefox/4.0.1

Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1

Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre


Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1

Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1

Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1

Mozilla/5.0 (X11; Linux i686; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre


Mozilla/5.0 (Android; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1

Mozilla/5.0 (Android; Linux armv7l; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre Fennec/2.0b1pre

Mozilla/5.0 (Maemo; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1

Mozilla/5.0 (X11; Linux armv7l; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1

Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1

Mozilla/5.0 (X11; Linux i686 on x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Fennec/2.0.1

Mozilla/5.0 (X11; Linux i686; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre Fennec/2.0b1pre


Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Camino/2.2.1

Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre Camino/2.2a1pre


There are some other important changes relating to how the UA string can be modified by external programs, Firefox addons, and users themselves. These changes will be detailed in another post, but the upshot is that the strings you see here are what you’ll see in the wild.

Now, if you’re a web developer, take note! All these changes will be in Firefox 4 Beta 6 (soon to be released), so if you want to be ahead of the game, you’re welcome to test against it. As noted above, for a complete list of UA strings to test against in all their glorious variations, see the [link above](https://developer.mozilla.org/En/Gecko_User_Agent_String_Reference) and the [text file](http://people.mozilla.com/~dwitte/ua.txt). Happy sniffing!

## 47 comments

fearphageSeptember 9th, 2010 at 12:08Nicholas C. ZakasSeptember 9th, 2010 at 12:15ddahlSeptember 9th, 2010 at 13:47Robert KaiserSeptember 9th, 2010 at 13:47RobinSeptember 9th, 2010 at 14:34BorisSeptember 11th, 2010 at 07:31Don MartiSeptember 9th, 2010 at 14:53Tony MechelynckSeptember 9th, 2010 at 17:25BorisSeptember 9th, 2010 at 18:09Tony MechelynckSeptember 9th, 2010 at 20:58HenrySeptember 12th, 2010 at 01:36DavidSeptember 9th, 2010 at 19:00Tony MechelynckSeptember 9th, 2010 at 21:18DavidSeptember 9th, 2010 at 22:27Tony MechelynckSeptember 10th, 2010 at 04:34HenrySeptember 12th, 2010 at 01:32Hans WalterSeptember 13th, 2010 at 06:44ThomasSeptember 10th, 2010 at 00:05ThomasSeptember 10th, 2010 at 00:08Ben BuckschSeptember 10th, 2010 at 06:30discoleoSeptember 10th, 2010 at 08:12Tony MechelynckSeptember 10th, 2010 at 08:43Tony MechelynckSeptember 10th, 2010 at 08:44DavidSeptember 10th, 2010 at 17:10BorisSeptember 11th, 2010 at 07:29Don MartiSeptember 11th, 2010 at 07:41Stephen ZSeptember 11th, 2010 at 13:11Tony MechelynckSeptember 13th, 2010 at 03:44Stephen ZSeptember 13th, 2010 at 13:55RCLSeptember 24th, 2010 at 11:34RSEDecember 7th, 2011 at 02:39ThomasSeptember 12th, 2010 at 09:45Hans WalterSeptember 13th, 2010 at 06:49JohnSeptember 14th, 2010 at 11:26gialloporporaMarch 17th, 2011 at 11:25Tony MechelynckMarch 18th, 2011 at 09:30Peter DMarch 21st, 2011 at 23:59HemiltonMarch 22nd, 2011 at 09:24Tony MechelynckMarch 22nd, 2011 at 16:31AlenônimoMarch 31st, 2011 at 16:15RihardsMarch 31st, 2011 at 19:16TravisApril 1st, 2011 at 10:47gialloporporaMay 5th, 2011 at 09:55Tony MechelynckMay 6th, 2011 at 07:57CristianJuly 6th, 2012 at 23:07AstridSeptember 13th, 2012 at 06:19Chloe VevrierDecember 18th, 2012 at 14:42