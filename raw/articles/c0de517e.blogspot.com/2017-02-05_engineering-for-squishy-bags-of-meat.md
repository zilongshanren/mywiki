---
title: Engineering for squishy bags of meat
url: https://c0de517e.blogspot.com/2017/02/engineering-for-squishy-bags-of-meat.html
published: '2017-02-05'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**The section you can skip**

I'm Italian, and I grew up in a family of what you could call middle-class intellectuals. My parents came from proletarian families, and were the first generation being university educated, not working in the fields.

A teacher and a doctor, embedded in the life of the city and involved in local politics; we used to often host people over for dinner. And I remember, at the time, being fairly annoyed at how people could be highly regarded for their knowledge and intelligence even if they were limited to the sole study of the humanities, without knowing even the basics of math, or scientific thinking.

Fast forward and today, as a computer science professional, society in my small bubble seems to have undergone a (non-violent) cultural revolution. Today "nerds" are considered "smart", the lack of social skills almost a badge of honor, and things seem to matter only when they relate to quantifiable numbers.

Not always, I have to say the professional world of smart computer scientists is not a stereotyped as your average Hollywood portrayal, yet too often we live in a world that is yet again too vertical: programmers, artists, managers, often snarking at the other categories lack of "skills".

**"We wanted to build an elegant, robust, and beautiful product"**

I've been wanting to write this post for a while now, I have various sketches in my notebook from almost a year ago, but recently I found this very well written

[post-mortem analysis of RethinkDB failure](http://www.defstartup.org/2017/01/18/why-rethinkdb-failed.html)as a startup. I'm no database expert, but what I found particularly interesting is the section talking about the design principles behind their product.
You want to make a new database product; what is that you're going to focus on? For RethinkDB, the answer was three key factors:

[correctness, simplicity of interface and consistency](http://dreamsongs.com/RiseOfWorseIsBetter.html).
Seems pretty reasonable, databases are the central infrastructure for most of today's applications, and who would like to build a billion-dollar product on something that doesn't

[guarantee correct operation](http://jepsen.io/analyses)? And definitely, today's startups need to move fast and are willing to adopt whatever new technology that helps to get results fast, so simplicity and consistency could give a competitive advantage.
Of course, it's no surprise as they were talking candidly about the reasons why the failed, that these were "the wrong metrics of goodness" (their words). What did people want? According to the article, the right metrics would have been: timely arrival, "palpable" speed (benchmarks, marketing), and a good use case. In other words, a product that:

1) Solved a problem (use case)

2) Now (timely arrival)

3) While making people happy (the importance of perceived performance)

This misjudgment led not only to the demise of the startup but also to a lot of frustration, depression, and anger, as what could be seen as inferior products made big impacts in the market.

**Clash of worlds**

The sin is, of course, the idea that an abstract notion of beauty matter at all. We write software to achieve given results, and these results are for all but the most theoretical of works, something that somehow has to make people happy.

Everything else is just a mean towards that, a tool that can be used well or not but not a goal. The goal is always to sell to your market, to do something that people will... like.

It requires understanding your customers and understanding that we are all people. It's the clash between "features" and "experiences".

When we think about features it's easy to end up in the measurement fallacy. We are doing X, and we are doing X measurably better for certain axes of measurement than another product, thus, we are better. Wait for adoption and success.

This is the peril of living in a verticle bubble of knowledge. People in tech think about tech, we work with it, we create it, it's easy and to a degree even inevitable to start technology for technology's sake.

But the truth is that user experience, workflows, and subjective experiences are about technology, and they are about research and computer science.

They are just -harder- problems to solve, problems that most often have no good metric to optimize at all, sometimes because we don't know how to measure "soft" qualities, but many times because these qualities are truly hard to isolate.

Better evolves through "blind" iteration and luck, and it's subject to taste, to culture, to society. Look at all the artifacts around you. Why is a musical instrument better than another one? Or a movie, game, car, pen, table, phone...

Good design is humanistic in nature, we have to understand people, what they like, what they fear, how they use technology, how much they can adapt to change, what risks they evaluate. Objectively good is not good enough. Good design makes objective sense but overcomes also emotional, social, environmental obstacles.

**Specialization**

To be fair though it's not surprising that people who are deeply invested in a given field, don't fare well in others. The tension between vertical knowledge, specialization, and horizontal knowledge that allows us to be well-rounded, is ineluctable.

We are more and more pushed towards specialization because our fields are so deep and complex, and even the most brilliant minds don't have infinite mental resources, so there are always tradeoffs to be made.

Whether you went to a university or not, chances are that to become a specialist you needed a deep, technical immersion in a given field. We isolate ourselves into a bubble, and to a degree, we need to.

The real problem begins when we start thinking that a given bubble is representative of the world, that because given qualities matter inside it, they actually do matter.

When that starts, then we start adopting the wrong metrics to judge the world, and we end up frustrated when the world doesn't respond to them.

Bubbles are of course a very general problem, even a very scary one when you think that really our world is becoming more and more complex to the degree that's not easily explicable even by experts, it's not easy to encapsulate in a set of rules. Complexity can push us inwards, to simplistic explanations and measure of goodness that we can become very attached to, even if they are very narrow-sighted.

It doesn't help that we, as humans, seek confirmation more than truth.

**Academic research**

Take for example the world of academia and scientific research. Researchers are judged on novelty, what a paper really needs is a measure, then, given such measure one can assert that a given technique is objectively better in a given context.

If something is better, but not in a way that is easily measured, it's not something that can be easily published. This is not per se a terrible problem, it becomes a problem when we start thinking that these measures are all that really matters.

I work in computer graphics; if I make a new system that generates simplified 3d models, and all the artists that use it think it's revolutionary, it produces a much better output and it's easier to use than anything else, did I make something novel and noteworthy? Surely yes, that's, in fact, all that matters.

But if this notion of how much better it is can't be measured in some kind of metric, it's not something that can be considered a novel research in academic terms. This is the nature of applied research, but it also creates a disconnect between academia and the rest of the world: a bubble, that we have to be aware of.

When we ignore the existence of the bubble, frustration arises. Industry professionals are frustrated when academic research doesn't end up "working" for their needs. And researchers are frustrated when they see the industry "lagging behind" the theoretical state of the art.

**Conclusions**

Is it all bleak? To a degree, yes, it is when you realize that the world is not easily reducible to comforting measures that we like. That biases are inevitable, that specialization is inevitable and bubbles are inevitable.

I say that "experience is a variance reduction technique", we become more predictable and entrenched, better, at doing something, but we pay a price to it.

What we can certainly do though is to at least -aware- of these mechanisms. Doubt ourselves. Know that what we think it matters, might not matter at all, and seek different point of views. Know that what we think is rational, most of the times is just a rationalization. Be aware of the emotional factors in our own choices.

What we can certainly do is to break -a bit- out of our vertical pits of knowledge, and be just curious enough, learn just enough to be able to interface with different people. That can be just the solution we need, we can't know all, and we can't really understand the world without any filter. We can though make sure we are able to talk and engage with people that are different, that invested their verticality in other fields.

In the end, personally, I don't consider my journey towards being truly "smart" complete or even really started. But at least I am a bit aware... I also have the gift of a spouse that beats me down showing me how bad I still am at many aspects of "smartness", and a strong enough ego to take that beating. Small steps.

## 1 comment:

While I am personally not on a journey to being truly smart (at least it is not my intrinsic motivation) I did enjoy your article, especially the part about specialization and the honest last paragraph! Reminded me of some rants about “boundaries of ignorance” and “circles of knowledge” I had recently.

Post a Comment