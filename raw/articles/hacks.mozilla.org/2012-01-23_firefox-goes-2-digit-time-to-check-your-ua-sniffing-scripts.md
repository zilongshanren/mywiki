---
title: Firefox goes 2-digit, time to check your UA sniffing scripts – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2012/01/firefox-goes-2-digit-time-to-check-your-ua-sniffing-scripts/
author: Jean-Yves Perrier
published: '2012-01-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We all know it: [UA-based browser detection](http://en.wikipedia.org/wiki/User_agent_string#User_agent_sniffing) is bad, [the right way is feature-detection](https://developer.mozilla.org/en/Web_development/Writing_forward-compatible_websites). Regardless, legacy code relies upon UA sniffing and may need to be updated for Firefox 10’s release.

Even if it looks simple, UA parsing has proven to be a headache for numerous script authors. Though the [structure of an UA is defined in the HTTP specification](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.43), the way relevant information is conveyed varies from one vendor to another. Also, the information you want to extract from it is not always the same: sometimes you want to know the browser (Firefox, SeaMonkey, Safari, Chrome, IE, Opera…), but most of the time you want to know the engine that powers them (Gecko, Webkit, Trident,…). You also need to get the version of the browser or the engine.

Old scripts often made some undue assumptions. Some are assuming that browser version numbers will never reach 10… This is not the case: Opera and Chrome have already crossed this landmark long ago, Firefox will reach it next week and [IE soon after](http://blogs.msdn.com/b/ie/archive/2011/04/15/the-ie10-user-agent-string.aspx).

A few examples of Firefox UAs that your scripts should allow:

- Regular Firefox version:
*Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:10.0) Gecko/20100101 Firefox/10.0* - Nightly and Aurora Firefox versions:
*Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:12.0a1) Gecko/20120122 Firefox/12.0a1* - Chemspill Firefox version (three numbers)
*Mozilla/5.0 (Windows NT 6.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1*

*So, it is the last moment to check your UA-based browser detection code before your site goes havoc!*

### Last chance to check

*Do it right now, in two weeks it would be too late.*

What to do?

- Code inspection: check your code to see if there is some UA-based browser detection code. If so, check if it handles multi-digit versions. (At the same time you could check if it is useful at all. Some old UA-detection code has not worked in ages, or try to go around problems fixed since years in browser…)
- Library inspection: lots of libraries perform UA-based browser detection. If you are using any of them, check if it still is working with a version of Firefox with 2 digits. If not, notify the author of the lib and
[open a bug on bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Tech%20Evangelism)so that we can help others as all their customers are likely to suffer from the same problem. **Check if your site is working with the next Firefox version**: download the[Beta release of Firefox 10](http://www.mozilla.org/firefox/channel/)(you can run[several versions](http://robertnyman.com/2009/07/01/firefox-35-is-released-information-about-having-multiple-firefox-versions-and-web-developer-extension-compatibility/)of Firefox[simultaneously](http://forums.mozillazine.org/viewtopic.php?f=23&t=2249039)) It is always a good idea to use the beta, or even the aurora, version of Firefox if you are maintaining a site: you’ll discover incompatibilities earlier and will get time to fix them before your users start complaining. We are doing our best to prevent problems, but sometimes old code rely on incorrect behavior and stop working even when we are only fixing bugs.- Test other sites :-). Use the beta or aurora version of Firefox and surf the web. When you hit a UA-related problem
[report it with bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Tech%20Evangelism). Give us as much info as possible like the importance of the site in your country and if you have conducted any action yourself. That way our evangelism team will be able to prioritize work adequately.

Finally, you should plan to get rid of these UA-based browser detection mechanism. If you can’t — and I know it isn’t always possible — I would be glad to know why: so please let us know in the comments below.

Now it is time to check your sites :-)

Thank you very much for your help.

## About Jean-Yves Perrier

Jean-Yves is a program manager in the Developer Outreach team at Mozilla. Previous he was an MDN Technical Writer specialized in Web platform technologies (HTML, CSS, APIs), and for several years the MDN Content Lead.

## 41 comments

David MulderJanuary 23rd, 2012 at 02:12Mathias BynensJanuary 23rd, 2012 at 03:11Jean-Yves PerrierJanuary 23rd, 2012 at 04:56BennoJanuary 23rd, 2012 at 04:44Jean-Yves PerrierFebruary 14th, 2012 at 05:01Aryeh GregorJanuary 23rd, 2012 at 16:52MogdenJanuary 25th, 2012 at 13:12Tai TravisJanuary 25th, 2012 at 21:05Leisha FlemingJanuary 31st, 2012 at 11:17ProbablyFebruary 1st, 2012 at 03:52David W, SmithFebruary 2nd, 2012 at 15:22Jean-Yves PerrierMarch 1st, 2012 at 00:42Robert SchwedtFebruary 29th, 2012 at 13:47Jean-Yves PerrierMarch 1st, 2012 at 00:45Nick GilbertJanuary 31st, 2012 at 13:31Brent TilleyJanuary 31st, 2012 at 13:48YehudaJanuary 31st, 2012 at 14:53SimonJanuary 31st, 2012 at 15:19Nick GilbertJanuary 31st, 2012 at 15:48Nick GilbertJanuary 31st, 2012 at 15:52Brent TilleyJanuary 31st, 2012 at 16:03SimonJanuary 31st, 2012 at 19:11ZiggyTheHamsterFebruary 13th, 2012 at 14:35fgsfgsgFebruary 3rd, 2012 at 08:20Jean-Yves PerrierFebruary 10th, 2012 at 11:00Jean-Yves PerrierFebruary 10th, 2012 at 22:54AlhadisFebruary 7th, 2012 at 01:11meiFebruary 8th, 2012 at 11:02Jean-Yves PerrierFebruary 10th, 2012 at 10:57Herbert PetersFebruary 10th, 2012 at 21:46Chas4February 11th, 2012 at 10:08Jean-Yves PerrierFebruary 14th, 2012 at 05:07Phil PishioneriFebruary 13th, 2012 at 17:08Chris HeilmannFebruary 15th, 2012 at 04:07anggelFebruary 14th, 2012 at 04:55PeteFebruary 14th, 2012 at 11:55Jean-Yves PerrierMarch 1st, 2012 at 00:47Zafar Al MasoodFebruary 18th, 2012 at 02:12Jean-Yves PerrierFebruary 18th, 2012 at 02:16joeFebruary 22nd, 2012 at 11:41Jean-Yves PerrierMarch 1st, 2012 at 00:52