---
title: Geeks, MOPs and Lightsabers
url: https://acko.net/blog/geeks-mops-and-lightsabers/
author: Steven Wittens
published: '2020-10-15'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![Geeks, MOPs and Lightsabers](../../assets/54599878de7661b1.jpg)

# Geeks, MOPs and Lightsabers

Imagine going to a restaurant. The food is amazing, and you're having a great time. You tell the waiter, *"Compliments to the chef!"*, who dutifully reports the news to the kitchen.

Only the chef is crazy. He runs out and snatches your plate while you're still eating, saying *"If you liked this one, wait until you try my next recipe!"* He doesn't return for two days, so you leave hungry and dissatisfied.

When you write a letter in complaint, the chef considers you entitled and refuses to acknowledge you, because he discovered you put some extra salt and pepper on the food he served.

Welcome to Beat Saber, by Beat Games.

![A chef carefully pouring oil on a salad](../../assets/480df99e593e18d8.jpg)

## Nerds Trying To Dance

For a few months now, I've been enjoying this game in VR. It's a fantastic intersection of rhythm game, exercise and rave culture. It solves the biggest problem I've always had with going to clubs: that most people are there for the meat market instead of just dancing and having fun.

In fact, I would say Beat Saber is not a video game, but rather a *sport*. It is also a sport that many people have put significant time and effort into getting good at, myself included. We have the muscles and missing body fat to prove it:

*This doesn't just take practice, it takes training.*

The game is popular in large part because of numerous mods and player-created levels. The devs however refuse to play nice with all this. Every time the game updates, all that breaks. Most of your custom songs stop working, i.e. the ones you actually like. The UI goes back to being terrible, with lists not even sorted alphabetically, so you can't find anything. The last update completely changes the UI, which will require significant re-investment by mod authors. There are plenty of other complaints in comments and review bombs, ranging from graphical bugs to misaligned sabers. What I personally noticed is that the new effects make it harder to see what you're doing on the Expert+ levels.

It's like taking a tennis player's racket collection, bending them all by, say, 5 degrees, and then calling that person entitled if they explain that they can't hit the balls correctly this way.

![Steam auto-update options: 1) keep this game up to date, 2) keep this game up to date when I start it, 3) keep this game up to date with high priority](../../assets/a58ed54c21094b00.png)


Naturally, you can't turn off auto-updates... that would be too simple for Steam, which only offers a choice of *"Yes."*, *"Yes?"* and *"Harder, daddy."* You can't revert back to an older version of the game, because the developer doesn't let you. What you can do is:


- Figure out how to
[spoof Steam depot downloads](https://github.com/SteamRE/DepotDownloader). - Learn to manually downgrade the game
[while tricking Steam](https://steamcommunity.com/sharedfiles/filedetails/?id=1985923465)into thinking it's up-to-date. - Compile a custom version of
[ModAssistant](https://github.com/Assistant/ModAssistant)because somebody didn't parse a[JSON file](https://github.com/Assistant/ModAssistant/blob/master/ModAssistant/Classes/Utils.cs#L31)on a server[forgivingly enough](https://github.com/Assistant/ModAssistant/blob/master/ModAssistant/MainWindow.xaml.cs#L198). - Decide to mirror Beat Saber mod meta-data on your own web server because at least it will never break this way.

It took hours just to get it back to what it was the day before, and which I was perfectly happy with. If other people hadn't already done the heavy lifting, it would've taken days, maybe weeks. Regardless, I would've tried to escape the update treadmill, because it would be absurd to have a hobby I can't enjoy when I want to.

## $100 Bills

I have spent thousands of dollars on VR equipment now, and specifically bought a new set of Index controllers for this game, at ~$300 for the pair. I am the ideal customer for Beat Games, someone who is willing to spend a lot of money on their niche. Initially I bought a few music packs just to support them, even if the songs were meh. Several forced updates later, I hate them with the burning passion of a thousand suns and refuse to buy anything else these people make, because I hate being cockblocked by my own purchases. It's infuriating.

I'm sure the devs think it's the users who are entitled, expecting them to support our modded copies forever. But this is a case of Sinclair's Maxim in action: it is hard to get a developer to understand that customers *don't want* auto-updates, when his salary depends on not understanding it.

In this case, Beat Games appears to be following two incentives. First, they can only get more money out of existing customers by pushing new song packs on them through the game. Second, they can attract more mainstream customers by making the game more "accessible." So they think that's what they need to do, and think it outweighs the downsides. In reality, each forced update teaches a new cohort of the *most engaged fans* that the game they love doesn't love them back, and probably isn't worth spending any money on at all. The devs keep doing this.

This isn't just *"this is slightly different and therefor I hate it,"* because I can easily compare now. It's different in a game-altering way. My muscle memory and visual cortex are honed for a sport that no longer officially exists. Maybe it will come back, I don't know. They think just because I liked one of their ideas once, that therefor I will like every new idea they have, *and* like it more than the last one. That the bugs they introduced simply don't exist and that their creation is perfect. That I will be willing to waste hours of my time, and then days more to adjust, when the net change is worse to me. Who feels entitled to whose time in this transaction?

Let's be honest, this problem is universal in software, and reflects the average developer's attitudes today: they force their users into accepting updates, without backwards compatibility or the choice of old vs new. They then interpret their users' reluctant resignation as a ringing endorsement. If you do this, I wish you a thousand stubbed toes forever, for you are a hare-brained prima donna who does not even consider what your customers experience when they try to use your work in the field.

## Trainwreck Of Electro Swing

In the community, a common refrain is that this is just a temporary issue, and that in a few days the modders will have caught up. Ironically, this assumes that the good will of modders is endless, and that they won't tire of having to update their work over and over just to stay current. Anyone who has worked in open source knows this is a lie. As soon as the selfless contributor stops feeling the work is inherently rewarding, you have a pile of abandoned code on your hands that almost nobody knows, but a lot depends on.

Beat Saber's own success depends on it too. If you look on Youtube, you will see almost everyone is playing unofficial songs. Players use mixed reality set-ups to put themselves in the game, and even mod in entirely custom environments. It's purely there to look cool, so it looks nothing like it in-game. This level doesn't actually transform into an epileptic seizure:

It also reveals a choice Beat Games has, and which they seem be leaning into. Is Beat Saber a game that *feels great* to play, or is it a game that *looks amazing* to play? That is, is it for playing, or for watching? The latest update is notable for its rather obnoxious restyling of the entire UI, which replaces the relatively sober title screen with illustrations of people partying. Call me a grouch, but this is normie stuff, for one very simple reason: the people who only show up to the party when it's already banging... those are not the people who actually make great parties happen. This is trying to ensure people have fun by asking them, with a megaphone to their ear, *"Are you having FUN yet???"*

To me it's a text-book case of David Chapman's [Geeks, MOPs and Sociopaths](https://meaningness.com/geeks-mops-sociopaths) model, of trying to make something "cooler" while diminishing what made it work in the first place. It's not the pro-youtubers with their meticulously green screened performances... it was everyone else who vindicated the Star Wars Kid by shamelessly pretending to be a Jedi in their living room. You see, it is very rare when somebody who isn't Valve does what they do best: they give people a super-power and carefully teach them how to use it.

![Star Wars Kid - 1](../../assets/7c5c30d7c1f5359e.jpg)

![Star Wars Kid - 2](../../assets/f82f2a4a3f8b7b52.jpg)

![Star Wars Kid - 3](../../assets/1dc09cbfbb2d3147.jpg)

At the very least Beat Games should let the uncool, smelly nerds keep their hobby as it is, because that's how we liked it, and that's what we actually paid for when we bought it. Subscribing to software was supposed to help us keep our software secure and reliable, and allow users to benefit sooner from new functionality. If those updates break people's set ups for days, disrupt muscle memory even if it does work, and target a different audience, you are doing it completely wrong. Because the correct answer to that is *product differentiation*, dickbrains.

## The Only Thing They Fear Is You

When faced with a community of enthusiasts eager to hack your game to bits, you have a choice. You can push back hard and say "no, *we* are the devs, *we* control this thing." Or you can realize you have a luxury of free talent, man-hours and passion at your disposal and figure out how to work best with it, instead of giving them the middle finger and cold shoulder.

You can see mods as free prototypes, already validated in the market, and try to integrate their functionality natively. You can plan and implement smooth support for legacy content. You can set up a Discord to act as a recruiting pipeline. You can identify the modders that would make a good addition to your team, who know your code from [angles you never considered](https://skystudioapps.com/bs-viewer/?id=e7c2). You can use modding guides to figure out what the typical end-user's copy actually looks like in the wild, and try to handle the 90% case, to cut down on hate mail. You can also use it as a spec for the modding API you probably should've built but didn't.

Yes, you can actually have specs, and automated tests. This is a thing people sometimes do when they want to engineer reliable and reproducible behaviors in a collaborative environment, without increasing the amount of things they have to keep track of in their head. I know, it's wild.

If Beat Games keeps it up, then they are basically attributing all their success only to their own efforts, instead of what their customers did with it. The devs are outnumbered, so some humility is advised. In 10 years nobody will remember a "Linking Park DLC." But there will probably be an OpenBeatSaber, created by one or more passionate fans, motivated by love for their hobby and spite for the people who mismanaged it. Unless they change their approach.

If you want an example of how to do this right, learn from *Line Rider* creator, [Boštjan Čadež](https://www.bostjancadez.art/en). You'd be amazed what happens when somebody understands the value of a deterministic physics engine.