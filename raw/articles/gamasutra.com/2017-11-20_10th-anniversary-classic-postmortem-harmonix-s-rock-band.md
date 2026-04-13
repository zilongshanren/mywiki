---
title: '10th Anniversary Classic Postmortem: Harmonix''s Rock Band'
url: https://www.gamedeveloper.com/audio/10th-anniversary-classic-postmortem-harmonix-s-i-rock-band-i-
author: Rob Kay
published: '2017-11-20'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

When Harmonix’s Rock Band launched ten years ago on this date, it was the culmination of one of the hottest gaming trends of the decade. It involved designing four new peripherals as well as an ambitious multiplayer rhythm game with an iTunes-like online store.

To celebrate its 10th anniversary, we present this postmortem, which first ran in the May 2008 issue of Game Developer Magazine. It was written by [Rob Kay](https://twitter.com/robkaysf), who was then the director of design at Harmonix, with contributions from Eran Egozy, VP engineering, Ryan Lesser, art director, Dan Teasdale, senior designer, Tracy RosenthalNewsom, director of production, Daniel Sussman, director of hardware development, and Greg LoPiccolo, VP of product development.

THE STORY OF ROCK BAND’S BIRTH, AND the transformation we’ve gone through as a company to create it, is a tale that an accomplished writer will someday pen, but for now you’ve got me. I was the lead designer on Rock Band. Working with our senior management to capture their vision for this game, I did wonder if they’d lost their minds. Their vision was simple: create a music game that takes instrument simulation to its logical conclusion—getting a full band together.

The intimidating reality the team faced was that this wonderful vision entailed an enormous workload. The drumming component gameplay of Rock Band would need to be built from a standing start. Guitar, bass guitar, and singing gameplay would have to be refined to work in a band setting. Finally, and crucially, we had to develop new cooperative multiplayer gameplay to tie drums, vocals, guitar and bass components together into one cohesive Rock Band experience.

In short, we strove to create the ultimate party game. But it didn’t end there. The vision included customization features to give bands their own identity, a world to tour, and enough depth to keep bands playing for months. Add in unparalleled DLC that would transform the game into a music platform, and it was one tantalizing package. Of course, then we had to make it!

The team would eventually grow to around 160 people at Harmonix, and countless contractors elsewhere, but it all began with three people making a drum prototype at the tail end of 2005.

# WHAT WENT RIGHT

# 1) PROTOTYPED DRUMS EARLY

We got our drumming prototype up and running before doing anything else. This afforded us time to understand the unique hardware needs, interface challenges, and learning ramp inherent in learning to play the drums.

As with all instruments in Rock Band, we wanted something that captured the feel of playing the real thing. We threw around various ideas for the basic form factor, and as our prototype hardware was configurable, we were also able to experiment with different pad layouts before settling on four pads and a kick pedal. We connected this to our PC-based prototype software, gave the drum setup its own room, and encouraged people around the company to come play it and let us know what they thought.

This drum prototype taught us a great deal. Crucially, it revealed an interesting drum-centric problem with our Harmonix 3D interface concept. Our usual row of note lanes (as seen in many of our games, including Frequency, Amplitude, and Guitar Hero) worked fine for the drum pads but failed spectacularly on the kick drum pedal.

The spatial organization of notes on screen didn’t match the spatial relationship of the pads and pedal. This made readability of note patterns exceptionally tricky. Through a combination of theorizing and experimentation, we arrived at the solution seen in the final game—an orange line stretching across the whole track. We’re proud of this solution, and how early we nailed it considering how many other challenges lay ahead.

Perhaps the greatest discovery of this drum prototype was simply how fun it was to play. It really captured the feel and power of real drumming, which gave us a huge confidence boost.

# 2) DEVELOPED THE HARDWARE AND SOFTWARE IN TANDEM

We began Rock Band as a software developer, but decided to take on the task of designing and manufacturing the hardware ourselves. Designing the controllers from scratch—and starting up a major manufacturing effort in under a year—was an enormous undertaking with a considerable learning curve.


The payoff though was more than worth it. For a game like Rock Band, the hardware is at least as important as the software, if not more. We were able to design and develop the hardware and software together, taking full control over the user experience.

We began hardware development in February 2006, working with an industrial designer (J. Hayes Industrial Design) and a contract manufacturer (Canyon Creations). Because it was the least understood controller, we attacked the drums first. The big challenge was delivering the playing experience of a real drum kit, in a videogame controller that would cost a fraction of the price. The guitar controller was less blue sky, and development started after we had the basics of the drum controller down.

Hardware was a brave new world to us. Throughout the whole eighteen-month project cycle, we made mistakes (see "What Went Wrong") but tried to focus on understanding the critical decisions and making the right calls. In April 2007 we began tooling for both drums and guitar (cutting the steel molds that shape the plastic parts).

The molds take about eight weeks to complete, and then you have at least another four weeks of preproduction and tuning. In September 2007 our first containers left the China warehouse. By January 2008 over two million Rock Band bundles had shipped.

![](../../assets/c11e36cd1b5d3fbd.img)


# 3) CAPTURED THE FEELING OF PLAYING IN A BAND

The biggest design challenge for Rock Band’s gameplay became all too obvious the moment we got our first version of a four-player game up and running. It was not a stellar group experience. Obviously, something key was missing—player interaction! There was no reason to care how other players were doing, let alone any of the interactions musicians in a real band might recognize. This cooperative multiplayer game mode was to be Rock Band’s reason for being, so it had to become amazing.


Enter the Harmonix Design Cabal, a mix of wily Harmonix vets and senior designers. This group identified some experiential goals for the gameplay team to go after. The experiential goals were “togetherness” and “distinct roles.” The gameplay team (three game coders, two UI artists, the audio lead, and myself) experimented for many months with gameplay mechanics and UI that met these goals.

We were scheduled loosely with three days a week set aside for iteration time. Each week, we’d meet with the cabal and review progress, which gave us enough freedom to react quickly and experiment, but also enough direction to stop us veering off course. We experimented with many scoring systems and gameplay mechanics to try and meet the high level goals. The whole company played this evolving game, and offered feedback and ideas, which fed into the process on numerous occasions.

Many experiments were failures, but taught us something valuable. Some worked well with four players, but fell apart with two or three. Some were diamonds in the rough, which we kept and revised and eventually honed into a cohesive whole. This was the process that birthed all of the unique Rock Band gameplay including individual fail outs, saving fallen band-mates, Unison Bonuses, Bass Grooves, Guitar Solos, Drum Fills, and Big Rock Endings. Together these features formed the “band” in Rock Band.

![](../../assets/237214ce43a1a69c.img)


# 4) EMBRACED “AUTHENTICITY” AS A GUIDING PRINCIPLE

Very early on we knew our songs would encompass all forms of rock music, and that players would be choosing their own look in the character creator. We needed a way to approach the visual presentation that was generic enough to host any sub-genre of rock, and yet still offer a distinctive look and feel.


We focused on an authentic recreation of traditional rock & roll, with serious attention to detail and high production values. Character animation was motion captured from performing musicians who played in bands of a particular sub-genre rather than actors (we got punk rockers to do the punk rock mo-cap, for instance).

Clothing was labored over, with shops representing each sub-genre. Instruments were recreations of the real thing. The camera work and post-processing was tailored to present the live show through the lens of a music video. The lighting mimicked real rock show lighting as closely as possible. We even went so far as to create a custom animation system for the drummer so that every single drum hit is realistically played on the right drum or cymbal!

The litmus test “is it authentic?” began as an art direction, but quickly spread project wide. “Authenticity” became a buzzword in not only art reviews, but also design, hardware, music and writing discussions. The music had to be authentic, so we secured as many master tracks as possible. The guitar hardware had to be authentic so we worked with Fender to create a replica of their iconic Stratocaster guitar. It spread through our collective conscience; everyone heard the “authenticity” mantra and got behind it, unifying the overall presentation and vibe of the game.

![](../../assets/d639b9a22e70bc44.img)


# 5) MADE GOOD EARLY CALLS ON NETWORKING TECH

We made some key technical decisions about our approach to networking early on that really paid off.


We chose to use Quazal instead of making do with the network solution provided by the platforms alone. This decision had to be made far earlier than when our network features were fully designed. As it turned out, the flexibility afforded by Quazal far outweighed the additional complexity of integrating another middleware provider.

We came out with an awesome feature set that was custom crafted for our game, including head-to-head battles, online band play, a flexible leaderboard system that can hold thousands of boards, and persistent band data storage. We were also able to create a common code base for both Xbox 360 and PlayStation 3, which helped reduce development time and kept platform differences to a minimum.

We also decided to conduct extensive network bot testing for our online solution before release. We spent months developing a tool that simulates realistic network traffic and user behaviors.

We rented time on a huge supercomputer system with a 2 gigabit Internet connection and proceeded to attack the servers with complex scenarios simulating over 100,000 concurrent users. These tests uncovered piles of bugs and helped us make tons of client and server optimizations. The result: when we went live, everything worked! We had hardly a hitch and things continued to run smoothly, even into Christmas Day (which saw the largest number of simultaneous users online to date).

![](../../assets/7ffece4b08c9fd1e.img)


# SIDEBAR: Weekly DLC and Music Store

From day one, we hoped Rock Band would become a fledgling music platform as well as a game. Our weekly song releases, generally two dollars a song with discounts for song packs, have proved incredibly popular, surpassing our expectations. We passed 2.5 million song purchases in our first two months alone, and the biggest seller so far has been the Metallica Pack.

Since launch, a Music Store has been added to the game via a free software update. We wanted to get this into the shipped game, but simply ran out of time. The UI has been designed to handle the sheer volume of DLC we’re making available, and improve the experience of browsing new songs (via things like cover art, audio previews, and difficulty ratings).

We’ve invested a huge amount of time and resources to make weekly DLC and the Music Store possible. It’s been well worth it though, and we’ll continue to develop this approach because we believe it’s the future of music gaming. Not only do game consoles now have hard drives and broadband Internet connections, but also our players seem to have an insatiable appetite for more music.



# WHAT WENT WRONG

# 1) DIDN’T GO TO CHINA EARLY ENOUGH

With 20/20 hindsight, we clearly should have made an effort much earlier in our cycle to understand our hardware manufacturing partners. It is so critical that all the people building your game have a true understanding of that game, of the people who will be playing the game, and of the initial design intent of every feature. Good hardware specs are incredibly important but they only go so far, especially in areas involving the subtleties of feel. Also, the language and time difference (China is a full 12 hours ahead) need to be considered when dealing with Asian manufacturing.

In the early stages of our development, we sent just our industrial designer and our manufacturing agent to China to represent Harmonix. It wasn’t until March 2007 that a full-time Harmonix employee made their first trip. After that first trip, it became clear that we had to have people on the ground there. From June through September, we had a team there basically full time and that was a critical part of our success. Had we sent people there earlier, we wouldn’t have needed the intensive 3-month grind that it took to get our drums and guitars on boats.

![](../../assets/9fead25035b9a8f3.img)


# 2) DIDN’T HIRE AGGRESSIVELY ENOUGH

From the outset, it was clear this was the biggest game we’d ever made. The inherent scope of the project was such that it couldn’t be significantly scaled back. For competitive reasons, missing our November launch wasn’t an option either. The only way to complete the title on time was to grow the team. We put most of our staff onto the game, and expanded the organization to new levels. Our offices were bursting at the seams. With staff spread across three floors, and no room left for the new hires we needed to finish the game, we bit the bullet and moved the entire company to a larger space midway through Alpha.

Despite all of this, we still didn’t hire aggressively enough. Many years making small, tightly focused games had ingrained an efficiency bias and “smaller is better” mentality that was hard to shake. We were afraid of the additional management required to hire more people, and it resulted in a longer harder crunch for all of us.

Things became most acute on the code team, with pretty much everyone working insane hours to complete the game. For a while in alpha, we fooled ourselves into thinking it was too late to integrate any new hires. Yet when things got really hairy in beta, and we looked dangerously close to slipping, we did just that. The coders we added in the eleventh hour were an essential part of the collective push to finish in time for a Thanksgiving launch. It would have made our lives much easier if we’d made those hires months earlier.

![](../../assets/eda1f78f767c3411.img)


# 3) LACKED SENIOR BANDWIDTH

This beast of a game ate up senior bandwidth like no other we’d worked on. We assembled a huge team of leads and sub-leads. Every Monday morning we’d meet and fill a large conference room. This senior powerhouse drove the game forward, but was seriously overworked. Our own internal postmortem revealed that in too many cases these people, who included senior management, had been doing the job of two people each.

Had we realized this during the game’s development we could have done something about it, but ironically it’s precisely because all of us were so busy that we didn’t truly realize how widespread the problem was. Each lead was so busy working with their team to keep their goals on track that collectively we just didn’t make enough time to assess the bigger picture.

Our senior figures and team leads often provide the best design insights, and have been instrumental in crafting our earlier games. But they can only do this if they’re playing the game regularly, and because of the huge demands on their time this was a real challenge. We plugged them into weekly play sessions, and numerous internal playtests to gain their design insights, but still big swathes of the game didn’t get the relentless internal examination they deserved. I’m not convinced that many people outside of Q/A played some of the less mainline game modes like Bass Guitar Tug of War, or online Vocal Score Duel for example. They just didn’t have the time.

# 4) STRUGGLED TO DEAL WITH MULTIPLE UNIQUE CONTROLLERS

We knew going into Rock Band development that one of the challenges we’d have to overcome would be getting three different controller experiences working in one game, but we underestimated how entrenched the single controller type mindset is with console manufacturers and certification, and how much that would impact our own plans for shell flow and online play.

The concepts of an “active controller” and “profiles attached to controllers” work great when you have one type of controller that you want a player to stick with (like a joypad), but work horribly when you have multiple profiles signed into multiple controllers that have different functions (like a drum kit, guitar, and microphone). Since there’s no need to swap controller types in most games to be able to play all areas of the game, there is no functionality on the system level to swap profiles between controllers, or allow one controller to use another profile’s data.

Systems like online matchmaking and invites complicate this even more—inviting is simple on a single controller, but on a multi-peripheral game it raises issues like “what if there is already a drum player in the session?” and “what if I want to play guitar, but my vocal controller is signed in? Can I sign out and sign in without leaving the session?”

For months, we struggled to reconcile our multiple controller types reality with first party certification requirements and system architecture designed for ‘one controller type at a time’ games. As we engaged in the technical and certification challenges with these systems, all essential to solve, it left very little time to properly test and refine usability. We ended up releasing something that functioned and passed certification, but it could certainly have been friendlier.

# 5) DIDN’T DO ENOUGH TECH DESIGN

Historically, we’ve managed without much formal technical design documentation. This approach, or rather the lack of lack of one, probably sufficed in the past because our programmers were actually superstar designer-programmer hybrids who considered both technical and design impact as a matter of course.

Expanding our code department for Rock Band meant bringing in new programmers who were very talented but weren’t all designer-programmer hybrids, or if they were didn’t know they were allowed to be. Too often we jumped headlong into implementation of a new system without taking the time to properly examine the implications or test the edge cases of the design. This bit us in a few areas, notably online matchmaking, which had to be redesigned multiple times.

No doubt about it, jumping into development of complex new systems without a technical plan upfront was a flat out mistake. We’ve now formalized our design process to include code review and a technical design document before implementation of a new system begins.

# THANK YOU AND GOOD NIGHT!

Rock Band was a unique project, with challenges that transformed us as an organization and worked us incredibly hard, but it was an absolute joy to work on. The victories that keep spirits high came thick and fast.

Working on a game with so many firsts was incredibly exciting. Our staff was set out early: this was to be the most ambitious music game ever made, and the spirit of confident innovation was rampant. Rock Band is full of features and moments that were born of a team committed to pushing the quality bar as high as possible.

Things like the crowd singing along when you’re performing really well, the Band World Tour’s open ended play, and the Art Maker tool (that allows you to, among other things, design your own tattoos) would not have made it into the game if the talented people who made them weren’t so utterly committed to making the game shine.

Seeing the drumming gameplay of Rock Band come to life, and realizing how close it is to real drumming has been a definite highlight of the project. We spent a long time breaking down the skills that absolute beginners learn to become competent drummers, and applying that to our note authoring and difficulty tuning. Taking people with zero musical experience, and watching them gradually learn how to drum on Rock Band may well be the closest we’ve come yet to realizing the Harmonix mission: To bring the joy of making music to everyone.

Throughout development and since release, the universal appeal of Rock Band has hit home on numerous occasions. The fantasy of being a rock star is one that all of us harbor, and music reaches us on an emotional level that’s almost impossible to explain. It has to be felt, and this is what video games do so wonderfully.

It’s been a particular joy to see children playing with their parents, guys playing with their girlfriends, first-time gamers playing with life-long gamers, and friends playing with strangers. Cooperative multiplayer games are rare, and multiperipheral games even rarer. In Rock Band though, it’s hard to imagine it any other way.