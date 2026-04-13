---
title: Why adding multiplayer makes game coding twice as much work
url: http://joostdevblog.blogspot.com/2015/08/why-adding-multiplayer-makes-game.html
author: Joost van Dongen
published: '2015-08-09'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*adding online multiplayer makes a game twice as much work to program*. Most programmers who build this for the first time hugely underestimate how much work it really is. For those who have never made an online multiplayer game, here are some of the reasons why it doubles the programming effort needed.

Before I start, of course note that the real complexity of building multiplayer depends on the game. Adding a multiplayer match-3 minigame to Mass Effect probably wouldn't be much work compared to the main game, but that isn't realistic: big, complex games usually also have big, complex multiplayer features. Roughly doubling the time it takes to program a game when multiplayer is added is in most cases a good guideline.

![](../../assets/b9eab9f80388cadc.jpg)

**Latency**

The basic cause of all multiplayer complexities, is that it takes time for a message to travel from one computer to another. This might take anywhere between a few milliseconds and a few seconds. Whenever you need to know something about another player, you always have to take into account that you don't know when the answer will come. To make things worse, it's impossible to know exactly how long any specific messages takes and latency might vary wildly between packets.

**Gameplay synchronisation**

All players need to have the same view of the game world. When things happen on one computer, packets need to be sent to make sure all computers know about it. This adds a lot of complexity to an otherwise simple game, because the game suddenly needs to be able to put all the information about the game in packets and send those over the internet. And what to do if we want smooth animations while some packets take way longer to travel over the internet than other packets?

**Waiting**

In a normal game, when you want to start a match, you just do so. In a multiplayer game, computers first need to talk about that to make sure all computers go into the game together. Since sending messages takes time, you need to wait for answers to come back. But what if a message takes longer than expected? Is it indeed coming later and should we just wait, or was the other computer suddenly turned off and is the reply never coming? Basically, any communication you do needs a timer to keep track of how long you are waiting and to cancel communications if the answer takes too long. And, also important: you need to handle if the message unexpectedly comes in after you decided to continue and not wait for it any more!

**Gameplay balancing**

All the other topics in this list are about tech, but of course game design for a multiplayer game is also really complex, especially in the balancing department. Our game

[Awesomenauts](http://www.awesomenauts.com)now features 22 characters and a thousand upgrades, and more are underway. What if some very specific combination of characters and upgrades is way too powerful?

Even with thousands of hours of balance testing you can still be certain further balance issues will be found once your game launches. Even Blizzard, with their extensive beta periods, never manages to get balance completely right at launch. If your game involves any kind of balance, then be prepared to spend ages getting it right, and more ages to improve it after launch.

**Bandwidth**

Modern internet connections can handle lots of data, but not everyone has such fast internet, so any commercial game needs to be able to run on low bandwidth. Most games seem to settle for something around 10 to 20 kilobytes per second as the minimum bandwidth required to play the game. Awesomenauts is no exception. Updating dozens of characters lots of times per second without using way more bandwidth than that requires some really smart optimisation tricks.

**Scalability**

If your game uses any kind of servers, then those better be prepared for any number of players. What happens if all of a sudden a thousand players all try to join matchmaking? Writing scalable server code is incredibly difficult. Testing it is a challenge since you can't easily get thousands of people to run your game simultaneously, especially before launch.

With Awesomenauts we once had a free week in which the concurrent player count went from 1,000 to over 12,000 within 24 hours. If your netcode and servers can't handle success, then you won't have it. One workaround for this problem is to not have servers of your own at all: Awesomenauts launched using only the services that Sony/Microsoft/Valve provide. Since those are scalable, so was Awesomenauts. I expect that if it had been 100,000 instead of 12,000 it would still have worked, simply because Valve's system are used to much more. Still, we spent a lot of time before launch analysing and testing our code to make sure it really was as scalable as we thought.

![](../../assets/d334793a5b4f4c8b.gif)

**Invites**

One particular topic that may seem like a detail, but turns out to be horrible, is inviting people. On modern platforms like Xbox, Playstation and Steam players can invite their friends to play with them. The complexity here is that these platforms allow players to accept invites from basically anywhere. Not just while in the menu or while playing another match, but also during a loading screen, during the intro cinematic, from outside the game or even

*while joining a game based on an earlier invite*!

To give a nice example of something that could happen on the Xbox 360: while a player is in the loading screen, another player on the same console might pick up the second controller, log in with another account, and accept an invitation to play with someone online. Now the first player's match should quit as soon as the loading screen ends, the second player should become the Active Player and should join his match. This particular situation is really cumbersome to handle, and it becomes way worse when you realise there is an enormous amount of similarly weird combinations of events and they all need to be handled correctly.

**Console requirements**

Which leads me to the final topic here. Modern consoles have long lists of requirements that games need to abide by to be allowed to launch, and this list gets a lot longer if your game has online multiplayer. If any of the weird combinations above goes wrong in the game then Sony, Microsoft or Nintendo might refuse to release it until it's fixed. Of course, console manufacturers are right to demand quality for all the games that launch on them, but it does take a lot of extra work to build.

**Debugging**

Just starting the game to test your code isn't good enough for an online multiplayer game. Instead, you need to start several instances of the game, make them connect to each other, and

*then*test whatever you just programmed. Also, the number of possible combinations of events explodes in online multiplayer situations, so not only does testing become much more cumbersome, it also requires many more tests.

I could easily have added dozens of other items to this list, but I think you already get a clear picture of how complex creating a multiplayer game really is. Many programmers think they can add online multiplayer to their game in just a month or two, but for a game of significant size it generally takes way longer than that, especially the first time you do it!

Wonderful article, it is my first time going for online multiplayer, but since I'm just a kid, I got time for it to double the work :) I loved the article though, thanks again!

ReplyDeleteBecomes even more complicated when collision detection and physics handling has to be done accurately across the network.





ReplyDeleteIt can get more tricky when collision handling and physics come in to play as well.

For instance a racegame. Player A sees player B racing next to him, while B sees Player A racing just two car lengths behind him. Now consider Player A thinking he will collide with B when steering to the side. How to solve this collision? (That is: collision on computer of A but no collision on computer of B).

Or imagine a football game where ownership of ball has to change once you get in posession of the ball. When player A has the ball and player B comes in position, player A will always end up with a wrong position of the ball as ownership just changed from A to B and B saw the ball at a different spot than A.

Yeah, we've had so much 'fun' with this problem in Awesomemenauts...

DeleteThose are the spare times of life where 'fun' is obtained.

DeleteYeah, so true, that's gonna be fun for me, haha!

ReplyDelete