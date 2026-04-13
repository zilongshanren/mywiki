---
title: The Modulith
url: https://fgiesen.wordpress.com/2015/07/22/the-modulith/
published: '2015-07-22'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# The Modulith

Much has been written about all the myriad ways to go wrong when writing software. Poor management; scope creep; too little structure, not modular enough, and it’s a “big ball of mud”. Too much (or too rigid) and it’s a “software crystal”, impossible to alter. And so on.

Suppose you get all that right, and actually ship a useful system to users, it solves their problems well enough, and the code is reasonably clean, has a sound design and a modular structure with interface that, while not perfect, work okay. That’s about as good as it gets! Well done.

Alas, you’re not out of the woods. Success has its own failure modes, and I want to talk about one in particular that affects modular designs.

The arguments for modularity are well known: separating concerns breaks large systems down into smaller constituent parts that can be understood individually, with clearly-defined interfaces between them. Ideally, modules are designed so they can be developed and tested in isolation, and if an individual module is found wanting (say it’s unreliable, faulty or there are simply better solutions available), it can be replaced with another module provided it has the same interface.

And there really are systems like that, where the interfaces are rigid and well-specified, components come only in a handful of “shapes”, and everything cleanly fits together, like Lego bricks. But more commonly, shipping systems look like this (prepare for an extended metaphor):

The modules have irregular shapes and irregular sizes. Some are big, some are quite small. Some closely align with their neighbors; others have big gaps between them. They add up to a coherent whole, but it’s clear that for most of the development time, none of these components really had to have any particular shape. Occasionally you need a small piece with a specific shape to fill a gap, but for the most part, you just work with the materials you have.

The result is still “modular”; it’s built out of smaller pieces, each with their own clearly defined boundaries. But it’s not very regular, and outright weird in some places. That chipped corner on one of the bottom pieces was just an early mistake, but it made for a good place to stick that one flat rock on and somehow that ended up being one of the primary supports for the whole thing. And while building that wall, “I need a rock, about this big” was the only constraint you really had, and you just sort of piled it on. But when repairing it after one of the pieces has been damaged, working out the right shape, finding a replacement that meets that description and getting it in place is really tricky, fiddly work. (End of extended metaphor.)

Know any systems like that? I certainly do. And the end result is what I hereby dub a “modulith” (I am sure this has been observed and named before, but I haven’t seen it elsewhere yet). Made out of small, distinct, cleanly separable pieces, but still, everything but the topmost layer is actually kind of hard to disentangle from the rest, due to a myriad of small interactions with everything surrounding it. Because once you use a module as a building block for something else, there’s a disturbing tendency for all of its remaining quirks and bugs to effectively become part of the spec, as other modules (implicitly or explicitly) start to rely on them.

This is related to, but distinct from, other concepts such as software entropy and technical debt, which primarily deal with effects within a single codebase over time. Here we are dealing with something slightly different: as a particular component is successfully used or re-used (in unmodified form!), the users of said code tend to end up relying (often inadvertently) on various unspecified or underspecified behaviors, implicitly assuming a stronger contract than the component is actually supposed to provide. At that point, your choices are to either make those assumed behaviors actually contractual (not breaking existing code at the cost of severely constraining future evolution of said component), or to fix all users that make stronger assumptions than what is guaranteed (easier said than done if the component in question is popular; often causes ripple effects that break yet more code).

Either way, I don’t have any good solutions, but I’m feeling whimsical and haven’t seen this exact problem described before, so I’m naming it. In the extremely likely case that this has already been described and named by someone else, I’d appreciate a reference!

Just the other month, I saw Martin Sústrik discuss this effect, albeit as part of a larger, different argument: http://250bpm.com/blog:49