---
title: Interview mistakes
url: https://c0de517e.blogspot.com/2012/01/interview-mistakes.html
published: '2012-01-28'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Interviewing candidates is undoubtedly a tricky and important task for a software company who is seeking for new talents. Books have been written on the topic and while I can't call myself an expert, I do have been through the process enough times, on both ends, to have at least a good opinion of it.

There is a lot to talk about and things are different depending on if you're looking for a junior or a senior, also, a lot has been said already by people which are more competent than I am, so I would like here to focus on my personal experience as an applicant to senior/lead rendering roles, and the mistakes I see more often in the process. It's going to have some rant-ish undertones :)

In my opinion, two are the main problems to take care of:

**Don't waste time.**

Who would you rather employ? Someone who's working, has lots of competing offers, and little free time, or someone who things spending a days on your coding test is the most exciting thing happened to him that week? You want to hire the busy people.

If you applicant has three companies which are interested in interviewing him (and even in this economy, you know well that for seniors it will happen), who do you think he will try first? The one that lets him a technical interview the day after, or the one which asks for a long test for pre-screening?

Of course your engineers are busy too and pre-screening is effective in reducing the time wasted, but be reasonable. And differentiate between juniors or newly graduates which would probably have more time on their hands and fail more often, and seniors with years of experience. A one hour test is ok, a day long one, not so much, more than that and you'll start risking to be ignored or considered last.

This though does not apply to pre-screening in general, it applies to everything really. Get to the point. Yes, warm up questions might be useful if your applicant seems nervous, but there is really no need to start with things which won't get you any useful information, if you want to chat start with more colloquial questions instead of going straight to equations or code, and bring these to the table after the more loose conversation on a given topic.

A lot of the time waste though comes from not creating different interview paths for the different engineering positions, which also brings me to the next issue:

**Show some effort.**

Who would you rather employ? Someone who is in love with your company or someone who wants proof that you're worth his time? An interview is usually the first point of contact between the applicant and your company. And you should assume that he is there all the time analyzing you, he's evaluating you at least as much as you are evaluating him.

I never, so far, applied to a company for which I was absolutely persuaded I wanted to work with them when I applied. There are some games that I really would have loved to make, but I find impossible from the products a given company does to understand how working for them will be, and I suspect a lot of games I love are not made in environments I would have loved to be part of.

There are certain persons who fascinate me and who I would like to work with, but still, every time I interview I'm interviewing the company at the same time.

Put some effort, come prepared, don't waste my time. I have been asked questions which made me seriously doubt the kind of job they were interviewing me for (like once, when my whiteboard math question was about computing the distance between two points...), I've seen questionnaires with errors in them, and have been asked the same "tricky" algorithms over and over again. Nowadays, if someone asks me about polymorphism in C++ and the "virtual" keyword, it's an immediate flag that I raise.

Virtual functions? Distance between a point ad a line? Dot product? But, I hear you say, you would be surprised to know how many technical directors can't code. No I won't, but are you seriously going to think "oh, finally, a lead that knows virtual, let's hire him".

What are you asking? Is it relevant even or are you just wasting time? Seriously you can't think of a simple function to write, or problem to solve which tests all of these things and more?

Be original! Reversing the words in a string? The building and two eggs "google" problem? Finding the missing number in a sequence? Do your homework, are you going to test if your candidate studies the list of the ten most common interviewing questions, or if he has a working brain?

Even simple variants will do better. The distance between a line and a circle instead of a point. Same thing but it avoids the mechanical "go to my dictionary of ready-made answers I've studied the night before".

There are plenty of simple problems you can invent which can expand in all sorts of interesting directions, craft a few, unique for your company, for each engineering level, and maybe change them every few years.

P.S. So are there companies which did it "right"? My best experience so far was with Sony Santa Monica. Original, effective and required little time, showed effort and respect, which is not surprising knowing how smart Christer Ericson is... Crytek was also good I have to say, I rate it second because the process required way too much time, but talking with Ury Zhilinsky was awesome. The worst ones? Probably left me so unimpressed that I won't remember the companies.

## 6 comments:

Nice article!



Personally, I have never seen a good technical test.

The main problem is often that they are not done in a "real world" way. Seriously, what does it tell you that a candidate does not remember a mathematical formula? It happens to everyone, and when it happens in real life, we just open our favorite textbook/website and get the information we want. What you want is to find if your candidate can use those formula in a creative way, and at the good time too. For this reason, I favor "high level" questions during interview than "low level" implementation detail. I want to know how the candidate work, when facing a problem that he does not already know the answer.

Borelaux: There is a certain middle ground to it. I don't believe that an interview can be effective with only high level chat, even if we all love to talk about high level stuff.





You have to make sure that a given person still can code, do math, and that he actually has experience in what he's talking.

Asking to remember Ford-Fulkerson or quaternion to matrix? Surely a stupid idea. Most low-level questions should still be about the candidate's ability to reason, and not to just remember, that's why I said in the article, craft your own logic questions.

On the other hand though, asking what [isolate] does with the 360 hlsl compiler, or the distance between a plane and a point, or what is C++ "restrict" on the other hand "proves" the the person has seen these things enough times, that are part of his job, so there is a degree of memorization which is useful to test.

But these questions should be aimed at checking things which are common enough for a given kind of programmer (i.e. "feature rendering" versus "system or optimization rendering") to work with them daily or so, while not so common that people could have just studied them and not learned through first-hand experience (that's why I hate asking about "virtual")

An interesting read, thanks for sharing.


I have very little interview experience myself, but I find myself agreeing with Borealux about low level details or math questions. If a programmer knows plane-point intersection verbatim because he has implemented it on a daily basis or so, one might even argue a lack of abstraction capabilities :)

Forget my previous post, plane-point intersection... I couldn't have disqualified myself any better even if I tried :)

I really like the article, but I don't fully agree with everything. Usually when I do a phone interview I first like to talk to the person and get more information on his background (after explaining a bit about ourselves, the project and company to make him feel relaxed of course). Find out what he likes, what he is proud of, what makes his day .. and where he wants to go.



From this info it's possible to find out his expected technical knowledge, and then some low level technical questions are always good to see if he 'lives' up to the expectation of what he told you before.

For this the 'virtual' function question is actually pretty good. What and how is not important. Everyone knows that. More interesting is, how is it implemented in C++, what is the extra runtime and memory cost, what about cache misses (code, data caches), why is more expensive on consoles compared to PCs, how do you profile the cost of this? This all starts from a simple virtual function question, but can easily go rather deep and see how much the person actually knows about C++, and how interested he is in trying to understand systems. Of course not everyone has to know everything, but the reaction of the person is also very good to see how they react to things they don't know yet.

Oh, yes, virtual versus function pointers or jump tables, the powerPC implementation etc, these are great questions. I was criticizing the kind of lame questions about polymorphism and "can you make a simple example of where do you use virtual?" and stuff like class A : public B... what would B::Foo print? And so on, when asked to a senior programmer.

Post a Comment