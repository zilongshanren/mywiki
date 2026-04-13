---
title: 'RPG Playground 0.6: Add characters'
url: https://dewitters.com/rpg-playground-0-6-add-characters/
published: '2013-04-03'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

It’s time for a new release of [RPG Playground](http://rpgplayground.com)! This time you can add characters and monsters to your levels. Unfortunately they currently just stand there doing nothing. But don’t worry, in the next releases the NPC’s will be able to talk, and the monsters will walk around and attack the hero.

![entities entities](../../assets/7b6e5023dd9dc2ee.png)


When loading your old levels, you will see a popup that it is an old level. You can add characters to these levels as normal, and when you save them, they are automatically saved in the new format.

I also did some fixes and other things, so here is the full list of things that this new release brings:

- Errors that happen during the loading of levels are now shown
- A status bar is added at the bottom right that shows connection errors and other messages
- You can add and delete characters
- Fixed the ‘HTTP IO error’ issue when trying to save a level
- Main hero is replaced by one that matches the other characters
- Tiles are now placed at the correct mouse position

For the next release I’m going to improve the save/load project dialog. You will be able to give your project names, so that it’s easier to know which level to load, and that you don’t have to select the project every time you save.

## 6 Comments

## ash kukucka · April 17, 2013 at 21:59

hi, i like this rpg playground but for some reason i cant load my project, and if i cant load my project then i definitely wont be using rpg playground in the future only because i put to much effort into this map that i was working on to start all over again and watch this one not load as well, and yes i did create a account and i did save it, on the other hand if you do end up fixing the problem than i have an idea with some features: u should make the npc’s and monsters face other ways, it annoying how they are only facing down, and making more tiles that the player can walk on such as water,stone,gravel and maybe lava?( that could kill you), also when the games finished, will the player start where u left him when u last saved it or where he was when u fisrt started to create the map. ty

## Koen Witters · April 18, 2013 at 11:37

Hi Ash,

I’ll mail you about the issue with loading your level, I should be able to restore your saved level. I’m currently working on improving saving/loading levels, and also making things more robust. You have a valid point here, that it’s important to know your created levels aren’t lost. I currently take regular backups, but of course there is no way for my users to check this. I’m considering to support an external backup service that you can use to back-up your created levels. This way you can be 100% sure that you have full access to your levels, and can take backups as you please.

Letting the characters and monsters face other directions is indeed on my list. And more tiles is definitely on my list, since a lot of people already requested this.

The player always starts at the same starting point, so you have to take that into consideration when you create your levels. In the future you will be able to configure where he starts.

## Chris · May 22, 2013 at 10:59

I can not get the up and down arrows to work on the tile editor. I am using Chrome with flash version 11.7.700.203.

## Midhun · March 28, 2014 at 06:40

Hi! I like RPGPlayground, but, Can you tell me how to change the player? I know how to add characters.

## Koen Witters · March 30, 2014 at 12:35

@Chris

Is your level big enough for scrolling? When you move your mouse over the arror button, do you see it highlighting?

## Koen Witters · March 30, 2014 at 12:39

@Midhun

There currently is no way for you to adapt the hero character in your game. But if you send me an email with the character you want, and for which project, I can set it manually. mail me at koen@koonsolo.com