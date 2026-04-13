---
title: Why Scrum is fundamentally broken (but we still use it)
url: http://joostdevblog.blogspot.com/2014/03/why-scrum-is-fundamentally-broken-but.html
author: Joost van Dongen
published: '2014-03-23'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Ronimo](http://www.ronimo-games.com). Most companies don't use pure Scrum: they change parts to fit their needs. This is so common that there is even an official name for it: ScrumBut (as in: "We use Scrum,

*but*..."). Any Scrum purists I have met are strongly opposed to ScrumBut, but when talking to them I learned that their views are so rigid and stubborn that they don't understand that one of the core concepts of Scrum is fundamentally broken when used for game development. The purists I met simply deny the problem and come up with fancy crap like this:

*"ScrumButs are reasons why teams can’t take full advantage of Scrum to solve their problems and realize the full benefits of product development using Scrum. ... A ScrumBut retains the problem while modifying Scrum to make it invisible so that the dysfunction is no longer a thorn in the side of the team."*(

[source](https://www.scrum.org/ScrumBut))

Purists want you to believe that only pure Scrum works, but Scrum is fundamentally flawed and therefore not a full solution to project management. I think Scrum is still the best methodology around, but it is crucial to understand its problems and to not overestimate what it can do.

Scrum is mostly know for the stand-up meetings and the blackboards full of post-its, which are both great concepts. The big problem is in how Scrum relates to the overall process. Project management methodologies have many goals, like internal communication, empowering developers, facilitating innovation, communicating with stakeholders and the happiness of the team. Scrum is really good at each of these, but it falls flat on the face in the area that people most often associate with project management: meeting deadlines.

![](../../assets/5a7b95da6a7c8b60.jpg)

Scrum works with Sprints. A Sprint is a period of typically 1 to 4 weeks in which a certain feature or set of features is built. At the start of every Sprint it is decided which things to work on, and at the end of the Sprint the product is reviewed. Scrum deliberately asks the team not to look too far ahead: the core question when deciding what to work on during a Sprint is what the biggest improvement to the product is at that moment. During the Sprint this is then build and completely finished: Scrum emphasises that whatever is build during a Sprint should be finished and potentially shippable by the end of the Sprint.

This idea of having a fixed period of development and then evaluating what is most useful to work on next is a very good concept for game development: it is often impossible to really know what works until you are playing it in game, and once you are playing it you will learn all kinds of things about what the game actually is and where to bring it next. Regularly evaluating what works and what does not is really important for making good games and Scrum facilitates this really well.

The fixed period of a Sprint also manages to fix the big downside of constantly evaluating: it can be pretty frustrating if the plan changes from day to day and you cannot finish what you are working on because the plan changed

*again*. Scrum forces that the plan cannot change during the Sprint, so it gives a certain amount of stability to the developers. This way they know where they stand during the Sprint.

The emphasis on re-evaluating what is needed next at the beginning of every Sprint brings up an important question: how do we know when the product will be finished? How to meet deadlines? Scrum has a short and simple answer to this: since every Sprint requires the things made in that Sprint to be finished, and since the most important things are always made first, the product is potentially shippable after

*every*Sprint. The product gets better during every next Sprint and at the end of every Sprint it is again potentially shippable. Shipping dates are therefore always met according to Scrum: just stop developing at the deadline and release the product in whatever state it was in at the end of the last Sprint.

**This is where Scrum fails utterly and brutally for game development, as this only works in theory.**

Let's have a look at a couple of examples of why this does not work:

-To be able to ship a game on console it needs to abide by the console certification rules. These rules are things like showing an error if the harddisk is full when the game wants to save, and pausing the game if the controller is unplugged. Console manufacturers provide long lists of certification requirements. If the game fails to pass their tests, it cannot release. Since the number of requirements is so large, implementing all of them is a very big task. For a game to be "potentially shippable" after every Sprint (as Scrum requires) the certification requirements should be implemented

*first*. Which is a horrible idea. One could in theory indeed start there, but in practice one really should not. Early in the project the most important thing is to get the core gameplay playable as quickly as possible and to set up the tools needed for the artists and designers, so that they can do their work. If the programmers start by focusing on certification requirements, then the artists and designers will waste several months with no game to work on. To enable the artists and designers as much as possible, gameplay programming should have priority and certification requirements should not be implemented until relatively late in the development period. In other words: the game cannot be 'potentially shippable' until very late in development.

-Many larger features also don't work with the concept of being 'potentially shippable' after every Sprint. Some things you either do entirely or not at all, like telling a story through cutscenes. Doing this the Scrum way probably means first very roughly animating all the cutscenes and putting them in-game. This is indeed a good idea for prototyping story flow early on. However, after that the next practical step is to just make each of those animations in turn. This means that halfway through that process, half of the animations are finished and the other half are still rough. Theoretically that might be a 'shippable product', but in practice you really cannot ship until all the rough animations have been replaced.

-Finally, the goal of game development is not "to finish a game" but "to finish a

*good*game". Meeting the release deadline by just releasing whatever you have at that point is a pretty worthless strategy because it does not say anything about the quality of what you release. I can imagine that if the project has completely derailed and failed then you might want to release whatever you have and forget about it, but in all somewhat normal cases I am not interested in just "meeting deadlines": what I am interested in is "making quality games on time". Scrum helps a lot in making quality games, but it hardly helps in making them on time.

Absolutely baffling is that when I discussed this topic with a couple of official Scrum trainers, they simply denied that the problem existed. They claimed that if the game is not in a shippable state after every Sprint, then you are simply doing Scrum wrong. The above examples clearly show their error, but they just kept repeating that if Scrum is done right, the problem does not exist. This is why despite that we use Scrum and I like many aspects of it, I strongly dislike Scrum purists. Good thing not all Scrum trainers are like that!

![](../../assets/19ce6aa1ce057cf4.jpg)

Most project management methodologies are bloated with too many rules and too many claims of being able to solve almost any problem. Scrum is no exception, and Scrum's concept of ending every Sprint with a 'potentially shippable' product just doesn't provide a solid solution to the problem of meeting release deadlines. However, none of the other methodologies I have seen does this much better, so I think that despite this major flaw, Scrum remains the best project management methodology for games. Just be sure to keep in mind its flaws (and to always distrust Scrum purists).

Tried posting a long reply and then hitting preview made it blank :( let's try again.




ReplyDeleteWith 'potential shippable' it doesn't mean shipping it to your players necessarily after each Sprint (hence 'potential' :p). Exactly for the reasons you are describing. We simply can't make a baby in 1 month, similar as we can't fit every feature in a 2 week Sprint.

Scrum encourages however to do design choices, development and testing all in one Sprint (according to your definition of done). Rather than doing huge design docs, months of architectural layers or do testing somewhere later after 3 months when you hit a milestone. It promotes delivering value for your players with doing all layers of production in a Sprint like a vertical slice of the game, making sure all departments closely collaborate. Incrementally increasing the game on the previous delivery where you learned more and can make better choices. Making it 'potentially' shippable in terms of quality, but not necessarily in quantity. Which is why it is still very normal in Scrum to have releases and milestones for stakeholders/players where a version makes sense.

My problem with some people who are using Scrum-But is that they are changing things in the framework without understanding the underlying motivations. You can change anything you like but need to understand the core agile principles behind it. For example if you do 2-week Sprints but skipping the retrospectives as it was a painful meeting you are not really getting it, unless you have other means in place that nurtures continuous improvement.

Compare it to copying game mechanics from other games: If you simply copy a #1 grossing title's mechanic because the game is so successful but you don't understand the reasons why it is working so well it will most likely fail. If you change something you have to understand why it's there.

I am actually quite happy with this article. Joost shows he has a good understanding of the application of scrum and he asks some understandable questions. At first glance scrum looks so easy. And it is! Though the application of scrum is a much tougher cookie. Another reason why I am happy is that opposed to last weeks blog on Coding Structures (which is just pure abracadabra to me) I actually understood this one ;)









ReplyDeleteMaurice his comments hit the mark regarding the shippable product. At the end of every sprint the product increment is ‘potentially’ shippable and thus optional and not mandatory. The scrum guide also states “The purpose of each Sprint is to deliver Increments of potentially releasable functionality“ (Schwaber & Sutherland 2013). The difference between product and functionality might seem minor, but the latter gives more leeway as product hints to something that is finished.

In your blog you state the following:

“it (scrum) falls flat on the face in the area that people most often associate with project management: meeting deadlines.”

It is not that I entirely disagree on this part, but I do feel the need to clarify. Scrum is not about meeting pre set deadlines. Deadlines that most of the time are based on nothing more than gut feeling or external obligations. Scrum is about predicting when a development team will meet the required set of features that are tied to that deadline.

Scrum is based on empirical process control. With scrum you manage the projects release cycle by based on facts. One of the most important facts you have in scrum is your team’s velocity (the amount of work delivered during each sprint). By (re)estimating the entire product backlog, taking your teams velocity into account (yesterdays weather in scrum terms) and the features you want to ship with your next milestone; you can predict with a certain degree of certainty when you will be meeting that deadline.

So rather than breaking your backs to meet an unrealistic deadline, which was conjured up out of thin air, your product owner can take informed decisions regarding deadlines and releases.

The other point Maurice got right was scrumBUT. Without going in full detail, it is my opinion that most agile coaches take an American stand to the implementation of scrum. It is an: ask no questions, shut your trap, believe me and just do it mentality. Kind of similar to the way they practice religion… True agile coaches will embrace change, though those changes - like Maurice points out - have to be made with a solid understanding of the underlying motivations. The preferred way to implement scrum is to start with everything and then scale down - if needed - based on personal experience. Unfortunately most scrum teams elect to scrap parts of scrum without actually having tried them first. Like I said before, scrum is easy, but the application isn’t. It requires determination and an open mind.

"thin air".. that comment is the problem the author was addressing.. you automatically dismiss a deadline as meaningless.. I worked in an ecommerce company.. was trying to get holiday gift cards out before Christmas a "thin air" deadline? I think not.. deadlines do exist for many valid reasons..

DeleteDeadlines are indeed an important thing. For example as a small company you might run out of money if development takes too long.


DeleteI do agree with Alexander's point that deadlines are a conjured thing, so I think that a project management methodology that tells you what is achievable and what is already doing the maximum. However, I think that Scrum's strengths are not there. Scrum provides prediction tools with the empirical process control, but it is far from perfect. Scrum really shines in how it fosters iterative development with the Sprints and evaluations and all that jazz. :)

Hi Gary,

DeleteI understand that some deadlines are important business wise. Perhaps I implied otherwise with the words I used. If so, i did not mean to. The main point I was trying to make with the 'thin air' quote is that most non empirical product plannings are based on "it would be great if we could do this" opposed to "we can actually do this"

@Gary. In this scenario, Scrum will help you mitigate that risk. After sprint 1 you are able to deliver a simple text card


DeleteAfter sprint 2 you can have different fonts

After sprint 3 you can add images

...

Getting to DONE in each sprint and being able to release is tremendously beneficial, compared to realizing on December 23rd that you're not gonna make it.

What Scrum will not help you do is (and no other framework that I am aware of) is "deliver exactly X functionality by Y date".

Really liked this post, thanks Joost! I have to agree with the comments made by Maurice and Alexander. 'Potentially shippable' shouldn't be taken so literally, for the exact reasons Maurice stated. That's why I prefer the term 'playable' for the teams I'm working with, and reserve the final sprint(s) for platform certification (although you'll probably release an Alpha or Beta during production and will have to adhere to some platform requirements then as well).




ReplyDeleteIndeed Scrum isn't about 'just putting out there what you have, when the deadline arrives'. It's about being able to predict what your team will be able to deliver feature-wise within the given deadline, based on the team's velocity. If you feel this set of features isn't going to give you the level of quality you want, you have ample time to steer: move the deadline, edit the composition of the team or adjust your goals.

The argument about not being able to finish large features within one sprint is quite common, these are called 'epics'. When a team feels that they won't be able to finish a certain feature in one sprint, the feature should be split into smaller, achievable chunks.

The essence of Scrum is its flexibility to reflect upon the work delivered after each sprint and to iterate if necessary until the level of quality has been met. It's exactly because of this core principle of flexibility that it makes perfect sense to adjust the Scrum method to fit the needs of game development, don't let anybody tell you otherwise!

I know that 'potentially shippable' shouldn't be taken that literally, but if you don't then the point those Scrum purists made to me fails, because their point was really based on the idea that the game is shippable after every Sprint...



DeleteI have heard several Scrum trainers say different things about the backlog. The way it was explained to me, it was often just a list of user stories/features, not nearly detailed enough to give any kind of estimate of when the project will be done.

If you extend this to have more detail and add Scrum's empirical process, then it very much goes back to an improved Waterfall approach. There is a list of features (called the backlog in Scrum) and the game is finished when all of those features are. Scrum surely has some interesting methods of estimating how much work something is, but backlog+velocity+monthly re-evaluations is very much just a flexible Waterfall. Not that I am opposed to that (we use something like that ourselves as well), but the long term planning method of Scrum isn't as special as Scrum might make it seem.

Guess we both disagree with the Scrum purists. I do believe in first trying to follow the principles as strict as possible, but when the team has adjusted to the ways of Scrum, it's only natural to adjust it to your specific needs.





DeleteIn fact, the only book written about Scrum in combination with game development (Clinton Keith's 'Agile Game Development') actually encourages to change up the method for game dev requirements. Check it out, it's quite interesting (a must read at my studio).

The way I see it, is that the backlog is indeed a list of all the features/user stories the game consists of. The thing is, this will be ever-changing, since the design will become clearer over time during development. So you start of with an initial backlog that gets updated with new or edited stories after every sprint. You can't have a complete backlog at the get go, since you won't be able to determine every detail of the game beforehand. Otherwise the games we make would be exactly like described in the game design documents, and we both know that's never the case :)

Scrum is about dealing with what you know and respond to change.

If you look at it like that, it's safe to say that Scrum isn't as much a planning method as it's more of a way to determine what can be done within a certain time frame.

Also, I wouldn't want to call it an improved Waterfall method, since it's an entirely different way of approaching software development. Waterfall has a phase-like approach, where (simply put) you go through the 'Concept-Design-Production-QA' phases for the entire game. This usually results in having a playable game after the production phase when you're probably already close to your deadline.

Scrum on the other hand delivers the aforementioned vertical slice of Concept-Design-Production-QA every sprint, making it a lot faster & easier to evaluate and adjust if necessary.

I'm not saying Scrum is the holy grail, it does have its flaws. But to me it feels like a method that deals in a realistic manner with the everyday pitfalls of game development, whilst putting quality upfront through the 'inspect & adapt' principle of iterative cycles.

Anyways, it would be cool to have a look at how you guys have set up the process at Ronimo, I'm always interested to learn from my peers!

I just call having long lists of features "Waterfall", but you are right that Waterfall is more than that. We indeed work with a long list of features that we constantly update with whatever new knowledge we get. :)

DeleteIf your definition of a long list of features is waterfall, then yes, scrums backlog is waterfall :)

DeleteThe main thing here is that not every userstory in scrums backlog needs to be finished to release the product. You can compare it to the good old MoSCow list.

Hi, nice article there. I agree 100% and although I never met any SCRUM –experts I think I would probably want to head-butt vigorously (ok, I’m kidding. Sort of).












ReplyDeleteOther downsides of SCRUM in gamedev I experienced:

- Some parts of the development process just don’t work in SCRUM. Bug-fixing is the first that come to my mind. There is no SCRUM, only pain :D

- It can be super hard and tricky to assess the completeness of a feature because of any kind of implicit dependencies. This is especially true for systems-heavy games where you need to have different interacting systems in place to actually get a “feel” of the game.

- Like all processes, it comes with its loads of standup things where people actually prefer to sit, planning/review meetings with hugely varying levels of motivation and all other ways of messing it up. It’s normal human behavior and it requires strong will, motivation and energy. Works fines when cruising. Not so much when under pressure.

- Integrating a QA/testing feedback loop with SCRUM is a must but is definitely hard to do consistently throughout development. It requires a very strong-willed producer/manager.

- Assuming you get to a “content-production” phase where all your design is done, SCRUM can work pretty well to get steady deliverables. In truth, I think you’re more likely to meet a sasquatch than experience this.

- Never seen SCRUM work in a team with no dedicated producer. It works with someone who can really take care of the respecting the process with no production tasks in between.

The interesting part is that while I have absolutely no perfect solution for all this, I still believe it can work when you take into account the specificities of gamedev. The sprints I managed to complete as planned really felt great and lead to great deliverables. I wish it would happen more often. :-)

Ultimately, I think the power of SCRUM resides in the people using it. If you can get your whole team to believe in your own variant of SCRUM and uphold it (meaning: kicking your butt when you’re feeling blue with no energy to chant the virtues of the MIGHTY PROCESS) it can work wonders.

As you say, integrating testing in the Sprint is difficult. However, I don't know whether you really should in game development. The coder can test his own code and beyond that any relevant bugs are automatically encountered during playtesting.


DeleteThe point to me is that there needs to be a balance between making everything perfect and actually moving the game forward. If too much emphasis were put on making everything entirely bugfree during development, then progress on trying new gameplay would be too slow. Bugfree is definitely an important thing to strive for, but there is a limit to what extend is still worthwhile during development. Some bugs takes days to fix while designers are waiting for new features that they want to playtest with, and then sometimes it is better to ignore those bugs for the time being. Truly perfect systems just take much more time to develop and integrate the testing.

Being bugfree is indeed something that is done over time and is less critical in the meta-discussion about SCRUM. I'm more interested in (Production time) VS (Design/Feedback time) debate which often ends up with the team feeling rushed to the next sprint with no






DeleteA couple of hints I have positive experience with:

- Alternate between a sprint (like 2 weeks) and 1 week of polish/testing/debugging. This is especially interesting if your team is committed enough to crunch at the end of a sprint. The following week is more relaxed and the whole team can participate in preparing the upcoming sprint.

- If the above is not possible or if you tend to work on longer sprints (3-4 weeks), one day of the week can be spent testing the game and fixing things that are relevant to the team members. The overall quality/stability of the game is improved AND the team keeps a "feel" for the game and participates more constructively in the project as a whole (instead of being narrow-minded on their single task). This also makes late Thursday the weekly deadline.

Actually, we happen to be trying that very approach soon: next week part of our art team is going to do "polish week", where they don't have a planning and figure out together whatever they feel they want to improve in that week. I doubt we should do that as often as you suggest, but making that a recurring thing is certainly an interesting idea!

DeleteCool! Make sure that the team talks about it at the beginning of the week so everyone can share they thoughts on what they think is important.



DeleteNot sure how any of you guys are working on the project (and if you have someone with enough time to set this up) but if you can start this "polish week" with some in-house testing (with outside testers) and have all the team check it out it can be really productive.

Some major breakthroughs happened on my last project when our programmers/artists had a chance to see people playing the game. Not to mention the natural motivation boost that comes with seeing your game being played.

Good luck, keep us posted ;)

We already have the meeting at the beginning of the project scheduled. :)


DeleteWe do so much testing with external people that we don't really need to set up extra testing. That is one reason why I don't care much for integrating QA specifically with the sprint: we invite people to play our work all the time already. :)

Another small note; one thing I remembered from Jeff Sutherlands (yes, he is one of those scrum purists) scrum workshop, is what he said about fixing bugs and having a dedicated bug fix sprint.

DeleteThe main thing was that the time involved in solving bugs went up exponentially after 48 hours of encountering those bugs (can't cite a source right now, my scrum books are at work..)

This has to do with reproducing bugs and familiarity with the code.

Totally bug free is really hard, and most likely impossible. The thing is to strive for is to bake quality in your process, like automate testing as well as some manual tests. As fixing bugs on issues 3 months later will cost you a lot more time than fixing it on the same day as you are still into the code etc. (or not at all and accumulating bigger and bigger technical debt).



DeleteThe discussion on "hardening Sprints" is an interesting one as it can be an easy trap to do it wrong but also very needed (a Sprint before a release to fix things rather than focusing on new features).

This article (http://swreflections.blogspot.de/2013/01/hardening-sprints-what-are-they-do-you.html ) shows arguments from both sides and pretty much hits home to your initial discussion as well with "[...] that a "potentially shippable product" and a system that is actually “shippable” or ready for production aren't the same thing." :)

Hi Joost,




ReplyDeletejust think of how easy it would be to release a game if you hadn't to go through implementing the console certification rules. That is what Scrum is all about: Whenever you think you found an example why Scrum is failing you, it is actually you failing to find and implement a solution. If you were able to get rid of this "big task" by cutting it smaller, automating it, renegotiating the exact terms with the console manufacturers - then you would be able to see why Scrum works.

Scrum is rigid to remind your brain to stay flexible.

Looking into Lean helped me when I was sure that Scrum sucks ;-) Check out http://www.amazon.com/exec/obidos/ASIN/0321896904/poppendieckco-20

Your answer is exactly why Scrum purists are a problem. You just ignore reality and wish for a better world where problems did not exist and Scrum could function perfectly.


DeleteConsole certification cannot be 'renegotiated'. It can be cut into smaller parts, but then you should still do it near the end of development because getting gameplay and tools running early is much more important.

Mhh... somehow I wasn't able to say what I meant to say. I'll try again, because I know how you feel - this article could have been written by me not long ago. First of all, I totally agree with you - saying that you should release a game that sucks because scrum says so is obviously utter bs. Regarding my earlier comment: I wasn't suggesting that you actually renegotiate anything. I was trying to show you why and where scrum is very, very helpful: It forces you to see the impediments you have and makes you address them. It does not deliver a solution to every (or any) problem, it let's you see the problems - the solution is still up to you. That's why I wouldn't say it is a tool for project management but for change of perspective. As "deliver fast" is your ultimate goal, seeing and removing impediments is the only way to achive this. And Scrum is very good at showing your impediments. So, if you look at Scrum this way, your question could be "Which Framework will let me see my impediments better than scrum", and my would answer: None (that I have seen).




DeleteAnd again, if you really are interested in finding a way to adapt Scrum or any other technique to your needs, look into lean. I only started liking scrum once I saw how very elegantly Scrum integrates lean and agile in a very short and precise framework.

PLEASE! ;-)

Interesting, I definitely didn't get that from your original reply. Thanks for taking the time to elaborate what you meant! :)




DeleteI agree that Scrum is great at making people work efficiently and goal-oriented, and that this gives a great focus on solving problems in certain ways.

At the same time, I do think Scrum does not force the mind to be 'flexible' in general: Scrum is a certain kind of hammer and it forces the mind to look at problems from the perspective of that specific hammer. I doubt that trying to write a book using Scrum would be a good idea, for example (an interesting experiment, though!). It is just that the particular kind of hammer that Scrum is, is really good for a lot of things, so looking at problems with the Scrum hammer is often a good idea. :)

Nevertheless, I think solving problems like console certification is above all a software engineering topic and not really all that related to Scrum.

Joost, before I reply once more, why not make this easier: as you are not far from us, maybe you want to come to Düsseldorf, Germany for a day and have a look at our company and have an open discussion with some devs/POs/SMs here? We are about 100 people here in the telco business with 7 scrum teams right now. We'd be happy to have you here!



DeleteTim

Thanks for the invitation! :) Düsseldorf is still a bit far fr a quick visit though... Also, game development is a very specific beast, as the cooperation with artists and game designers needs to be very tight and this shapes the workflow in many ways. The telco business is very different in this respect.

DeleteInteresting article, but though I am not a scrum purist I stopped when you started talking about certification requirements. Internally releasable is an acceptable benchmark for scrum.

ReplyDeleteI know that 'potentially shippable' should be interpreted in a more lenient way, but my point is that some of the scrum trainers I met said that release deadlines are no problem with Scrum because you can just release whatever you have at the point. That would only work if 'potentially shippable' were taken very literally.

DeleteI am a certified SCRUM master and I fully agree with this article. I have seen Scrum fall down on many levels specifically in game development. The reason being is because you are applying emperical methods to a creative process that has specific requirements and standards. Functionality does not equal fun, or for that matter, a complete gaming experience and Scrum makes no accounts for this.

ReplyDeleteThis is most common where big or "all or nothing" tasks come into play. Sometimes I call these vanity tasks, things like cinematics, voice overs, additional artwork. Sure I could breakdown a huge system like a branching logic narrative system into smaller pieces but if it is a huge part of your game identity, then axing it is not an option.

Not everything is meant to be completed in a two week sprint cycle. This works well with functional software that fills a very rigid end definition. If you are using Scrum on small free to play mobile games then this method is purely feasible because the only requirements are an MVP product that turns a profit but on larger projects that have very specific requirements as well as artistic elements involved, then Scrum falls down.

I like Scrum a lot but for high production value games with unique definitions of fun, you might as well pray, because neither relies on a very realistic premise. :)

Do you have any suggestions for how to tackle these things in game development, either with modifications to Scrum or with something else altogether? Any interesting things you tried to solve it that did or did not work? I suppose you didn't leave it at "you might as well pray"? ;)

DeleteJust a small hint regarding 'huge features': scrum preferes getting multiple smaller things done in a single sprint opposed to doing 50% of the work on a big feature.

DeleteIf you are having trouble on this part I would advice breaking that huge userstory into vertical slices instead of horizontal slices. http://goo.gl/5kT3O6

This way you deliver (multiple) working features each sprint opposed to a massive working feature after x sprints.

For "*feature* potentially shipable" of course you do not need to pass a certification test. The fail is in understanding Scrum here.

ReplyDeleteI know that 'potentially shippable' should be interpreted in a more lenient way, but my point is that some of the scrum trainers I met said that release deadlines are no problem with Scrum because you can just release whatever you have at the point. That would only work if 'potentially shippable' were taken very literally.

DeleteHoly shit this post turned a ScrumWar.


ReplyDeleteAlso, ScrumButt, hehe :)

With scrum, you should be able to publish the product outside of the dev team after every scrum. It doesn't mean you're able to sell it to the final clients. As you wrote in the example you needed to satisfy console requirements, that's a significant goal and you decided to postpone its implementation. Therefore you can not release the game to the public, but you surely can release it to testers or make a demo to some stakeholders.

ReplyDeleteThe simple answer to not delivering on time is not that Scrum is flawed, but rather poor release planning and estimating. This is an extremely difficult job to do, even for something fairly simple, let alone something as complex as a video game. However, it's not Scrum's failing, but rather the failing of dealing with anything sufficiently complex and changeable that accurate estimates are very difficult to come by. There's much too much that's unknown at the beginning and you make this clear in your post by saying that without sprints the requirements would change every day.

ReplyDeleteScrumstudy

“but Scrum is fundamentally flawed” - I would not agree to this statement. Scrum is not flawed since it is still a developing methodology, and there are several methods and ways in which it can be implemented. A product can be stated as “being flawed” once it is completely developed and presented to the market as such. Scrum does not state as being “perfect” – it is merely a “suggestion” which can prove to be helpful to you if you desire to implement it. I guess it also depends a lot upon how you use a particular development methodology as far as getting the desired results is concerned.

ReplyDeleteAre you familiar with Clinton Keith's Agile Game Development with Scrum? He talks about similar things as you, including using different flows & controls for different parts of the development effort.





ReplyDeleteAs a Scrum trainer (or rather, Agile trainer), I don't recognize your description as my Scrum. I have my purist side and it does not agree with your purist description. To me that is not pure Scrum. Then again, my pragmatist side asks "is there some particular special value to doing pure Scrum [answer is no, assuming it's the wrong thing to do]?" And "what is pure Scrum anyways?"

> Purists want you to believe that only pure Scrum works, but Scrum

> is fundamentally flawed and therefore not a full solution to project

> management

I would say this differently (unless my intent was to get inflamed responses, which it might), "Purists ..., but Scrum flow is not a complete project management solution, and it was never intended to be. The user of the framework is expected to fill in the blanks with other frameworks and practices they find necessary and useful in their environment. The doesn't make Scrum flawed, but it may be an incorrect choice for certain problems. Also, it doesn't work as intended if it's modified in wrong ways. But you don't get extra points for 'perfect Scrum' if you fail to achieve your goals." Or something like that.

Good luck with your great work! Thanks for writing the post (even if I didn't like the tone of it the most :) - but I think I understand your frustration).

If there is one thing that the replies to this blogpost have taught me (including yours), it is that "pure scrum" has many interpretations. My post was mostly aimed at the people who ran a Scrum training I visited and at the very purist texts at scrumbut.org, but it turns out that most people replying here are much more realistic about what Scrum does and about what it does not do. And of course the post was written a bit more aggressively than is needed because that sparks more discussion. :)


DeleteI actually bought Clinton Keith's book now, but have not read it yet. In practice at Ronimo we are gradually moving away from Scrum, so I am curious whether Keith's book will convince me we need more Scrum, or that my reasoning for moving away from it is good for how we like to work.

I've used scrum at two employers. At the first, we created what you refer to as Scrumbut (I call it hybrid scrum) -- basically the team leads/management/product owner would waste time in a room figuring out epics/stories/etc. Then as an entire team, we'd break out the tasks. Tasks were assigned to individuals, you do the tasks. During the next iteration, QA team tests what you built during the previous iteration. We do a "sprint review" when it makes sense. This approach worked VERY well. My current employer worships scrum proper to the letter. We waste hours upon hours in meaningless meetings, have a three hour sprint review after every sprint...even if it means painfully demoing installers, form layouts, other stupid trival crap. The software can not be shown in a review unless it is 100% done...this means if you have functionality in place that isn't finished, it must be removed (freaking waste of time...only to re-add it again during the next sprint)


ReplyDeleteOn top of this we are trying to train our QA folks to be software developers (many of whom have limited interest in such and do not have the technical grounding in algorithms and software design to build production code -- it's a complete nightmare)

Hybrid Scrum (Agile) has merit.. Scrum proper has shown itself to be a colossal waste of time IMO.

Thanks for sharing! I have never done full Scrum because all the extra meetings fell like such a waste of time, interesting to hear from someone who actually tried that.

DeleteI've worked in four different SCRUM environments, each worse than the last.


ReplyDeleteIn the present situation, it's more or less an excuse to cram the development of critical and complex funtionality into two weeks sprints. Wash, rinse, repeat. The developers are not allowed to talk to the product owners until they are forced to demo crappy implementations every other Thursday. And we have to take the grilling while the UX guy and BA roll their eyes and huff and puff.

Hi Joost,






ReplyDeleteThanks for this nice article. We figured out that standup meetings are great but needed improvement (they took a lot of time and de-focused our colleagues). Because of this we developed a SaaS tool to "automate" the daily standup meetings - with just a single email. If you like to take a look: www.30secondsmail.com.

Best,

Ajie

Project management methodologies are not for the benefit of the software developers, they are for the benefit of the project managers.






ReplyDeleteProject managers who do not see the benefit to Scrum (or Scrumbut or Scrumban, or any other agile-based methodology) will not use it.

Project managers who embrace Scrumbut are doing so because they find the variant of Scrum useful. As a project manager tool.

For the longest time, as an individual contributor, I had thought that the primary reason for Scrum was for my benefit. As a software engineer.

Once I realized that Scrum is a tool employed by-and-for the benefit of the project manager, then I realized when / why / where Scrum works, and when / why / where Scrum fails.

In that I, as a software engineer, find that Scrum is a productive methodology is a secondary concern, and just icing on the cake.

But it is just plain stupid to define a "potentially shippable" as conforming to all console certification rules. I don't who defined this like that in your team, but this is so stupid as to the point of being hilarious! The idea of scrum is to have something concrete, something finished at the end of the sprint, and that you should start with the thing that add most value! The certification rules ARE THE LAST THING you are going to do using scrum. Oh my god!

ReplyDeleteYou fail to mention one of the most important aspects of scrum, which is that the product owner is in charge of prioritizing the backlog. You may be developing for multiple consoles, the web, etc. Some of which may have no specification rules and some of which may have lenient specification rules and some of which may have strict specification rules. It is up to the product owner to prioritize tasks, since they are technically the voice of the customer. You also fail to realize the key word of "potentially" in "potentially shippable product". In other words, the product could work just fine without the specifications, so it is potentially shippable. It is not completely shippable until all specifications are met and the PO agrees to release.

ReplyDeleteMy point is that some Scrum masters claim that Scrum will make you achieve deadlines, but it won't. If the product is only "potentially shippable" on the final deadline, then you've failed the deadline as it needs to be truly shippable, including all required console certification requirements.


DeleteOf course, the replies to this post show that most Scrum users don't think Scrum guarantees making deadlines. My post however was in response to a Scrum workshop I did where the Scrum trainers claimed that with Scrum done right, we would meet our deadlines and always ship our games in time.

I have moved across various roles such as a Software developer, Programmer Analyst, Business Analyst, Project Manager and a Product Manager. I totally agree that SCRUM is not meant for robust, scalable, large, complex projects. For such projects as mentioned above SCRUM is a framework to fill GAPS (I'll say minor GAPS) in a project. SCRUM in my opinion will be best for resolving defects in an existing customized Vendor product/ application launched at your company. Or as a Vendor releasing a minor customized version of your Product/ application for a particular client. In both cases you function within the confines of the designed architecture and not build a product from scratch. If one is developing a complex application, can you imagine involving your high end ($/hr) business users or client in an endless saga of meetings to list EPICS and USER stories, and then ask them to tune in again after a period to provide acceptance criteria, and then assist in test cases. Why? because we think the NBT/ silver bullet is SCRUM.

ReplyDeleteI see a big flaw in your article where you state “Scrum is mostly know for the stand-up meetings and the blackboards full of post-its, which are both great concepts. “


ReplyDeleteThis tells me that in reality you do not know what Scrum is.

Scrum allows the team to self-organize, develop the most efficient way to deliver value to the end user without being told by management how to do it and take ownership of what they are working on.

Scrum is not about standups or scrum boards. Standups is the most efficient way to review if yesterday’s plan was achieved and plan new day worth of work. Scrum boards are the most efficient way for the team to track if they are moving in the right direction in finishing each story.

Sprints were created so that the team does not get caught in a spiraling work without seeing end in sight. It is meant to allow the team to break down the work into manageable pieces and finish each feature at a time.

Scrum allows everyone to see if the delivery date is in trouble months ahead of it, giving a choice to teams and management to make decisions that can correct the situation.

I have worked in highly complexed regulated industries (railroads) and we still ended up using Agile (Scrum/Kanban) as the best methodology.

What I see you describe shows that your company did not have good Scrum Masters and Agile coaches. Your story deliverables are defined in Definition of Done. If a team is awesome, it will include more things than a team that is younger. Nowhere does it say that complex certification needs to be done within a sprint. In fact, any work that is not done by the team is done outside of the sprint. The Scrum Team is only responsible for the work they ship. However, the team does need to take certification into their acceptance criteria. For example if you include automation testing or extra checks and balances that replicates certification, your product quality will improve and have a higher chance of certification to take place.

Agile purist is someone who focuses on the duration of meetings (planning, grooming, retro), shipping whole game in a sprint or asking team to be generalists from day one.

Agile realist is someone who keeps the key Scrum/Kanban pieces to sync in and then seeks how a team can improve them.