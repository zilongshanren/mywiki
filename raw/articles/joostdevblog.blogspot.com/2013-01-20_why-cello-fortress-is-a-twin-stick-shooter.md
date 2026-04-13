---
title: Why Cello Fortress is a twin stick shooter
url: http://joostdevblog.blogspot.com/2013/01/why-cello-fortress-is-twin-stick-shooter.html
author: Joost van Dongen
published: '2013-01-20'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Cello Fortress](http://www.cellofortress.com)could have been any kind of game. The core concept is nothing more than: "

*a game in which a live cellist controls the game by playing cello, and plays with or against the audience*". This idea can be applied to any genre. The cello could control a brawler, a puzzler, a strategy game, a racing game, with some imagination maybe even a point and click adventure. So why did I specifically make a twin stick shooter? A lot of thinking and brainstorming went into this choice, so today I would like to explain that a bit.

Doing something with improvisation on my cello and my computer is a topic I have been thinking about for years, but it wasn't until a year or two ago that it dawned on me that the cello could actually be a game controller. Before that, I was mostly thinking about writing a procedural music generator that could accompany my own cello improvisations. Quite a big step from a game, but it slowly evolved into one from there nevertheless.

![](../../assets/73fd1576c151c501.jpg)

Knowing that the game needed to be about a live performance with my cello, with or against the audience, creates a number of requirements for the game design. These requirements fuelled what would become the actual game, and it was quite a challenge to find something that really met them all well enough.

- Game is fun to play, and also fun to watch for the audience.
- Playable by as many people in the audience at the same time as possible, while also being playable by only a single player.
- Such simple controls that no long explanations or tutorials are needed, and that even non-gamers can play.
- The cellist has room to improvise and play something that sounds good, while still controlling the game in a meaningful way.
- The influence of the cello is direct enough that players and audience can quickly recognise and understand it.
- Bonus requirement: the core game itself is original.

Each of these requirements brings a different view on what this game should be. Number 2 for example favours games with a zoomed out view, so that several players have room to move within the same screen. Splitscreen is also an option for this, but didn't seem such a good fit for readability in case of a larger audience where people might be standing further away. Specifically inspiring games for me where

[Gatling Gears](http://store.steampowered.com/app/102810/)by our Dutch friends at Vanguard, and the WiiWare racer

[Driift Mania](http://www.youtube.com/watch?v=b5Qp7yUs6AA). Both of these games are also excellent fits for requirement number 3, since they require very few sticks and buttons to control, which makes the gameplay easy enough to explain in just a couple of seconds.

![](../../assets/a468649416db36a1.jpg)

Another game genre that came to mind was rhythm games. Dance mats are really nice controllers for festival-like situations, since they are so physical. However, this kind of game seemed at odds with requirement number 1: most rhythm games don't have an on-screen hero that onlookers can follow and root for.

Requirements numbers 4 and 5 are where the real complexity of the game design steps in. How does a cello control a game while still making music? For example, going left by playing high notes and going right by playing low notes is way too boring. I needed something more subtle. At the same time, the influence of the cello should be clear to the audience as quickly as possible, to make sure people don't think it is a 'normal' game with only a live soundtrack. The cello actually controls the game and ideally people would understand this without my explanation.

This makes the racing game a difficult proposition. I had in mind that the cello would generate the track. But to give players a chance at reacting to it, the track needs to build up a bit in front of the furthest player. This has the big downside that it happens just beyond where most people are looking.

I also struggled with how to build the track from the music. I thought about things like making difficult, spiky roads if the cello plays in minor, while generating more smoothly curving roads when playing in major. However, this is way too subtle. Most people probably can't even recognise the difference between major and minor well enough, let alone link it to the gameplay. In my mind I tinkered with lots of other ways in which the cello could control the game, but I didn't come up with anything that worked as well and as naturally as the current twin stick shooter.

![](../../assets/1852636f9e9d1f21.jpg)

I arrived at the twin stick shooter as a good genre for Cello Fortress pretty early in the process, yet for a long time I kept brainstorming and looking further. This was because of requirement number 6. Twin stick shooters are a pretty overused genre in games, and it is difficult to still do something interesting with them in terms of gameplay. So I preferred something more original and kept searching.

However, in the end a quote from my former teacher JP van Seventer reminded me that keeping the core game less original might actually be a good thing. JP is a Wise Person (tm) and is also

[Ronimo](http://www.ronimo-games.com)'s regular outside advisor. He currently works at the

[Dutch Game Garden](http://www.dutchgamegarden.nl/)to give advice to young Dutch game start-ups. He once said something along these lines:

"

*Innovating everything at the same time is not a good idea, because it alienates the audience too much. It is better to innovate on a number of aspects of the game, and keep the rest recognisable. That way players can relate to it much better and understand how it works more quickly.*"

This has been very influential on my thinking about games. Before this I had dreams of coming up with a game that would be totally unique

*in every possible way*, and this quote made me realise that that might often not be a good idea. This quote definitely applies to Cello Fortress.

With Cello Fortress having been in the media quite a bit in the past week, I see now how difficult it is to explain what Cello Fortress is. Even after the

[very explanatory trailer](http://www.youtube.com/watch?v=C-CljFEynm4)that I posted

[last week](http://joostdevblog.blogspot.nl/2013/01/cello-fortress-trailer-revealed.html), I read lots of confused comments online from people who don't really get how it works. So I am happy that I chose a genre in which the core gameplay itself at least is really easy to explain, so that I can focus my communications on the much more interesting side of the game: the way the cello controls it and the way the game is halfway between a game and a live performance.

About trying to be original - there's an advisory article about it on tvtropes http://tvtropes.org/pmwiki/pmwiki.php/SoYouWantTo/BeOriginal . Altough it's a little more about writing, truths which this article contains are quite universal.

ReplyDeleteNice article, it has a lot of similarities to how I view creativity and originality. :)

DeleteNice work Joost! One of the very few examples of seeing what can happen when you give sound more than a supportive role in a game. More of this, please.









ReplyDeleteA couple of questions, if you don't mind:

In what ways did you find the choice for a fairly traditional twin-stick shooter influence the musical component of your concept?

Can you really achieve a meaningful relationship between your musical output and the game without reevaluating the core game design?

Looking at the actual inputs for the game -- which meaningfully connect the game and the music played on the cello -- I see three: low, medium and high frequency amplitude values derived by spectrum analysis. A good start, and easy for the players and audience to grasp. What are your thoughts on more complex relationships between game and music?

I see the musical performance in Cello Fortress as much more a part of the experience of playing or watching, than as part of the actual gameplay itself. Depending on the skill of the performer, the musical performance really makes or breaks the experience of playing or watching. The actual musical input required for a functioning game session is small subset of the entire performance.

Now that you've completed this experiment, where to next? :)

Could I interest you to join a discussion I'm organizing with Soundlings in Februari? Soundlings is a growing collection of sound and interaction artists, and they organize regular meetings. The topic will be game audio, and where it can go next. Cello Fortress would be a wonderful case study, and we'd value you input greatly.

There is an important aspect of Cello Fortress that you are not aware of: these three types of input in the game are only examples. In the current game there are nine types of input and I am going to add some more.







ReplyDeleteThe types of input are also not all as rigid. For example, I have a special attack that is triggered by playing an eight-note melody. After the fourth note, the charging animation becomes visible, but the attack doesn't land until the eight note. This gives a wonderful interaction with the players: they start fleeing after the fourth note and depending on whether I increase or decrease the speed of the final notes of the melody, I can time the actual attack to react to the players.

So the link between music and gameplay is a lot stronger than you are aware of.

As for how the twin-stick-shooter influenced the music: it is more the other way around. I based the game design on how I improvise on my cello, and analysed what kinds of things I do while improvising to derive gameplay from that. Cello Fortress very much started with the music and the gameplay followed from there.

Nevertheless, now that I have it running, I adapt my improvisations to what inputs I made. The game reacts well to extremes, so I try to play more extremes than I normally would. Fast sections are faster and slow sections are slower. This also greatly helps the audience to distinguish the link between music and game more quickly.

Cello Fortress is far from completed: I have a lot of improvements and extensions that I want to make to what it is now. I don't think I'll be completely done with implementing all my plans until the end of 2013 at the earliest.

Where would this Soundlings meeting be? I don't think Cello Fortress is all that interesting for 'normal' game music, since Cello Fortress is such a weird out-there experiment, but it might still be interesting to discuss it.

Interesting! I'll have to witness it live soon, and I'm curious where you'll take it conceptually. :)






ReplyDeleteRegarding the Soundlings meeting: Cello Fortress will fit right in! Soundlings folks have a tendency to be artsy, high-concept people, and I'm specifically looking for out of the ordinary! You'll probably know some of them already.

Not speaking for the entire group: I'm so very bored with the current state of game audio. It's always in this supportive role; giving you information about the current game state and playing evocative music is usually all that it does. What I'm interested in is games in which sound and music are part of the game mechanics intrinsically.

We're hoping to host the meeting at the Dutch Game Garden, around the 13th or 14th of next month. They usually start at 19:30 and go on until around 23:00.

The organizational hub is on Facebook. I could invite you to the group so you'll stay up-to-date and so you can participate in the conversation there? The sub-topics aren't set in stone yet, so if there's anything particularly out-there that you'd like to discuss feel free to suggest it.

If you don't feel like joining yet another facebook group we could always just send you an email with the details once they're fleshed out.

If Soundlings is in the Dutch Game Garden, then I'd be happy to join in, since Ronimo is located there as well. :)


DeleteI don't really use Facebook all that much, so I'd rather just receive an email with an invitation for the event.

Perfect! I'll let you know the details once they're finalized.

DeleteHi Joost,




















DeleteWe've got confirmation from the Dutch Game Garden, and we'll indeed be hosting the discussion(s) there. I've copy/pasted the event description below. We hope to see you there!

The Soundlings collective organizes regular meetings to informally discuss current topics of interest for the broader field of musicians, producers, and sound artists. This specific series of events is organized in partnership with the Dutch Game Garden. Attendance is limited and by reservation.

With these Think Tank sessions we will be homing in on the field of Game Audio. We will discuss sound design and composition in the context of this new and dynamic medium. What is it, where did it come from, where is it now, where is it going, where do we want it to go?

Since this will be quite a big topic, the discussion will be split into at several sessions:

Session 1 (Meetup #13, February 13th) : Establishing Context

We will briefly cover the history of game audio as a field and see how it has evolved to what it is this day, highlighting the use of available technology and the role audio has in selected games. We will examine the where the fringes of game audio currently are in the broadest sense, again using case studies. How is audio in games used today, on a technical and conceptual level? You're invited to review and critique either the provided case studies or particular examples that lie close to heart. We share our current knowledge of the field and make sure we are all on the same page for the next sessions.

Please let us know of any games or projects that you think should be mentioned during this session! You can either post on the Think Tank Facebook page, or mail directly to thinktank [AT] soundlings [DOT] com.

Date: Wednesday 13 February, 2013

Time: 19:30

Cost: Free. Attendance is by reservation.

Location: Dutch Game Garden, Neude 5 3512 AD Utrecht

Session 2 (To be scheduled): Audio Creation Workflow

We look at how audio for games is created today, from concept to execution. What tools are used? How is the audio creation process integrated in the whole of the development process? Can we identify any bottlenecks or design flaws? How do our tools influence the type of audio and the type of games we make? Are there concepts we struggle to realize because our tools hold us back?

Session 3 (To be scheduled): Future Gazing

We combine the findings from the previous sessions, discover trends, and attempt to extrapolate into the future. What role will audio have in the games of tomorrow, and how will we make them? Where do we want to take game audio?

Note: The specific order and number of sessions is subject to change.

Thanks! I will probably be visiting only one of these sessions, I guess the first one is the most relevant one for me to visit, then?

DeleteI'd value your input on any one of those sessions, but if you join the first we could use Cello Fortress as a case study (if you don't mind doing so, that is). So yeah, just come to the first one! There's at least two weeks between each session, so can decide for yourself if you'd like to join the remaining sessions after that. :)

DeleteOkay, see you next week! Since it is a roundtable, I suppose I don't have to bring my cello? Or would you guys want a demo?

DeleteWe probably won't have the time, no. I'll do an introductory presentation including gameplay videos from several games in which I can include Cello Fortress footage. If you have any preference for clips to show let me know!

DeleteThis sounds fascinating. Is there anything forcing you to use a cello as a controller? I ask because I'm not a cellist and I'd love to play about with it on guitar.

ReplyDeleteMost inputs are rather particular at the moment, like the division between high and low notes, so a guitar would not be able to use all skills. Also, notes outside the range of a cello are ignored altogether. So to make a guitar really work, quite a few things would need to be modified and tweaked.

DeleteI smell a framework. ;)

DeleteNice article. I really like your blog.

ReplyDelete