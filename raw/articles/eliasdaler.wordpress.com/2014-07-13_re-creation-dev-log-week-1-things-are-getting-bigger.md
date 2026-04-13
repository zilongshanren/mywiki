---
title: 're:Creation dev log. Week #1. Things are getting bigger!'
url: https://eliasdaler.wordpress.com/2014/07/13/recreation-week-1/
published: '2014-07-13'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

This week was really awesome. I spent lots of time working on the game and I’m very satisfied with results.

I discussed the game with artist and somewhat determined its scope, story, main gameplay elements and levels which is also great.

Here is some amazing concept art Dmitry (artist) did.

![](../../assets/eae564ad237f318c.jpg)



![](../../assets/8043a42f734e2e1e.jpg)


![](../../assets/e5423ceec877ca8d.jpg)


![](../../assets/4c6ac0e71c082edf.jpg)


![](../../assets/a6a7ae7553851b4e.jpg)


I spent lots of time debugging and working on level editor, but there were some cool other things I did this week.

## Player can pick up items

![](../../assets/9bc8ea0794f5f301.gif)


Adding this feature was actually very easy with a power of Lua!

When two entities collide they each call their “collide” functions which then launch “collide” function in script.

Here’s how heart’s collide script function looks:

collide = function(this, second) -- "second" is id of entity with which heart collided if(isPlayer(second)) then addHp(second, 1) playSound("res/sounds/got_heart.wav") killEntity(this) end end

Here’s how bow’s collision script looks:

collide = function(this, second) if(isPlayer(second)) then say("Got awesome bow!\nToo bad you can't use it yet") addToInventory("bow") setState(getPlayerId(), "Idle") playSound("res/sounds/got_item.wav") killEntity(this) end end

As you can see, scripts are easy to read and give me lots of power and flexibility!

## Enemies can drop items

![](../../assets/b7ca70527b17a613.gif)


Well, it was really satisfying to implement. I created **DropComponent** which reads item names and their drop chances.

When enemy dies, it calls their **DropComponent** drop() function which then determines based on chance whether to create some entity or not.

I’ve learned that C++11 has** <random>** header and some random generators. I’ve heard that it’s cooler to use this than **rand**(), so I give it a chance. Works pretty good, though I didn’t properly tested it yet. (Enemies won’t drop some significant things, I think. Mostly HP and money, maybe.)

## Destructible items

![](../../assets/d86f214127252e9d.gif)


Scripts were useful there too. Every time player attacks an invisible entity named “damage” is created. It calls damaged() function each entity it collides with and that functions call “damaged” function from their script. Here’s an example of such script function. It’s used for pot in a gif:

damaged = function(first, second) setState(first, "Destroyed") playSound("res/sounds/pot_destroyed.wav") end

The thing that really bugs me is that “Destroyed” state is still coded in C++(because I haven’t figured out how to implement states in Lua yet). But still, looks good!

## Triggers

![](../../assets/08e173f1348f45dc.gif)


Well, you guessed it right… more scripts! I didn’t even had to add something special! Just a script and it’s good. Here’s an example

trigger_F = { CollisionComponent = { boundingBox = { 0, 0, 100, 40 }, collide = function(first, second) if(isPlayer(second)) then say("Press F to attack") setState(getPlayerId(), "Idle") killEntity(first) -- destroy trigger end end } }

I also coded some stuff so triggers are highlighted in level Editor

![](../../assets/0bd20d47a245f5d3.jpg)


## Sound Manager

Some **SFML** specific stuff. Here’s how you play a sound in **SFML**:

sf::Sound sound; sf::SoundBuffer buffer; buffer.loadFromFile("sound.wav"); sound.setBuffer(buffer); sound.play();

Pretty easy, but here’s a catch: you need to be sure that buffer and sound must not be destroyed when the sound plays. That means that you can’t do something like that:

void playSound(const std::string& filename) { sf::Sound sound; sf::SoundBuffer buffer; buffer.loadFromFile(filename); sound.setBuffer(buffer); sound.play(); } ... // in some other function playSound("sound.wav");

because they will be out of scope when function finishes!

Here’s how I approached this problem. I have a queue of sf::Sounds. SoundManager’s update() function is called during some intervals. It goes through all current sounds and if some sounds have stopped playing, it deletes them. It works, yay!

## Screen transitions

When the players goes to another screen I place entities in their initial positions and restore their HP. That’s the things most games do. Why do they do that? Well, I don’t speak for all developers, but I do that because I don’t want enemies to chase players through different screens or to attack them immediately after the screen transition. I also disable all entities which are not currently seen on screen and it’s a huge performance boost, because levels can be really huge and there’s no need to update everything. I can write about how I do that if someone is interested.

## Level editor improvements

![](../../assets/1a764acaa49d65eb.gif)


I’ve implemented rectangle selection. It was a lot harder than I expected.

And here’s the thing I’m proud of: entity creation menu. I can choose entities from menu and create them. I can also change scripts using arrows keys(only entities from one script are displayed at one moment).

And that’s it! As you can see, that’s a lot of work. I have some plans for next week: level transitions, combat, simple inventory system, some level editor stuff, I’ll also refactor some code and draw some sprites and prototype one of the levels. Yeah, and I also plan to start working on the fourth part of Lua/C++ tutorial(FINALLY!)

Follow me on twitter ([@EliasDale](http://twitter.com/eliasdaler)r) for more updates

Interesting vlog man, I’ll keep an eye on it. Love the LUA usage :)

Thanks a lot :)

Nice work man! Its looking so good. Im waiting for next tutorial ^_^

Thanks a lot! :D

Man Lua is awesome! So flexible!