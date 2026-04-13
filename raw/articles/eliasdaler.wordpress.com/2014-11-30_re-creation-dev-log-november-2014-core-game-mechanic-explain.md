---
title: Re:creation dev log. November 2014. Core game mechanic explained and more.
url: https://eliasdaler.wordpress.com/2014/11/30/recreation-dev-log-november-2014/
published: '2014-11-30'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

[Re:creation info/press kit](https://eliasdaler.wordpress.com/2014/10/19/recreation-info-press-kit/) | [Previous dev log](https://eliasdaler.wordpress.com/2014/10/30/recreation-dev-log-october-2014/)


I did a lot of stuff this month and I’ll start with the most important thing.

I’m ready to present the core game mechanic in the game!

# Recreation

I call this mechanic “**recreation**“. Here’s how it works.

First, you kill someone

![](../../assets/2b115190d3db48b3.gif)


Then you can become a ghost and travel around the screen without taking any damage and colliding with anything

![](../../assets/3824445c4a556700.gif)


You can’t get too far away from your body though!

When you are in the ghost form you can become the enemy you just killed

![](../../assets/9472991082819712.gif)


It gets revived in the zombie form. You don’t have many health in this form so you can’t complete an entire level like that, you’re most likely to die. When you die, you return to your original body.

This mechanic is used to solve puzzles and progress forward. Each enemy will have unique skills which will help you on your way.

Here’s an example of solving a simple puzzle.

![](../../assets/abd317cb4a334f98.gif)


I have some other puzzles but I can’t show them right now because they need to be polished! I also don’t want to spoil too much for people who read my dev logs.

There are lots of puzzles which can be invented with this mechanic and I’m really excited to work on puzzles involved it!

And now I’ll tell you about other things I’ve done


# Ta-da-da-da!

I’ve decided to work on “Got item” animation.

Here’s what I came up with first:

![](../../assets/67dddb527d909171.gif)


But then after a little talk with [Gordon Little](https://twitter.com/G_O_R_D) I’ve realized that I can make the hero react to items differently based on their importance. Here’s how it looks:

![](../../assets/5c390f7ea27b0a7b.png)


I’ve recieved lots of positive feeback for this screenshot which makes me want to do these little things more. I like them in other games. I’d love to make more things like this in mine.

# Working on the dungeon

![](../../assets/311de127e80d7815.png)

The importance of colors. Tuned them a bit. Looks better!

Drawing a dungeon tileset was harder then I’ve thought. Look how many tiles I have to draw to have floor, walls and doors! Most of them are copied and rotated but still, lots of unique tiles. Looks neat though.

![](../../assets/649d3cf405d73fad.png)

Dungeon tileset looks like this right now


![](../../assets/1d6754f1830626e2.png)

A little problem. Notice that there are two types of corners in the tileset to make this cell work.

## Scrolling

Notice how level scrolls when you go to another screen

![](../../assets/3ea31edbea14918d.gif)


Here’s how the scrolling looks there:

![](../../assets/3da597be0577188b.png)


So, when the screen scrolls up, you see one tile from the previous screen. So, there’s a little overlap between the screens. This is done to make the world feel more continuous.

This doesn’t work for dungeons because you’ll be able to see one wall tile from the previous screen. This is not good. This is why scrolling works like this:

![](../../assets/4aad6ce1ed401cdc.png)


![](../../assets/9aa5c2767cfd5c02.gif)

Notice that hero makes a little step when he arrives at the next screen for smoother effect.

## Musician

![](../../assets/474d57e2e55284c0.gif)

His words rhyme!


He can play any song you hear in the game. You should bring them notes first, though. Notes can be found in different levels. But musician’s role doesn’t end here. More about that later!

I was inspired to make him by **Shovel Knight** which basically has the same NPC. A great idea, I think.

# Triggers and buttons

![](../../assets/ce6a9483c3a6fb29.gif)


This trigger is very easy, it opens a door when you step on the button and closes it when you’re not standing on it. The triggers have a lot of common things with triggers in Unity. They have three main function in a Lua script: **onEnter**(), **onStay**() and **onExit**(). When you enter the trigger, **onEnter**() gets called. When you stay in the trigger area, **onStay**() function is called every frame. And finally, when you exit the trigger area, **onExit**() is called. With three functions most of the triggers can be scripted easily.

# Other stuff

I’ve also made copy-paste function for tiles in the level editor to make rooms quickly by copy-pasting them.

Worked on entity/component/system part of the engine a lot and made it a lot better and faster to expand. There was a ton of bug fixing made but there’s nothing very interesting there.

# Plans

I plan to make a system which will let me make rooms/areas which will be larger than one screen and they will scroll continiously. This won’t be too difficult but will allow me to make levels a lot more interesting. Actually I’ve made the first prototype of this system and it works pretty great!

This will make my game closer to** A Link to the Past **because it’s level system works in the same way**.**

I also plan to add a GUI for the level editor because as it gets more and more features, it’s easy to get lost in all those key bindings. Some menus will be nice for it. I’ll check out [http://cegui.org.uk/](http://cegui.org.uk/) first.

And the most important plan: I’ll be working on the first boss of the game. The fight will make you learn **recreation** mechanic and will be kinda unique, I think!

And that’s it. Thanks for reading my dev log. Share it with your friends, leave your feedback and subscribe to my blog or my [twitter ](https://twitter.com/eliasdaler)to get the latest **Re:creation** updates!

Looking good. Nice Link to the Past feel.

Thanks a lot! :D

Woah, I didn’t know about the ghost mechanics, that’s so cool! Like everything else you have in the game. I love it so far and I’m looking forward to the game.

I’m sorry, I simply can’t follow everything on regular basis but tell me, any betas / preorders soon?

Thanks a lot!

Ghost mechanics isn’t something I showed off before. This is the first time ever.

It’s too far from beta. Even for alpha! I don’t yet know how much time it’ll take. :)