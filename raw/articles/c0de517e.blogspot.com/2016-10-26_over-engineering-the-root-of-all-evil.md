---
title: Over-engineering (the root of all evil)
url: https://c0de517e.blogspot.com/2016/10/over-engineering-root-of-all-evil.html
published: '2016-10-26'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**Definitions**

Over-engineering: using prematurely for tools, abstractions or technical solutions, resulting in wasted effort and unnecessary complexity.

When is a technique used prematurely? When it doesn't solve a concrete, current problem. It is tempting to define good engineering in terms of simplicity or ease of development, but I think it's actually a slippery slope. Simplicity means different things to different people.

One could see programming as compression (and indeed it is), but we have to realize that compression, or terseness, per se, is not a goal. The shortest program possible is most often not the simplest for people to work with, and the dangers of compression are evident to anybody that had to go through a scientific education: when I was in university the exams that were by far the most difficult came with the smallest textbooks...

Simplicity also means different things to different people. To someone in charge of low-level optimizations working with fewer abstractions can be easier than having to dive through many software layers. To a novice, a software written in a more idiomatic way for a given language might be much easier than something adapted to be domain specific.

Problems, on the other hand, measurable,

**concrete issues**, are a better framework.

They are still a soft, context-dependent and team-dependent metric, but trying to identify problems, solutions, and their costs brings design decision from an aesthetic (and often egocentric) realm to a concrete one.

*Note: This doesn't mean that good code is not or shouldn't be "beautiful" or elegant, but these are not goals, they are just byproducts of solving certain problems the code might have.*

*Also, "measurable" does not mean we need precise numbers attached to our evaluations, in practice, most things can't be better than fuzzy guesses, and that's perfectly fine.*

**Costs and benefits**

**Costs**are seldom discussed. If a technique, an abstraction, an engineering solution doesn't come with drawbacks, it's probably because either it's not doing much, or because we've not been looking hard enough.

- Are we imposing a run-time cost? What about the debug build? Are we making it less usable?
- Are we increasing build-times, lowering iteration times?
- A human one, in terms of complexity, obfuscation, ability to on-board new engineers?
- Are we making the debugging experience worse? Profiling?
- Do our tools support the design well? Are we messing up with our source control, static analyzer and so on?
- Are we decreasing code malleability? Introducing more coupling, dependencies?
- Reducing the ability to reason locally about code? Making details that matter in our context hidden at call-site? Making semantics less explicit, or less coupled to a given syntax? Violating invariants and assumptions that our code-base generally employs?
- Does it work well with the team culture? With code reviews or automated testing or any other engineering practice of the team?

I've seen countless time people going on stage, or writing articles and book, honestly trying to describe why given ideas are smart and can work while totally forgetting the pain they experience every day due to them.

**Under-engineering**

And that's why over-engineering truly is the root of all evil. Because it's vicious, it's insidious, and we're not trained at all to recognize it.

It is possible to go out and buy technical books, maybe go to a university, and learn tens or hundreds of engineering techniques and best practices. On the other hand, there is almost nothing, other than experience and practice, that teaches restraint and actual problem solving.

We know what under-engineering is, we can recognize duplicated code, brittle, and unsafe code, badly structured code. We have terminology, we have methodologies. Testing, refactoring, coverage analysis...

In most of the cases, on the other hand,

**we are not trained to understand over-engineering**at all.

*Note: In fact over-engineering it's often more "pronounced" in good junior candidates, whose curiosity lead them to learn lots of programming techniques, but that have no experience in their pitfalls and can easily stray from concrete problem solving.*

This means most of the times when over-engineering happens it tends to persist, we don't go back from big architectures and big abstractions to simpler systems, we tend to build on top of them. Somewhere along the road, we made a bad investment, with the wrong tradeoffs, but now we're committed to it.

Over-engineering tends to look much more reasonable, more innocent than under-engineering. It's not bad code. It's not ugly code. It's just premature and useless, we don't need it, we're paying a high price for it, but we like it. And we like technology, we like reading about it, keeping ourselves up-to-date, adopting the latest techniques and developments. And at a given point we might even start thinking that we did make the right investment, that the benefits are worth it, especially as we seldom have objective measures or our work and we can always find a rationalization of almost any choice.

I'd say that under-engineering leads to evident technical debt, while over-engineering creates hidden technical debt, which is much more dangerous.

**The key question is "why?"**. If the answer comes back to a concrete problem with a positive ROI, then you're probably doing it right. If it's some vague other quality like "sharing", "elegance", "simplicity", then it's probably wrong, as these are not end goals.

When in doubt, I find it's

**better to err on the side of under-engineering**, as it tends to be more productive than the opposite, even if it is more reviled.

*"Premature optimization is the root of all evil" - Hoare, popularized by Knuth.*

I think over-engineering is a super-set of premature optimization. In the seventies, when this quote originated, that was the most common form of this more "fundamental" evil.

Ironically, this lesson has been in the decades so effective that nowadays it actually helps over-engineering, as most engineers read it incorrectly, thinking that in general performance is not a concern early on in a project.

**Intermission: some examples**

- Let's say we're working on a Windows game made in Visual Studio. Let's say that you are using a Visual Studio solution and it's done badly, it uses absolute paths and requires the source-code and maybe some libraries to be in a specific directory tree on the hard drive. Anybody can tell that's a bad design, and the author might be scorned for such an "unprofessional" choice, but in practice, the problems that it could cause are minimal and can be trivially fixed by any programmer.

On the other hand, let's say we started using, for no good reason, a more complex build system, maybe packages and dependencies based on a fancy new external build tool of the week.

The potential cost of such a choice is huge because chances are that now many of your programmers aren't very familiar with this system, it's bringing no measurable benefits but now you've obfuscated an important part of your pipeline. Yet, it's very unlikely that such decision will be derided.

- Sometimes issues are even subtler, because they involve non-obvious trade-offs. A fairly hard-coded system might be painful in terms of malleability, maybe doing changes in this subsystem requires every time editing lots of source files even for trivial operations.

We really don't like that, so we replace this system with a more generic, data-driven one which allows to do everything live, doesn't even require to recompile code anymore. But say that such system was fairly "cold", and the changes were actually infrequent. Suppose also that the new system takes a fair amount more code and now our entire build is slower. We ended up optimizing a workflow that was infrequent but on the down side we slowed down the daily routine of all our programmers on the team...

- Let's say you use a class where you could have used a simple function. Maybe you integrate a library, where you could have written a hundred lines of code. You use a templated container library where you could have used a standard array or ad-hoc solutions. You were careless and now your system is becoming more and more coupled at build-time due to type dependencies.

It's maybe a bit slower in runtime than it could be or it makes more dynamic allocations than it should, or it's slow in debug builds, and it makes your build time longer while being quite obscure when you actually have to step in this library code.

This is a very concrete example, happens often yet chances are that none of this will be recognized as a design problem, and we often see complex tools built on top over-engineered designs to "help" solving their issues. So now you might use "unity builds" and distributed builds to try to remedy the build time issues. You might start using complex memory allocators and memory debuggers to track down what's causing fragmentation and so on and so forth.

Over-engineering invites more over-engineering. There is this idea that a complex system can be made simpler by building more on top of it, which is not very realistic.

**Specialization and constraints**

I don't have a universal methodology for evaluating return on investment, once the costs and benefits of a given choice are understood. And I think there isn't in general one because this metric is very

**context sensitive**. What I like to invite engineers to do is to think about the problem, be acutely aware of it.

One of the principles I think is useful as a guidance is that we operate with a finite working set: we can't pay attention to many things at the same time, we have to find constraints that help us achieve our objectives. In other words, our objectives guide how we should specialize our project.

For example, in my job I often deal with numerical algorithms, visualization, and data exploration. I might code very similar things in very different environments and very different styles depending on the need. If I'm exploring an idea, I might use Mathematica or Processing.

In these environments, I really know little about the details of memory allocations and the subtleties of code optimization. And I don't -want- to know. Even just being aware of them would be a distraction, as I would naturally gravitate towards coding efficient algorithms instead of just solving the problem at hand.

Often times my Mathematica code actually leaks memory. I couldn't care less when running an exploratory task overnight a workstation with 92 gb of ram. The environment completely shields me from these concerns and this is perfect, it allows me to focus on what matters, in that context. I write some very high-level code, and somehow magic happens.

Sometimes I have to then port these experiments to production C++ code. In that environment, my goals are completely different. Performance is so important to us that I don't want any magic, I want anything that is even remotely expensive to be evident in the location where it happens. If there was some magic that worked decently fast most of the times, you can be sure that the problems it creates would be lost until there are so many locations where that happens that the entire product falls apart.

I don't believe that you can create systems that are extremely wide, where you have both extremely high-level concerns and extremely low-level ones, jack-of-all-trades. Constraints and specialization are key to software engineering (and not only), they allow us to focus on what matters, keeping the important concerns in our working set and to perform local reasoning on code.

**All levels**

Another aspect of over-engineering is that it doesn't just affect minute code design decisions or even just coding. In general, we have a tendency to do things without proper awareness, I think, of what problems solve for us and what problem they create. Instead, we're often guided either by a certain aesthetic or certain ideals of what's good.

**Code sharing**for example and de-duplication. Standards and libraries. There are certain things that sometimes we consider intrinsically good, even when we have a history of failures from which we should learn.

For engineering, sharing in particular is something that comes with an incredible cost but that is almost always considered a virtue per se, even by teams which have experience actually paying the price in terms of integration costs, of productivity costs, of code-bloat and so on, it came to be just considered "natural".

"Don't reinvent the wheel" is very true and sound. But "the wheel" to me means "cold", infrastructural code that is not subject to iteration, that doesn't need specialization for a given project.

Thinking that sharing and standardization is always a win is like thinking that throwing more people at a problem is always a win, or that making some code multithreaded is always a win, regardless of how much synchronization it requires and how much harder it makes the development process...

In a videogame company, for example, it's certainly silly to have ten different math libraries for ten different projects. But it might very well not be silly to have ten different renderers. Or even twenty for what matters, rendering is part of the creative process, it's part of what we want to specialize, to craft to a given art-direction, given project scope and so on.

**People**

Context doesn't matter only on a technical level, but also, or perhaps even more, on a

**human level**. Software engineering is a soft science!

I've been persuaded of this having worked for a few different projects in a few different companies. Sometimes you see a company using the same strategy for similar projects, only to achieve very different results. Some other times on the other hands, similar results are obtained by different products in different companies by employing radically different, almost opposite strategies. Why is that?

Because people matter more than technology. And this is perhaps the thing that we, as software engineers, are trained the least to recognize. People matter more than technology.

A team of veterans does not work the same as a team that has or needs a lot of turnover. In the game industry, in some teams innovation is spearheaded by engineers, in some others, it's pushed by artists or technical artists.

A given company might want to focus all their investment in a few, very high profile products, where innovation and quality matters a lot. Another might operate by producing more products and trying to see what works, and in that realm maybe keeping costs down matters more.

Even the mantras of sharing and avoiding duplication are not absolute. In some cases, duplication actually allows for better results, e.g. having a separate environment for experimentation than final production. In some cases sharing stifles creativity, and has upkeep costs that overall are higher than the benefits.

It's impossible to talk about engineering without knowing costs, benefits, and context. There is almost never a universally good solution. Problems are specific and local.

**Engineering is about solving concrete problems in a specific context**, not jumping carelessly on the latest bandwagon.

Our industry I feel, still has lots to learns.

## 11 comments:

Great article! (feeling the pain right now)


one minor thing: " ... chances are that now many of your programmers are very familiar with this system" i guess you meant UNfamiliar?

Thanks for the correction & the compliments. Fixed.

It's so great!! Thanks a lot~

Wonderful article!




My favorite part,

"I don't believe that you can create systems that are extremely wide, where you have both extremely high-level concerns and extremely low-level ones, jack-of-all-trades."

I recently had this realization and being able to stop constantly thinking that there is a "best" generic solution has been very freeing.

Good article, there should definitely be more discussion around how to become aware of over-engineering and how to avoid it.



As you mentioned OE is more pronounced in junior developers. I feel for more experienced developers, OE is often a symptom of what The Mythical Man-Month described as the Second System Effect.

"The second-system effect proposes that, when an architect designs a second system, it is the most dangerous system they will ever design, because they will tend to incorporate all of the additions they originally did not add to the first system due to inherent time constraints. Thus, when embarking on a second system, an engineer should be mindful that they are susceptible to over-engineering it." (https://en.wikipedia.org/wiki/The_Mythical_Man-Month#The_second-system_effect)

Hum, the article left me flabbergasted with is definition of over-engineering that totally is a symptom of the problem in so called Computer Science.









Over engineering used to describe how in front of not yet totally discovered physical law (hence hard science) how aeronautical industry was applying factor of safety.

For instance if a resistance for a pressure of x N/M² was expected for an element, it would be applied a «safety factor» of 1.5, namely designed to stand a 1.5 * x pressure higher than the expectation. Just in case we made a mistake of 40% in the modeling.

The S in computer Science is totally close to the S in BS: the over-engineering in CS would be to make server able to handle 1.5 times the connections/sec more than expected.

The definition here of over engineering are about decision made without prior knowledge, nor even close to the real situation data or feedback from actual situations. It is not even close to over-engineering, it is alter-engineering or religion at best.

The truth is in CS there no modeling, no thinking, no math involved. Just «artistic» intuition applied for building stuffs in some academic ways even when we have hard evidence it does not work.

The article is all about in its premise, development and conclusion about the lack of rigor and science in CS.

Which, weirdly enough by a very lucky «two wrongs may make a right» does make a point. But in a very twisted way.

Very good article indeed. I do want to add something related to the "Premature Optimisation is the root of all Evil":

http://ubiquity.acm.org/article.cfm?id=1513451

This marvellous article touches the topic of the misusage of that statement and how something taken out of context (historical context) can do more harm then good.

Julien - computer science is different than engineering in the physical world because CS is deterministic, so you can't build redundancies like you can in mechanical engineering - I agree with you that "over-engineering" is maybe not the best term as that had some positive connotations in some realms, but I think it's very clear to programmers.



Regarding your critique of computer science, I think you mean "software engineering", really, the two things are different. CS is math, no more and no less, in my opinion, one of the purest forms of maths as it deals with the logic and formalisms that define maths itself (at least if you're not a Platonist) among other, more "mundane" things (like algorithmic complexity and so on). CS has no problems at all, it's perfectly sound and perfectly rigorous.

Software Engineering is indeed more soft and squishy, but it's not BS, or at least, it -shouldn't- be. It should be a science like all other soft sciences, based on people and their behaviors. Unfortunately often it isn't and it's taught dogmatically without any solid experimental backing, I agree. But there are lots of people that are doing good work to improve that, to be fair.

> I don't have a universal methodology for evaluating return on investment ... [once cost/benefit known]






It's task/domain-specific, as you pointed out.

Maybe decide big-picture prioritization weights up front, and get everyone on the same page with them. Reassess them or figure out exceptions to them if and when needed.

Then, instead of individuals having to make hard calls while coding and solo, could decide in a prioritization/triage meeting.

I assume the duration between "time to first identifying a task" and "time to having to ship code" is long enough that the cost/benefits can actually be assessed and escalated, as you implied by "the costs and benefits of a given choice are understood".

... says the Project Manager in me

The last point about humans being more important than technology is extremely important. The economics of human psychology are far more difficult to evaluate than even the already opaque costs of engineering practices.





If there's such a strong drive for over-engineering and clean code, to the point where we recognize it as a problem, we should ask ourselves if the real benefits are simply different from the touted benefits.

Suppose you have a codebase that is considered "ugly" yet it simply does the job, problems are fixed with relative ease and spending effort on cleaning it up would be economically irrational.

Nevertheless, this is the codebase that every developer dreads to touch, that gives them a feeling of unease, that scratches their pride, their ego. This is the codebase that makes developers feel worse about their job and about their company and it'll be one of the points of consideration when they decide to switch jobs.

Since these are all fundamentally *irrational* reasons, they cannot be countered by rational arguments as presented in this blog post. Letting your developers do some cleanups, refactorings and re-designs (*their* choice, *their* pain points) can be very beneficial to morale, while by any "hard" metrics they are a complete waste of time.

I experience exactly what Anonymous just said.

I feel the uneasiness of dealing with bad written code, even when it does the job. I think my ego just needs some gratification in cleaning it up, and doing it actually is very beneficial.

Nonetheless I'll think more next time trying to figure out if I'm being overkill or not in my design.

Post a Comment