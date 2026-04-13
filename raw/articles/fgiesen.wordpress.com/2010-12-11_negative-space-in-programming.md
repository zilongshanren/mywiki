---
title: Negative space in programming
url: https://fgiesen.wordpress.com/2010/12/11/negative-space-in-programming/
published: '2010-12-11'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Negative space in programming

There’s a lot of material out there about code; how to design it, write it, document it, build it and test it. It is, after all, the primary artifact we programmers produce (okay, that and long rants about why we’re right and almost everyone else is wrong). Considerably less attention is paid to what’s not there – the design alternatives that were rejected, the features that were omitted, the interfaces that got changed because they were too complicated/subtle to explain properly in the docs, the lack of excessive dependencies that helps keep build times down, the tests that aren’t necessary because certain types of errors are made impossible by the design of a system.

I think that’s a mistake. In my experience, the main way we actually give our programs shape is not by putting things in, but by leaving them out. An elegant program is not one that checks off all the bullet points from some arbitrary feature list; it’s one that solves the problem it’s meant to solve and does so concisely. Its quality is not that it does what it’s supposed to; it’s that it does almost nothing else. And make no mistake, picking the right problem to solve in the first place is hard, and more of an art than a science. If you’ve ever worked on a big program, you’ve probably experienced this first-hand: You want to “just quickly add that one feature”, only to discover hours (or days, or even weeks) later that it turns out to be the straw that breaks the camel’s back. At that point, there’s usually little to do except take one last glance at the wreckage, sigh, and revert your changes.

So here’s my first point: Next time you get into that situation, write down what you tried and why it didn’t work. No need to turn it into an essay; a few short paragraphs are usually plenty. If it’s something directly related to design choices in the code, put it into comments in that piece of code; if the issues stem from the architecture of your system, put it into your Docs/Wiki or at least write a mail. But make sure it’s documented somewhere; when working on any piece of code, knowing what doesn’t work is at least as important as knowing what does. The latter is usually well-documented (or at least known), but the former often isn’t – no one even knows the brick wall is there until the first person runs into it and gets a bloody nose.

Second point: If you’re thinking about rewriting a piece of code, be very aware that the problem is not one of deleting X lines of code and writing Y lines to replace it. Nor is it one of understanding the original data structures and implementation strategies and improving of them; even if the approach is fine and you’re just re-implementing the same idea with better code, it’s never that simple. What I’ve consistently found to be the biggest problem in replacing code is all the unspoken assumptions surrounding it: the API calls it doesn’t use because they don’t quite do the right thing, the unspecified behavior or side-effects that other pieces of code rely on, the problems it doesn’t need to deal with because they’re avoided by design.

When reading code, looking at what a program does (and how it does it) is instructive. But figuring out what it doesn’t do (and why) can be positively enlightening!

That’s a really great insight.

It also relates to the problems of publication bias in science. You can’t get a paper published on a failed line of research. The best you can do is write a paper on a successful line of research in which you make a brief and cryptic side comment that alternative X doesn’t work. But even that wouldn’t make it past the reviewers and editors of most journals.

Another problem in academic mathematical writing is that what is published usually represents a fine gem from which all smudges and rough edges that might suggest the genesis of the underlying ideas and their development have been polished away. The same thing can happen with code as it becomes more elegant or optimized over time and so loses all trace of its coarse and earthy origins. Comprehension of such code would be greatly aided if you could see several representative snapshots of the code side by side from over the course of its evolution.

“The same thing can happen with code as it becomes more elegant or optimized over time and so loses all trace of its coarse and earthy origins.”In fact, that’s the issue that got me started on this post in the first place. Over the past few months, I’ve worked a lot on low-level rendering code for Iggy (upcoming 2D UI product by RAD), improving its performance significantly on several platforms. Now I need to do a small write-up on the various optimizations I did, and it’s turning out to be quite difficult to write. Yes, there’s some handy tricks I discovered along the way (some of which I’ve described on this blog), but the truth is that none of that makes a really big impact.

Ultimately, all low-level rendering code just takes some high-level (or medium-level) stream of rendering operations to do and converts it into a command buffer for the GPU. If you’ve done your job well, the resulting code is little more than a memcpy with a minimum amount of conversion: Write this pointer into that GPU register, change 4 vertex constants, draw 500 indexed triangles, done. Another pointer change, change blend settings, draw 800 triangles, next. There’s no complicated logic to explain, no algorithmic insights to boast of; if you’ve done your job right, nothing fancy ever happens. Just get it over with and don’t spend more cycles than necessary. That’s the whole point.

That’s true for a lot of optimization work. Often, it’s not about what you do. It’s about how much you can get away with not doing without sacrificing correctness.

“Another problem in academic mathematical writing is that what is published usually represents a fine gem from which all smudges and rough edges that might suggest the genesis of the underlying ideas and their development have been polished away.”I hate it when textbooks do this, by the way. My pet peeve is the standard proof of the Cauchy-Schwarz inequality using the magic quadratic form. Congratulations, you’ve turned a beautiful,

insightfulproof into a complete black box. What a poor way to save 3 lines! The other extreme (particularly bad in Analysis) is when the presentation of a proof is so bogged down by technicalities that it’s almost impossible to discern what the actual argument is. Avoiding the technicalities altogether is the wrong answer; knowing how the proofs go is an important part of the trade. But please, give me the “unpatched” proof first so I can see the idea, and then describe the necessary modifications afterwards. I find the usual presentation of 4-5 obscure Lemma followed by the actual Theorem unnecessarily hard to follow, and I doubt I’m the only one.“My pet peeve is the standard proof of the Cauchy-Schwarz inequality using the magic quadratic form.”

Yeah. If you tell someone the geometric meaning first (i.e. the length of vector X’s component parallel to vector Y is less or equal to X’s total length) then not only is it intuitively obvious but it should also be clear how to fashion a simple proof from the axioms of inner products.

I admit I’m pretty bad at analysis and don’t like it. Fortunately a lot of the content of soft analysis can be comprehended from non-analytic perspectives where you can put most of the inequalities and estimates in black boxes and not worry about them too much.

For example, when I want to prove the existence and uniqueness theorem for ODEs or the inverse and implicit function theorems, I think in terms of Newton’s method. Its global convergence is intractable but its local behavior is pretty straightforward. The workhorse for showing convergence is then Banach’s contraction mapping theorem. You only really need to get your hands dirty for getting a Lipschitz constant for the derivative. But even there you can mostly think qualitatively as long as you don’t want the absolute tightest version of the theorem.

That is exactly the reason why I started blogging in the first place!

I noticed that I was too lazy to keep track of the things I tried out. So I found out that a simple diary (blogging) was a good way to record both the success and failure. A lot of subtle details still gets lost, but at least I’m able to capture the overal progress.

The very same idea applies to game design too. Game design docs are always written like bibles, trying to describe the holy truth. Where as it would be more interesting to see the whole progress, the raw ideas, the prototypes, etc.

Great blog.

I’m currently writing a piece which is considering how you can bring concepts such as visual hierarchies to the design of units in code. Designing negative space is a powerful tool, I was struggling to visualize how this translated into code.

Your blog demonstrates it really neatly – thanks.