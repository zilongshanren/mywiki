---
title: 'Classic Postmortem: Guitar Hero'
url: https://www.gamedeveloper.com/audio/classic-postmortem-guitar-hero
author: Game Developer
published: '2015-11-08'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

This classic postmortem of the rhythm game that launched a million plastic guitar peripherals first appeared in the February 2006 issue of Game Developer magazine.

### HARMONIX MUSIC SYSTEMS WAS FOUNDED BY ALEX RIGOPULOS AND Eran Egozy in 1995. Alex and Eran met at the M.I.T. Media Lab, and their original goal was to use technology to allow non-musicians to experience the joy of playing music.

### This goal continues to drive all of our development efforts. Collectively, we believe that making music is one of the most exciting and satisfying experiences possible, but one that is denied to most people, given the time and commitment necessary to achieve proficiency on a musical instrument. We were convinced that if we could remove the technical impediments to musical performance, we could create a compelling experience for our audience and build a business around it.

### It took us a while to realize that video games would be the most effective platform to achieve this vision, but since we made that connection (triggered by our first look at PARAPPA THE RAPPER), we haven’t looked back.

Given this goal, our strategy has been to focus on music titles, beginning with FREQUENCY and AMPLITUDE on the PlayStation 2, and continuing with the KARAOKE REVOLUTION series on multiple platforms. (There was also a brief detour into EYETOY: ANTIGRAV, but that’s another story.) We learned valuable lessons from the development of each of these titles, and when GUITAR HERO showed up, we were well prepared to tackle it.

It wasn’t apparent to us until it was done and in the hands of the game-playing public, but GUITAR HERO is probably the most successful realization of the Harmonix vision to date. We’ve gotten tons of feedback from musicians and non-musicians alike about how much the game feels like actually playing rock guitar. In its most successful moments, GUITAR HERO crosses the line between gameplay and actual performance. This is a source of great pride to us, given our early conviction that we could achieve this goal and the amount of time and effort that it has taken to realize it in practice.

# FROM OUT OF NOWHERE

For Harmonix, the opportunity to create GUITAR HEROwas pretty unexpected. RedOctane approached us at exactly the moment we had a team available, and as soon as we put serious thought into it, we realized it was the game we had always wanted to make. We were given a modest budget and a short (nine months) development cycle to work with, but we were equipped with a mature codebase, a lot of relevant design experience, and a huge reservoir of passion and enthusiasm for the subject matter.

Project leader Greg LoPiccolo and audio lead Eric Brosius had played together in Tribe (bassist and guitarist, respectively), a prominent Boston rock band from the distant past. Art director Ryan Lesser had toured the U.S. playing guitar in The Laurels; game systems programmer Dan Schmidt is front man and rhythm guitarist for indie pop group Honest Bob and the Factory-to-Dealer Incentives; and producer Daniel Sussman is currently guitarist for the Acro-Brats, a Boston-based punk band. Many other team members previously had been or are currently in bands. Rock music is a big part of our lives and of the Harmonix company culture, and GUITAR HERO provided a perfect opportunity for us to celebrate and pay tribute to (not to mention poke fun at) the music we love.


# WHAT WENT RIGHT

## 1) STRONG CONSENSUS ON THEME.

When we started, it was important that the entire team had a unified vision of what this game would be about. Initially, RedOctane just inquired about the possibility of a guitar game. About 10 minutes into our first brainstorming session, we realized that it needed to be a rock guitar game. There was unanimous support for a no-holds-barred rock experience, something that could seep into every element of the game, from the music selection, to the art direction, to the HUD design. When confronted with any art or design question, it was great to be able to ask, “Does this rock?” and proceed accordingly. The entire team was committed to this vision, which gave us tremendous focus and saved a lot of time and debate. We also owe a big shout-out to RedOctane, who got the vision immediately and gave us plenty of space to realize it. They were involved in the big design calls, but they demonstrated a lot of faith in our team and let us make the game we wanted to make.

## 2) SOLID PRE-PRODUCTION MILESTONE.

We kicked off the first GUITAR HERO milestone in style, gathering all the leads together for an introduction to rock. Greg’s brother has a nice pad with a ceiling-mount projection TV and an enormous stereo. It was there that we met up to drink some beer and watch music videos. We spent about three hours watching live Led Zeppelin, AC/DC, Rolling Stones, and lots of other classic material. It sounds cheesy, but getting together and talking about how great Jimmy Page was or how much we loved or hated The Who really had a cohesive effect on the team. Finding out that we were all opinionated music snobs was awesome. From there, we went to work drawing up character and venue concepts and building a playable prototype. Having such a productive pre-production period was a big part of why GUITAR HEROwas successful. It’s amazing how much of the initial concept work made it into the final product.

## 3) STRONG PROTOTYPE.

We had the multitrack audio files for Weezer’s “Dope Nose” from AMPLITUDE and, because it has a guitar solo, we thought it would serve as a decent prototype. Game systems programmer Dan Schmidt wired up a simple 2D display with white lines scrolling down the screen. Then he added a basic scoring system, and all of a sudden everyone on the team was putting high scores up on the white board. Eric Brosius (audio lead) spent some time in his home studio working up some other songs (he did sound-alikes of “Walk This Way,” “Back in Black,” and “Ain’t Talkin’ ’Bout Love”) and we were hooked. The fact that GUITAR HERO was a compelling play experience very early on in development gave us a lot of confidence that we could make a successful title.

## 4) STRONG CODEBASE.

One reason we got GUITAR HERO up and running so quickly was that we were sitting on five years worth of well-architected and well-maintained music game code. We didn’t actually reuse any of the beatmatching code from prior titles, but lessons learned from those earlier efforts took a lot of the guesswork out of developing the gameplay core. The venue and character systems we developed for KARAOKE REVOLUTION provided a basis for the GUITAR HERO venue and character systems. There’s no way we could have completed GUITAR HERO in nine months without such an advanced and flexible game engine and codebase. Not only did it provide an excellent springboard for development, but it meant we could be flexible in development. We were able to prototype different game mechanics in days instead of weeks. We also had the luxury of drawing from the experience behind the code. We had already made several 3D rhythm-action games and were aware of some of the potential pitfalls.

## 5) GOOD GUITARS.

We knew going in that the title would stand or fall on the strength of the guitar peripheral, which made us extremely nervous, since we knew nothing whatsoever about peripheral development. To their great credit, RedOctane was able to design and manufacture a guitar peripheral that surpassed our expectations. Very early in the process, they asked us for our guitar feature wishlist. We asked for the tilt sensor and whammy bar well before we had any clear idea of how they would be used in the game. They responded that these features would significantly raise the manufacturing cost for the peripheral, to which we replied that we needed them, because they would kick ass, even though we couldn’t explain exactly how just yet. And they agreed to keep them. Thanks guys!

Harmonix worked with House of Moves for motion capture.

# WHAT WENT WRONG

## 1) NO GUITARS.

The development of the guitar controller started at the same time as the game. As a result, a lot of the game was developed on third-party guitar controllers that we could only find over the internet (and in short supply, at that). These controllers were pretty low-grade and we went through a ton of them; there’s still a pile of dead plastic guitars in our storage space. The third-party guitars had flaky buttons, no whammy bar, and a strum bar that only worked in one direction, which meant that there was a whole set of features we couldn’t test. And they were useless for difficulty tuning. We didn’t get our first controller prototype from RedOctane until a few days before E3. Even after that, they came in such small batches that we didn’t have enough guitars for every developer and were constantly running up and down the halls borrowing guitars from each other. We also felt pretty strongly that Q/A should be testing with the guitars as much as possible, which put a further strain on the guitar supply. Not having a healthy supply of guitar controllers made it tough for us to thoroughly test both the software and the hardware.

## 2) FREESTYLE MODE.

We were really excited about including a freestyle mode so players could assemble their own crazy solos with divebombs, feedback, finger-tapping, and all the other adolescent guitar showboating moves that we so dearly love. We poured a lot of precious development time and resources into this feature, and sadly, had to cut it. It was very ambitious and we simply didn’t have the time we needed to both make it sound good and integrate it into gameplay. Some of us feel that it was a gamble worth taking. Others aren’t so sure.

## 3) SCHEDULING OVERSIGHTS.

For the most part, we were successful in creating a complete and detailed schedule early in the project and sticking to it. However, there were a number of seemingly small and mundane features (such as the unlock store, the intro cut-scene, and the win sequence) that were either underspecified or didn’t make it into the schedule at all, and they added up to quite a bit of work. We got blindsided by this at the onset of beta, at which point we were still dropping lots of new content into the game. If the team hadn’t been so good, we would have been in serious trouble. This is a classic developer misstep, and one that we’ve made before. We thought we had learned our lessons and applied the necessary structure to avoid this problem, so it really stung when it cropped up again. As a result of this experience, Harmonix has now instituted a much more rigorous and detailed set of practices for producers and assistant producers, which apply to all of our projects.


We’ve since developed a detailed project-scheduling template for use in all Harmonix projects, with a checklist of generic features due at each milestone. Obviously, there’s a great deal of content and features which are unique to each title, but we’re now much less likely to overlook the mundane features that are common to all of our titles, and we have a much clearer set of guidelines for when in the project timeline such features should be complete (examples include memory card save/load system and icon, having win sequences designed and implemented, and so forth).

None of this is rocket science; they’re all features that are not that hard to implement, but if you overlook more than a few, you can get burned pretty badly if your team is on a tight schedule. None of us like working crunch hours, and although we haven’t been able to completely avoid them at Harmonix, we are constantly striving to keep them to a minimum. Crunch hours caused by poor planning are a mark of shame which we work hard to avoid. If we had planned for those features better and more completely, we could have implemented them more efficiently and possibly had more space for some of the features that were cut. Which leads us to:

## 4) WE HAD TO CUT STUFF.

Good stuff. Stuff like a practice mode that would let you select individual song sections and slow them down so that you could learn them. We did a lot of focus testing and learned that most players were able to pick the game up without much instruction. Based on this experience, we concluded that practice mode was somewhat expendable, though it’s a feature that a lot of players have been crying out for.

The need for feature cuts was partly dictated by our development philosophy. We had a very ambitious feature set at the beginning, with the knowledge that we might have to trim it as development progressed. We designed what we thought would be a full, deep game and then cut what we needed to in order to finish on time. We think we made the right calls, but some of those cuts really hurt.

## 5) NO AC/DC SONGS.

Booooo! Although we were very happy with our final song list, we couldn’t get all the songs and bands we wanted. We had a respectable song licensing budget, but there were acts that were beyond our financial reach or simply weren’t interested in participating. No need to list them; we all know who they are. Maybe in a sequel? We can always hope.

# GOT THE TIME

GUITAR HERO was a resounding win for us, and it wouldn’t have come together if we hadn’t been properly set up to make it in the time we did. Game projects at Harmonix usually have short development schedules and lots of design mystery, which can be a challenging set of issues to manage effectively. We have evolved some tactics over the last few years to survive in this environment, and they served us well on GUITAR HERO. A few key tactics worth mentioning:

Low barriers to communication between all disciplines and all levels of management, coupled with aggressive attempts to facilitate communication. Anyone can talk to anyone else about anything, in newsgroups, in meetings, or over lunch. It’s understood that everyone on the team is responsible for the total experience, no matter what their role is. Lots of suggestions and complaints are made, most get rejected, but the good stuff usually ends up in the game.

Large, professional in-house Q/A team. We generally don’t have time to rely overly on publisher Q/A. We need quick turnaround on new builds, and instant communication between the developers and Q/A staff to identify and address issues as fast as possible. We usually assume from the onset of any project that we are going to do the bulk of Q/A in-house. We try to empower our Q/A teams to participate actively in the design process and to be the conscience of their projects. At this point, we couldn’t imagine making games without having the Q/A teams integrated this way.

Early prototyping, with lots of review and iteration cycles. At the onset of development, completed design docs are not always very useful to us, as we’re not yet sure what will be fun. A perfect case in point for GUITAR HERO was the integration of Star Power and the whammy bar. We tried a number of different modulation effects and gameplay roles before settling on the shipped design. In retrospect, it seems like an obvious implementation, but it wasn’t obvious to us beforehand. It took several months of constant experimentation and revision before we settled on the final design.

Because of the compressed development cycle, we had to be merciless about keeping our project scope under control. This was made easier by our shared conviction (learned the hard way on previous titles) that if development resources are limited, it is crucial to focus on the core experience and eliminate resource expenditure on anything that’s peripheral to the core. Even so, it was somewhat of a white-knuckle ride down the home stretch. We burned time on some features that didn’t work out, we cut some features that we wished we didn’t have to, but the rock’n’roll experience we were hoping for survived pretty much intact.

## KNOCK ’EM DEAD, KID

We on the GUITAR HERO team are all somewhat astonished that we actually got paid to make this game. Scary moments notwithstanding, it was pure fun from beginning to end. Since the launch, it has been gratifying and shocking to discover how many people (including many who are way out of our core demographic) share our juvenile dreams of rock glory. It really doesn’t make much sense that a little plastic guitar should make you feel like such a badass, but somehow, it does. We learned some surprising things about fun, passion, and suspension of disbelief while working on this game, and we can’t wait to apply those lessons to our next title. Hint: It won’t feature white belts or guitars above the waist. *