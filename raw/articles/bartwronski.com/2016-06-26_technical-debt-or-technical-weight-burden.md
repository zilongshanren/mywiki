---
title: Technical debt… or technical weight/burden?
url: https://bartwronski.com/2016/06/26/technical-weight/
published: '2016-06-26'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Introduction

The whole idea for this post came from a very inspiring conversation with my friends and ex-colleagues from Ubisoft that we had over a dinner a few months ago.

We started to talk about a sophisticated code algorithm – an algorithm that is very well written, a brilliant idea, and lots of hard work of talented and experienced people to make it robust and perform very well on many target hardware platforms. On the other hand, the algorithm and its implementation are so complex that it takes almost full time for some people to maintain it. One of my colleagues called it a “technical debt”, which I disagreed with, and we started to discuss differences, and I came up with a name, “technical weight”. Later, a coworker of mine named it “technical burden” and as they are a native English speaker, it’s probably a better term – but for the purpose of this post, I’ll call it “technical weight”.

A quick definition of technical weight would be a property that makes your solutions (very) costly and “heavy” not when implementing them, but in the long run; but in the clean and properly designed environment (unlike technical debt).

## This is not a post about technical debt

Let me be clear – this is not yet another post about technical debt. I think enough people have covered it and it’s a very well-understood problem. I like the analogy to a real debt and taking credit (or even a mortgage) – for short-term benefits and to move/grow faster, one can avoid the hard work of “doing it properly” (analogy of paying with cash) and instead take this “credit”. It can be many things – “hacking”, introducing unnecessary globals and states, ignoring proper data flow and data structures, injecting weird dependencies (like core data logic depending on visual representation), writing unextendable code, or sometimes writing just ugly, unreadable and aesthetically unpleasant code.

There are posts about what technical debt is, how to avoid it, how to fix it, or even necessary cultural changes within the company structure to deal with it (like convincing product owners that something that has no visible value can make an investment that will pay off).

What most posts don’t cover is that recently, a huge amount of technical debt in many codebases comes from shifting to naïve implementations of agile methodologies like Scrum, working sprint to sprint. It’s very hard to do any proper architectural work in such an environment and in a short time, and POs usually don’t care about it (it’s not a feature visible to customer / upper management). There are some ways of counter-acting it, like clean-up weeks (great idea given that your team actually cares about working with clean, good code – but unfortunately, many teams don’t)…

…But this is not a post about it. 🙂

## Enter the “technical weight”

So what is technical weight, then? I wouldn’t call this way a single item – technology / decision / process / outcome; I think of it as a property of every single technical decision you make – from huge architectural decisions through models of medium-sized systems to, finally, the way you write every single line of code. Technical weight is a property that makes your code, systems, and decisions in general more “complex”, difficult to debug, difficult to understand, difficult to change, and difficult to change active developer.

The technical weight of code producing technical debt will usually be very large – this goes without saying. But also beautiful, perfectly written, and optimized, data-oriented code can have a large technical weight. It is also inevitable to have some systems like that, so what is the problem here?

I also wanted to talk about my motivation behind writing a blog post about it. Enough people cover things like code aesthetics, “smart” (hmm) code tricks to make your code shorter; fighting technical debt, or even potentially counter-productive ideas like design patterns or technical-debt-inducing methodologies like naïve Scrum – but I haven’t seen many posts about taking technical weight nor psychology of picking technical solutions. So while lots of things will seem “captain obvious”, I think it’s worth writing and codifying at least some of it.

Before proceeding, I need to emphasize (more on it later): that every decision and solution has some technical weight. Some problems are just difficult, and the “most lightweight” one can be still a huge struggle. Some very heavy solutions are the way to go for given project and team and only way to progress.

Also, I do not want to criticize any of the examples I will give, I think they are great, interesting solutions, but just not always suitable.

## Analogy one – tax / operating costs

The first analogy that I would like to compare it to is similar to “technical debt” investment strategy. Imagine you want a car – and you decide to buy with cash a 1966 Ford Mustang or, not to imply an “outdated” technology, a new Corvette / Ferrari. Dream of many people, very expensive, but if you have enough money, what can go wrong…? Well, the initial cost of the item is just the beginning. They use lots of gas. They are expensive in maintenance (forget an old car if you don’t have a special workshop or trusted car mechanic). They can break often and require replacement parts that are hard to come by. Insurance costs will be insane, and in many countries, their registration cost / tax is much higher (“luxury goods”). Finally, you don’t want to take your perfect Ferrari on a dirt road.

So even if you could afford something, didn’t take a loan, and bought something in technically perfect condition, initial costs are just the beginning, and you will end up having to spend huge amounts of money or time and still won’t be able to do many tasks.

## Analogy two – the literal weight of carried baggage

The second analogy is comparing a project / product / developing a technology to packing up when going on some trip. Depending on the kind of trip (something longer than a casual walk / hike), you need to pack. A minimum change of clothes, some water / food, a backpack, maybe a tent and a sleeping bag… But someone can decide, “let’s take a portable grill!”; “let’s take specialized hiking gear!”; “let’s take a laptop, portable speakers, and a guitar!”. All of those ideas can be decent and provide some value for certain kinds of trips, but then you need to carry them around for the duration of the whole trip. And for sure, if your trip doesn’t involve a minivan, you don’t want to take all of those. 🙂 If you are just walking, the weight on your back will be too heavy for a long trip – it is inconvenient, making you more exhausted, stopping you more often, and in some cases, you might not be able to finish your initial trip because of this weight. You can always throw them away after some point, but this is a pure waste of money / initial investment.

## Back to tech

So we have some solution that is well architected, designed, and written – no hacks involved. But it is very complex and “heavy” – why it *could* be bad?

- Required staffing to maintain it

Almost no system is ever “finished”. After you write and commit it, there will probably be many iterations. Obviously, it depends on the field of IT and domain (I can imagine some areas require very careful and slow changes – medical equipment and space rockets? Some others can rely on one-off products that, when you are done, you never go back to), but in most cases, when you are working on a longer-term project, you (or someone else taking it over) will revisit such code again and again and again. You need someone to be able to maintain it – and the heavier the solution, the more staffing you need. Think of it as property tax – you will “pay “ (in time spent) on average every month some percent of project time. It can be anything from marginal 0.5% to anything like 50% – scales almost directly with the quality of code /solution (but as I explained – this is not a post about bad code) but also complexity.

- Difficulty in getting new developers into the system

Very heavy, smart, and sophisticated solutions can take lots of time for new people to learn and start actively working on them. Sometimes it can be even impossible within the project time frame – imagine an algorithm written by some world expert in the given domain; or even a team of experts that decide to leave your project one day (it happens, and it’s better to be prepared…).

- Bugfixing costs

Every system has some bugs. I don’t remember the exact estimate, but I remember seeing some research conducted on many code bases that found the average number of bugs per 1000LOC – it’s quite constant from language to language and from developer to developer (at least statistically). So more complicated systems mean more bugs, more time bug-fixing, but also, if they have lots of moving parts – more time spent debugging every single bug. If your code is “smart”, then the “smartness“ required during debugging is even higher – good luck on that when you are later time-pressured, stressed, and tired (as lots of bug fixing happens at the end of projects)…

- Complicated refactoring

Requirements change, especially in many agile-like projects like game development. If you made your project very “heavy”, any changes will be much more difficult. I noticed this is usually when technical weight can creep into technical debt – under time pressure, you add “just one, innocent hack” (that at the end of the project, after N such worse and worse hacks means huge and unmaintainable tech debt). Or spend months on a refactor that nobody really asked for and adds zero value to your project. So, technical weight and shortage of time or resources can evolve into technical debt.

- Complicated adding new, unrelated code

Similar to the previous point, but unlike requirements changing, this one is almost inevitable. You always have systems surrounding your system, various interacting features and functionalities. Now anyone wanting to interact with it has to understand lots of its complexity. It’s a problem no matter how well interfaced and encapsulated it is; in general, it is something I would require from every good programmer – if you call a method/use a class, you really should understand how it works, what it will do, what is the performance impact and all consequences.

- Psychological aspect

With technically heavy solutions, one of the major aspects that is ignored by most developers is psychology and cognitive biases. (Side note: we often tend to ignore psychology as we want to believe we as programmers, engineers, scientists, and educated “computer people” are reasonable – what a fallacy). All kinds of biases can affect you, but I will list just few that I see very often with programmers regarding “technical weight”:

[https://en.wikipedia.org/wiki/Confirmation_bias](https://en.wikipedia.org/wiki/Confirmation_bias) “I made a decision so I see only its advantages and no disadvantages”.

[https://en.wikipedia.org/wiki/Escalation_of_commitment](https://en.wikipedia.org/wiki/Escalation_of_commitment) “We already invested so much time/money into it! We cannot back out now, it will pay off soon!”.

[https://en.wikipedia.org/wiki/Progress_trap](https://en.wikipedia.org/wiki/Progress_trap) “We have to keep on going and adding functionalities, otherwise we will regress”.

[https://en.wikipedia.org/wiki/Loss_aversion](https://en.wikipedia.org/wiki/Loss_aversion) “It’s more important to avoid bad performance / instability / whatever than focus on advantages of other solutions”.

To put it all together – if we invest lots of thought, work, and effort into something and want to believe it’s good, we will ignore all problems, pretend they don’t exist, and decline to admit (often blaming others and random circumstances) and will tend to see benefits. The more investment you have and heavier is the solution – the more you will try to stay with it, making other decisions or changes very difficult even if it would be the best option for your project.

## Examples

I’ll start with an example that started the whole discussion.

We were talking about so-called “GPU pipelines”. For anyone not specializing in real-time graphics, this is the whole family of techniques driven by a great vision – that to produce work on the GPU (rendering / graphics), you don’t need to produce work on the CPU – no need to cull visibility, issue draw calls, put pressure on drivers – it all (or almost all) could be potentially generated on the GPU itself. This way, you can get great performance (finer granularity culling / avoiding work; also GPUs are much better at massive amounts of simple/similar tasks), have your CPU available for other tasks like AI, and even allow for efficient solutions to the whole family of problems like virtual texturing or shadow-mapping. What started the discussion was that we all admired the quality of work done by our colleagues working on such problems and how it made sense for their projects (for example, for projects with dynamic destruction, when almost nothing can be precomputed or user-generated content or massive crowds), but started to discuss if we would want to use it ourselves. The answer was everyone agreeing “it depends”. 🙂 Why wouldn’t we “always” use something clearly better?

The reason was simple – the involved amount of work of extremely smart people and the complexity of not only initial implementation but also maintaining it and extending it – especially when working on multiple platforms. Maybe your game doesn’t have many draw calls? Maybe lots of visibility can be pre-computed? Maybe you are GPU-bound but not on Vertex Shading / rasterization? There can be many reasons.

Another example could be relying heavily on complex infrastructure to automate some tasks, like building your data / code and testing it. If you have the manpower to maintain it and make it 99.999% robust, it is the way to go. On the other hand, if the infrastructure is unreliable and flaky and gets changed often – technical weight totally outweighs the benefits. So yes, maybe you don’t need to do some tasks manually, but now you need to constantly debug both the automation and the automated process itself.

Yet another example – something that will probably resonate with most programmers (I have no idea why it’s so fun to write “toy” compilers and languages; is it because it’s true “meta”-programming? 🙂 ) – domain-specific languages, especially for scripting! It’s so enjoyable to write a language, and you can make it fit 100% your needs, you have full ownership of it, no integration etc. But on the other hand, you just increased the entry barrier for anyone new to the system, you need to maintain and debug it, and if it is your first language, it will probably have some bad decisions and will be difficult to extent (especially if needs to be backward compatible). Good luck if every programmer on your team eventually adds or writes a new language to your stack…

Conversely, the opposite can also be technically heavy – relying on middlewares, off-the-shelf frameworks and solutions, and open-source. Costs of integrating, debugging, merging, sending e-mails to tech support… Realizing (too late!) that it lacks some essential or new functionality. Using a complex middleware/engine can definitely add some technical weight to your project. It often is the right solution – but weight has to be taken into account (if you think “we will integrate it, and all problems with X are gone”, then you have clearly never worked with middleware).

## Reasons for heavy technical weight

- Difficult problem

The first one is obvious and simplest – maybe your problem is inherently difficult, and you cannot work around it; it is the nature of your work. But then there is probably nothing to do about it, and you know it. Your solution will provide a unique selling point to your product, and you are aware of the consequences – all good. 🙂

- Thinking that you have a problem / your problem is difficult

On the other hand, sometimes you may think that your problem is difficult, and you want to solve it in a “heavy” way, but it is not, or you shouldn’t be solving it. Often, heavy solutions for such category of problems come from “inheriting” a problem or a system from someone. So, for example – continuing work on a very legacy system. Trying to untangle technical debt caused by someone else N years ago with gradual changes (spaghetti-C code or lava cake OOP code). Trying to solve non-tech (cultural? people?) problems with tech solutions – a category that scares me most and is proof of our (yes, almost every engineer, me included, falls into such fallacy) technocratic arrogance. 🙂 Numerous problems only seem very difficult – but it’s pretty hard to see it. Advice here – just ask your colleagues for a second opinion (without biasing them with your proposed solution); if both you and them have some extra time, don’t even phrase the problem yourself, let them discover it partially themselves and comment on it.

- Not enough scoping

Often, a scoped user story will describe a very complex system that needs to do EVERYTHING, has tons of features, functionalities, and all possible options, and works with all existing systems. You, as a programmer, will want it to also have great performance, readable code, etc. If you don’t apply some scoping, splitting implementation stages and don’t allow for users to start giving you feedback on early iterations (“hey you know, I actually don’t use those options”), you are probably guaranteed to end up with too heavy a solution.

- a. Future coding

To explain the term – excellent blog post from Sebastian Sylvan that inspired me and helped me grow as a programmer. [http://sebastiansylvan.com/post/the-perils-of-future-coding/](http://sebastiansylvan.com/post/the-perils-of-future-coding/)

This is a subcategory of 3, but even worse – as your over-engineering doesn’t even come from the user! It is a programmer trying to be overly abstract and predicting user problems ahead. On its own, it is not a bad thing, but instead, the solution should be as always – KISS, write simple systems with not many moving pieces and strings to the outer world that you can replace.

- Not willing to compromise

This one is really difficult as it’s not a bad thing per se in many situations… Sometimes, you need to sacrifice some aspects of the final result. Is 5% performance increase worth a much more complicated system (10x more code)? Is having automatic boilerplate code generation worth spending months on some codegen system? It always depends on many factors, and you cannot predict the future… And for sure, if you are open-minded, you would agree that some past decisions you made were bad or even regret them.

- Not enough experience seeing the technical weight and evaluating consequences

This is a problem mostly for junior programmers – I remember being inexperienced and jumping with enthusiasm to every single new feature and request, writing complicated things and wanting them to be the best in every possible aspect. Shipping a few products, especially if dealing with consequences means lots of effort/problem, usually teaches more humility. 🙂

- Programming dogmas / belief

Horrible, horrible reason to add technical weight. Someone says that it has to be “true OOP,” “idiomatic C++,” “this design pattern,” or obey some weird religious-like arguments. I heard people saying, “oh you should code in this way, not that way, because this is how you do things in Java”. Or recently, “multi-inheritance is better than composition or polymorphism, in general, better than if statements” (wtf?). My advice? If you don’t feel you have enough energy to inspire a major cultural change with months of advice, examples, discussions, and no guarantee of succeeding – then you don’t want to work with such zealous people. Whether Java, C++, or other fanatics. Change your job.

- Fun!

Okay, this is a weird point, but if you enjoy programming and problem-solving, I am sure you will understand.

We like solving complicated problems in complicated ways! C&P 5 lines of code are not so “fun” as writing a complex code generator. Using off-the-shelf solutions is not as enjoyable as writing your own domain-specific language. In general – satisfaction and dopamine “reward” from solving a complex problem and owning a complex, sophisticated system is much higher than simple solutions to a reduced/scoped problem. We want to do cool things, solve ambitious problems, and provide interesting solutions – and it’s okay to work on them – just admit it; don’t try to lie to yourself (or even worse, your manager!) that it is “necessary”. Evaluate if you have some time for this fun coding and what kind of consequences it will have in 1/3/6/12/24 months.

- Being “clever” and optimizing for code writing, not reading

It is something between points 6 and 7, but fortunately, it often happens on a very small scale (single lines/functions/classes); on the other hand, unfortunately, it can grow and later impact your whole codebase… Some programmers value the perceived “smartness” of their solutions, want to solve mental puzzles, impress themselves or other programmers, or optimize time spent writing the code. They would hide complexity using some macros, magic iterators, constructors, and templates. This all adds lots of technical weight – but can slip through code design and reviews. Good luck reading and debugging such code later, though!

- Career progress – individual

Thanks to Kris Narkowicz for pointing out that I forgot about a very common reason for people trying to write sophisticated, over-ambitious systems and solutions.

I think it can be split into two subcategories.

The first subcategory is individual growth. It’s a pretty interesting one, as it’s something between 7 and 8. We want to do interesting things and get challenged every day, working on more and more ambitious things to develop our careers and skills. Many programmers are ambitious and don’t treat their work just as a “day job”. They would like to develop something that they could do talks at conferences, be proud of having in CV/portfolio, or even contribute to the whole computer science field. Easy solutions and simple tasks don’t get you this, and they don’t leave a “legacy”. You can do it in your spare time, contribute to open source etc. – but you have limited time in your life, and, understandably, some people would prefer to do it at work.

Again – it’s something that is ok on a limited scale – if you never do it, you won’t feel challenged, your career will stagnate, and you can get burned out (and eventually look for a more interesting / ambitious job). Just make sure it is not an unnecessary, common pattern and doesn’t eat up the majority of your time (and especially doesn’t cause lots of work for others…).

- Career progress – in the organization structure

Similar to the previous one – but this point is not driven by the individual and their goals and ambitions, but by weird organizational structure and bad management. Pathological organizations will promote only people who seem to do very complex things. If you do your job right, pick simple solutions, predict problems, and make sure they never happen – in many places, you won’t be appreciated as much as someone who writes super complex system, puts lots of overtime into it, causes huge problems and in the end “saves the day” last night. As I said – it is pathological and not sustainable. It definitely should be recognized and fixed in the organization itself.

I even heard of major tech companies that make it a clear and explicit rule to get bonuses and getting promoted – that you need to be an author and owner of whole systems or products. I understand that it is an easy and measurable metric, but in the long run, problems and pathological behaviors outweigh benefits; it can be detrimental to any teamwork and good working culture.

## How to deal with technical weight?

You will probably be disappointed by the length of this paragraph, but there are no universal solutions. But – being aware of technical weight will help you make better decisions. Thinking about every problem, evaluate:

– How much technical weight can you carry on? Do you already have some heavy systems and spend a lot of time supporting them?

– For how long do you need to carry this weight? Is your product / tech a sprint, or a marathon / “trip around the globe”?

– If your team gets reduced or the main contributors leave, can you continue carrying it?

– Is a heavier solution providing you some unique value? Are your users going to be able to iterate faster? Is it some unique feature that customers will truly appreciate? Are you going to be able to use, for example, cutting-edge performance to make your product unique?

– What are the disadvantages of lighter solutions? Are they really unacceptable? Can you prove it, or is it just intuition driven by biases?

– Are you proposing this solution because it is more interesting and fun problem to work on? Trying to be “smart” here and want to do some impressive work?

– Are you psychologically biased towards this solution? Did you already invest a lot in it? Is there an ego aspect? Are you obsessed with loss aversion? Have you really considered alternatives with an open mind, and others suggest the same “weight” of solutions without you guiding them?

To close this post, an observation that I had looking at how different is to work with teams of different sizes – adding technical weight can be most difficult for medium-sized teams.

Usually, small, experienced teams will add some technically complex and heavy solutions to add unique value to their unique, hand-crafted product. There are some specific teams (often coming from demoscene) and games that have some very original, beautiful tech that could be difficult to maintain and use for anyone bigger (and good luck convincing lots of people in a bigger company to such risky ideas!). If you like video games and rendering, you probably know what studios and games I talk about, Media Molecule and Q-Games and their amazing voxel, splatting, or SDF-based tech. There are more examples, but those 2 come immediately to my mind.

On the other hand, technically heavy solutions are also suitable for giants. EA (specifically their engine, Frostbite division, and amazing work they do and publish) or Ubisoft (that this year at the GDC broke the record of valuable, inspiring, and just great technical presentations) can invest lots of money and manpower for R&D and maintenance of such technology, and because it is shared between many products, it will pay off. So even if solutions are “heavy”, they can manage to develop them.

Medium-sized teams have neither of those advantages – usually, they have to have many different features (as targeting a wider audience – costs – they are not able to stick to a single unique selling point), but don’t have enough manpower to waste time on too complex problems and endless R&D. Therefore they have to choose appropriate solutions carefully, calculating ROI per every single decision. There is again a psychological aspect – having a team of, let’s say, 6-10 developers, you might think that you can do a lot more – and even if you do your planning perfectly and reasonably, having even a single person leave or tech requirements change can totally shift the scales.

Nothing really special here – but working with technical weight is like working with psychological biases – everyone has them, but just being aware of them makes you able to make better, less biased decisions. I recommend reading from time to time about cognitive biases as well – and analyzing own decisions when looking for them.

## Special thanks

Special thanks go to my friends who inspired the whole discussion a few months ago – alphabetically – Mickael Gilabert, John Huelin, David Robillard, and lots of insight into the problem. I miss such inspiring conversations with you guys!

Extra special thanks to Kris Narkowicz for pointing out an important missing reason for technical weight.

Pingback: Weekly Links #21 | Useful Links For Developers

Pingback: technical debt/technical weight | Bibliographic Wilderness