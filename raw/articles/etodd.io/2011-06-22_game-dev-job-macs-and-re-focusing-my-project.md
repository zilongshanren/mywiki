---
title: Game dev job, Macs, and re-focusing my project
url: https://etodd.io/2011/06/22/game-dev-job-macs-and-re-focusing-my-project/
published: '2011-06-22'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Game dev job, Macs, and re-focusing my project

Apologies for the lack of Parkour Ninja updates. I do have fresh info about it somewhere in this post. But first! A list of potentially interesting goings-on of late:

- School's out for summer! And I'm one year closer to a Computer Science & Engineering undergrad degree from Ohio State. I'll graduate in about a year and a half, right around my 21st birthday actually. I haven't the foggiest idea what to do after that. I'm looking at grad school, but I've heard it's not as important for CS people.
- I got a job making iPhone games! I'm working for a small studio in Columbus with three other interns. The original plan was to have the four of us collaborate on a single game, but now they've given us each a separate project (at various stages of development) to work on. I wish they had kept us together because a) I doubt we'll finish all the games now, and b) I need experience collaborating on a game instead of my usual lone wolf habits; I was hoping this job would put me out of my comfort zone a little. On the other hand, where else would I got almost full control over every aspect of a professional title? That's pretty cool.
- On a random note, I'm getting into shooting this summer. After a few more weeks of saving up I plan to buy an assault rifle (still researching what to buy there) but until then my buddy is lending me his AR-15 for the summer. :)

As a consequence of number 2, I now spend 40 hours a week working with Apple products. IT IS KILLING ME SLOWLY AND PAINFULLY. My Twitter feed is now steadily filling up with complaints about these products. Let's look at some comparisons to see why.

**Resizing windows on Windows.**To maximize you can click the button, double click the bar, drag it to the top of the screen, or heck use the little system menu on the app icon. Reverse the operation and it returns to its original size. You can tile windows, you can stack them, you can use Aero snap, you can resize them by grabbing any edge or corner.

**Resizing windows on Mac.**Okay, to maximize all I've got is this tiny little button, but no biggie... wait, I can still move the window when it's maximized? Crap, now the ONE AND ONLY tiny resize widget is off the screen! No wait, I can see it through this ridiculous translucent dock thing...

**Moving files on Windows.**Ctrl-X. Up one level. Click into different directory. Ctrl-V.

**Moving files on Mac.**Command-X. Back. Click into different directory. Command-V. Nothing happened?? Great, gotta open a whole 'nother Finder window...

**GIMP on Windows.**Ugly but functional. At least it sort of fits in with the system chrome. The usual keyboard shortcuts work and the multi-window setup doesn't get in the way too much.

**GIMP on Mac.**Well it took five minutes to load, but it looks okay... wait Command+N pulls up a bash prompt?? And now I've switched focus to some weird X11 app?? Okay back in GIMP now... wait ALL THE SHORTCUTS STILL USE THE CONTROL KEY. Well okay, at least I can zoom... oh wait, NOPE. *facepalm*

**Visual Studio on Windows.**Open a project... ah, there's all the files. Oh cool, I can completely customize the layout here... and oh yay, tabs!

**Xcode on Mac.**Waiiiit... are you sure this isn't iTunes?

**C# on Windows.**Whoops, looks like you have a syntax error here. You probably forgot a brace right here. Or perhaps you're missing an assembly reference? Let me help you with that. Would you like to refactor this a bit while we're at it?

**Objective C on Mac.**ERROR: (*) MAY NOT RESPOND TO (*). UNDEFINED TYPE "bool". INVALID ATTEMPT TO ASSIGN TO READ-ONLY PROPERTY "int main()". 30,000 ERROR THRESHOLD EXCEEDED. COMPILATION STOPPED.

**TortoiseSVN on Windows.**One right click, and you've got the repo browser, blazing fast logs, instant comparisons with syntax highlighting, single-click blaming, merging and branching, etc., etc...

**SmartSVN on Mac.**Import existing working copy. Okay, repository browser. What's the URL? I dunno, you tell me. Fine, view log then. You want me to set up a log cache? I don't know where to put it, save it in the application folder. Okay, here's the log. Wait, wrong folder. Back to the repo browser. Navigate weird tree folder structure... there we go, view log. WHAT? SET UP

*ANOTHER*LOG CACHE?

Sorry, I just needed to get this stuff off my chest. Granted, some of these complaints have to do with free software. Seems you have to shell out at least $20 to get a half decent app on Mac.

**ANYWAYS, about that Parkour Ninja update.**I've made progress since the last update. There are more animations, more features, more coolness! However, I finally took the time to build a somewhat larger map, and the gameplay is just... frustrating. And not fun. I've spent many hours tweaking the existing moves, but I still spend the majority of the time careening off the map into oblivion or fighting the game to make it do what I want.

The problem is, the game in its current form is very different from the game I originally designed. I originally envisioned a heavily physics-based game, where the main draw was the destructible/constructable environment. It was going pretty great for the first month or so (I still think

[this early video](https://etodd.io/2010/11/11/back-at-it/)is pretty sweet), and then I installed it on my friend's Xbox. Thing crawled like molasses. Turns out, Xbox live indie games basically can't have physics, because the CLI floating point performance is absolutely abysmal. I was shooting primarily for the Xbox live indie game market then, so I decided to axe the physics and use simple collision and movement code for the player. The rest is history.The object lesson here is: don't axe your core gameplay mechanic! Notice that one unpolished early video has 1,500 views while the other more polished videos (post physics engine lobotomy) have about 300 views apiece. I think that proves a few things: a) people love watching physics engines at work, and b) if the game concept is fun, people will like it even if it's extremely unpolished.

So the bottom line is, I am no longer targeting the Xbox market. For now at least, Parkour Ninja will be a PC-only, singleplayer-only game. I will be bringing back the physics and focusing more heavily on that aspect. I may have to re-do the whole Parkour Ninja thing to reflect this shift in focus. I mean, I'm considering making the player character a cube right now, I don't think I can make that look like a ninja. Fortunately, I probably won't have to scrap much code, thanks to the

[nifty component system](https://etodd.io/2011/02/02/refactoring-with-components/). So this project is far from dead, but it's going to take a different direction in the coming months. It's a tough decision to make, but I think it's necessary, and the sooner it's done the better.Whew, that was long. Thanks for reading!