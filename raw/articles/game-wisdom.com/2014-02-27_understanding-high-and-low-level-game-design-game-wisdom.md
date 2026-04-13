---
title: Understanding High and Low Level Game Design - Game Wisdom
url: https://game-wisdom.com/critical/high-and-low-level-game-design
author: Josh Bycer
published: '2014-02-27'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

When it comes to talking about game design, it’s one of those topics that anyone of any expertise level can get into a discussion over. But taking that next step from going from your mind to a computer requires a more detailed thought process and is something that anyone interested in game design needs to know about.


## Seeing the Forest and the Trees:

Chances are if you ever had an interest in game design, you’ve probably written a basic design document or pitched an idea to your friends or a message board. And that’s a great first step: Being able to visualize mechanics and systems in your head and being able to explain them.

But taking that idea further and being able to do something with it is another matter entirely and where the distinction between just thinking about games and making them comes in. To make that move forward you need to understand the concepts of high and low level design. These terms are used by any profession that makes use of systems, not just game design.

High level is talking about systems from a generalized or abstracted point of view: Something you would say to someone not familiar with game design or during the preliminary stages of design.

While low level refers to the technical details and when it’s time to start putting something down on the computer.

Here’s an example of the difference between the two when talking about the basic detection system of a stealth game —

**High Level:** The player’s chance at being detected is determined by whether they are standing in light or in the dark. When the player is spotted, a detection meter begins to fill up and when it completely fills, the player is detected.

That was easy to understand whether you are a designer, newcomer or a programmer building the game. Now, here’s the same idea but describing it with low level design. —

**Low Level:** The player has two statistics called “detection rating” which is based on whether they are standing in light or in dark and “visibility” which is also determined by where the player is. When the player is in the dark their visibility is considered low, meaning that enemies will only detect the player from 3 feet away or closer.

![Civ 5, originally posted on 2kGames.com Game Design](../../assets/de81c3b98f54e310.jpg)


![Civ 5, originally posted on 2kGames.com Game Design](../../assets/de81c3b98f54e310.jpg)

Strategy Games often show the numbers or inner workings of their systems, making them great for understanding low level design.

When detected while in the dark, the player has a detection rating of 1.5 which will fill the detection meter at a rate of 1.5 points per second.

With the meter having a max at 5 seconds, meaning that the player will be detected in 4 seconds.

If the player is not in the dark, visibility is considered high and the player can be spotted from at least 5 feet away. With a detection rating of 4, meaning that the player will be detected in 1.25 seconds.

As you can see, the low level version offers a lot more detail and probably more than you would want to know when reading a basic design doc or talking about the idea casually. But low level thinking is very important when talking to programmers or other designers as it is the nuts and bolts of how your game is going to work.

Now those numbers that I used were just random numbers and not some magical guide to perfect stealth design. The importance of talking in that level of detail is that you can start to see how things will play out and adjust them accordingly. Something you couldn’t do if you were just talking still at the high level.

## Thinking Deeper:

For designers reading this, everything that I’ve said so far is something that you are already well aware of. But for students or casual folks who are interested in taking that next step towards understanding design, it’s critical to be able to think in these two methodologies. Knowing when to switch between high and low level thinking is also important.

If you’re still building a prototype or even the design doc, getting stuck thinking in low level mode isn’t that useful as chances are, you’re going to be changing a lot of details as the design goes forward. But if you’re already building an alpha or even a beta, it’s important to start thinking in that level of granularity to make sure that things are working right and so that your programmers can implement them.

![Super Mario 3d World, originally posted on Mariowikipedia Game design](../../assets/68471c696ec31386.png)


![Super Mario 3d World, originally posted on Mariowikipedia Game design](https://game-wisdom.com/wp-content/uploads/2013/12/MarioWikipedia-300x168.png)

However action or console games tend to obscure or don’t show a lot of information about the design and are much harder to learn how things work.

Now, thinking in terms of high level design is pretty easy as it goes along with your regular thought process. However low level design is a bit trickier.

If you have ever studied programming, you should have been taught how computer logic works. In that it is very literal and based on hard concepts and numbers.

Without having any programming background it can be hard to learn low level design strictly from playing video games as that information is generally hidden from the player’s view. The reason is that it tends to overwhelm a player with information and it is normally considered good design to make the abstracted or basic view of the mechanics simple enough to understand. You’ll never see a Mario game that gives you the exact statistics for Mario’s height and jumping ability for example.

Finding out low level design in action games is just about impossible for the average user, as all in game information is usually abstracted. Fighting games have been making some strides in this front, with many of them now featuring the option to turn on information like attack frames, attack speed, hit location and more for competitive gamers.

Some strategy titles tend to have an option to turn on more detailed tool-tips, allowing you to see exactly the attributes and ratings for every unit, research and building. Another option would be to watch master level play or speed runs of let’s plays, as these players have a full understanding of both the high and low level design of the mechanics and can usually explain it.

![Etrian Odyssey, originally posted on gamingtrend.com game design](../../assets/85d7fb79c3923623.png)


![Etrian Odyssey, originally posted on gamingtrend.com game design](../../assets/85d7fb79c3923623.png)

While RPGs do show a lot of numbers and data, they are still abstracted and hard to get down to the low level of their design without a strategy guide.

One last possible source would be strategy guides or FAQs that list detailed notes on games. But these have become a bit harder to find as paper guides have disappeared for the most part.

Being able to think both from an abstract point of view and technical is an important step for going into game design. As it will allow you to critically examine game design and make it easier to understand how a game works.