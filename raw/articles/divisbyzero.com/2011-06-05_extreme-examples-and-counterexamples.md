---
title: Extreme examples and counterexamples
url: https://divisbyzero.com/2011/06/05/extreme-example-and-counterexamples/
author: Dave Richeson
published: '2011-06-05'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I recently read [this puzzle at the Futility Closet](http://www.futilitycloset.com/2011/05/14/current-affairs-2/) and it reminded me of a technique that I like to use to test conjectures (when possible). I don’t know if it has a name, so I’ll call it “looking for extreme examples and counterexamples.” I like this technique because when it works it is fast and easy, and it can often be used without writing anything down. I’ll give three examples to illustrate this technique.

**Example 1.** Let me rephrase the puzzle in the form of a conjecture.

Two runners are in an airport standing at one end of a moving walkway (one of those 100 foot long treadmills). They run at equal speeds to the end of the walkway and back—but one runs on the moving walkway and the other runs on the (unmoving) floor next to the walkway. Conjecture: they both finish at the same time.


The idea, of course, is that the runner on the walkway will get helped by the treadmill going one direction and hindered (by the same amount) in the other direction. He’s traveling the same distance both ways, so the effect of the treadmill cancels itself out.

When you’re imagining the problem in your head you’re thinking that a person runs 15 mph and the treadmill is going 3 miles an hour, or something like that. You may reach for some paper to do some calculations…

But there are no details about velocity in the conjecture. So consider an extreme example—the walkway and the runner are moving at the same speed. Then, running with the walkway the runner goes very fast, but when he tries to come back, he runs on it like a gym-goer does on an exercise treadmill, and makes no progress. He not only loses, he *never reaches* the finish line. Thus the conjecture is false.

(Note that in the original puzzle the question is: who wins? If the answer HAS a correct answer, then you can use the extreme example given above to conclude that it is not the person running on the moving walkway.)

**Example 2**. There is a long history of mathematical cranks claiming to be able to [trisect an angle](http://en.wikipedia.org/wiki/Trisecting_the_angle). Recall the problem: you are given an angle with measure . Is it always possible, using only a straightedge and compass, to construct an angle with measure

? It is a famous result of

[Pierre Wantzel](http://en.wikipedia.org/wiki/Pierre_Wantzel) that while it is sometimes possible, it is not possible in general (in particular, it is impossible to trisect a angle).


Here is a favorite “trisection method” given by the mathematical cranks. Suppose you are given an angle . Draw a circle with center

and radius

. We may as well assume that

is on this circle. Draw the chord

. Trisect this chord; that is, find a point

on

such that

(it is well known that it

**is possible** to trisect a line segment using the Euclidean tools). Then .


Conjecture: this is a valid method of angle trisection.


For small angles, this technique looks convincing (see below).

But it must work for **all angles**. Don’t dust off your copy of *Elements *and start looking for relevant propositions, look for an extreme example! For example, suppose . Clearly, as we see below, this technique does not trisect such an angle. Thus the technique fails.


**Example 3.** My last example is the famous [Monty Hall problem](http://en.wikipedia.org/wiki/Monty_Hall_problem). I’m sure this problem is well known to many of the readers of this blog, but here’s the setup. Monty Hall (a game show host) presents 3 closed doors to a contestant. He promises that behind one door is a new car and behind the other two are goats (obviously, the contestant wants to win the car). The contestant picks a door. Monty says that he will open one of the two remaining doors to reveal a goat (which he does). Then he asks the contestant if she wants to switch doors.

Conjecture: there is no advantage to switching. (Your rationale: at first your chance of winning was 1/3. But now there are two doors, one hiding a car and one hiding a goat, so it is a 50/50 shot either way.)


Of course this conjecture is FALSE. Here’s an extreme example to illustrate this point. Suppose there are 1000 doors hiding 1 car and 999 goats. You pick one door. There’s a 99.9% chance that the car is behind one of the other doors. Now Monty (who knows what is behind each of the doors) opens up 998 of the remaining doors. There are two closed doors—your door and one other. Using the same rationale as above, your chance of winning is now 50%, right? No! I hope it is clear that** you want to switch**!

(By the way, I read this explanation in [The Drunkard’s Walk](http://www.amazon.com/Drunkards-Walk-Randomness-Rules-Vintage/dp/0307275175/) by Leonard Mlodinow.)

Would it be an extreme case if Monty did not open any door at all but let you open the remaining ones? What difference does it make who opens the doors?

http://www.cut-the-knot.org/Curriculum/Probability/MontyHall.shtml

I like that explanation. Thanks for the link!

I think this is a common trick in mathematician books, right? It does well in these contexts, but I think some people (politicians, for example) try to use it in contexts where the solutions are not so boolean. “If we let gays marry, then what next, people marrying goats?!”

Thanks, Dave. I’m surely not claiming that this was my invention, but I don’t know how often it is taught. Do you know where, and when in the curriculum it appears? I’d be curious to know.

I thought about your example (well, not exactly that example, but the idea of it) while writing the post. Does this type of fallacy have a name? It is like the slippery slope fallacy, but not quite. It is all about the domain. In math domain is a very clear concept, but in everyday life it goes unspoken. Picking something from an extreme part of “the domain,” like you did in your example, is not fair. I suppose lawmakers do have to be aware of this issue so that the law is correctly applied to the right people/institutions/etc. (Although these extreme examples are often the source of “loopholes” that financial wizards exploit to make money.)

Good method, poor example (example 1).

The problem specifies that the moving surface is an airport’s moving walkway, which we can safely assume does not move at extreme speeds. So in this case the ‘extreme value’ heuristic is misapplied.

However, I’m not sure if this has any effect on the problem’s solution.

Intuitively it seems true that given a slow-moving walkway that adds x mph to the runner A’s speed in one direction and subtracts that same speed in the other will nullify the speed difference with runner B, but you’ve injected enough doubt that I’m not so sure anymore…

Correction:

It’s not that I think the extreme-value heuristic isn’t applicable here, just that the way it’s applied is incorrect. A better application might be something like:

According to the problem, runners A and B are running and A is on an airport walkway.

Usain bolt’s top speed was approx 27mph and on a hot day when I’m tired and hung over, the slowest I move while still legitimately ‘running’ is around 5mph. We can guess that an airport walkway might move at something between close to but greater than 0 mph and 3 mph (since it doesn’t move at ‘running’ speeds).

Suppose runner A is slow and runs at 5mph and the walkway, fast, moves at 3 mph. Then A moves at 8 mph in one direction and 2mph in the other. Runner B moves at 5 mph in each direction. So the conjecture is true.

Suppose runner A is fast and runs at 27mph and the walkway, slow, moves at nearly 0 mph. In this case, too, the conjecture is true.

Wait! Correction to my correction —

I just went through the trouble of doing the arithmetic and I was wrong–the conjecture *isn’t* true.

(1mile / 5mph) + (1 mile / 5mph) != (1mile / 8mph) + (1 mile / 2mph)

But I don’t see how the extreme value heuristic is very useful in this case, since you have to substantively alter the problem in order to get an intuitive result from its application.

Oh but that’s because I misapplied it myself — the extreme speeds for the walkway should be close to 0 and close to 5mph (not 0 and 3mph). In the latter case, when runner A is slow and running at 5mph, A’s net speed is approx. zero on the return trip.

“I see!”, said the blind man :)

Thanks for the post!

When I saw your Example 1, I immediately thought of it as a pilot. Pilots know from experience that if you make a round trip and there is a headwind one way and a tailwind the other, overall you lose time, because you spend far more time cursing the headwind slowing you down than enjoying the free ride provided by a tailwind. Having just spent an extra 15 minutes in the air watching my low groundspeed because of a 30 knot headwind returning from the Reading Airshow [ http://goo.gl/4duMA ], the topic is fresh on my mind.

Geoffrey,

If you click through to the solution at Futility Closet you’ll see that he mentions that same scenario (wind/airplane). I hadn’t heard that before, but it makes sense. Cool.

Ps. Looks like a fun trip!

Interestingly, we were taught to use exactly this principle back in school when entrance examinations to colleges were the order of the day. Some of the difficult ones had very close options in the list of multiple choices, and often the fastest way to solve such problems was to eliminate the options using extreme cases rather than to actually solve the problem at hand.

There is another problem where the “looking for extreme examples and counterexamples.” method worked great.

The problem goes like this:

You and an adversarial opponent are given a circular table to play a game on. The game goes like this: You have an infinite supply of black coins (2 dimensional), and your opponent has an infinite supply of white coins. Players alternate by keeping a coin on the circular board. The first person to not have space to place on his turn loses. Given these rules, would you play first or second?

This problem has a solution based on symmetry, etc. But the extreme problem variant solves it much more elegantly, imho. The idea is to start with the assumption that the board is smaller than the coins, and the answer is immediately obvious.

“The idea is to start with the assumption that the board is smaller than the coins, and the answer is immediately obvious.”

Is it? If the board is smaller than the coins, the first player loses (he can’t put his coin on the table). But if the board is bigger than the coins, the first player wins.

Regarding the Monty Hall problem, I’ve always liked it because it enables me to point out why I had such a hard time doing homework problems in my Probability semi-course in college. My more mathematically minded friends said, “You just aren’t identifying the sample space properly.” But I later learned that my real problem was that I didn’t realize that probability depends on information (knowledge). Those who get the Monty Hall problem wrong forget that Monty knows where the car really is. You

want to switchbecause Monty is trying to keep you from winning.There are three kinds of probability. There are (1) axiomatic (a measure space with total measure 1) and (2) frequentist (a ratio of number of successes divided by number of trials). The Monty Hall problem uses neither. It uses (3) subjective probability, which is best modeled by a Bayesian analysis.

Who said that mathematicians aren’t people of faith? Do those three ways to do probability give the same answer? A modeler would say, “In the limit, the frequentist’s probability is the axiomatic probability for the roll of a fair dice.” But a more humble answer would be “as a matter of faith, I hold that the limit would be the theoretical probability.” And of course determining whether a die is fair is itself an exercise in probability, using statistics and confidence intervals, unless we’re willing to engage in circular reasoning, where “fair” means equally likely, which is to say equally probable.

When Marilyn Vos Savant popularized the Monty Hall problem, she had school children run simulations to show that her answer was right:

http://en.wikipedia.org/wiki/Marilyn_vos_Savant#The_Monty_Hall_problem

I felt good about the fact that I was one of the academicians who submitted a correct argument to her first column. By then I had learned that probability depends on information.

Forgive the slight thread drift. This rant is not about extreme examples. But it is about pedagogy. I think that both identifying extreme examples and kinds of probability should be taught explicitly in mathematics courses.