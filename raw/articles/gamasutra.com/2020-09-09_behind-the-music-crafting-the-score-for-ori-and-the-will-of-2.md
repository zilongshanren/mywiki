---
title: 'Behind the music: Crafting the score for Ori and the Will of the Wisps - Part
  2'
url: https://www.gamedeveloper.com/audio/behind-the-music-crafting-the-score-for-ori-and-the-will-of-the-wisps---part-2
author: Chris Kerr
published: '2020-09-09'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Behind the music: Crafting the score for Ori and the Will of the Wisps - Part 2

Speaking to us during aÂ Q&A, composer Gareth Coker explained how he crafted the score to Ori and The Will of the Wisps. This is the second half of an incredibly detailed two-parter filled with tales and tidbits from the world of game audio.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

This is the second part of our full, unedited Q&A with Ori and the Will of the Wisps composer Gareth Coker. [You can find part one here](https://www.gamasutra.com/blogs/ChrisKerr/20200909/369567/Behind_the_music_Crafting_the_score_for_Ori_and_the_Will_of_the_Wisps__Part_1.php).

Gamasutra: Could you talk a bit how your score was actually implemented. What technical considerations did you have to keep in mind when composing? For example, how did you work with the audio and animation teams to craft a cohesive cutscene? Did you ever have to rework tracks to fit a scene?

Gareth: I finally get to talk about my hero on the project, [Guy Whitmore](https://en.wikipedia.org/wiki/Guy_Whitmore), without whom I’d be very much not having all of the things I’ve described in the previous question! Guy is not only an audio implementer but a composer too, so it was great to be able to communicate with someone who would be able to get exactly where I was coming from with not just my musical ideas but also thoughts on implementation.

While it was my choice and design where and how the music is played in the game, the actual technical nuts and bolts of making it playback in the game, I did precisely none of that! That was all Guy. I am not a composer who likes to get lost in [Unity](https://unity.com/) and [Wwise](https://www.audiokinetic.com/products/wwise/). I prefer to create content and think about it’s role in the game. But, I do understand how to communicate with the people who do have the task of getting my music to play in the game. I provided Guy with my gameplay videos with music overlaid on top, and captions of what music track I wanted to play, and where each musical shift/switch was. I’d also provide a PDF that went into more detail on what was happening in the video. This combination usually gave Guy no doubt in to how the music should be implemented and if my explanation was unsatisfactory, I was a Skype window away. Between all of this and the cue sheet, we made sure that enough information was readily available to keep track of all the cues.

![](../../assets/82e20dd9b9b78149.img)


Example of master cue sheet tracking on Will of the Wisps

Guy implemented every single musical cue, stinger and transition in the game. The flow of one music cue into another was executed by him based on my own design. I can’t thank him enough for what he did with the very large amount of music he was given to implement.

I’d like to give a major shout out to all of those hard workers who are implementing music on behalf of composers. Quite literally, our work cannot be heard without you.

As for the cutscenes, it’s a wonderful and highly unusual process (at least in my experience) where there is extensive back and forth before we reach something that is time-locked. I generally work to storyboards at first to produce a piece of music that I feel is well-paced.

![](../../assets/a528340838796ae2.img)


Example of a shot from a rough video that I work with that is mocked up quickly(left), to final (right).

Then the animation team animates something that is based on the storyboards but more tightly timed to my musical peaks and valleys. It then goes back and forth to tighten timings a bit more, but overall if the cue is conceptually right from the beginning then the changes are very minor. On most projects I’m writing music to locked or close-to-locked picture when it comes to cutscenes, which is absolutely fine, but with Ori, maybe because a lot of the cutscenes are so dependent on music and animation working in harmony, the approach is super collaborative and I get to focus on just writing a piece of music that feels good, and not be restricted by an arbitrary timing. It’s a rare luxury for sure but I enjoy it while it lasts!

As for reworks, I’ve already mentioned the rewrite of the prologue, but there were several other scenes which weren’t hitting quite right. We were extremely fortunate to be able to split our recording sessions between December 2019 and January 2020. That January session allowed us to fix any issues that came up from the December 2019 recordings. It was less that there were issues with the recording, but there were some timing changes that happened in scenes that couldn’t be solved by simple music editing, so we were able to re-record. Two scenes in particular stand out, one at the end of Act One which I won’t showcase for spoiler reasons, but also the end of the prologue (a rewrite of a rewrite!), Ku’s First Flight.

I don’t mind reworking scenes, it happens and you just have to get on with it as it’s part of the job. It’s all in service of trying to do your best for the game.

Gamasutra: Carrying that thread, what was the biggest challenge you encountered during production from a technical point of view?

There are two things that stand out. The first being the implementation itself. Due to the horizontal nature of how the music plays back and switches in the game, the fact that there are so many individual music cues, and the game is a Metroidvania so players can trigger different game states in different orders, it took quite some time to figure out the technical aspect of getting the right cues to playback at the right moments and most importantly make sure the game was tracking the correct game state. This was especially the case where several cues played within the same Unity scenes - a particular issue with backtracking later on in the game and revisiting areas.. The only way to overcome it was with extensive testing of the game to make sure the music was playing back as I expected. Guy was also implementing and creating ambiences for the game too so he already had an incredible workload, thus I did everything I possibly could to give him as much information as possible to fix music-related playback issues. Thankfully [Formosa Group](http://formosagroup.com/interactive/), who took care of the audio on the entire project - led by Kris Larsson - also had several people on their team play the game too that were able to pick up on these things and make sure it was all logged.

The second one is more personal, and it was the schedule changes. Everyone knows that the game was delayed several times and this mostly affected our recording dates. Looking back, we should have recorded the soundtrack in a more modular way with several recording sessions spread over a longer period of time. But the way things were planned and the way the game was being developed, a lot of the final music decisions were left a lot later, and as a result we had the recording sessions as late as possible into development. But ‘late as possible’ shifted each time the ship date got moved, and it became a logistical challenge to get things set up over and over. So many people are involved in the production of a soundtrack, it’s not just the composer, it’s the orchestrators, engineers, copyists, librarians, conductors, studio support crew, and of course the players! They all have to be booked (and then rebooked). Thankfully, a contractor can always take care of this for you, but it’s still something that has to be worked into the thought process as a composer. Additionally the soloists on the soundtrack: Aeralie Brighton, Kelsey Mira, and Kristin Naigus were always ready and willing to record whenever I needed them!

A key aspect of having a fixed date for the recordings means it gives me a target I can work towards. I like to press the accelerate pedal harder and harder as we get closer to that date, aiming to peak a few weeks before, but it’s obviously hard to figure out where that peak is when the schedule changes!

That said though, the delays helped us ship a game that people seemed to love, so I have no regrets. I was able to overcome it thanks to my brilliant team of people that help me get my recordings over the line. [Alexander Rudd](https://en.wikipedia.org/wiki/Alexander_Rudd) and [Zach Lemmon](http://www.zachlemmon.com/) in particular, who I went to school with and excellent composers in their own right, we have worked together on every single one of my projects and they make the stress of a recording session so much easier. The team overall allowed me to focus on just writing and finishing the music and focusing on the game while they got through all the orchestration (a mammoth task completed by [David Peacock](http://www.daviddpeacock.com/), [Eric Buchholz](http://www.ericbuchholz.com/), and overseen by Zach) and music preparation assignments in order to make sure that the music would be ready to record on the stage.

![](../../assets/18c5e717ea320496.img)


Recording crew on Ori and the Will of the Wisps. Front row: David Peacock (orchestrator), Jessica Kelly (score co-ordinator), Alexander Rudd (conductor), Gareth Coker (composer), Zach Lemmon (supervising orchestrator), Jake Jackson (engineer), Cassandra Brooksbank (film crew and closest friend!). Back row: Steve Kempster (engineer), Allan Wilson (librarian and copyist), Gianluca Massimo (assistant engineer), Alex Ferguson (recordist), Ashley Andrew-Jones (assistant engineer), Dakota Adney (film crew).

Gamasutra: What did your studio setup look like on Will of the Wisps? Were there any specific tools, software, and equipment you relied on to shape the score? (Some behind-the-scenes shots would be great!)

Gareth: My personal studio is fairly simplistic in terms of how it looks, but the power is all under the hood. I’m a bit of a computer nut and I’m always on the hunt for the latest parts and I’m unreasonably excited to build a new workstation at the end of this year! I’ve just purchased a 32TB SSD which was advertised first on LinusTechTips and uses the PCIE 4.0 interface to deliver insane bandwidth. One of the things I’m constantly looking to reduce is loading times which is something that all composers working with large virtual orchestras have to deal with, I’m looking forward to seeing how this drive performs. However, that’s the future setup, the current setup is an 18-core processor, 128 GB of RAM, with my orchestral samples spread out over 7 different SSDs, 2 of which are M.2 drives, the remaining 5 being Samsung 860 EVOs. There’s a system drive on M.2 and a project drive which is on another EVO. I always buy the latest and greatest graphics card because it helps me when I’m playing games I’m working on that aren’t optimized! (And yes, it does make my downtime playing other games fun playing with high settings!). I monitor my work on Genelec speakers but honestly I do most of my actual writing on headphones. The biggest asset in my room is honestly it’s acoustic treatment which was done by [GIK Acoustics](https://www.gikacoustics.com/). They did a great job in tailoring this room with appropriate treatment and it’s helped a lot to make sure I can trust in what I’m listening to.

The software I used to write the music for the project was a mix of [Reaper](https://www.reaper.fm/) and [Cakewalk](http://www.cakewalk.com/). Blind Forest was written in Cakewalk so for legacy reasons I kept it around to access the old project files, but I’ve gradually moved over to a highly customized version of Reaper. Notation is all done in [Sibelius](https://www.avid.com/sibelius) notation software though I’m eyeing up [Dorico](https://new.steinberg.net/dorico/) as a potential alternative. The amount of score printed out for this gargantuan soundtrack was quite a sight to see all in person at the studio!

![](../../assets/b527e500093c9367.img)


Stacks of music…! (Nowhere near all of it)

A couple of technical things on the music side that I was particularly excited to utilize on the project were being able to create custom samples for the score. I did this both myself but also commissioned a sound design team to make some bespoke Ori sounds. The company, [Slate & Ash](https://slateandash.com/), had produced work on Arrival, Into the Spiderverse, amongst others and I had been familiar with their sound design work for a while. I contacted them and I’m fortunate that they agreed to work with me and they made some particularly appealing sounds for the project and built a software instrument for me to playback those sounds.

![](../../assets/184df8af9a4826c7.img)


A custom Slate & Ash patch made for playback in Native Instruments Kontakt.

As for custom samples, I had woodwind player extraordinaire [Kristin Naigus](http://field-of-reeds.net/) record 951 different woodwind samples for the project. Some of which I’d written out, but some which she’d improvise based on my written ideas. She played these ideas across several different wind instruments, the alto whistle, bansuri, fujara, quena, quenacho and shinobue. They all have subtly different characteristics. We used these samples to create various pad sounds in the score, but also they are used in stingers in the game, and various musical flourishes or transitional moments. Often a composer might use a cymbal roll to flourish from one music section into another, but on Ori, more often than not we used a woodwind flourish instead. That’s all Kristin. She not only provided these samples, but she also performed several stellar solos on the soundtrack, including ‘Separated by the Storm’, and ‘[In Wonderment of Winter](https://open.spotify.com/track/4x8hBoYYlsQk6ZYNzQLSzq?si=cn9MRtonQFaFuM7rZ9GMCA)’. This latter track also features several of the sounds created by Slate & Ash.

In addition to the woodwind samples, I created some custom string samples along with my orchestration team specifically for use in the game. These were recorded in Vienna by the [Synchron Stage Orchestra](https://www.synchronstage.com/en/orchestra). They focused on creating constantly shifting sonic textures. The standard way to write for strings is for the section to be divided up into 5 lines (Violin 1, 2, Viola, Cello, Bass). However I booked 20 players and gave each player something different to do (20 lines). This resulted in some extremely interesting textures that provided that constantly moving and evolving feel in some of the softer string work in the game.

![](../../assets/f91b9d8f506fb3df.img)


Ori and the Will of the Wisps vocalists Aeralie Brighton and Kelsey Mira.

In terms of the recording and production any featured solo instruments such as the aforementioned woodwinds were recorder remotely. Aeralie Brighton, the singer of the ‘[Main Theme](https://open.spotify.com/track/0BqVTj3PfExdgXUu4vq7tb?si=RKvjkX3KSFu8O0CJYqJWQA)’ amongst many other tracks, and Kelsey Mira, the singer featured on ‘[Luma Pools](https://open.spotify.com/track/7dw8VjZYf3DyUyMMpMliNp?si=foJx87UKTq6-nCCfceZVpw)’ both recorded at home. There are a wealth of amazing musicians who have the capability to record themselves at home and this has become even more of a necessity now with the pandemic. I must admit as a composer I feel somewhat spoiled when I can just send a ZIP file with what I need recorded and then what I receive back I can just drop straight into the music with no fuss.


The orchestra was recorded in the Lyndhurst Hall at [AIR Studios](https://www.airstudios.com/) in London. I’ve long wanted to record here and always thought it would be the perfect room for an Ori score recording. Steve Kempster, an engineer who is a key part of establishing Ori’s sonic aesthetic, worked with AIR’s terrific team helmed by engineer Jake Jackson to put together the setup for the [Philharmonia Orchestra](https://philharmonia.co.uk/), who I’d worked with before on ARK Survival Evolved and was delighted to work with again here. For the largest cues in the game we used 73 players, down to a chamber string group of 22 for the smaller cues.

![](../../assets/2503b88cd29a84a1.img)


Gareth Coker, Alexander Rudd and Zach Lemmon with the Philharmonia Orchestra.

We also had the chance to record choir with the Pinewood Singers, a 20 voice ensemble. Human voice is a big component of Ori’s soundtrack, both soloist and choral. In the first game we had to use samples, but we were able to use a real choir this time around and their value is especially felt in the weightier scenes in the game.

When you combine the above and my work on the first game, I look back and feel very fortunate to have been given the resources to put together these two scores. Both scores deliberately have a bit of a different feel, but between them I feel like that at this point in 2020, between the almost 6 hours of music I’ve written for the franchise, I’ve said all I can say musically with regards to Ori. But were there another compelling story to work with that would help me tread new ground, it would be fun to re-explore down the line!

Gamasutra: They say hindsight is 20/20, so looking back at the process from start to finish, what's the biggest lesson you learned? A takeaway you'll carry forward into future projects.

Gareth: By far the biggest benefit of being embedded so heavily in the team since the first game has been the ability to understand the game development process from start to finish and being able to learn at least the basics of several different roles in the team. I think it’s important for any game composer to at least have a cursory understanding of as many roles in the production process on a game as possible. I feel the same way about film. Having been to a university with an amazing film school (University of Southern California), it opened my eyes to the importance of cinematography, editing, sound design, production design, and how all of these departments work together to become a cohesive unit.

Being able to come together and not work in a vacuum is to me a very important part of making games. Music is no exception to that. I’ve experienced working on a variety of titles big and small and have been part of workflows which offer variable levels of access. Even if a composer lacks the technical skill to understand the nitty-gritty of game making and only wants to focus on writing the music, an effort needs to be made by all parties to not keep them at arm’s length from the game.

A composer who doesn’t play games? Fine, but find someone to play on your behalf, or get as much footage as possible. I personally don’t believe you can do your best work as a composer if you’re not putting yourself in the shoes of the player. Absolutely you can deliver a great score when working with a great audio director, but how can a composer truly know what is best for the game if he/she is not experiencing it themselves with regular gameplay tests? This is something I am constantly asking for on every project I work on. It’s amazing to me that even in 2020, this reasonable request can sometimes be challenging to meet.

![](../../assets/af82dea5e57dbeeb.img)


Pinewood Singers conducted by Allan Wilson

Without doubt there is a ton of fantastic music being written for games but I think there is a fundamental difference between fantastic music that exists in a game, and fantastic game music. There are so many great composers working in the industry currently who can produce great music, but the success of that music is always going to be dependent on how well it is integrated, and how tightly to the player’s experience it is matched. Different approaches are required for all games but irrespective of that, whether you’re doing a score like Ori that favours a horizontal approach, or a score that is dependent on layers and stems and real-time recompositions and new edits of tracks that are passed over from your composer to an edit team, your game is still going to require moments where the score truly hits home.

I’m not just talking about cutscenes, it’s the entire gameplay experience. Every game has peaks and valleys. I’d suggest that those are identified early on so you can really get your composer stuck into them and understand on a far deeper level than simply reflecting what is happening on screen. I don’t personally believe it is enough to simply produce great music, that is the absolute minimum of our job. A composer and audio team need to spend as much time if not more making sure it works with the game.

Great music for games has more than a functional role to play. While music’s role starts at conveying the action on screen, it can often communicate far better what isn’t happening on screen, something that occurs on a far deeper level, a character’s state of mind, a perspective that isn’t necessarily being directly portrayed to the player through a visual. It’s this level of connection that players are looking for especially when they play their narrative games.

Whether your game is 7 hours long or 70 hours, a player wants experiences or moments that they’ll remember. You’re not going to make every minute of a 70 hour experience memorable but you’d like to hope that you can carve out moments within that. Music is a big part of that but it’s something that all key creatives need to play a role in. It’s a problem to me if I spend a large amount of time in a game but can’t rememberanything about it. I hope moving forward into the next generation we make sure that we remember the importance for the players that the handcrafted human touch brings and that is required to make great interactive experiences.