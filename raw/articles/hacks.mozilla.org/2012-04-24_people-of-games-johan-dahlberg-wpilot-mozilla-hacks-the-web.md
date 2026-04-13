---
title: 'People of Games: Johan Dahlberg (WPilot) – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2012/04/people-of-games-johan-dahlberg-wpilot/
author: Robin Hawkes
published: '2012-04-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[People of Games](https://hacks.mozilla.org/category/people-of-games/) is a series of interviews on game development for the Web. In this first edition we talk to [Johan Dahlberg](https://github.com/jfd), creator of the [WPilot](http://jfd.github.com/wpilot/) HTML5 space-shooter.


![Johan Dahlberg](../../assets/643b1ec7ce1d7f44.jpg)


## About Johan Dahlberg

Johan currently resides in Stockholm, Sweden and started coding (in quickbasic) when he was ten years old. He worked as a business developer for [North Kingdom](http://www.northkingdom.com) for two years, then started [Hydna](http://hydna.com) two years ago. He also created the [WPilot](http://jfd.github.com/wpilot/) HTML5 game that really showed off the capabilities of multiplayer games on the Web.

## What made you decide to work on WPilot?

I had a lot of friends that developed games in Adobe Flash. I’m a big fan of open standards and the open Web, so I wanted to show them and the community what was possible with just the Web browser. I had not seen a real-time action game built with just JavaScript and HTML, but I did know that it was possible. So, WPilot is a result of that. A high-phase multiplayer game in your browser, no plug-ins required.

## Had you done game development before WPilot?

Yeah, I have worked on some projects before, but I did not complete any of them. I started my programming career in QBasic twenty years ago, and the main reason was gaming. I also did some game programming in C# six to seven years ago.

WPilot is the first game in the browser, and also the only gaming project that I have finished!

## How did you go about making sure you’d complete WPilot? Did you have a plan in place or just make stuff up as you went along?

Well, I did not plan to do a complete game in the beginning. The goal was just show the network stuff. Basically, I wanted to show two ships flying, on two different screens, using WebSockets to transmit the positions. But, I thought it was a fun project, so it grew with time.

I only added a couple of features at a time. Then, after a month or so, I decided to do a couple of milestones. I wanted to implement so many features, but I knew my limitations. It is hard to complete something if you put down too many things on the list. So, WPilot today is like version 0.5 of my original idea.

## So I take it you didn’t have the game code as it currently stands as the vision from day one — the codebase just evolved and refined itself over time and not specifically to a plan?

Yeah, exactly. I think I re-wrote the game logic and networking stuff like four or fives times. I had some problems with networking performance, so I had to re-think what I was doing all the time. The problem with the old WebSocket standard was that you had to use UTF8 instead of binary (the two control chars, 0x0, and 0xff were a pain). I tried to be smart about how to encode the packets, but I did not find a optimal solution for this. It ended up with me using JSON instead. It is not optimal, but it works.

## I want to touch on networking in a moment but while you’re talking about problems, what else did you find most troublesome about creating the game aside from networking?

The second trickiest part was the interpolation. In network games, you are always playing in the past; the server is always ahead of you. I did spend a lot of time to make the game experience as smooth as possible. The algorithm that I’m using is trying to guess where the ship is headed. I think its pretty OK today, but it was really hard to nail it.

## From looking at the source, you seem to have some really solid networking logic; message priorities, single-packet messages, interpolation, etc. Is that something you learnt as you went along or did you have prior experience with how to make the networking feel right?

I started to work on a networking protocol for games in C# ten years ago. I did not finish the library, but the project taught me a lot around game networking, latency, interpolation, etc.

Quake was a great inspiration as well. The protocol is open today and I took a lot of design decisions from there. Most examples that I looked at were designed for high-phase multiplayer games using UDP and C. Javascript has some limitations, so I had to re-think some logic along the way.

## What were the key tips and lessons that you learnt from your game networking experience that other game developers should know before getting scared by it?

Keep it simple is my best advice, it’s not that hard once you have figured out the basics. The key here is to look at other projects. I think that taught me everything that I know today. I can’t give a more concrete tips unfortunately, it is all knowledge combined.

Version 1 of my protocol was way too heavy and advanced. For example, I sent the bullet position at each game-tick. This was of course a big mistake. The bullets never changed direction, so I could simply send them once and let the client do the calculation.

## What would you do differently if you rewrote the game today, knowing what you now know?

Oh, that is a hard question! I should definitely keep it more simple. The code today is a result of many rewrites. I have tried to prematurely figure out problems that may or may not come up in the future. This approach make the project much more complex that it has to be. I’m planing to write the game to our new platform ([Hydna](http://www.hydna.com/)) and the main goal will be to reduce the amount of code.

## Would you say it helps to rewrite the game now that it is fully functional and you know what it needs to do? In comparison to rewriting the game during development when game features are still evolving and changing all the time.

Yes, it would be much easier today, much more straight forward, less thinking and less experimenting. If you write something for the first time, then it is hard to have everything figured out from the beginning. I find it useful to create small lab projects, where I can test a concept before implementing in the “real” project.

## Are there any plans to update the game to work with the recent improvements to WebSockets?

Yes, there is a plan, and the plan is of course to port it to [Hydna](http://www.hydna.com/)’s infrastructure! Hydna solves many of the issues and problems that I had when dealing with the server logic in WPilot. Hydna will remove the need for a server at all. The player can just surf into the website and create a game on their local machine.

## That’s good news, and Hydna sounds awesome! Are you able to talk a little more about how it works and will help game devs?

Hydna is a so called “hosted platform”. The goal is to send a message from point A to point B as fast as possible, and without thinking about things like scaling. If you are a game developer for example, you don’t have to worry about how to setup a Linux box, which server language to use, what would happen if your game gets popular, etc. You only have to focus on the actual game (JavaScript and HTML), we take care of the rest.

Hydna won;t eliminate things like latency and interpolation, but we will give the community a lot of tips here. We are currently writing some articles that explains the basic concepts of network gaming, and how to use Hydna to solve the issue. Hydna is really easy to get started with. The interface looks a lot like the WebSocket class, but has some real “magic” implemented behind the scenes.

I really like the concept that you can run the “server” in the client, and Hydna solves this for you. Your Web browser becomes both server and client, no need for server scripting at all.

## Can people use Hydna yet?

Yes, it’s up and running, at [Hydna.com](https://www.hydna.com/).

Our dream is to help developers (both game and Web) as much as possible. We have worked in the business for many years now, and I really think that our combined knowledge can help others to solve day-to-day problems. Hydna really takes away a lot of headache that you normally would face when building real-time applications. It’s a two-year long project, we have put a lot of sweat and tears into it. But we are really happy with the final result, and we really hope/think others will find it useful.

## Thank you Johan!

[Keep an eye open](https://hacks.mozilla.org/feed/) for the next edition.

## About
[
Robin Hawkes ](http://rawkes.com)

Robin thrives on solving problems through code. He's a Digital Tinkerer, Head of Developer Relations at Pusher, former Evangelist at Mozilla, book author, and a Brit.