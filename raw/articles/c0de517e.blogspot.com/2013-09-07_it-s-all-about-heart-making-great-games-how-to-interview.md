---
title: It's all about heart (making great games; how to interview)
url: http://c0de517e.blogspot.com/2013/09/its-all-about-heart-making-great-games.html
published: '2013-09-07'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[This also appears on AltDevBlog](http://www.altdevblogaday.com/2013/09/07/the-technical-interview/), albeit in a shorter version (which I see few reasons not to prefer...), I decided it was best not to ramble too much on other websites.


**Introduction**

The original post title was "it's all about people" but I couldn't resist

[quoting Fight Night](http://www.youtube.com/watch?v=V1NfPEUSE6o)… Bear with me, as I don't think this will be short :) As always I talk from a perspective of a rendering engineer making videogames, but this really applies to anything. Here,[take a comic](http://dangerousminds.net/comments/jimi_hendrix_job_interview)and let's go...
I've had in my career the pleasure (mostly) of working with a few different studios (and teams), seeing a few others at work and talking with people from many more. And of course, as we are scientists/engineers/geeks after a while of this exposure you start wondering what's "best", or at least, what's good and bad, the science of making great games (great, not successful, that would add marketing to the equation).

Truth is though, I still don't really know. (*shocking* huh...)

I've seen great games made by twenty creatives having fun and good games made by two thousand slaves burning their life away. Smart people coding in pretty oldschool C and equally smart people coding in "modern" C++, and both parties with their reasonable reasons to do so. Wonderfully "engineered" practices, shared by juniors and seniors alike, to code relying on hackers and their ability to work without any engineering. You get the picture...

Now, of course part of this is due to the fact that "great games" come in all sizes and genres, and there's probably not much in common to how "great" (and successful) Little Big Planet is with how "great" (and successful) Call Of Duty is.

And of course in practice a given process works best only at a given scale (similarly on how a given algorithm is best for a given problem size), something good for two people is not for twenty or two hundred.

It's uncanny the similarity to good programming: over and under engineering are problems, and we should apply fancier methods only when they actually save us time (and profile, always!). That said, all true, but even with all things being comparable, the ways for greatness seem to be many.

I always use as an example of how success seems hard to transfer,

[Fifa](http://www.youtube.com/watch?v=APMrtUd4WW8)and[Nba](http://www.youtube.com/watch?v=i_Qs0QqqD04). Maybe it's not a good example, I've worked only for a very short while in Fifa and never on Nba, so don't get this as an "insider" opinion, just as something puzzling when seen from the outside...
These are two teams that seemingly make two fairly similar games, sport simulations, on huge licenses. They do that under the same company, label, studio, and a company that is notorious for its organizational practices. They were even physically closer, same building, same floor... They had access to the same technology (what now EA brands as the "Ignite" engine) and shared many people too. Yet, somehow, one thrived, squashing its competition both in quality, innovation and sales, while the other lost year after year, went through different "rewrites" and eventually led that team at EA Canada to be shut down and the franchise moved to Tiburon...

Now, surely there are reasons, and I might even have my idea of what level is to blame most, but that's matters nothing, the reality is, success evidently is very hard to transfer...

That's not to say that there is no good and bad. Certainly there is

*bad*.
I've seen it, horrible projects with horrible processes, with horrible code that horribly failed, there certainly is a quality to the process of making games. And there are even things that are "universal", that are never or always are a good idea.

But most of what makes a big difference, I'm persuaded, is relative. And it's relative, I think, to the people you have. Not even the product you're making, that comes second, it's informed by the people you have but even if it's not (we have to make the game X), the ways you'll make it depend on the people.

Initially, the people you have are the ones you happen to have, companies are made, somehow, not much to say about that... But then you keep (or steer towards) a given bias via hiring. And that's why I'll spend the rest of this post on interviewing, and my half-wrong opinions on how you should interview "good" people...

**Interviewing is a bidirectional communication process**

When I started drafting this article (unfortunately, I wrote less that I though I did, and ended up using nothing), I was looking for a new job and so was a period where I was interviewing more than usual, talking with many studios (maybe even too many, some interviews, I came in shamefully unprepared), and I was reminded now to finish it as I went through a few calls as an interviewer. So, I won't claim to be good at this, but I'm not lacking experience :)

From my empirical survey of the state of the industry, I'd say the number one "offender" in the process is not realizing, or caring enough, about the fact that interviewing is a bidirectional communication.

What you ask and say is not only used by you to assess the candidate, but by the candidate to assess you, and the job you're offering. You're not an university professor giving an exam, the goals of an interviewer and as an interviewee are fundamentally the same. Find a work relationship that makes

[both parties happy](http://dilbert.com/strips/comic/2007-11-24/).
I remember when I first landed at EA, six years ago now. It was my first international job (that's to say, going outside Italy), I flew for an entire day and I was terribly jet-lagged. After interviewing with six (IIRC) teams I left with more doubts than I had before, I didn't know what to expect from the job, and I thought that if I accepted, I would be tasked with the most trivial things, as most interviews were surprisingly basic.

In the end EA made me a good offer and I accepted the job, it also helped that I thought I had no more to grow in my current company at the time, it was the right decision and a very lucky one, I landed in an incredible team, making an amazing game and I was free from the get-go to do much more than I was doing at the "peak" of my career in Italy. But, the interview process almost killed all this for me.

It wasn't an isolated incident. Since then, only a very few times I was "sold" on a job by the interview, really excited by the process. Most of the other days I consider it lucky if I had some fun, talked to some nice people, but left with knowing at all what a given job and company really looks like. Unlucky if I went through everything as a chore, procrastinated on tests and kept going on motivated only by the name of the company and the role of the opening rather than true interest...

Before diving in, as a disclaimer I have to say (because I predict that would also be a comment) I might nowadays be biased towards "seniors", as I happen to interview more experienced engineers than juniors, on average, but I believe that it doesn't fundamentally matter what position you're hiring for, I think the same principles apply, even if they should be implemented differently.

**Eight common, bad mistakes in the technical interview**

*Coming up next: eight magic foods for a flat belly your doctor doesn't want you to know about*

**1)**Wasting time.

It's good to assume that smart people are busy, and that they are in demand. So, having to spend weeks on an interview test is often not a great idea.

Now, to be fair, longer tests are not necessarily bad, and not necessarily a waste of time. They can be even fun and truly informative, e.g. interesting mini projects done with good communication could be great. Even trying out a candidate as a contractor could be not a bad idea. But, pragmatically, chances are that good candidates are busy, and won't subject themselves to all this while interviewing with many other companies, so you might lose some great people to your lengthy test. It's a compromise, be aware of that, and make your process as long as it needs to be but not any longer.

Like good code, avoid waste.

*Great companies with (in my experience) longer tests? Media Molecule, Sucker Punch (their rendering engineer code test was publicly available on their website!), Crytek. The best, short, elegant one? Sony Santa Monica.*

**2)**Overused questions.

Simple to google, simple to memorize, boring to answer over and over again. Overused, simple questions are bad in many ways. To the experienced, they signal that you're not doing a great job interviewing people, that quality is not a priority, that you did not take much effort crafting your interview. For "juniors", they encourage memorization (or looking things up on the net) over reasoning.

It's not hard to come up with original questions and even slight variants of common problems are great. Why asking the distance of a point to a line if you can ask for a sphere versus a line, or capsule? It tests exactly the same knowledge, but applied, instead of just recited.

A common side-effect of using such "dumb" question is the necessity of strict timing, where as your questions are too stupid and easily googled, you counter-act not by "fixing your bug" but by asking a load of them in quick succession to "defeat" google.

**3)**Useless questions.

This is an extension and aggravation of the former, often, overused questions are also worthless, not needed. Questions that require a follow-up which would already demonstrate the knowledge of the preceding, e.g. I ask you what's a class in C++, then I ask you to apply it in a practical context.

Now, it's true that there is merit in making your candidate comfortable, but useless questions often come in written questionnaires where there is less stress, often don't make a "difficulty ramp" but are just random.

Good questions sidestep the issue though, as you can, and should, design ones that can be as easy as needed to answer trivially but as deep as possible for smart candidates to dive into and provide smarter solutions.

An example is N-d AABB vs AABB intersection, but there are so many deep and fascinating simple problems in computer science that there are no excuses.

**4)**Worthless questions.

Delving into

[bad questions](http://theoatmeal.com/comics/interview_questions), the worst are ones that are not just too simple, overused, boring or made useless by the structure of the test, but questions that are not good at all per se.
An example could be of the

[kind of "IQ"](http://www.businessinsider.com/answers-to-15-more-google-interview-questions-that-made-geniuses-feel-dumb-2012-11?op=1), not even slightly related to the field, questions that infamously some large organizations are said to use (but that[I doubt they really do](http://www.technologywoman.com/2010/05/17/debunking-the-google-interview-myth/)). Another are questions that test knowledge that really one shouldn't need for the job.
Try your best to keep your questions relevant. Large organizations can analyze the performance of the questions they ask, but most studios won't interview enough for the data to be really significant. A good indicator could be to "eat your own dog food" and "submit" your questions to your employees to see and rate. Ask how much they think they're relevant, and how much they think they're interesting, and fun...

Unfortunately, often one is genuinely asking questions that are worthless because it doesn't think that's the case. At least that does communicate something though, e.g. if you ask me about design patterns I'll know I won't like to work for you.

**5)**Not tailoring to the skill level.

As good code, good questions are specialized. Not tailoring to the skill level is often associated with the previous mistakes, as for sake of generality you tend to ask more questions and wasting more time.

True, certain things have to be asked. And true, certain companies might hire people all of similar skill levels (i.e. smaller studios with mostly senior generalists), but that only means that you won't need many different questionnaires, still, the one you have will be tailored for the people you're looking for.

**6)**Pretending to interview.

Asking what you're supposed to ask. Saying what you're supposed to say. Going through a checklist someone made somewhere, not understanding what you're really doing. Happens often with standardized tests when interviewers don't really understand the purpose or depth of the tests.

This hampers the communication really, it makes the interview not a real interaction but a standardized bureaucratic chore that leaves both parties with very little information.

This hampers the communication really, it makes the interview not a real interaction but a standardized bureaucratic chore that leaves both parties with very little information.

Yes, you made sure that the candidate knows certain things. What does that mean? That's necessary but by no mean sufficient! A counterexample, and one of the worst thing to work with, is people that have a sufficient knowledge but not enough experience to know their limits, and openness to learn and experiment more.

Knowledge is easy nowadays, much easier than finding people that understand a given domain or that are able to produce smart ideas about it.

Ideally, interview questions are coauthored by the interviewers, and every new interviewer has a chance to discuss the process, understand and even add or change it.

Ideally, interview questions are coauthored by the interviewers, and every new interviewer has a chance to discuss the process, understand and even add or change it.

**7)**Not paying enough attention.

Pretending to interview redux. Pretending not only doesn't make much sense as a test of the candidate, but it also usually leaves the candidate with no impression of how working at your company will be, what really are its strengths, how does it work.

Remember, as you won't accept a candidate that just -says- he's good at certain things, the same applies to you.

You have to show that your company is smart, you have to prove you are smart, and you have to prove that you work in the ways you say you work! And asking the right questions is one strong hint that the candidates (especially the smarter ones, the ones you want) will look for…

**8)**Over-engineered platforms.

Lastly, there is the sin of over-engineered testing platforms. That probably doesn't depend on you, but it can be so bad, and such a waste of time, it will make people not want to apply to your company or prioritize it after others that use more friendly processes.

If you need a person to jump through a hundred hoops, register to faulty online services, scan, copy and paste all his resumé, write pages after pages of forms on his education and so on, I really hope you're getting a great return on all that neatly catalogued information, because surely you're pissing off your applicants a LOT to gather them.

Also you're giving the impression of a overly bureaucratic company with a ton of management levels and an HR group that doesn't know what technical people find fun.

**Going further**

Your interview is as short as possible. Your questions are simple but deep. They are relevant to the job, tailored to the skill level. You understand them, what kind of people your company needs, you discussed about interviewing with your peers, and you're doing all this in a fun, informal process.

Great! You're doing everything right, and even with just interviews you should be able to make an impression in your candidate, paint a picture of what's valued at the company, how it works, and making a good effort of finding not just people that you can use, but actually good fits. People that work they way you work, or that can learn to.

Can it go even further? I'm partial to openness, and collaboration. What can you show? Are you looking for someone that will hack through your code? Then maybe you could use some of said code in the process. Are you looking for someone that will need to work with the artists? Then you might want them in a room to brainstorm techniques to get a given visual result. The more you can incorporate of the job and of the company in the interview process, the better.

Many companies won't do that because it's complicated to disclose anything, even of past projects, even under NDA. It's a shame and a problem that bogs said companies down, but even if you have to face such restrictions, can you imagine ways around them? Put some effort, and remember that getting the right people is most probably all that it takes to make great games.



## No comments:

Post a Comment