---
title: Trig identities from complex exponentials
url: https://fgiesen.wordpress.com/2013/05/13/trig-identities-from-complex/
published: '2013-05-13'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Trig identities from complex exponentials

There’s tons of useful trig identities. You could spend the time to learn them by heart, or just look them up on Wikipedia when necessary. But I’ve always had problems remembering where the signs and such go when trying to memorize this directly. At least for me, what worked way better is this: spend a few hours familiarizing yourself with complex numbers if you haven’t done so already; after that, most identities that you need in practice are easy to derive from Euler’s formula:

Let’s do the basic addition formulas first. Euler’s formula gives:

and once we apply the identity again we get:

multiplying out:

The terms in parentheses are all real numbers; equating them with our original expression yields the result



Both addition formulas for the price of one. (In fact, this exploits that the addition formulas for trigonometric functions and the addition formula for exponents are really the same thing). The main point being that if you know complex multiplication, you never have to remember what the grouping of factors and the signs are, something I used to have trouble remembering.

Plugging in x=y into the above also immediately gives the double-angle formulas:



so if you know the addition formulas there’s really no reason to learn these separately.

Then there’s the well-known

but it’s really just the Pythagorean theorem in disguise (since cos(x) and sin(x) are the side lengths of a right-angled triangle). So not really a new formula either!

Moving either the cosine or sine terms to the right-hand side gives the two *immensely* useful equations:



In particular, that second one is perfect if you need the sine squared of an angle that you only have the cosine of (usually because you’ve determined it using a dot product). Judicious application of these two tends to be a great way to simplify superfluous math in shaders (and elsewhere), one of my [pet peeves](https://fgiesen.wordpress.com/2010/10/21/finish-your-derivations-please/).

For practice, let’s apply these two identities to the cosine double-angle formula:



why, it’s the half-angle formulas! Fancy meeting you here!

Can we do something with the sine double-angle formula too? Well, it’s not too fancy, but we can get this:

Now, let’s go back to the original addition formulas and let’s see what happens when we plug in negative values for y. Using and

, we get:




Hey look, flipped signs! This means that we can now add these to (or subtract them from) the original formulas to get *even more* identities!





It’s the product-to-sum identities this time. I got one more! We’ve deliberately flipped signs and then added/subtracted the addition formulas to get the above set. What if we do the same trick in reverse to get rid of those x+y and x-y terms? Let’s set and

and plug that into the identities above and we get:





Ta-dah, it’s the sum-to-product identities. Now, admittedly, we’ve taken quite a few steps to get here, and looking these up when you need them is going to be faster than walking through the derivation (if you ever need them in the first place – I don’t think I’ve ever used the product/sum identities in practice). But still, working these out is a good exercise, and a lot less likely to go wrong (at least for me) than memorizing lots of similar formulas. (I never can get the signs right that way)

Bonus exercise: work out general expressions for and

. Hint:



.


And I think that’s enough for now. (At some later point, I might do an extra post about one of the sneakier trig techniques: the [Weierstrass substitution](http://en.wikipedia.org/wiki/Weierstrass_substitution)).

Same basis, but it seems like it’d be easier to just remember the axiom for complex numbers and the conjugate, then you can get the angle addition and subtraction and proceed as you have.

Nice post, but your notation is outrageous. For example, cos(x)^2 means cos(x^2), and not (cos(x))^2, as you intended. Please fix these, in order not to confuse the students. Thanks for the tutorial!

I’ve had, variously, professors that used “cos^k(x)”, “(cos(x))^k”, “(cos x)^k” and “cos(x)^k”. All of them would object to some of the other forms.

The non-parenthesized notation for trig functions is a historical artifact, (arguably) an abuse of notation, and riddled with special cases; the cos^k notation is one example, another would be that some authors will write “cos 2a” while some require “cos(2a)” in this case, and there’s some ambiguity whether writing “cos(a)b” means “(cos(a))*b” or “cos(a*b)”. I have seen both interpretations in the wild, which to me is solid evidence that the conventional notation is problematic and should be avoided.

At this point, I just write the trig functions like I write all other function, namely, parentheses (or brackets, or braces, …) around the arguments required on function evaluations. This is consistent, always unambiguous, and matches the behavior of most programming languages in existence (and remember, the audience for this blog is programmers) as well as all symbolic algebra packages I’m familiar with. You’re free to disagree with my choice of course.

Could you give another hint for the bonus exercise? I tried for like 5 hours and still dont have a solution…

Oh geez! Use the binomial theorem, then look at the expansion you get and see if you can wrangle it back into cosines or sines, respectively. (For the latter part, it might help to consider even and odd n separately.)

mhh I’m forming around like crazy and can’t get it working… I don’t know how it will help, if n is even or odd (except for i^n) because I also have terms like (A)^(n-k). And there I don’t have any use of n even, do I? I used the binomial theorem and then I extracted the “k-independent” variables to the front of the sum-symbol. Then I tried to get rid of (cos(x)+isin(x))^(n-k) * (cos(x)-isin(x))^k, but I have no Idea how I could wrangle this back…

Okay, worked through, writing C(n,k) for the binomial coefficient n choose k since I don’t have math formatting in the comments:

cos(x) = 1/2 (exp(ix) + exp(-ix))

-> apply Binomial theorem:

cos(x)^n = 2^(-n) sum(k=0; n) C(n,k) exp(ix)^k exp(-ix)^(n-k)

= 2^(-n) sum(k=0; n) C(n,k) exp(ix*(2k – n))

This sum is symmetric (if you substitute k -> n-k you get the same result).

If n even, that sum has an odd number of terms, and the middle term is C(n,n/2) * exp(0) = C(n,n/2). Pulling that middle term out and rearranging the sum to group the negative-i and positive-i terms together:

= 2^(-n) [C(n,n/2) + sum(k=0; (n-1)/2) C(n,k) (exp(ix*(2k – n)) + exp(ix*(2(n-k) – n))]

= 2^(-n) [C(n,n/2) + sum(k=0; (n-1)/2) C(n,k) (exp(ix*(2k – n)) + exp(-ix*(2k – n))]

= 2^(-n) C(n,n/2) + 2^(1-n) sum(k=0; (n-1)/2) C(n,k) cos(x*(2k-n))

The case for n odd works out similarly except there’s no “middle” term in the sum and therefore no corresponding constant term, you can straight-up split the sum (which now has an even number of terms) in the middle.

sin is analogous.

okay, two questions. First of all, how do you get the 2^(1-n) in the last line? I thought it should be 2^((n-1)/2) because you expant the sum by 2/2 to apply the cosinus.

And for the sinus I have (2i)^(-n) in front of the sum and in the sum I have (1)^(n-k) haven’t I? And this would mean that I only have sin() for odd “n-k” and some cos() for even “n-k”, right? (and what I do with the i if I apply the cosine?

Counter-question: where would you get the 2^((n-1)/2) from?

I turn pairs of terms of the form “exp(ixk) + exp(-ixk)” into “2 cos(x)”. But this is a sum, not a product! E.g. for n=3, we end up with

1/8 (exp(-3ix) + 3exp(-ix) + 3exp(ix) + exp(3ix))

= 1/8 (2 cos(3x) + 2*3 cos(x))

= 1/4 (cos(3x) + 3 cos(x))

because we cancel out exactly one factor of 2 that happens to appear in front of every term.

As for the second question, correct on both counts. What to do with the “i” for even n: absolutely nothing. You end up with “2i ^ (-n)” = 2^(-n) i^(-n) in front of the sum. n is even, so i^(-n) is just (-1)^(-n/2).

Yeah but then you end up with 2^(n-1) and not with 2^(1-n), don’t you?

2^(-n) * 2 = 2^(1-n). I just don’t know what more to explain here.

ahh yeah omg, now I got it sorry and thank you so much :D