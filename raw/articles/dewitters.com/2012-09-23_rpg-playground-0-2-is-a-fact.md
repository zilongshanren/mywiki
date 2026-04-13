---
title: RPG Playground 0.2 is a fact
url: https://dewitters.com/rpg-playground-0-2-is-a-fact/
published: '2012-09-23'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

I just put [the new release of RPG Playground](http://rpgplayground.com) online, which features a login and registering system. Unfortunately logging in doesn’t have any real purpose yet, but it’s the first step towards saving levels, since that will require you to log in.

I tried to make it as easy as possible to create a new account on RPG Playground, and I think the final result is perfect. You can read more about it in [my previous blog post](http://www.koonsolo.com/news/the-simplest-most-easy-login-system-in-the-world/).

Fortunately for you, I also added some real functionality, although a small one: You can now switch to fullscreen mode by using the fullscreen button at the bottom right.

Implementing this release was a heavy one. My plan was to include saving and loading levels in the 0.2 release, but this functionality requires a login framework, which also includes password resets etc. So first I worked on the login system, but this alone already required a vast amount of work. I didn’t have any server code yet, and my GUI framework was build for games and not really for GUI heavy programs. So it took me some time to implement the entire framework.

I wanted to include the saving and loading levels in the 0.2 release, but since it took so much time, I’m now releasing the login functionality first, and the saving and loading levels will be for the next release (Since I now have the main framework running, this shouldn’t take so much time)

So try the new version, and see if you can register and log in: [http://rpgplayground.com](http://rpgplayground.com).

## 4 Comments

## Spencer H · September 23, 2012 at 13:29

Looking good Koonsolo! One step closer to perfection! Unfortunately registration seems to give me an error. (Cannot send message to server:no connection) Also, the fullscreen button doesn’t seem to do anything when I click on it. Some things to consider. Thanks for making such an awesome game, keep up the good work!

## Koen Witters · September 23, 2012 at 23:41

The fullscreen button is indeed a problem. Seems that Flash in a browser doesn’t allow you to go fullscreen unless it’s on a ‘push button’ event. But my framework handles this differenlty. I’ll see if I can get a dirty hack in there so it works in all browsers.

The registration problem seems to be a problem on the hosting side, I’ll see if I can host my server software somewhere else.

## Koen Witters · September 24, 2012 at 12:53

Fullscreen problem is fixed!

The registration/login problem is a security issue with Flash policy files. I’m working on that now…

## Spencer H · November 15, 2012 at 14:56

The login feature works perfect every time, congrats on a successful version update. We now patiently await saving and loading:)