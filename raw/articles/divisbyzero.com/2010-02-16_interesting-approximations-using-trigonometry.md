---
title: Interesting approximations using trigonometry
url: https://divisbyzero.com/2010/02/16/interesting-approximations-using-trigonometry/
author: Dave Richeson
published: '2010-02-16'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Today on Twitter [John D. Cook](http://www.johndcook.com/blog/), writing as [@AlgebraFact](http://twitter.com/AlgebraFact), posted [the following tweet](http://twitter.com/AlgebraFact/status/9198144080):

In radians, sin(11) is very nearly -1.


(It happens to be -0.9999902…)

I thought that was awesome! So, I ([@divbyzero](http://twitter.com/divbyzero)) [replied](http://twitter.com/divbyzero/status/9199869318) that cos(333) is approximately 1. (It is 0.999961…)

Then [@michiexile](http://twitter.com/michiexile) [chimed in](http://twitter.com/michiexile/status/9200080264), pointing out that cos(355) is closer to -1 than cos(333) is to 1. (It is -0.9999999995…)

Finally, I [countered with](http://twitter.com/divbyzero/status/9200236234) cos(103993), which is 0.9999999998…

So what’s going on here?

All of this comes from the [continued fraction for ](http://mathworld.wolfram.com/PiContinuedFraction.html),

.


It is well known that the convergents of a continued fraction (i.e., the fraction you obtain by truncating a continued fraction at some point) are the best rational approximations for the number. The first ten convergents of are


,

,

,

,

,

,

,

,

,

.


Notice that , so

. Thus

. This was John D. Cook’s observation.


Similarly, , so

, and

. The other two approximations come from the next two convergents.


After the conversation on Twitter, I started playing a little more.

First, I noticed that

.


()


This comes from the third convergent. Since implies that

,

.


Actually, we can do better than that:

.


()


The approximation, implies that

, so

.


Next, I noticed that

.


()


This comes from , which implies that

. Thus


Finally, I noticed that

.


()


In this case, gives

, and

. We obtain the result by substituting the previous approximation for

.


Of course, we also have

.


()


That’s great! You really ran with this.

One footnote: Good approximations to pi lead to great approximations to 1 when you take sines. Taylor series says sin(pi/2 + h) is approximately 1 – 0.5 h^2 for small h. So the error in the approximation for pi gets squared.

John,

Thanks for pointing that out. I did notice that some approximations were better than others, but hadn’t thought about why.

Dave

Reminds me of my favorite calculator trick.

Set your calculator to degrees mode (NOT radians).

Type in a bunch of 5’s: 555555, or whatever.

Press “1/x”.

Press “sin”.

Examine the mantissa of the result. Magic!

Excellent, I’d never seen that before! Good use of

and the radians-to-degrees conversion. I’ll have to show that to my students.

Found a small typo in your typesetting: the CF of pi is 3; 7, 15, 1, 292 – you forgot the 1 after the 15 in your nested fraction.

Wow, good eyes. Thank you for catching that. I updated the post.

Awesome.. You guys really doing some good approximation and bringing some fun to it. How I wish Twitter had been there in my school days.

Hi, seems like you have done gross approximations.

Tan 4pi/3 is no way near sec 4pi/3 . Same goes for 5pi/3. Unless i am missing something :)

Thanks for catching the typos. They’re fixed now.

I read through the post several times and discussed it with my friends. I am unable to understand why have you approximated tan(111) using sec(111) and tan(69447) using sec(69447).

This is especially puzzling when I consider that computing sec(4*pi/3) in radians yields -2 and tan(4/3 * pi) is 1.7320! They aren’t even close! I’m utterly puzzled.

I’d really appreciate some insight into your thought process.

On an aside, I’d much appreciate it if you deleted my previous comment. I can’t really edit my comment, so I re-posted.

Thanks for catching those typos.

No problem. :)