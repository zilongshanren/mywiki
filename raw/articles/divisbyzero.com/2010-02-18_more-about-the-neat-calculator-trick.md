---
title: More about the neat calculator trick
url: https://divisbyzero.com/2010/02/18/more-about-the-neat-calculator-trick/
author: Dave Richeson
published: '2010-02-18'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Yesterday I wrote about [a neat calculator trick](https://divisbyzero.com/2010/02/17/the-math-behind-a-neat-calculator-trick/) that I had just learned.

We saw that if the calculator was set to degree mode, then times a high enough power of 10 is approximately

.


A commenter named Robert suggested looking at the difference between this approximation for and

itself. He remarked that the error is also approximately

too (when multiplied by a sufficiently high power of 10)!


For example,

If we shift the decimal point over we get an approximation of :


Now we look at the error

which if we shift again is

Wow! Now why is *this* true?

The key observation is that

or in general,

where denotes the

-digit integer of all 5’s. With a little algebra we see that


As I mentioned last time, if the calculator is in degree mode and , then

. So,


This implies that

Now, the error in this approximation is

We can rewrite this as


Thanks for providing the explanation!

Instead of remembering the decimal expansion for 1/180, I usually just remember that .kkkkkk… is k/9 (where k is any single digit). .1111… is 1/9, from which it follows that .222… is 2/9, etc.

The analogous statement is true in other numerical bases; for example, .222222… in base 3 is 2/3.

All of which follows trivially from the formula for infinite geometric sums, but remembering it this way is sometimes useful.

For example, 555555 is approximately 5/9 times 10^6.

“The analogous statement is true in other numerical bases; for example, .222222… in base 3 is 2/3.”

Shouldn’t that be 2/3 for base _4_, ie, the denominator is base – 1? To state it a different way, .22222… in base 3 is like .99999… in base 10 = 1.