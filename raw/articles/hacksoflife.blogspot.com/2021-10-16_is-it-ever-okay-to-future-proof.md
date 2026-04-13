---
title: Is It Ever Okay to Future Proof?
url: http://hacksoflife.blogspot.com/2018/10/is-it-ever-okay-to-future-proof.html
author: Benjamin Supnik
published: '2021-10-16'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A while ago I tried to make a case for solving domain-specific problems,





[rather than general ones](http://hacksoflife.blogspot.com/2018/08/solve-less-general-problems.html). My basic view is that engineering is a limited resource, so providing an overly general solution takes away from making the useful specific one more awesome (or quicker/cheaper to develop).
Some people have brought up

[YAGNI](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it), with opinions varying from "yeah, YAGNI is spot on, stop building things that will never get used" to "YAGNI is being abused as an excuse to just duct tape old code without ever paying off technical debt."
YAGNI is sometimes orthogonal to generalization. "Solving specific problems" can mean solving two smaller problems separately rather than trying to come up with one fused super-solution. In this case, there's no speculative engineering or future proofing, it's just a question of whether the sum can be less than the parts. (I think the answer is: Sometimes! It's worth examining as part of the design process.)


But sometimes YAGNI is a factor, e.g. the impulse to solve a general problem comes from an assumption that this general design will cover future needs too. Is that ever a good thing to assume?

But sometimes YAGNI is a factor, e.g. the impulse to solve a general problem comes from an assumption that this general design will cover future needs too. Is that ever a good thing to assume?

### Nostradamus the Project Manager

So: is it ever okay to future proof? Is it ever okay to have design requirements for a current engineering problem to help out with the next engineering problem? Here are three tests to apply - if




I find the three tests useful to cut off branches of exploration that aren't going to be useful. If my coworker is worrying that the design is too specific and can't stop playing "what if", these tests are good, because they help clarify how much we know about the future. If the answer is "not a ton", then waiting is the right choice.


And I think it's worth emphasizing


The act of writing feature A doesn't just ship feature A - it's the R&D process by which you learn enough to write feature B. So fusing A & B's design may not be possible because you have to code A to learn about B. These questions hilight when features have this kind of "learning" data dependency.




Given how strong the business case is for scenery effects, and given that we basically already know how this code would be implemented on its own (almost exactly the same as the aircraft code, but over here), it's very cheap to craft the aircraft code with this in mind.


But it requires a lot of really solid information about the future to make this win.

**any**of them fail, don't future proof.- Do you for a fact that the future feature is actually needed by the business? If not, put your head down and code what needs to be done today.
- Do you know exactly how you would solve the future feature efficiently with today's code? If not, back away slowly.
- Would the total engineering cost of both features be, in sum, smaller if you do some future proofing now? If not, there's no win here.

*still*be a dumb idea. If you are going to grow the scope of the feature at all by future proofing, you had best check with your team about whether this makes sense. Maybe time is critical or there's a hard ship date. Keep it tight and don't slip schedule.I find the three tests useful to cut off branches of exploration that aren't going to be useful. If my coworker is worrying that the design is too specific and can't stop playing "what if", these tests are good, because they help clarify how much we know about the future. If the answer is "not a ton", then waiting is the right choice.

And I think it's worth emphasizing

**why**this works. When solving new coding problems, one of the ways we learn about the problem space and its requirements is*by writing code*. (We can do other things like create prototypes and simulations, test data, etc. but writing code absolutely is a valid way to understand a problem.)The act of writing feature A doesn't just ship feature A - it's the R&D process by which you learn enough to write feature B. So fusing A & B's design may not be possible because you have to code A to learn about B. These questions hilight when features have this kind of "learning" data dependency.

### Sometimes Ya Are Gonna Need It

With that in mind, we*do*sometimes future proof code in X-Plane. This almost always happens when we are designing an entire subsystem, we know its complete feature set for the market, but there is an advantage to shipping a subset of the features first. When I wrote X-Plane's particle system, we predicted (correctly) that people want to use the effects on scenery and aircraft, but we shipped aircraft first with a design that wouldn't need rewrites to work with scenery.Given how strong the business case is for scenery effects, and given that we basically already know how this code would be implemented on its own (almost exactly the same as the aircraft code, but over here), it's very cheap to craft the aircraft code with this in mind.

But it requires a lot of really solid information about the future to make this win.

## No comments:

## Post a Comment