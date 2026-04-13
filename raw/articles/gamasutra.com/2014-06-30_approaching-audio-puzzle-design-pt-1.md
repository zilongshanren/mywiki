---
title: Approaching Audio Puzzle Design (pt 1)
url: https://www.gamedeveloper.com/audio/approaching-audio-puzzle-design-pt-1-
author: Rodain Joubert
published: '2014-06-30'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Approaching Audio Puzzle Design (pt 1)

How does one work on an audio game using the "left-brained" mindset without messing up its creativity? Includes a model for various design goals that a sound game typically considers, and how this will influence my work on the audio game Cadence.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

In my existence as a game designer, my best projects tend to be as deterministic and logically interesting as possible: games with turn-based mechanics, meaningful choices and quantifiable rulesets (and nothing where nuanced physics apply, thanks). There’s little room for “feel” in my games, since I think mainly about the left-brained engagements swallowing my players whole. Sure, there's always realistic room for cosmetics, interface tweaks and other feel elements, but overall the games I work on tend to embody something like this:

![](../../assets/a898801574523926.png)


All hail information density!

A short while ago, I realised that my desire for rigid mechanical precision and the hard laws of good balance and puzzle designs were great for hectically mechanic-driven projects such as [Desktop Dungeons](http://www.desktopdungeons.net), but that I’d paid scant attention to creating what I call “sexy” games: wow-inducing action spectacles, gut-feel physics simulators and directly emotive experiences like Journey. I’d certainly never released a game hinging on some aesthetic like music (though I’m always vicariously proud of the Desktop Dungeons [soundtrack](http://dbsoundworks.bandcamp.com/album/desktop-dungeons-original-soundtrack)).

So I started following the discussion on game feel, quietly poking at one or two corners of the Internet where people were buzzing about it. I learned about [Steve Swink](http://www.steveswink.com/principles-of-virtual-sensation/), read more into what Thatgamecompany calls “[feel engineers](http://www.develop-online.net/news/get-that-job-daily-how-to-be-a-feel-engineer/0188663)” and drew inspiration from fellow developers who focused on engrossing game experiences to inspire particular emotions.

Given the limits of my capabilities, I wondered if I could start practicing the general idea of “feel” within my own realm, creating games that remained fiercely mechanical while still offering some sense of flow and emotive value. My best compromise in the area of game feel was a prototype called [Stoic](https://makegamessa.com/discussion/1617/stoic-prototype-video-now-playable/p1), which was 10% coding functionality and 90% tweaking for good combat flow. The game itself was turn-based: the replays, however, were designed for as much awe and spectacle as I could manage.

The most important thing Stoic taught me was the difficulty of balancing good mechanics against good feel. In the course of developing the prototype, practically every adjustment I made would further one area but compromise another. The best “mechanical” combat I could devise was static and uninspiring to look at, but a lot of my efforts at making the action look better would start to erode the ruleset’s integrity.

I took this lesson with me to the audio arena soon afterwards, approaching the design for a puzzle-driven musical sandbox called [Cadence](http://www.madewithmonsterlove.com). A brainchild of fellow South African developer [Peter Cardwell-Gardner](http://www.twitter.com/thefuntastic), Cadence is the project I’m working on at the moment because it provides me with several valuable opportunities to apply my design philosophy in interesting ways, especially for audio. And it helps that the project’s lead has a far more keenly developed sense of aesthetic value for his games than I do (as well as actual sound production experience).


Regardless of whether you have the time to watch a gameplay video, the design deal is this: I think that audio games have a somewhat inevitable difficulty harmonising several concepts of importance to me, and Cadence sports a puzzle foundation with the potential to address that. It helps to envision the goals for a good music project as being a three-way tug-of-war:

![](../../assets/e89d9caddc2a0c27.png)


One of the core values of any musical project will be its musical feel. Feel in games is generally used to describe a much broader set of requirements, but it’s safe to argue that the sound the game generates will be the make-or-break factor in this sort of genre. It’s at the centre of your game’s mechanical and emotional payoffs. Most serious audio projects aim to do feel as well as possible.

Mechanical integrity is the value of the puzzle, game or situation independently of the music. To envision this most clearly, ask yourself: how interesting would a given game’s “left brain” challenges be if the music were to be switched off? Rewarding and engaging, or shallow and uninteresting? An audio game with mechanical integrity would be one where, in my books, you look forward to the puzzles as much as you do their musical output. Music helps you feel inspired, but mechanics help you feel smart and challenged.

The final category is creative freedom and the ability to feel authorship over the output of challenges and situations. In this case, I consider the output to be whatever audio is generated by the player’s actions. This can be the most thorny requirement because fulfilling it comes with inherent disadvantages. Pre-scripted sounds and devices do well to present awe-inspiring melodies, but don’t really give true feelings of ownership – the music really belonging to the player. On the other hand, giving players too much control over the “sound solution” can leave them without the guidance or incentive to make especially good music – or to put it more bluntly, it’s easy for people to make stuff that sounds awful and leaves them dissatisfied.

Pursuing any one of these goals tends to be disruptive of the others, at least in my understanding. It feels like a three-way split of the challenge I encountered with Stoic and it may be one of the reasons developers tend to embrace an astounding variety of sound game “styles” in their search for a great musical game. I’ll use a few for comparison:

1: [Auditorium](http://www.cipherprime.com/games/auditorium/)

![](../../assets/fed21820c4c616aa.jpg)


Probably my personal favourite at the moment, Auditorium is one of those gems which puts true priority on mechanics while maintaining a high level of feel. The puzzles are clever and interesting on their own, but feel enhanced by the audiovisual journey and thematic structure of the game. That said, feelings of ownership over the music are limited to the process of tweaking your puzzle solution (which is nonetheless a satisfying journey in itself). The musical output is otherwise quite curated and I would describe Auditorium as having less creative freedom than others in this list.

2: [FRACT OSC](http://fractgame.com)

![](../../assets/f548b4a77b1e5b34.jpg)


Easily the biggest sound game out in a while, and I’m speaking quite literally about its scope. An indie game this massive has the capability to address all three of our design goals quite well. The puzzles are a mixed bag for me, though I utterly adore the light-tube-pipe-pressure-redirect ones (an elegant term, I deem it). And its feel is great – basically a musical Myst. Otherwise, authorship is confined to the tweaking process, with a pre-determined end product as with Auditorium. It’s also dependent on players building up their skills for the “live-fire” studio attached to the game, though that’s a little too meta and long-term for me to consider it equivalent to puzzles with an open solution space.

3: [Circuits](https://www.youtube.com/watch?v=fyf7lKt7vTw)

Circuits is a purist musical dream, cranking feel to the max in a tight, elegant package that I cannot help but respect. It’s one of the few games where I’ll deliberately explore wrong solutions to hear different sound combinations. Unfortunately, the core of its puzzles are listening tests, and the game doesn’t actually include much logical challenge. Disappointing for a gaming style like mine, but really close to the feeling of good music and the sense that you're playing with a sort of aural Lego. The game is so agnostic about its mechanical challenges that it actually allows you to skip levels whenever you want, which I both admire and hate.

4: Any Guitar Hero stuff

I mention this series, but the words here apply to “play-along” games in general. It’s difficult for these music games to really have much creative room since they’re really just testing rhythm, or matching up with preset tracks as in Audiosurf. They can have a great feel and tend to be mechanically superior or more satisfying (as well as great skill builders), though players lose out hard on the authorship front as a consequence.

5: [Nodal](http://www.csse.monash.edu.au/~cema/nodal/index.html)

![](../../assets/99c345bc77e829ba.png)


Ha, okay, first: not a game. Nodal is actually an audio controller resembling the core node-edge structure of Cadence. It gets consolation points for feel, because as a functional music generator it actually attempts to reinvent people’s way of envisioning the music they’re making (and this project’s creative authorship is, of course, a solid 10/10). So it’s a really cool idea with a mechanical base that’s not actually game-suitable, but nonetheless a good study. This is one example of how a project can be separated from similar ones by its differing design goals.

![](../../assets/e89d9caddc2a0c27.png)


I hope this smattering shows a respectable diversity of audio projects with the lens I’ve provided. Due to the natural competition among these three design elements, different projects stack these chips in rather diverse ways, contributing towards overall variety in the audio game scene.

In my next writeup, I’ll go a little more into where I think Cadence sits with these three categories, how I hope to refine its mechanical base to match its feel more closely, and how I keep my head above the water by using my work partner's sound experience to inform the game's design evolution from here.