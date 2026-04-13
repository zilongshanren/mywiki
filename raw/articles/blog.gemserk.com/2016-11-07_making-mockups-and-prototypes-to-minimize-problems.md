---
title: Making mockups and prototypes to minimize problems
url: https://blog.gemserk.com/2016/11/07/making-mockups-and-prototypes-to-minimize-problems/
published: '2016-11-07'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

I’m not inventing anything new here, I just want to share how making mockups and prototypes helped me to clarify and minimize some problems and in some cases even solve them with almost no cost.

For prototypes and mockups I’m using the [Superpower Assets Pack](https://github.com/sparklinlabs/superpowers-asset-packs) of [Sparklin Labs](http://superpowers-html5.com/index.en.html) which provided me a great way of start visualizing a possible game. Thank you for that guys.

I will start talking about how I used visual mockups to quickly iterate multiple times over the layout of the user interface of my game to remove or reduce a lot of unknowns and possible problems.

After that, I will talk about making quick small prototypes to validate ideas. One of them is about performing player actions with a small delay (to simulate networking latency) and the other one is about how to solve each player having different views of the same game world.

## UI mockups

For the game I’m making the player’s actions were basically clear but I didn’t know exactly how the UI was going to be and considering I have small experience making UIs, having a good UI solution is a big challenge.

In the current game prototype iteration, the players only have four actions, build unit, build barracks, build houses and send all units to attack the other player. At the same time, to perform those actions, they need to know how much money they have, available unit slots and how much each action cost.

To start solving this problem, I quickly iterate through several mockups, made directly in a Unity scene and using a game scene as background to test each possible UI problem case. For each iteration I compiled it to the phone and “test it” by early detecting problems like “the buttons are too small” or “can’t see the money because I am covering it with my fingers”, etc.

Why did I use Unity while I can do it with any image editing application and just upload the image to the phone? Well, that’s is a good question, one of the answers is because I am more used to do all these stuff in Unity and I already have the template scenes. The other answer is because I was testing, at the same time, if the Unity UI solution supported what I was looking for and I could even start testing interaction feedback, like how the button will react when touched, if the money will turn to red when not having anymore, etc, something I could not test with only images.

The following gallery shows screenshots of different iterations where I tested button positions, sizes, information and support for possible future player actions. I will not go in detail here because I don’t remember exactly the order nor the test but you could get an idea by looking at the images.

![](../../assets/8970d3a9d00156d6.png)


![](../../assets/2d9f588a82fe14f0.png)


![](../../assets/0e4e1850a228dc65.png)


![](../../assets/fdbbcde205455f38.png)


![](../../assets/cb7816e545bcb884.png)


![](../../assets/614e5d34a2545607.png)


![](../../assets/d8e88ff0b957d189.png)


It took me like less than 2hs to go through more than 10 iterations, testing even visual feedback by discovering when testing that the player should quickly know when some action is disabled because of money restriction or not having unit slots available, etc. I even have to consider changing the scale of the game world to give more empty space reserved for the UI.

## Player actions through delayed network

When playing network games, one thing that was a possible issue in my mind is that the player should receive feedback instantly even though the real action could be delayed a bit to be processed in the server. In the case of a move unit action in a RTS, the feedback could be just an animation showing the move destination and process the action later, but when the action considers a consuming a resource, that could be a little tricky, or at least I wasn’t sure so I decided to make a quick test for that.

Similar to the other, I created a Unity scene, in a separated project, I wanted to iterate really fast on this one. The idea to test was to have a way of processing part of the action in the client side to validate the preconditions (enough money) and to give the player instant feedback, and then process the action when it should.

After analyzing it a bit, my main concern was the player experience on executing an action and receiving instant feedback but watching the action was processed later, so I didn’t need any networking related code, I could test everything locally.

The test consisted in building white boxes with the right mouse button, each box costs $20 and you start with $100. So, the idea is that in the moment the button is pressed, a white box with half opacity appears giving the idea the action was processed and $20 are consumed, so you can’t do another action that needs more than that money. After a while, the white box is built and the preview disappear.

Here is a video showing it in action:

In the case of a server validating the action, it will work similar, the only difference is that the server could fail to validate the action (for example, the other player stole money before), in that case the player has to cancel it. So the next test was to try to process that case (visually) to see how it looks like and how it feels. The idea was similar to the previous case but after a while the game returns the money and the box preview disappears.

Here is a video showing this case in action:

It shouldn’t be a common case but this is one idea on how it could be solved and I don’t think it is a bad solution.

## Different views of the same game world

The problem I want to solve here is how each player will see the world. Since I can’t have different worlds for each player the idea is to have different views of the same world. In the case of 3d games, having different cameras should do the trick (I suppose) but I wasn’t sure if that worked the same way for a 2d game, so I have to be sure by making a prototype.

One thing to consider is that, in the case of the UI, each player should see their own actions in the same position.

For this prototype, I used the same scene background used for the mockups, but in this case I created two cameras, one was rotated 180 degrees to show the opposite:

![](../../assets/e1ae278c0dd33fc4.png)


![](../../assets/f45351f0a0405dfe.png)


Since UI should be unique for each player I configured each canvas for each camera and used the culling mask to show one or another canvas.

Again, this test was really simple and quick, I believe I spent like 30 mins on it, the important thing is that I know this is a possible (and probably the) solution for this problem, which before the test I wasn’t sure if it was a hard problem or not.

## Conclusions

One good thing about making prototypes is that you could do a lot of shortcuts or assume stuff since the code and assets are not going to be in the game, that gives you a real fast iteration time as well as focus on one problem at a time. For example, by testing the mockups I added all assets in one folder and used Unity sprite packer without spending time on which texture format should I use for each mobile platform or if all assets can be in one texture or not, or stuff like that.

Making quick prototypes of things that you don’t know how to solve, early, gives you a better vision of the scope of problems and it is better to know that as soon as possible. Sometimes you could have a lead on how to solve them and how expensive the solution could be and that gives you a good idea on when you have to attack that problem or if you want it or not (for example, forget about a specific feature). If you can’t figure it out possible solutions even after making prototypes, then that feature is even harder than you thought.

Prototyping is cheap and it is fun because it provides a creative platform where the focus is on solving one problem without a lot of restrictions, that allows developing multiple solutions, and since it is a creative process, everyone in game development (game designers, programmers, artists, etc) could participate.