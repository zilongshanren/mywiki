---
title: Battle For Wesnoth and Open Source Design
url: https://www.gamedeveloper.com/audio/battle-for-wesnoth-and-open-source-design
author: Daniel Shumway
published: '2014-08-16'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Battle For Wesnoth and Open Source Design

An interview with members of the Battle For Wesnoth team about community involvement, organization, and Open Source design/development for games.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Reposted from [http://blog.latinforimagination.com/interview-with-battle-for-wesnoth-devs-open-source-design/](http://blog.latinforimagination.com/interview-with-battle-for-wesnoth-devs-open-source-design/)

The following is an edited transcript of an interview I conducted over IRC on February 12, 2014 with members of the[ Battle for Wesnoth](http://www.wesnoth.org/) community, including David White (Sirp_), the game's original creator. The following transcript has been both edited and reorganized for conciseness and readability purposes. The full, unedited log of the entire conversation is available online at [http://www.wesnoth.org/irclogs/2014/02/%23wesnoth.2014-02-12.log](http://www.wesnoth.org/irclogs/2014/02/%23wesnoth.2014-02-12.log)

## Initial Release and early development

danShumway: So, Wesnoth was originally designed by one person, I think by the name of White.

zookeeper: yes, david white

danShumway: Do you know at what point he originally released the game? I mean, was it a playable product, or did he propose the idea and some of the engine first?

zookeeper: ...it was released at some very early point, but as far as i know it was fully playable

shadowm: The 0.1 version I got hold of only had two playable scenarios IIRC.

danShumway: And I'm assuming only a couple of the eventual races?

zookeeper: i'm pretty sure it was just some elvish, human and orcish units at that point

danShumway: Was design mostly being done by White, or was there some type of community process to make those decisions?

galegosimpatico: There are some screens of the early versions. There you can see elven fighters and archers had almost the current stats.

danShumway: So not a huge amount has changed, I guess?

galegosimpatico: If you get deeper and build an old version, you can see human wizards have changed more. But talking about graphics and everything outside the core, it is obviously the impact of a larger contributor base.

danShumway: The core game seems to stay pretty consistent, but you guys still make decisions about other elements - the most recent features for planning moves springs to mind.

zookeeper: some of the very original features (like the game rules) have remained largely untouched, it's more like stuff being added than any core aspects being revised

## Community Structure

danShumway: Basically, what I'm trying to research is how Open Source communities avoid some of the steriotypical "designed by commitee" problems that seem at first glance like they *should* pop up in development.

tdk27: the key difference is between democratic development and collective development. OS software is developed collectively by volunteers, but (generally) not democratically voted on by said volunteers, so I can write all the patches I like to turn wesnoth into a deterministic real time game, but they'll just be rejected

danShumway: I think that makes sense. So the thought process is that you can get input from people, but you don't need to implement it?

galegosimpatico: I do not know, but I think that is exactly what Github promotes

danShumway: From a software perspective, I believe you're right. People fork projects, do some development, and then request they be merged back into upstream, I believe?

Sirp_: That happens with some software projects. It hasn't been common on Wesnoth.

zookeeper: we've only recently moved to git and github, and actual branching/forking has been very rare

danShumway: Do you typically work with a single core team of developers?

Sirp_: in Wesnoth usually somebody comes along and submits enough sensible patches and says enough reasonable things to make sure they are a decent developer and probably not crazy (or at least if they are crazy, the right kind of crazy) and then we give them source control write access

galegosimpatico: Older systems I have seen in other projects were about: 1. Join a team, and 2. Then ask for something that was published in the bugzilla, trac or whichever management system.

zookeeper: excluding summer of code, 90% of the time the process is 1) someone shows up who wants to contribute 2) that someone does some contributions which are deemed good 3) that someone gets commit access

danShumway: So you try to actually get to know what the contributions are/who they're from, as opposed to someone annonymous.

Sirp_: then once somebody has commit access, they can more or less work on what they want. We expect people to behave like adults though and listen for feedback on whether what they are doing works well.

danShumway: Do you coordinate a lot of that through IRC?

zookeeper: yes, #wesnoth-dev is where most day-to-day small-scale coordination goes on. more important stuff with a wider scale also gets talked about on the forums or mailing list.

danShumway: Do you feel that the process you use for managing code/engine development is similar to what you'd use for making design decisions?

Sirp_: it's quite similar. Usually code and engine development has a much smaller set of stakeholders though and so it makes it a little different.

## Community and Design

danShumway: Wesnoth seems like a fairly complete game, but let's say you decide to move an icon, or on a larger scale, add a new unit, or something. Is that something you'd talk to the rest of the community about before doing?

Sirp_: i.e. it's not common for more than a few people to have much interest in an area of code in the engine. While scores of people are likely interested in some game design decision. It's up to the developer whose implementing it.

Sirp_: if somebody wants to move an icon because they think it'd look better my recommended way of approaching it is to just do it, and then you'll naturally get feedback on whether others think it's a good idea or not. Different developers have had different approaches depending on what they're comfortable with, though.

Sirp_: It also depends on how much up-front investment you have to put in. If I think moving an icon is a good idea, it's easy to do. So I'll do it. Then I'll get feedback on it.

Sirp_: If I want to make some dramatic change that'll take 40 hours of work, I might want to get some feedback on if people think it's a good idea, since I wouldn'tw ant to put all that work in and then have to revert it later.

zookeeper: for larger changes, developers don't tend to specifically go looking for opinions of the playerbase at large (except maybe for some usability issues). if the rest of the developers don't heavily object then it's not likely to annoy the regular players either, and people rightly don't tend to make massive changes without having discussed it with other developers first.

## Mods and the Bicycle Rack Problem

galegosimpatico: Moreover there is the concept of the addon system, which makes a huge battlefield for candidate changes. I am (maybe wrongly) assuming Delfador and Mermen campaigns came from there.

galegosimpatico: Regarding units and races.

Sirp_: right, we encourage people to put experimental stuff on the add-on server so people can download and try it out

danShumway: That makes sense as well. Wesnoth is so extendable, you could make a change as a mod and get feedback before making any decisions.

galegosimpatico: For the system there is the development branch (1.9, 1.11, 1.13... and git head)

galegosimpatico: Sometimes the git head changes abruptly, but not to the point of causing brain damage.

shadowm: Pretty much every campaign added since 1.0 came from add-ons.

Sirp_: A lot of things suffer from the "bicycle rack problem" or whatever it's called. If you go and start a forum thread, "hey where should this icon go?" you'll get 30 different random opinions and likely poor quality feedback.

Sirp_: if you just go and do it you'll be more likely to get high quality feedback from people who actually care.

danShumway: Which is why modding makes so much sense. You can kind of in a weird way use mods as your patch requests.

zookeeper: well, sure but that only applies to content changes. the khalifate faction being a prime example

## Broader Design in Broader Communities

danShumway: How would you approach design in a context where you didn't have that luxury - ie a story driven game, or something that didn't have a lot of room for expansion? Would you still try to involve a larger community, or just get input from the core team?

galegosimpatico: There is always room for detail adding

shadowm: A larger community would be useful in that case for obtaining art assets, mostly.

zookeeper: i think you'd need to have a competent core team to get the game to a 1.0 stage; where the "story mode" or whatever is actually complete, and where further development would be expansion and improvement rather than finishing the WIP.

shadowm: And promotion.

galegosimpatico: 1.10 showed a great improvement in sea effects

zookeeper: it's pretty hard to say how you'd approach a situation like that, when it depends greatly on the people in your team

zookeeper: if you have no team then your best bet would be to invite people to join and then give them more or less free reign... if you have a team then it depends on what they're like, and obviously depends on the specifics of the game as well :p

danShumway: Do you think that most Open Source games take the same approach? I know the Nethack team was very secretive about their decisions inbetween releases, but many other projects seem to be very very open.

Sirp_: well, do note that Wesnoth started off as a single player campaign that had a storyline ... it was designed as a single player experience.

danShumway: I did not know that.

Sirp_: the expansion and so forth emerged later on; once others started expressing a desire to develop their own campaigns I added a plugin architecture to allow that

danShumway: I would not have guessed that, but it makes sense. The Wikipedia article said you were really interested in making the AI challenging with the original design?

Sirp_: Yes, I wanted to make an AI that was interesting to play against. So I designed a game that I felt an AI could play at least reasonably well. How successful I was in that is naturally a matter of debate. :p

## How do FOSS communities resolve debates?

Ivanovic: by the developers being selfish and just doing what they want to see included

danShumway: :) Fair enough.

Ivanovic: sometimes inspired by what players say but often also just ignoring the input - somehow similar to other areas in life

Ivanovic: Who "pays" for the result gets to decide what is being done, and payment can be in money for some contract or it can be in the time invested with "fame" being the only currency used.

Ivanovic: If it is the latter the projects are usually something the people enjoy themselves; either the way to the "goal" or the goal itself (to later on play it).

Sirp_: Ultimately Wesnoth is made by people who think it's fun, and they tend to optimize the experience for themselves. We hope others find it fun too.

danShumway: Do you think that lends itself well to certain games? - ie, things with high replayability, or games that allow for a lot of freedom within their gameplay?

Sirp_: Yes I think it lends itself much more heavily to games with more replayability

Sirp_: though it varies. I think when I first started on Wesnoth I thought back to gaming experiences I had as a 10 year old, and thought it would be enjoyable to try to recreate that kind of experience for some other people ...as well as for myself.

Ivanovic: I would answer it the other way around: there are games which are usually *not* created using this open source way

Ivanovic: Games which require lots of effort pulling in *exactly* on direction where everyone needs to closely colaborate and where the developers don't have too much freedom, e.g. games which are extremely and almost only centered around the story and dialogs like (classical) adventure games

Ivanovic: In fact i would say the open source model leads to games which are somehow modular where single persons are able to create some specific content block - that is the bulk of developers will more or less work on the engine which is then shared for possibly different content (c.f. campaigns in wesnoth)

Ivanovic: if you compared this to a single adventure game like monkey island it would probably just not work, there the "classic" open source part could just be the engine providing a basis for different "game modules"

danShumway: That makes sense as well - I'm trying to think of some of the really popular open source games, and the ones that spring to mind are Wesnoth, Nethack, 0 A.D.

Ivanovic: you could also look at games like tuxkart or world of padman - all are somehow similar in the end

danShumway: Yes, now that you mention it.

Ivanovic: there are exceptions like frogatto, but again just the engine is open source... ;)

## Additional Links and Resources

During the interview, shadowm provided me with a series of informal reviews he wrote back in 2010 of the first four Wesnoth releases. They're highly informative, go into way more detail than this interview, and are generally just a good read. I'd absolutely recommend checking them out. [http://shadowm.rewound.net/articles.php](http://shadowm.rewound.net/articles.php)