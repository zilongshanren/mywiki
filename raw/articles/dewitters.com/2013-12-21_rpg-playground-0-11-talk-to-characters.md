---
title: 'RPG Playground 0.11: Talk to characters'
url: https://dewitters.com/rpg-playground-0-11-talk-to-characters/
published: '2013-12-21'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

Are you ready for a new release of [RPG Playground](http://rpgplayground.com/)? It’s right in time before Christmas! This release allows you to talk to characters, and edit their dialogue. I know a lot of you have been waiting for this, so go ahead and try it! The conversation is currently still limited to the NPC saying maximum 3 lines of text, but in the future this will be extended to full blown conversation trees.

![release010 release010](../../assets/061cf7247653767f.png)


Besides this awesome cool new feature, other improvements have been done:

- Move characters and monsters by dragging them with the mouse.
- Scrolling is now visually smooth. We run at 50 frames per second now instead of 30.
- The last added NPC is selected by default
- Fixed a weird visual issue with big levels.
- Bug fixed that the hero is not able walk down again at the top of a tilemap.
- YouTube help video is now always correctly positioned in fullscreen mode.

For the next release I will work on the server back-end. It’s currently slow, and doesn’t allow scaling to a huge amount of users. After that is finished, loading levels should be way faster than they currently are. And it will allow a huge amount of players simultaneously playing your game.

Here’s the explanation for the technical people: I’m currently storing all data in a MongoDB database. But hosting large amounts of data inside that database is pretty expensive. So I’m going to rework this setup so that MongoDB will only contain account and project info, and the real data files will be stored on file, served by a web server. Reading these files will then just be a request to the web server, which should be really fast.

But anyway, for now, have fun by [adding conversations to your game](http://rpgplayground.com/)!

## 6 Comments

## Jesse A Swaney · June 2, 2019 at 15:36

Can I make NPC’s say something different after you touch them a second time? Like, I want to talk to someone, we exchange dialogue, the NPC says something like “follow me”, they walk somewhere else (location x/y) and I follow them. Once we get to the new location, I want the NPC to reveal new exposition. ie: when I touch them the second time ; after they’ve moved ; I’d like them to say something new – not just repeat what they’ve said the first time I’ve touched them.

Thank you for reading!

-a fan of RPG Playground,

Jesse

## Koen Witters · June 2, 2019 at 23:36

Yes you can do that with “tokens”. For an example, look here: http://rpgplayground.com/user-manual/#hero_receives_token_token

## Barry · July 24, 2021 at 12:05

Is there a way to interact with characters without the “when touched” option?

As if there were to be an ACTION or USE button?

## Koen Witters · July 24, 2021 at 12:26

Not yet no, but it’s planned

## James_30 · July 9, 2023 at 16:40

how do u make the hero/main character talk without any other characters? like, how do u make them talk to themself alone?

## Koen Witters · July 9, 2023 at 23:17

Hero also has a talk action, so use that.