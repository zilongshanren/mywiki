---
title: A neat probability rule-of-thumb
url: https://divisbyzero.com/2011/09/14/a-neat-probability-rule-of-thumb/
author: Dave Richeson
published: '2011-09-14'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Disclaimer: I am NOT a probabilist. Not only have I never taught probability, the last time I *took* a course in probability was in my sophomore year of college. So if this is well known (or totally wrong), forgive me.

A non-mathematician friend of mine shared [this link](http://www.flmnh.ufl.edu/fish/sharks/attacks/relarisklifetime.html) with me. It compares the lifetime risk of dying by various means—cancer, heart disease, shark attack, etc. There are many problems with the analysis presented on this web page (for example, you are not equally likely to die from the flu in each of your 77.6 years (the average lifespan), conditional probability would be a more useful measure of risk for some of these, etc.), but I will ignore all of that. I want to focus on the last line. It says:

Lifetime risk is calculated by dividing 2003 population (290,850,005) by the number of deaths, divided by 77.6, the life expectancy of a person born in 2003.


For example, for drowning the risk is 1 in

Stated another way, they are claiming that if people die each year from a given cause, the total population is

, and the life expectancy is

, then the probability of dying from the given cause is

. I saw this and I thought, “Surely this is wrong. Why would

*that formula* give the probability?”

So I tried to calculate it myself. Here is my back-of-the-envelope calculation. The chance of dying from this cause in one year is . The chance of

*not* dying from this cause in one year is , the chance of not dying from this cause for

years is

, and so the chance of dying from the cause in

years is

. (Of course, this leaves open the possibility of dying several times in those

years, but we’ll ignore that.)


Let’s use this formula with the drowning example. I get , or 1 in

.


What?!?! I was shocked to see an answer almost identical to the one using the “wrong” technique. There must be more to this than I first thought. Let’s look a little closer.

First, notice that . Sitting inside this expression is a sub-expression that looks a lot like the limit definition of

. In particular, because

is a large number, this expression is very nearly

. Aha! There’s the

term! But we still don’t quite have what we want.


What we’ve shown is that if the probability someone dies of a given cause in one year is , then the probability that they will die from it in

years is approximately

. Now suppose the probability

is small (like the probability of dying by drowning). We will compute the linear approximation to this function at

. We see that

. At

, that derivative is

. So the linear approximation at

is simply

. In particular, if we evaluate it at our specific annual probability value

, we obtain

. And there it is! [Update: thank you to the commenters for pointing out that the introduction of the exponential function, while fine, is unnecessary. Quicker: just use the linear approximation for

at

.]


Again, I’ve never seen this before. Perhaps it is well known. For example, maybe it is a good rule-of-thumb that all good actuaries know.

I’d be happy to hear people’s thoughts about this formula and my reasoning. Maybe there’s another, different way to see this.

[I’d like to thank my colleague Jeff Forrester for talking through this with me.]

Here’s an interesting follow up. If the actuaries have to assign a dollar value to a policy based on one of these probabilities, and they have 20,000,000 people signed up to a policy for 50 years each, how much money do they gain or lose depending on which approximation they use to calculate this probability?

Everything you’ve done is correct – here’s an equivalent though maybe mentally quicker way:

(1-x)^t = 1 – (t choose 1) x + (t choose 2) x^2 + … etc. (binomial theorem)

the interesting here is your x is D/P, which is typically a small number, in your particular case on the order of 10^{-5}. Thus, by the time you get to x^2 you’re already facing a 10^{-10} multiplier, whereas your t=L is only going to give you about 100 at most.

Therefore 1-(1-x)^t is roughtly 1 – (1-tx) = tx. Here your t=L and x = D/P, so you get your desired thing.

@dwee: since 10^{-10}*100 = 10^{-8}, and you have about 2*10^7 people, I wouldn’t see your total $ being off by more than a couple of orders of magnitude away from the dollar (on the safe side I may go with 100 dollars. I hope I’m not totally wrong with this since I really need to sleep).

If x is small, (1-x)^n = 1 – x*n + O(x^2).

So, (1-D/P)^L can be approximated by 1 – L*D/P. Your expression follows.

Thanks, Yan and Dude. You’re right. The introduction of the exponential function is unnecessary.

Very well known result, and quite useful. I’m surprised your sophomore course didn’t include it.

Well, maybe we did learn it. But that was 20 years ago…