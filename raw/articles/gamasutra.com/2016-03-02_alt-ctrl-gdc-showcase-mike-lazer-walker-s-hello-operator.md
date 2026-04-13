---
title: 'Alt.Ctrl.GDC Showcase: Mike Lazer-Walker''s Hello, Operator'
url: https://www.gamedeveloper.com/audio/alt-ctrl-gdc-showcase-mike-lazer-walker-s-i-hello-operator-i-
author: Game Developer
published: '2016-03-02'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

The 2016 Game Developer's Conference will feature an exhibition called [alt.ctrl.GDC](http://www.gamasutra.com/view/news/262813/Heres_the_game_lineup_for_GDC_2016s_AltCtrlGDC_showcase.php) dedicated to games that use alternative control schemes and interactions. Gamasutra will be talking to the developers of each of the games that have been selected for the showcase. You can find all of the interviews [here](http://www.gamasutra.com/search/index.php?search_text=%22alt.ctrl.gdc+showcase%22&submit=Search).

Instantaneous communication is an afterthought in our lives. Every day, we interact with people from all over the world at the press of a button or a swipe of a fingertip, and our calls are instantaneously relayed through cell towers. The olden days in which operators manually connected calls on vast switchboards may have long since passed, yet a certain charm remains. (Think of the world-weary operators in Mad Men.)

That unique period in long-distance communication has inspired [Mike Lazer-Walker](http://lazerwalker.com) of the Playful Systems group from the MIT Media Lab to create [Hello, Operator](http://lazerwalker.com/hellooperator). It's a time management sim that's reminiscent of Tapper or Diner Dash. It asks the player to juggle multiple callers with only a scant few lines to connect them over. What makes it truly distinctive is that it's played using a replica of a vintage telephone switchboard.

The game was selected to be in this year’s alt.ctrl.GDC showcase. Lazer-Walker took the time to answer some questions about the appeal of old technology, as well as the unique narrative potential that the game – and the switchboard – can explore.

## What’s your name, and what was your role on this project?

I'm Mike Lazer-Walker. I’m responsible for pretty much everything on the project, from design to programming to spending tens of hours soldering tiny little wires.

That being said, it takes a village to raise a child. I work in a very supportive research lab full of unbelievably smart and wonderful people, and many of them have been incredibly generous with their time and expertise, particularly on the electrical engineering side of things.

## How do you describe your innovative controller to someone who’s completely unfamiliar with it?

It’s an old-timey telephone switchboard where you use audio cables to connect people who want to talk to each other.

![](../../assets/5a80093a67386883.img)


## What's your background in making games?

I’ve been making games in some form since I was very young. Professionally, I had a brief stint in commercial games (I worked on Words With Friends) before going indie. The past few years, I’ve worked on a lot of little weird experimental games, largely playing around with custom interfaces and modes of interaction.

These days I’m at the MIT Media Lab, in the [Playful Systems](https://www.media.mit.edu/research/groups/playful-systems) research group. I'm working on site-specific audio-based narrative experiences: you go to a specific public space, download an app onto your phone, and take part in an interactive radio play that changes dynamically based on various sensors in your smartphone, such as where you walk within the space. They're a blend of experiential theater like Sleep No More and modern choice-based interactive fiction; they’re sort of like “walking simulator” games but with actual walking.

## What development tools did you use to build Hello, Operator?

Rapidly prototyping gameplay can be a real challenge when you’re dealing with physical hardware. For this project, I spent a decent amount of time investing in my own software tooling to make that easier.

The game is written in JavaScript, with a modular interface system that lets me use the underlying game logic in a bunch of different places. I can play the game on the actual hardware, on an iPad using a touch interface, or even as a text-only game on the command line. This makes it really easy to playtest changes wherever I am, and even do things like write automated tests and practice test-driven development that are traditionally very difficult to do with alt control games.

![](../../assets/fe39e333b5d3027d.img)


## What physical materials did you use to make it?

There have been two major iterations of the hardware. The first version of the game used a controller I built myself out of plywood and steel, milled using a CNC router for the wood and a waterjet for the steel, plus a handful of LEDs, switches, and audio jacks.

Since then, I bought an actual vintage telephone switchboard from 1927 off of eBay. This specific switchboard, a Western Electric 551-A model, was used in the Mead Paper Mill in Chillicothe, Ohio as recently as 1966. It’s absolutely incredible to think about the same piece of electronics being in commission for nearly 40 years, and even more incredible that it’s still in usable shape today. The actual circuitry has been gutted, but other than replacing its incandescent lightbulbs with modern LEDs, all of the hardware components are original. I’m even using the original wiring. They don’t make ‘em like they used to.

## How much time have you spent working on the game?

The absolute first prototype of the game – literally made out of a cardboard box – was built at a game jam maybe a year and a half ago. The current incarnation was first made over the course of a few weeks in December. I’ve been working on it since then, fine-tuning the gameplay and getting the vintage switchboard up and running.

## How did you come up with the concept?

Last year, I showed a piece at alt.ctrl.GDC called [What Hath God Wrought?](http://lazerwalker.com/telegraph) where you play as a telegraph operator in the 19th century, sending and receiving Morse code using vintage 19th century telegraph hardware. The glib answer is that going from a telegraph operator to a telephone switchboard operator was a natural progression.

At a high level, I’m fascinated by outdated technology. The same way that computers shape our lives today, technology like the telegraph and the telephone defined and expanded the ways that information could spread and societies could communicate. These are objects that were completely commonplace and quotidian to people 100 years ago, but are completely foreign to us today.

There’s a lot to be gained in exposure to this – I still can’t get over, for example, how 19th century telegraph operators had “chat rooms” that mirrored early Internet culture very closely – but the traditional ways we learn about these sort of things can be a bit dry. To me, being able able to physically engage with the objects that made the past tick is both interesting and valuable.

![](../../assets/de760acb328c946b.img)


## Can you tell us more about the experiments in narrative you want to explore with Hello, Operator?

The switchboard has a set of switches that, when flipped, let you listen in on its phone lines. What does it mean when you can use that to snoop on someone else’s conversation? How do you design and write a multilinear story where no matter which conversations the player chooses to listen to, they’ll get a coherent and satisfying experience? It’s a challenge that’s shared with other modern interactive narrative games, but there are still fun and unique structural problems to solve.

People have experimented with this exact mechanic before (in particular, there’s an iPhone game called [FreeQ](http://freeq-game.com), but I’m also interested in the use of physical controllers as theatrical props. Guitar Hero wouldn’t make you feel as much like a rock star without a plastic guitar to wave around; I’m excited to explore how that sort of physicality can encourage role-playing in a more story-focused context.

## You say that the switchboard is designed to fit the imagination of what a switchboard is like rather than an actual one. How much did you consider authenticity versus imagination with Hello, Operator, and what balance are you aiming for between the two?

There was a conscious decision to throw that balance out the window when we switched from the custom hardware to the vintage switchboard. Since then, there has been a huge emphasis on verisimilitude; the steps to answer a phone call within the game are exactly the same as you would were you actually operating this switchboard in the real world.

Making physical/digital hybrid games is a heck of a lot more work than pure digital games, and only being able to show a piece at events like alt.ctrl.GDC severely limits your audience. To me, an alt control game has to “earn” its right to exist in a physical form. For projects that repurpose vintage machinery to try to capture some bygone element of the past, the act of physically interacting with original hardware in an authentic way is a big part of the magic. That’s largely why the choice was made to switch to the vintage hardware – that authenticity is really conceptually important.

## What hardware is inside the switchboard, and how receptive have players been to it as a controller so far?

When we moved over to the vintage switchboard, just getting enough input/output pins to talk to a computer ended up being a surprising engineering challenge. A basic Arduino has 14 IO pins, a Raspberry Pi has 26, and most hobbyist microcontrollers are in the same ballpark. The switchboard needs 180 of ‘em! Making matters worse, many common techniques to reduce the number of pins needed (such as connecting multiple LEDs to a small number of shared pins) aren't possible without major changes to the existing vintage wiring. Right now, the game is driven by a Raspberry Pi connected to a handful of Arduino Mega boards I’ve outfitted with custom-designed and fabricated shields.

Players have been unbelievably receptive to the hardware. The tactility of the switchboard, from the individually-weighted cables to the mechanical switches, is absolutely wonderful. It’s naturally not something I can take credit for, but this thing just feels incredibly satisfying.

## How do you think standard interfaces and controllers will change over the next five or ten years?

For games specifically, I expect we'll see a major shift away from what we currently think of as controllers. So much exciting work these days feels completely inaccessible to a wider audience solely because navigating a virtual 3D space using a controller or mouse + keyboard is a prohibitively high barrier to entry. I’d like to think we’ll find a way to break that open to help modern narrative games find a wider audience.

I don’t know what this looks like – maybe it involves VR or AR, maybe it’s just a shift towards more touch- and gesture-based interfaces, maybe it’s something else entirely – but I definitely see the sort of experimentation that happens at events like alt.ctrl.GDC as an important part of that exploration.

Go [here](http://www.gamasutra.com/search/index.php?search_text=%22alt.ctrl.gdc+showcase%22&submit=Search) to read more interviews with developers who will be showcasing their unique controllers at Alt.CTRL.GDC.