---
title: How to Fold a Julia Fractal
url: https://acko.net/blog/how-to-fold-a-julia-fractal/
author: Steven Wittens
published: '2013-01-05'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![How to Fold a Julia Fractal](../../assets/476d408cb959f749.jpg)

# How to Fold a Julia Fractal

## A tale of numbers that like to turn

"Take the universe and grind it down to the finest powder and sieve it through the finest sieve and then show me one atom of justice, one molecule of mercy. And yet," Death waved a hand, "And yet you act as if there is some ideal order in the world, as if there is some… some rightness in the universe by which it may be judged."

Mathematics has a dirty little secret. Okay, so maybe it's not so dirty. But neither is it little. It goes as follows:

*Everything in mathematics is a choice.*

You'd think otherwise, going through the modern day mathematics curriculum. Each theorem and proof is provided, each formula bundled with convenient exercises to apply it to. A long ladder of subjects is set out before you, and you're told to climb, climb, climb, with the promise of a payoff at the end. "You'll need this stuff in real life!", they say, oblivious to the enormity of this lie, to the fact that most of the educated population walks around with *"vague memories of math class and clear memories of hating it."*

Rarely is it made obvious that all of these things are entirely optional—that mathematics is the art of making choices so you can discover what the consequences are. That algebra, calculus, geometry are just words we invented to group the most interesting choices together, to identify the most useful tools that came out of them. The act of mathematics is to play around, to put together ideas and see whether they go well together. Unfortunately that exploration is mostly absent from math class and we are fed pre-packaged, pre-digested math pulp instead.

And so it also goes with the numbers. We learn about the natural numbers, the integers, the fractions and eventually the real numbers. At each step, we feel hoodwinked: we were only shown a part of the puzzle! As it turned out, there was a 'better' set of numbers waiting to be discovered, more comprehensive than the last.

Along the way, we feel like our intuition is mostly preserved. Negative numbers help us settle debts, fractions help us divide pies fairly, and real numbers help us measure diagonals and draw circles. But then there's a break. If you manage to get far enough, you'll learn about something called the *imaginary numbers*, where it seems sanity is thrown out the window in a variety of ways. Negative numbers can have square roots, you can no longer say whether one number is bigger than the other, and the whole thing starts to look like a pointless exercise for people with far too much time on their hands.

I blame it on the name. It's misleading for one very simple reason: all numbers are imaginary. You cannot point to anything in the world and say, "This is a 3, and that is a 5." You can point to three apples, five trees, or chalk symbols that represent 3 and 5, but the concepts of 3 and 5, the numbers themselves, exist only in our heads. It's only because we are taught them at such a young age that we rarely notice.

So when mathematicians finally encountered numbers that acted just a little bit different, they couldn't help but call them *fictitious* and *imaginary*, setting the wrong tone for generations to follow. Expectations got in the way of seeing what was truly there, and it took decades before the results were properly understood.

Now, this is not some esoteric point about a mathematical curiosity. These imaginary numbers—called *complex numbers* when combined with our ordinary real numbers—are essential to quantum physics, electromagnetism, and many more fields. They are naturally suited to describe anything that turns, waves, ripples, combines or interferes, with itself or with others. But it was also their unique structure that allowed [Benoit Mandelbrot](http://en.wikipedia.org/wiki/Benoit_Mandelbrot) to create his stunning fractals in the late 70s, dazzling every math enthusiast that saw them.

Yet for the most part, complex numbers are treated as an inconvenience. Because they are inherently multi-dimensional, they defy our attempts to visualize them easily. Graphs describing complex math are usually simplified schematics that only hint at what's going on underneath. Because our brains don't do more than 3D natively, we can glimpse only slices of the hyperspaces necessary to put them on full display. But it's not impossible to peek behind the curtain, and we can gain some unique insights in doing so. All it takes is a willingness to imagine something different.

So that's what this is about. And a lesson to be remembered: complex numbers are typically the first kind of numbers we see that are undeniably strange. Rather than seeing a sign that says *Here Be Dragons, Abandon All Hope*, we should explore and enjoy the fascinating result that comes from one very simple choice: *letting our numbers turn*. That said, there *are* dragons. Very pretty ones in fact.

## Like Hands on a Clock

What does it mean to let numbers turn? Well, when making mathematical choices, we have to be careful. You could declare that $ 1 + 1 $ should equal $ 3 $, but that only opens up more questions. Does $ 1 + 1 + 1 $ equal $ 4 $ or $ 5 $ or $ 6 $? Can you even do meaningful arithmetic this way? If not, what good are these modified numbers? The most important thing is that our rules need to be consistent for them to work. But if all we do is swap out the *symbols* for $ 2 $ and $ 3 $, we didn't actually change anything in the underlying mathematics at all.

So we're looking for choices that don't interfere with what already works, but add something new. Just like the negative numbers complemented the positives, and the fractions snugly filled the space between them—and the reals somehow fit in between *that*—we need to go look for new numbers where there currently aren't any.

We've seen how complex numbers are arrows that like to turn, which can be made to behave like numbers: we can add and multiply them, because we can come up with a consistent rule for doing so. We've also seen what powers of complex numbers look like: we fold or unfold the entire plane by multiplying or dividing angles, while simultaneously applying a power to the lengths.

## Pulling a Dragon out of a Hat

With a basic grasp of what complex numbers are and how they move, we can start making Julia fractals.

At their heart lies the following function:

$$ f(z) = z^2 + c $$

This says: map the complex number $ z $ onto its square, and then add a constant number to it. To generate a Julia fractal, we have to apply this formula repeatedly, feeding the result back into $ f $ every time.

$$ z_{n+1} = (z_n)^2 + c $$

We want to examine how $ z_n $ changes when we plug in different starting values for $ z_1 $ and iterate $ n $ times. So let's try that and see what happens.

Making fractals is probably the least useful application of complex math, but it's an undeniably fascinating one. It also reveals the unique properties of complex operations, like conformal mapping, which provide a certain rigidity to the result.

However, in order to make complex math practical, we have to figure out how to tie it back to the real world.

## Travelling without Moving

It's a good thing we don't have to look far to do so. Whenever we're describing wavelike phenomena, whether it's sound, electricity or subatomic particles, we're also interested in how the wave evolves and changes. Complex operations are eminently suited for this, because they naturally take place on circles. Numbers that oppose can cancel out, numbers in the same direction will amplify each other, just like two waves do when they meet. And by folding or unfolding, we can alter the frequency of a pattern, doubling it, halving it, or anything in between.

More complicated operations are used for example to model electromagnetic waves, whether they are FM radio, wifi packets or ADSL streams. This requires precise control of the frequencies you're generating and receiving. Doing it without complex numbers, well, it just sucks. So why use boring real numbers, when complex numbers can do the work for you?

## The End Is Just The Beginning

In visualizing complex waves, we've seen functions that map real numbers to complex numbers, and back again. These can be graphed easily in 3D diagrams, from $ \mathbb{R} $ to $ \mathbb{C} $ or vice-versa. You cross 1 real dimension with the 2 dimensions of the complex plane.

But complex operations in general work from $ \mathbb{C} $ to $ \mathbb{C} $. To view these, unfortunately you need four-dimensional eyes, which nature has yet to provide. There are ways to project these graphs down to 3D that still somewhat make sense, but it never stops being a challenge to interpret them.

For every mathematical concept that we have a built-in intuition for, there are countless more we can't picture easily. That's the curse of mathematics, yet at the same time, also its charm.

Hence, I tried to stick to the stuff that is (somewhat!) easy to picture. If there's interest, a future post could cover topics like: the nature of $ e^{ix} $, Fourier transforms, some actual quantum mechanics, etc.

For now, this story is over. I hope I managed to spark some light bulbs here and there, and that you enjoyed reading it as much as I did making it.

Comments, feedback and corrections are welcome on [Google Plus](https://plus.google.com/112457107445031703644/posts/VGzZsTWnCHG). Diagrams powered by [MathBox](https://acko.net/blog/making-mathbox/).

*More like this: To Infinity… And Beyond!.*

*For extra credit: check out these great stirring visualizations of Julia and Mandelbrot sets. I incorporated a similar graphic above. Hat tip to Tim Hutton for pointing these out. And for some actual paper mathematical origami, check out Vihart's latest video on Snowflakes, Starflakes and Swirlflakes.*