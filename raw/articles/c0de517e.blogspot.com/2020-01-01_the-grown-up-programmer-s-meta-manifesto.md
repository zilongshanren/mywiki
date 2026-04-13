---
title: The grown-up programmer's (meta)manifesto
url: http://c0de517e.blogspot.com/2020/01/the-grown-up-programmers-metamanifesto.html
published: '2020-01-01'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Another year is almost over and years should bring wisdom. Most people make lists for things they want to do in the new year, here, let's write a manifesto for programmers.

If you've been following me for a bit here or in an even-less-coherent form over twitter, these principles won't come as a surprise, but outside's cold, I'm taking a few days (mostly) away from work in my hometown, perfect time to organize some thoughts on this blog.

**Meta-Rule 1: The only dogma is that we shall have none.**

I love the mathematical exactness of Computer Science, we sit at the foundation of mathematics (formal systems), reasoning (logic) with fascinating implications on philosophy as well. But that theoretical foundation has nothing to do with the actual job of programming computers.

In practice, ours is a huge industry made of companies, teams, people, products and problems so heterogeneous that I doubt anyone can claim to understand it globally.

It's rare to find truly "wrong" ideas or algorithms and technologies that have been superseded by newer systems that better them in all accounts. Most of our work deals in tradeoffs. Computers are binary, programming is not.

Ideas that are appropriate for a stable team of senior programmers are often not appropriate for a team that sees a rapid turnover or that wants to grow a significant amount of juniors.

Methodologies that work for innovative, research-driven projects are probably not the same that should be employed for less creative industries that on the other hand need to reliably evolve large, stable code-bases.

And of course, different industries have completely different cultures, requirements, expectations, constraints.

You can use goto(s).


*Corollary: Understand your self-defenses.*
Cosmic horror. When overwhelmed with complexity our minds tend to raise shields. Most often these come in two varieties, depending on if you're in your fascination phase or in your grumpy one.

Hype: In the former case, we tend to mindlessly follow others, ideas spread through hype and are embraced even when they are not appropriate in a given context. Eventually, we get burned by these, most of us learn our lessons and technology goes from hype to well-understood tool.

Hate: This is the latter case, where on the other hand we harden around what we already know, the trusty tools and ideas we can rely upon, and see new ideas in an overly negative way.

Most times, this makes us actually effective, because most new ideas have high failure rates (research and innovation is defined by the high possibility of failure). Always predicting that something new will fail is a good bet. But this efficiency and resilience to variance comes with the risk of being blind to the next big thing.

When the next big thing becomes obvious to all, it's usually too late to embrace it (the innovator's dilemma).

Note how both behaviors have virtuous traits. Hype helps new ideas to spread, and it's probably even necessary as we biased towards not wanting to move from our comfort zone, thus if we relied on perfect rationality for good new ideas to take their place in our collective tool belt, we would probably fail. And hate, as I wrote already, does indeed work most of the time, and makes people more effective at the job they do.

We have to understand, at a meta-level, that collectively these waves of hype and hate are there for a reason. Human behavior exists for a reason, and it is mostly there to serve us.

But if we understand this, then we can also be grounded and present to ourselves and understand when these behaviors do not serve us well. We should try to learn everything and idolize nothing. Know our history without becoming bound to it. Be curious without fully embracing something just because everyone else seems to be doing the same...


*Corollary: Be skeptical of theories without context.*
Only math is absolute. Any other science deals with primitives that we haven't invented (a.k.a. reality), thus, we can only hope to create models (theories) that are useful (predictive) in specific contexts (under given assumptions). Absolute statements are almost always propaganda, over-simplifications. We tend to like them because they are, well, simpler, and simplicity is attractive in an overly complex world. But unfortunately, they also tend to be wrong.

If a theory doesn't identify the conditions under which it applies, and the conditions under which it does not, then chances are it's not a good one. This applies even more broadly, to innovations, papers, algorithms, ideas in general.

**Meta-Rule 2: Our minds are (usually) the scarcest resource, we should optimize for them.**

"Everyone knows that debugging is twice as hard as writing a program in the first place. So if you're as clever as you can be when you write it, how will you ever debug it? — Brian Kernighan, The Elements of Programming Style

Again, it's unfortunate that we tend to take all these mantras as absolutes, we like to quote them, smart, famous people can't be wrong, right?

"Premature optimization is the root of all evil" amIrite?

Stop taking shortcuts to enlightenment. We need to actually think. To me, the famous quotes above is not really a call to not write clever code - we definitely do need to be clever, even often and often early on.

But the perils both Knuth and Kernighan (among many others) were trying to communicate are the ones that come with our tendency as passionate engineers to think too much about the machine.

And yes, I say that as someone who has few skills, but one of these few is a decent knowledge of modern hardware and how to exploit it. See. I didn't say that we should not think about the machine, we should. But the peril is to become persuaded that squeezing cycles or in other ways making the machine happy is the pinnacle of programming. The key part of what I wrote is "caring too much".

People (and products) are harder than hardware. Probably have always been, but it's especially true today with a stable industry and the commoditization of programming, where most software has hundreds of people behind and it's unlikely for new clever algorithms and implementations to be the key of the success of a product.


*Corollary: Be as simple as possible.*
Or, do not overcomplicate. Do not overengineer. As simple as possible might very well mean not simple at all, but we should fight needless complexity as our worst enemy.

Complexity is also very tricky to define, and that's why someone's overengineering might be someone else beautifully minimal code. Say, for example, that I need to do some numerical optimization in a C++ program. I can probably write my own small optimizer in say a thousand lines of code, from scratch. Maybe Nelder-Mead or Differential Evolution.

Or I could link Eigen to give me basic vector math and reduce my code to a hundred lines. Or, I could link an external optimization library and pick a ready-made algorithm with a single function call. Heck, I could even do a call into a Mathematica kernel that can do some fancy auto-selection of a good algorithm to use.

What is "simpler"? If you are a C++ programmer, you'll probably say one of the first two options. What if I said I'm doing this in Python? In that case, I'm pretty sure we would choose the latter ones! Why? Is it just because the library/module support in Python is better? I doubt it.

Complexity is contextual. It's not about the lines of code we write or the lines of code we depend on. It's about a window of concepts we care about. Our brain is limited and looks smarter than it is mostly because it aggressively focuses on certain things while ignoring others. We're perpetually blind.

I think that this translates to coding as well. Like it or not, we can work only within a limited window. C/C++ programmers tend to be system-level programmers, and these are tools used when we need to focus our window on performance and memory. In this context, oftentimes writing relatively small amounts of code from scratch, with no dependencies, is easier than depending on lots of unknown "magical" code, because of attention is on a given level of execution and exactly what code we execute usually matters.

On the other hand, if I'm working in Python or Mathematica I actually like to think I am blessed by not having to look at the lower levels of code execution. That is not where the window is, typically. Scripting is great to sketch and explore ideas, the minutiae of execution don't matter in this "prototyping" mode, they would actually be distractions. We don't really want to write Python code thinking how the interpreter is going to execute it.

Usually, every tool is good in a given context (tradeoffs), the context dictates what matters and what we can and should ignore, and when we talk about complexity we should think specifically of how conceptually simple the components we care about are.

This also yields another corollary. If we chose the right tool, a good default is to be idiomatic. It's usually wrong to try to "bend" a tool that is made for a given thing to go way out of its comfort zone. It usually ends up in not very well hidden complexity (because we need to interface two different worlds) and also a loss of familiarity (others can't tell how things work, it's not obvious from the local context).

While we shouldn't fear to go outside the familiar, we shouldn't do it if it's not necessary.


*Corollary: Constraints are useful.*
If it's true that our brain is limited to a given window, explicitly controlling said window by imposing constraints must be a useful tool.

This shouldn't be shocking, programming is creativity, and creativity does thrive under constraints. The paradox of choice that Barry Schwartz describes applies very much to programming as well. Writer's block.

I don't want to write much about this because I intend to write much more, and dedicate a future post to constraints in programming. I think that other than taking control, designing explicitly the window at which we operate for a given program, they can be useful when imposed artificially as well.

Over-constraining can help us focus on what matters for a given task, especially for people (like me) who tend to be "completionists" in programming - not happy if we don't know we did the "best" possible implementation. Here, adding constraints is a useful hack as we can re-define "best" to narrow the scope of a task.

## 1 comment:

This is great! I second the emphasis on simplicity as a virtue. Code is as much a means of communicating ideas to other engineers, including a future you, as it is a set of executable instructions. The scarce commodity is increasingly a programmer's attention, not hardware resources.

Post a Comment