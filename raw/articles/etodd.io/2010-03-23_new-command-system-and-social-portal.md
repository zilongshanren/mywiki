---
title: New command system and social portal
url: https://etodd.io/2010/03/23/new-command-system-and-social-portal/
published: '2010-03-23'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# New command system and social portal

Quick update just to keep this blog alive. I've made some improvements to the command/AI system. It's now much simpler and easier to tell your units to attack a specific enemy. The closest enemy you're aiming at is highlighted, and you can hit Q or E (depending on which one of your two units you want to command) to order an attack on that enemy. Special abilities are also mapped to Q or E, when tapped twice in quick succession.

Another project I've been working on is the social portal in which the game plugin is embedded. The menu has been completely removed from the game, which is a huge relief, because Panda3D's UI code is horrendous. Instead I am using HTML and Javascript menus, which call into the web plugin, as [described](http://www.panda3d.org/wiki/index.php/The_appRunner.main_object) in the Panda3D manual. This also means I can add a chat room and other social features much faster, without having to create a massive interface inside the game. So far I've only implemented the chat room, which is based on [Lace](http://socket7.net/lace/), but I plan on eventually adding stat tracking and a friend system at a bare minimum.

Here's a preview of the new social portal so far: