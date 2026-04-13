---
title: Mathematical magic tricks for kids
url: https://divisbyzero.com/2010/08/02/mathematical-magic-tricks-for-kids/
author: Dave Richeson
published: '2010-08-02'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

My six-year-old son loves the website [ActivityTV.com](http://www.activitytv.com/), especially their science, origami, cooking, and magic videos.

I watched a few of the magic how-to videos with him and was pleasantly surprised to see that some of them had a distinctly mathematical feel to them. For example:

[Jumping rubber bands](http://www.activitytv.com/124-jumping-rubber-band): topological properties of circles and linked circles[Magic knots](http://www.activitytv.com/828-magic-knots): knot theory[Ring escape](http://www.activitytv.com/694-ring-escape): topology/knot theory[Magic compass](http://www.activitytv.com/953-magic-compass): reflections of a square[Mathemagic](http://www.activitytv.com/564-mathemagic): properties of integers

When I stared to watch the “mathemagic” video I was expecting one of those formulaic tricks involving the integers which are simply basic algebra in disguise. While not earth shattering, the trick turned out to be slightly more subtle than that. In case you don’t want to watch the video, here’s the trick:

Pick a 3-digit number with all three digits different. Reverse the digits and subtract to get another 3-digit number (if the difference is negative, take its absolute value, if it is less than 100, add leading zeros (e.g., 71 becomes 071). Reverse the digits of the difference and add it to the difference. Your sum will be 1089.

For example, start with 845. Then 845-548=297 and 297+792=1089.

Usually “Ryan” explains his tricks afterward. For this one he doesn’t. So why does it work?

SPOILER: Suppose you pick the number (that is,

). Furthermore, suppose

(the other case is handled similarly). This implies that

. If we reverse the digits and subtract we obtain


.


This is perhaps easier to see if we line the digits up in columns (note that so we must “carry” twice):


Finally, if we reverse the digits and add we get

,


as promised.

(Actually, if you examine the trick more closely you see that the three digits need not be distinct. But the number cannot be a palindrome; that is, .)


[Aside: it is too bad that “Ryan” starts this video with his comments about math not being fun.]

David Acheson, A professor at one of the Oxford University schools has a book whose title is drawn from this “trick”, 1089 and All That.

In the first chapter he explains how he saw the trick at age ten or so, in a magazine for younger folks. He described it as, “The first piece of mathematics that really impressed me.”

His love of “tricks” led to a mathematical study of “the Indian Rope trick” which is pretty amazing.

I’ve seen that book, but hadn’t read it. I didn’t know what 1089 referred to. Thanks!