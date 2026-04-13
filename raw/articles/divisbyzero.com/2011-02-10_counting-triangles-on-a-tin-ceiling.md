---
title: Counting triangles on a tin ceiling
url: https://divisbyzero.com/2011/02/10/counting-triangles-on-a-tin-ceiling/
author: Dave Richeson
published: '2011-02-10'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

This morning a student popped in to my office and said he had a math question for me, and that it wasn’t related to a class he was taking.

He said that his apartment has a tin ceiling with square tiles. The tiles have X’s through them, as illustrated below:

![](../../assets/5ed5947303a6c593.png)


He asked: “Is there a formula for computing the total number of triangles in the ceiling?”

He went on to clarify that he wasn’t interested in counting only the small triangles, but * all possible* triangles that can be formed from these lines.

I said that in all likelihood the answer is “yes,” but that I didn’t know of a formula, and I didn’t know how to go about looking it up. So we rolled up our sleeves, grabbed a whiteboard marker, and started investigating.

First of all, we assumed that his ceiling was an grid of square tiles (we didn’t consider

—we’ll leave that case for homework).


I’ll end this blog post here in case you want to think about the problem yourself. I’ll give our solution in my [follow-up post](https://divisbyzero.com/2011/02/10/counting-triangles-on-a-tin-ceiling-solution-2).

Hi,

If the case is (m x n) = (4 x 3) or (3 x 4) then can we go for (3 x 3) calculation and then consider (1 x 3) separately and calculate the number of triangles?

I have done the same and came to a value, that is 3 rows and 4 columns are there in the tin ceiling, the number of triangles will be (158).

Please tell me if the answer is correct.