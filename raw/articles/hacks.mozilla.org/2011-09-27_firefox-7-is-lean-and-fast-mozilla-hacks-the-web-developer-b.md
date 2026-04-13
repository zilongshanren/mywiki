---
title: Firefox 7 is lean and fast – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/09/firefox-7-is-lean-and-fast/
author: Mozilla Hacks
published: '2011-09-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Based on a blog post originally posted here by Nicholas Nethercote, Firefox Developer. *

**tl;dr**

Firefox 7 now uses much less memory than previous versions: often 20% to 30% less, and sometimes as much as 50% less. This means that Firefox and the websites you use will be snappier, more responsive, and suffer fewer pauses. It also means that Firefox is less likely to crash or abort due to running out of memory.

These benefits are most noticeable if you do any of the following:

– keep Firefox open for a long time;

– have many tabs open at once, particularly tabs with many images;

– view web pages with large amounts of text;

– use Firefox on Windows

– use Firefox at the same time as other programs that use lots of memory.


Background

Mozilla engineers started an effort called [MemShrink](https://wiki.mozilla.org/Performance/MemShrink), the aim of which is to improve Firefox’s speed and stability by reducing its memory usage. A great deal of [progress](http://blog.mozilla.com/nnethercote/category/memshrink/) has been made, and thanks to Firefox’s [faster development cycle](https://wiki.mozilla.org/RapidRelease/Calendar), each improvement made will make its way into a final release in only 12–18 weeks. The newest update to Firefox is the first general release to benefit from MemShrink’s successes, and the benefits are significant.

**Quantifying the improvements**

Measuring memory usage is difficult: there are no standard benchmarks, there are several different metrics you can use, and memory usage varies enormously depending on what the browser is doing. Someone who usually has only a handful of tabs open will have an entirely different experience from someone who usually has hundreds of tabs open. (This latter case is not uncommon, by the way, even though the idea of anyone having that many tabs open triggers astonishment and disbelief in many people. E.g. see the comment threads [here](http://news.ycombinator.com/item?id=2840440) and [here](http://www.reddit.com/r/programming/comments/j7m7k/scalability/).)

**Endurance tests**

Dave Hunt and others have been using the MozMill add-on to perform “[endurance tests](https://wiki.mozilla.org/QA/Mozmill_Test_Automation/Endurance_Tests)“, where they open and close large numbers of websites and track memory usage in great detail. Dave recently performed an [endurance test comparison of development versions of Firefox](http://blargon7.com/2011/07/endurance-tests-demonstrate-firefoxs-memory-usage-improvements/), repeatedly opening and closing pages from 100 widely used websites in 30 tabs.

*[The following numbers were run while the most current version of Firefox was in Beta and capture the average and peak “resident” memory usage for each browser version over five runs of the tests. “Resident” memory usage is the amount of physical RAM that is being used by Firefox, and is thus arguably the best measure of real machine resources being used.]*

![2](../../assets/3ea011fd360c2d97.png)


![3](../../assets/dff5be1ed942648f.png)


The measurements varied significantly between runs. If we do a pair-wise comparison of runs, we see the following relative reductions in memory usage:

Minimum resident: 1.1% — 23.5% (median 6.6%)

Maximum resident: -3.5% — 17.9% (median 9.6%)

Average resident: 4.4% — 27.3% (median 20.0%)

The following two graphs showing how memory usage varied over time during Run 1 for each version. Firefox 6’s graph is first, with the latest version second. (Note: Compare only to the purple “resident” lines; the meaning of the green “explicit” line changed between the versions and so the two green lines cannot be sensibly compared.)

Firefox 7 is clearly much better; its graph is both lower and has less variation.

![ff6](../../assets/759c279120d1f05c.png)


![ff7](../../assets/3cc30d104011dded.png)



MemBench

Gregor Wagner has a memory stress test called [MemBench](http://gregor-wagner.com/tmp/mem). It opens 150 websites in succession, one per tab, with a 1.5 second gap between each site. The sites are mostly drawn from [Alexa’s Top sites](http://www.alexa.com/topsites/category) list. I ran this test on 64-bit builds of Firefox 6 and 7 on my Ubuntu Linux machine, which has 16GB of RAM. Each time, I let the stress test complete and then opened about:memory to get measurements for the peak resident usage. Then I hit the “Minimize memory usage” button in about:memory several times until the numbers stabilized again, and then re-measured the resident usage. (Hitting this button is not something normal users do, but it’s useful for testing purposes because causes Firefox to immediately free up memory that would be eventually freed when garbage collection runs.)

For Firefox 6, the peak resident usage was 2,028 MB and the final resident usage was 669 MB. For Firefox 7, the peak usage was 1,851 MB (a 8.7% reduction) and the final usage was 321 MB (a 52.0% reduction). This latter number clearly shows that [fragmentation](http://en.wikipedia.org/wiki/Fragmentation_%28computer%29) is a much smaller problem in Firefox 7.

(On a related note, Gregor recently [measured](http://gregor-wagner.com/?p=79) cutting-edge development versions of Firefox and Google Chrome on MemBench.)


Conclusion

Obviously, these tests are synthetic and do not match exactly how users actually use Firefox. (Improved benchmarking is one thing we’re working on as part of MemShrink, but we’ve got a long way to go. ) Nonetheless, the basic operations (opening and closing web pages in tabs) are the same, and we expect the improvements in real usage will mirror improvements in the tests.

This means that users should see Firefox 7 using less memory than earlier versions — often 20% to 30% less, and sometimes as much as 50% less — though the improvements will depend on the exact workload. Indeed, we have had lots of feedback from early users that the latest Firefox update feels faster, is more responsive, has fewer pauses, and is generally more pleasant to use than previous versions.

Mozilla’s MemShrink efforts are continuing. The endurance test results above show that the Beta version of Firefox already has even better memory usage, and I expect we’ll continue to make further improvements as time goes on.

## 40 comments

Duke S.September 27th, 2011 at 12:09Joe KatzmanSeptember 27th, 2011 at 12:16SeanSeptember 27th, 2011 at 13:23SeanSeptember 27th, 2011 at 13:26Joe MontibelloSeptember 27th, 2011 at 13:24DanieleSeptember 27th, 2011 at 14:01SanteSeptember 29th, 2011 at 14:36TillSeptember 27th, 2011 at 15:39garySeptember 27th, 2011 at 22:41Jack_IndiaSeptember 28th, 2011 at 01:14AdamSeptember 28th, 2011 at 06:34Carl114September 28th, 2011 at 08:20BwardSeptember 28th, 2011 at 13:38Rational Db8September 29th, 2011 at 02:19RAMOctober 27th, 2011 at 14:18TtoviyahSeptember 29th, 2011 at 06:24Nigel SmithSeptember 29th, 2011 at 07:43Thomas SvensonSeptember 29th, 2011 at 07:47JabbawestSeptember 29th, 2011 at 10:23JimSeptember 30th, 2011 at 10:20JimSeptember 30th, 2011 at 10:22KennethOctober 1st, 2011 at 04:14riqklaOctober 2nd, 2011 at 07:05Mark the Personalised wine GuyOctober 2nd, 2011 at 09:44RahlyOctober 2nd, 2011 at 17:38TranscontinentalOctober 4th, 2011 at 06:36thaddeusmtOctober 6th, 2011 at 10:12NormanOctober 8th, 2011 at 15:02Super SlaveOctober 9th, 2011 at 19:03ErikOctober 10th, 2011 at 12:12Janet SwisherOctober 10th, 2011 at 12:29jacquline kleissOctober 13th, 2011 at 10:00PeteOctober 25th, 2011 at 02:05PeteOctober 27th, 2011 at 19:43angieOctober 31st, 2011 at 20:21DavidNovember 1st, 2011 at 18:08vladNovember 6th, 2011 at 12:46BurnerDecember 15th, 2011 at 22:23BJEJanuary 21st, 2012 at 20:36ACMarch 3rd, 2012 at 13:00