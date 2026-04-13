---
title: The math behind a neat calculator trick
url: https://divisbyzero.com/2010/02/17/the-math-behind-a-neat-calculator-trick/
author: Dave Richeson
published: '2010-02-17'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

[Update: after you read this post, read [my follow-up post](https://divisbyzero.com/2010/02/18/more-about-the-neat-calculator-trick/).]

I received an interesting comment on [yesterday’s blog post](https://divisbyzero.com/2010/02/16/interesting-approximations-using-trigonometry/) from [Nemo](https://self-evident.org/). It was a cool calculator trick that I’d never seen before. Nemo wrote:

Reminds me of my favorite calculator trick.


Set your calculator to degree mode (NOT radians).

Type in a bunch of 5’s: 555555, or whatever.

Press “1/x”.

Press “sin”.

Examine the mantissa of the result. Magic!

Well, if you give it a try you find out that

,


and similarly

.


Surely it can’t be a coincidence that the significant digits look so much like . It isn’t.


So why does this work?

First, notice that . Thus, if

(the

-digit integer of all 5’s), then

.


Also, you may remember that for close to zero,

. Of course, this is only true if you are using radians. If you are using degrees, then for

close to zero

.


Putting this all together we see that .


Ta da!

Now take your result, multiply it time 1 x 10^(-k-2) so you get almost pi and subtract it from the real pi. The difference is close to pi (with the decimal point shifted).

Thanks, Robert! That’s amazing. Your comment inspired a follow-up post.

11 radians you mean. That’s the answer

Nice. This was just small enough and interesting enough to fit into my working memory and give me a jolt of happy.

Very nice trick, will be using that one myself =] and also nice explanation of why

Can we get e using similar trick?